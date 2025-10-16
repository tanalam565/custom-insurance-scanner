from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import time
import logging
from typing import List, Optional
from datetime import datetime

from config import settings
from models.database import SessionLocal, InsuranceRecord
from models.schemas import UploadResponse, ExportRequest, InsuranceDataResponse
from core.ocr_engine import OCREngine
from core.company_detector import CompanyDetector
from core.template_manager import TemplateManager
from core.exporter import DataExporter
from core.validator import DataValidator

logger = logging.getLogger(__name__)
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize components
ocr_engine = OCREngine()
company_detector = CompanyDetector()
template_manager = TemplateManager()
exporter = DataExporter()
validator = DataValidator()

# Ensure directories exist
Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
Path(settings.EXPORT_DIR).mkdir(exist_ok=True)

@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process insurance document."""
    start_time = time.time()
    
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    file_path = Path(settings.UPLOAD_DIR) / file.filename
    
    try:
        # Save uploaded file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Processing: {file.filename}")
        
        # Step 1: Extract text using OCR
        text = ocr_engine.extract_text(str(file_path), file_ext)
        
        # Step 2: Detect insurance company
        company_name, detection_confidence = company_detector.detect_company(text)
        
        # Step 3: Get appropriate extractor
        extractor = template_manager.get_extractor(company_name, detection_confidence)
        
        # Step 4: Extract data
        extracted_data = extractor.extract(text)
        
        # Step 5: Validate extracted data
        validation_results = validator.validate_all(extracted_data)
        
        # Step 6: Determine if needs review
        needs_review = validator.should_flag_for_review(extracted_data, validation_results)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Step 7: Save to database
        record = InsuranceRecord(
            filename=file.filename,
            policy_number=extracted_data.get('policy_number'),
            policyholder_name=extracted_data.get('policyholder_name'),
            property_address=extracted_data.get('property_address'),
            coverage_amount=extracted_data.get('coverage_amount'),
            liability_coverage=extracted_data.get('liability_coverage'),
            deductible=extracted_data.get('deductible'),
            effective_date=extracted_data.get('effective_date'),
            expiration_date=extracted_data.get('expiration_date'),
            premium_amount=extracted_data.get('premium_amount'),
            insurance_company=extracted_data.get('insurance_company'),
            detected_company=extracted_data.get('detected_company'),
            confidence_score=extracted_data.get('confidence_score'),
            raw_text=extracted_data.get('raw_text_preview'),
            processing_time=processing_time,
            needs_review=1 if needs_review else 0
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        # Clean up uploaded file
        file_path.unlink()
        
        # Prepare response
        response_data = InsuranceDataResponse(
            **{k: v for k, v in extracted_data.items() if k != 'raw_text_preview'},
            processing_time=processing_time,
            needs_review=needs_review
        )
        
        message = "File processed successfully"
        if needs_review:
            message += " - Flagged for review"
        if validation_results['warnings']:
            message += f" ({len(validation_results['warnings'])} warnings)"
        
        return UploadResponse(
            success=True,
            message=message,
            filename=file.filename,
            data=response_data,
            record_id=record.id
        )
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export")
async def export_data(request: ExportRequest, db: Session = Depends(get_db)):
    """Export extracted data in specified format."""
    try:
        # Get records
        if request.record_ids:
            records = db.query(InsuranceRecord).filter(
                InsuranceRecord.id.in_(request.record_ids)
            ).all()
        else:
            records = db.query(InsuranceRecord).all()
        
        if not records:
            raise HTTPException(status_code=404, detail="No records found")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if len(records) == 1:
            # Single record export
            data = records[0].to_dict()
            
            if request.format == "excel":
                filename = f"insurance_{timestamp}.xlsx"
                output_path = Path(settings.EXPORT_DIR) / filename
                exporter.export_to_excel(data, str(output_path))
            
            elif request.format == "csv":
                filename = f"insurance_{timestamp}.csv"
                output_path = Path(settings.EXPORT_DIR) / filename
                import csv
                with open(output_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Field', 'Value'])
                    for k, v in data.items():
                        writer.writerow([k, v if v else "N/A"])
            
            else:  # json
                filename = f"insurance_{timestamp}.json"
                output_path = Path(settings.EXPORT_DIR) / filename
                import json
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, default=str)
        
        else:
            # Batch export
            data = [r.to_dict() for r in records]
            
            if request.format == "excel":
                filename = f"insurance_batch_{timestamp}.xlsx"
                output_path = Path(settings.EXPORT_DIR) / filename
                exporter.export_batch_to_excel(data, str(output_path))
            
            elif request.format == "csv":
                filename = f"insurance_batch_{timestamp}.csv"
                output_path = Path(settings.EXPORT_DIR) / filename
                import pandas as pd
                df = pd.DataFrame(data)
                df.to_csv(output_path, index=False)
            
            else:  # json
                filename = f"insurance_batch_{timestamp}.json"
                output_path = Path(settings.EXPORT_DIR) / filename
                import json
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, default=str)
        
        return FileResponse(
            path=str(output_path),
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except Exception as e:
        logger.error(f"Export failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/records")
async def get_records(
    skip: int = 0,
    limit: int = 100,
    needs_review: Optional[bool] = None,
    company: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of processed records with optional filters."""
    query = db.query(InsuranceRecord)
    
    # Filter by review status
    if needs_review is not None:
        query = query.filter(InsuranceRecord.needs_review == (1 if needs_review else 0))
    
    # Filter by company
    if company:
        query = query.filter(InsuranceRecord.detected_company == company)
    
    # Order by most recent first
    query = query.order_by(InsuranceRecord.upload_date.desc())
    
    # Pagination
    records = query.offset(skip).limit(limit).all()
    
    return [r.to_dict() for r in records]


