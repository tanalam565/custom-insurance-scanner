"""
Flask API routes
"""
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import time
from pathlib import Path

from core.simple_extractor import extract_from_image, get_available_companies
from core.exporter import Exporter
from models.database import Database
from config import Config

api = Blueprint('api', __name__)

exporter = Exporter()
db = Database()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


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
    
    # Get company name from request
    company_name = request.form.get('company', 'nationwide')
    
    # Validate company
    if company_name not in get_available_companies():
        return jsonify({
            'error': f'Unknown company: {company_name}',
            'available_companies': get_available_companies()
        }), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = Path(Config.UPLOAD_FOLDER) / filename
        file.save(filepath)
        
        # Start timing
        start_time = time.time()
        
        # Extract data - NO detection, just use specified company
        extracted_data = extract_from_image(filepath, company_name)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Validate - check if we got some data
        required_fields = ['policy_number', 'insurer_name']
        is_valid = any(extracted_data.get(field) for field in required_fields)
        errors = []
        
        if not is_valid:
            errors.append("Could not extract required fields. Check if coordinates are correct for this company.")
        
        # Prepare database record
        db_data = {
            'filename': filename,
            'insurance_company': company_name,
            'company_confidence': 1.0,  # No detection, user specified
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
            'data': extracted_data,
            'is_valid': is_valid,
            'validation_errors': errors,
            'processing_time': processing_time
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error during extraction:\n{error_details}")
        return jsonify({
            'error': str(e),
            'details': 'Check console for full error details'
        }), 500


@api.route('/companies', methods=['GET'])
def get_companies():
    """Get list of available insurance companies"""
    companies = get_available_companies()
    return jsonify({
        'success': True,
        'companies': companies
    }), 200


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
    """Export extraction data"""
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