"""
Simple coordinate-based extractor - NO company detection needed
User specifies which company, we use those coordinates
"""
import pytesseract
import cv2
import numpy as np
import re
from config import Config

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_CMD


def extract_text_from_coords(img, coords):
    """Extract text from specific coordinates - EXACTLY like sample code"""
    x, y, w, h = coords
    
    # Extract ROI
    roi = img[y:y+h, x:x+w]
    
    # Convert to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold
    thresh = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # Extract text
    text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6 -l eng')
    
    return text.strip()


def parse_text(text):
    """Clean text - EXACTLY like sample code"""
    return text.replace(')', '').replace("'", "").replace(",", "").replace("'", "")


# HARDCODED COORDINATES FOR EACH COMPANY
COMPANY_COORDINATES = {
    'nationwide': {
        'insurance_company': (155, 33, 145, 30),
        'policy_number': (454, 77, 117, 19),
        'date_prepared': (610, 77, 92, 20),
        'insurer_name': (439, 198, 250, 20),
        'insurer_address': (434, 214, 250, 20),
        'insurer_city_state': (434, 230, 250, 20),
        'insurance_amount': (639, 630, 150, 20),
    },
    
    'state_farm': {
        'insurance_company': None,
        'policy_number': None,
        'date_prepared': None,
        'insurer_name': None,
        'insurer_address': None,
        'insurer_city_state': None,
        'insurance_amount': None,
    },
    
    'allstate': {
        'insurance_company': None,
        'policy_number': None,
        'date_prepared': None,
        'insurer_name': None,
        'insurer_address': None,
        'insurer_city_state': None,
        'insurance_amount': None,
    },
    
    'progressive': {
        'insurance_company': None,
        'policy_number': None,
        'date_prepared': None,
        'insurer_name': None,
        'insurer_address': None,
        'insurer_city_state': None,
        'insurance_amount': None,
    },
    
    'usaa': {
        'insurance_company': None,
        'policy_number': None,
        'date_prepared': None,
        'insurer_name': None,
        'insurer_address': None,
        'insurer_city_state': None,
        'insurance_amount': None,
    },
    
    'geico': {
        'insurance_company': None,
        'policy_number': None,
        'date_prepared': None,
        'insurer_name': None,
        'insurer_address': None,
        'insurer_city_state': None,
        'insurance_amount': None,
    },
    
    'travelers': {
        'insurance_company': None,
        'policy_number': None,
        'date_prepared': None,
        'insurer_name': None,
        'insurer_address': None,
        'insurer_city_state': None,
        'insurance_amount': None,
    },
    
    'liberty_mutual': {
        'insurance_company': None,
        'policy_number': None,
        'date_prepared': None,
        'insurer_name': None,
        'insurer_address': None,
        'insurer_city_state': None,
        'insurance_amount': None,
    },
    
    'farmers': {
        'insurance_company': None,
        'policy_number': None,
        'date_prepared': None,
        'insurer_name': None,
        'insurer_address': None,
        'insurer_city_state': None,
        'insurance_amount': None,
    },
}


def get_available_companies():
    """Get list of companies with coordinates defined"""
    return list(COMPANY_COORDINATES.keys())


def extract_all_fields(img, company_name):
    """
    Extract all fields for a specific company
    
    Args:
        img: OpenCV image
        company_name: Company identifier (e.g., 'nationwide', 'state_farm')
        
    Returns:
        Dictionary with extracted data
    """
    if company_name not in COMPANY_COORDINATES:
        raise ValueError(f"Unknown company: {company_name}. Available: {get_available_companies()}")
    
    coordinates = COMPANY_COORDINATES[company_name]
    data = {}
    
    for field_name, coords in coordinates.items():
        if coords is None or not coords or len(coords) != 4:
            # Skip if coordinates not defined
            data[field_name] = ''
            continue
        
        try:
            text = extract_text_from_coords(img, coords)
            
            # Apply appropriate parsing
            if field_name in ['insurance_company', 'insurer_city_state', 'insurance_amount']:
                text = parse_text(text)
            
            data[field_name] = text
        except Exception as e:
            print(f"Error extracting {field_name}: {e}")
            data[field_name] = ''
    
    return data


def extract_from_image(image_path, company_name):
    """
    Main extraction function - simple and direct like sample code
    
    Args:
        image_path: Path to image or PDF
        company_name: Company identifier (e.g., 'nationwide')
        
    Returns:
        Dictionary with extracted data
    """
    # Load image (handle PDF if needed)
    if str(image_path).lower().endswith('.pdf'):
        try:
            from core.pdf_handler import PDFHandler
            pdf_handler = PDFHandler()
            img = pdf_handler.get_first_page(image_path)
        except Exception as e:
            raise ValueError(f"Error loading PDF: {e}. Make sure pdf2image and poppler are installed.")
    else:
        img = cv2.imread(str(image_path))
    
    if img is None:
        raise ValueError(f"Could not load image from {image_path}")
    
    # Extract all fields using specified company coordinates
    data = extract_all_fields(img, company_name)
    
    # Add company name to data
    data['company'] = company_name
    
    return data