@router.get("/records/{record_id}")
async def get_record(record_id: int, db: Session = Depends(get_db)):
    """Get specific record by ID."""
    record = db.query(InsuranceRecord).filter(InsuranceRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    return record.to_dict()


@router.put("/records/{record_id}")
async def update_record(
    record_id: int,
    updated_data: dict,
    db: Session = Depends(get_db)
):
    """Update a record (for human corrections)."""
    record = db.query(InsuranceRecord).filter(InsuranceRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    # Update fields
    for key, value in updated_data.items():
        if hasattr(record, key) and key not in ['id', 'upload_date']:
            setattr(record, key, value)
    
    # Mark as reviewed
    record.needs_review = 0
    
    db.commit()
    db.refresh(record)
    
    return {
        "success": True,
        "message": "Record updated successfully",
        "record": record.to_dict()
    }


@router.delete("/records/{record_id}")
async def delete_record(record_id: int, db: Session = Depends(get_db)):
    """Delete a record."""
    record = db.query(InsuranceRecord).filter(InsuranceRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(record)
    db.commit()
    
    return {
        "success": True,
        "message": "Record deleted successfully"
    }


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics about processed records."""
    total = db.query(InsuranceRecord).count()
    needs_review = db.query(InsuranceRecord).filter(
        InsuranceRecord.needs_review == 1
    ).count()
    
    # Get company breakdown
    from sqlalchemy import func
    company_stats = db.query(
        InsuranceRecord.detected_company,
        func.count(InsuranceRecord.id).label('count')
    ).group_by(InsuranceRecord.detected_company).all()
    
    # Get average confidence
    avg_confidence = db.query(
        func.avg(InsuranceRecord.confidence_score)
    ).scalar() or 0
    
    # Get average processing time
    avg_processing_time = db.query(
        func.avg(InsuranceRecord.processing_time)
    ).scalar() or 0
    
    return {
        "total_records": total,
        "needs_review": needs_review,
        "auto_approved": total - needs_review,
        "company_breakdown": {
            company: count for company, count in company_stats
        },
        "average_confidence": round(avg_confidence, 2),
        "average_processing_time": round(avg_processing_time, 2)
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/companies")
async def get_supported_companies():
    """Get list of supported insurance companies."""
    companies = list(TemplateManager.EXTRACTOR_MAP.keys())
    companies.remove('generic')  # Don't show generic in list
    
    return {
        "supported_companies": sorted(companies),
        "total_count": len(companies),
        "has_generic_fallback": True
    }


@router.post("/validate/{record_id}")
async def validate_record(record_id: int, db: Session = Depends(get_db)):
    """Manually trigger validation for a specific record."""
    record = db.query(InsuranceRecord).filter(InsuranceRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    # Prepare data for validation
    data = record.to_dict()
    
    # Run validation
    validation_results = validator.validate_all(data)
    
    # Update needs_review flag if necessary
    needs_review = validator.should_flag_for_review(data, validation_results)
    
    if record.needs_review != (1 if needs_review else 0):
        record.needs_review = 1 if needs_review else 0
        db.commit()
    
    return {
        "record_id": record_id,
        "validation_results": validation_results,
        "needs_review": needs_review
    }


@router.post("/batch-upload")
async def batch_upload(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Upload multiple files at once."""
    results = []
    
    for file in files:
        try:
            # Process each file (reuse upload logic)
            result = await upload_file(file, db)
            results.append({
                "filename": file.filename,
                "success": True,
                "record_id": result.record_id
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    return {
        "total": len(results),
        "successful": successful,
        "failed": failed,
        "results": results
    }