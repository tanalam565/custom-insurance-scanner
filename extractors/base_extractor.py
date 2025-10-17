from abc import ABC, abstractmethod
from core.image_processor import ImageProcessor
from core.ocr_engine import OCREngine
from core.template_manager import TemplateManager

class BaseExtractor(ABC):
    """Base class for all insurance company extractors"""
    
    def __init__(self):
        self.processor = ImageProcessor()
        self.ocr = OCREngine()
        self.template_manager = TemplateManager()
        self.company_name = self.get_company_name()
        self.template = self.template_manager.get_template(self.company_name)
    
    @abstractmethod
    def get_company_name(self):
        """Return the company identifier"""
        pass
    
    def extract_field(self, img, field_name, field_type='text'):
        """Extract a specific field from the image
        
        Args:
            img: Input image
            field_name: Name of the field to extract
            field_type: Type of field (text, date, currency, etc.)
            
        Returns:
            Extracted and cleaned field value
        """
        coords = self.template.get(field_name)
        if not coords:
            return ''
        
        try:
            # Extract and preprocess ROI
            roi = self.processor.extract_roi(img, coords)
            processed = self.processor.preprocess_roi(roi)
            
            # Extract text
            text = self.ocr.extract_text(processed)
            
            # Apply type-specific cleaning
            return self.clean_field(text, field_type)
            
        except Exception as e:
            print(f"Error extracting {field_name}: {e}")
            return ''
    
    def clean_field(self, text, field_type):
        """Clean extracted text based on field type
        
        Args:
            text: Raw extracted text
            field_type: Type of field
            
        Returns:
            Cleaned text
        """
        if field_type == 'text':
            return self.ocr.parse_text(text)
        elif field_type == 'policy_number':
            return self.ocr.extract_policy_number(text)
        elif field_type == 'date':
            return self.ocr.extract_date(text)
        elif field_type == 'currency':
            return self.ocr.extract_currency(text)
        elif field_type == 'phone':
            return self.ocr.extract_phone(text)
        elif field_type == 'email':
            return self.ocr.extract_email(text)
        elif field_type == 'name':
            return self.ocr.clean_name(text)
        elif field_type == 'address':
            return self.ocr.clean_address(text)
        else:
            return text.strip()
    
    def extract_all_fields(self, img):
        """Extract all fields from the image
        
        Args:
            img: Input image
            
        Returns:
            Dictionary with all extracted fields
        """
        data = {
            'insurance_company': self.extract_field(img, 'insurance_company', 'text'),
            'policy_number': self.extract_field(img, 'policy_number', 'policy_number'),
            'date_prepared': self.extract_field(img, 'date_prepared', 'date'),
            'insurer_name': self.extract_field(img, 'insurer_name', 'name'),
            'insurer_address': self.extract_field(img, 'insurer_address', 'address'),
            'insurer_city_state': self.extract_field(img, 'insurer_city_state', 'address'),
            'insurance_amount': self.extract_field(img, 'insurance_amount', 'currency'),
            'property_address': self.extract_field(img, 'property_address', 'address'),
            'effective_date': self.extract_field(img, 'effective_date', 'date'),
            'expiration_date': self.extract_field(img, 'expiration_date', 'date'),
        }
        
        # Add company-specific fields if any
        custom_data = self.extract_custom_fields(img)
        data.update(custom_data)
        
        return data
    
    def extract_custom_fields(self, img):
        """Override this method to extract company-specific fields
        
        Args:
            img: Input image
            
        Returns:
            Dictionary with custom fields
        """
        return {}
    
    def validate_extraction(self, data):
        """Validate extracted data
        
        Args:
            data: Dictionary with extracted data
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check required fields
        required_fields = ['policy_number', 'insurer_name', 'insurance_amount']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
        
        return len(errors) == 0, errors
    
    def post_process(self, data):
        """Post-process extracted data
        
        Args:
            data: Dictionary with extracted data
            
        Returns:
            Processed data dictionary
        """
        # Override in subclass for custom post-processing
        return data