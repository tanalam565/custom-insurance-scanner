import pytesseract
import re
from config import Config

class OCREngine:
    """Handles OCR text extraction"""
    
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_CMD
        self.config = Config.TESSERACT_CONFIG
    
    def extract_text(self, processed_img, custom_config=None):
        """Extract text from preprocessed image
        
        Args:
            processed_img: Preprocessed image (thresholded)
            custom_config: Custom tesseract config (optional)
            
        Returns:
            Extracted text string
        """
        config = custom_config or self.config
        text = pytesseract.image_to_string(
            processed_img, 
            lang='eng', 
            config=config
        )
        return text.strip()
    
    def parse_text(self, text):
        """Clean and parse extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove unwanted characters
        cleaned = text.replace(')', '')
        cleaned = cleaned.replace("'", "")
        cleaned = cleaned.replace(",", "")
        cleaned = cleaned.replace("'", "")
        return cleaned.strip()
    
    def extract_policy_number(self, text):
        """Extract policy number from text"""
        # Common policy number patterns
        patterns = [
            r'[A-Z]{2,4}[-\s]?\d{6,12}',  # ABC-123456789
            r'\d{10,15}',  # 1234567890123
            r'[A-Z]\d{8,12}',  # A12345678
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return text.strip()
    
    def extract_date(self, text):
        """Extract date from text"""
        # Common date patterns
        patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # MM/DD/YYYY or MM-DD-YYYY
            r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',  # YYYY-MM-DD
            r'[A-Za-z]+\s+\d{1,2},?\s+\d{4}',  # January 15, 2024
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return text.strip()
    
    def extract_currency(self, text):
        """Extract currency amount from text"""
        # Remove common OCR errors
        text = text.replace('$', '').replace('S', '').replace('s', '')
        text = text.replace('O', '0').replace('o', '0')
        text = text.replace('l', '1').replace('I', '1')
        
        # Find currency patterns
        patterns = [
            r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?',  # 1,234.56
            r'\d+(?:\.\d{2})?',  # 1234.56
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                amount = match.group(0).replace(',', '')
                try:
                    return f"${float(amount):,.2f}"
                except ValueError:
                    pass
        
        return text.strip()
    
    def extract_phone(self, text):
        """Extract phone number from text"""
        patterns = [
            r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',  # (123) 456-7890
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # 123-456-7890
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return text.strip()
    
    def extract_email(self, text):
        """Extract email from text"""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        if match:
            return match.group(0)
        return text.strip()
    
    def clean_name(self, text):
        """Clean name field"""
        # Remove extra whitespace and special characters
        text = re.sub(r'[^a-zA-Z\s.-]', '', text)
        text = ' '.join(text.split())
        return text.strip()
    
    def clean_address(self, text):
        """Clean address field"""
        # Keep alphanumeric, spaces, commas, periods, hyphens
        text = re.sub(r'[^a-zA-Z0-9\s,.-]', '', text)
        text = ' '.join(text.split())
        return text.strip()