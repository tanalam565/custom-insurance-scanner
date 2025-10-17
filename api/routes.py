from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import time
from pathlib import Path
import importlib

from core.image_processor import ImageProcessor
from core.company_detector import CompanyDetector
from core.exporter import Exporter
from models.database import Database
from config import Config

api = Blueprint('api', __name__)

# Initialize components
processor = ImageProcessor()
detector = CompanyDetector()
exporter = Exporter()
db = Database()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def get_extractor(company_name):
    """Dynamically import and instantiate the correct extractor"""
    try:
        # Convert company_name to class name
        parts = company_name.split('_')
        class_name = ''.join(word.capitalize() for word in parts) + 'Extractor'
        
        # Import the module
        module_name = f'extractors.{company_name}_extractor'
        module = importlib.import_module(module_name)
        
        # Get the class and instantiate
        extractor_class = getattr(module, class_name)
        return extractor_class()
    except Exception as e:
        print(f"Error loading extractor for {company_name}: {e}")
        # Fall back to generic extractor
        from extractors.generic_extractor import GenericExtractor
        return GenericExtractor()

@api.route('/upload', methods=['POST'])
def upload_file():
    """Upload and process insurance document"""
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = Path(Config.UPLOAD_FOLDER) / filename
        file.save(filepath)
        
        # Start timing
        start_time = time.time()
        
        # Load and process image
        img = processor.load_image(filepath)
        
        # Detect company
        company_name, confidence = detector.detect_company(img)
        
        # Get appropriate extractor
        extractor = get_extractor(company_name)
        
        # Extract data
        extracted_data = extractor.extract_all_fields(img)
        
        # Post-process
        extracted_data = extractor.post_process(extracted_data)
        
        # Validate
        is_valid, errors = extractor.validate_extraction(extracted_data)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Prepare database record
        db_data = {
            'filename': filename,
            'insurance_company': extracted_data.get('insurance_company', company_name),
            'company_confidence': confidence,
            'policy_number': extracted_data.get('policy_number', ''),
            'date_prepared': extracted_data.get('date_prepared', ''),
            'effective_date': extracted_data.get('effective_date', ''),
            'expiration_date': extracted_data.get('expiration_date', ''),
            'insurer_name': extracted_data.get('insurer_name', ''),
            'insurer_address': extracted_data.get('insurer_address', ''),
            'insurer_city_state': extracted_data.get('insurer_city_state', ''),
            'property_address': extracted_data.get('property_address', ''),
            'insurance_amount': extracted_data.get('insurance_amount', ''),
            'extraction_status': 'success' if is_valid else 'warning',
            'error_message': ', '.join(errors) if errors else None,
            'processing_time': processing_time
        }
        
        # Save to database
        record_id = db.save_extraction(db_data)
        
        # Prepare response
        response = {
            'success': True,
            'record_id': record_id,
            'company': company_name,
            'confidence': confidence,
            'data': extracted_data,
            'is_valid': is_valid,
            'validation_errors': errors,
            'processing_time': processing_time
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/records', methods=['GET'])
def get_records():
    """Get all extraction records"""
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        records = db.get_all_extractions(limit=limit, offset=offset)
        
        return jsonify({
            'success': True,
            'count': len(records),
            'records': [record.to_dict() for record in records]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    """Get a specific extraction record"""
    try:
        record = db.get_extraction(record_id)
        
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        return jsonify({
            'success': True,
            'record': record.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete an extraction record"""
    try:
        success = db.delete_extraction(record_id)
        
        if not success:
            return jsonify({'error': 'Record not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Record deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/export/<format>', methods=['POST'])
def export_data(format):
    """Export extraction data to specified format"""
    try:
        data = request.json.get('data', [])
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if format == 'excel':
            filepath = exporter.export_to_excel(data)
        elif format == 'json':
            filepath = exporter.export_to_json(data)
        elif format == 'csv':
            filepath = exporter.export_to_csv(data)
        else:
            return jsonify({'error': 'Invalid format'}), 400
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=os.path.basename(filepath)
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/search', methods=['GET'])
def search_records():
    """Search extraction records"""
    try:
        search_params = {
            'insurance_company': request.args.get('company'),
            'policy_number': request.args.get('policy'),
            'insurer_name': request.args.get('name')
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v}
        
        records = db.search_extractions(**search_params)
        
        return jsonify({
            'success': True,
            'count': len(records),
            'records': [record.to_dict() for record in records]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/companies', methods=['GET'])
def get_supported_companies():
    """Get list of supported insurance companies"""
    companies = [
        'State Farm', 'Allstate', 'Progressive', 'USAA', 'Nationwide',
        'Travelers', 'Liberty Mutual', 'Farmers', 'GEICO', 'American Family',
        'Erie', 'Amica', 'CSAA', 'Chubb', 'Hartford', 'Country Financial',
        'Lemonade', 'Hanover'
    ]
    
    return jsonify({
        'success': True,
        'companies': companies
    }), 200