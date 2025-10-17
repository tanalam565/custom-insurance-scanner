from core.image_processor import ImageProcessor
from core.ocr_engine import OCREngine
from config import Config

class CompanyDetector:
    """Detects insurance company from document"""
    
    def __init__(self):
        self.processor = ImageProcessor()
        self.ocr = OCREngine()
        
        # Define detection regions (top portion of document usually has company name)
        self.header_regions = [
            (0, 0, 800, 100),      # Top header
            (100, 20, 200, 60),    # Top left logo area
            (0, 0, 400, 150),      # Extended top left
        ]
        
        # Company name variations and keywords
        self.company_keywords = {
            'state_farm': ['state farm', 'statefarm', 'state-farm'],
            'allstate': ['allstate', 'all state'],
            'progressive': ['progressive'],
            'usaa': ['usaa', 'u.s.a.a'],
            'nationwide': ['nationwide'],
            'travelers': ['travelers', 'traveler'],
            'liberty_mutual': ['liberty mutual', 'liberty-mutual', 'libertymutual'],
            'farmers': ['farmers insurance', 'farmers'],
            'geico': ['geico', 'government employees insurance'],
            'american_family': ['american family', 'amfam'],
            'erie': ['erie insurance', 'erie'],
            'amica': ['amica mutual', 'amica'],
            'csaa': ['csaa', 'aaa', 'triple a'],
            'chubb': ['chubb'],
            'hartford': ['hartford', 'the hartford'],
            'country_financial': ['country financial', 'countryfinancial'],
            'lemonade': ['lemonade'],
            'hanover': ['hanover', 'the hanover'],
        }
    
    def detect_company(self, img):
        """Detect insurance company from image
        
        Args:
            img: Input image
            
        Returns:
            Tuple of (company_name, confidence_score)
        """
        best_match = None
        best_confidence = 0.0
        
        # Try extracting text from different header regions
        for region in self.header_regions:
            try:
                roi = self.processor.extract_roi(img, region)
                processed = self.processor.preprocess_roi(roi)
                text = self.ocr.extract_text(processed).lower()
                
                # Check for company keywords
                for company, keywords in self.company_keywords.items():
                    for keyword in keywords:
                        if keyword in text:
                            # Calculate simple confidence based on keyword length match
                            confidence = len(keyword) / len(text) if text else 0
                            confidence = min(confidence * 2, 1.0)  # Boost and cap at 1.0
                            
                            if confidence > best_confidence:
                                best_match = company
                                best_confidence = confidence
                                
            except Exception as e:
                print(f"Error processing region {region}: {e}")
                continue
        
        # If confidence is too low, return generic
        if best_confidence < Config.COMPANY_DETECTION_THRESHOLD:
            return 'generic', best_confidence
        
        return best_match, best_confidence
    
    def detect_from_text(self, text):
        """Detect company from already extracted text
        
        Args:
            text: Extracted text
            
        Returns:
            Tuple of (company_name, confidence_score)
        """
        text_lower = text.lower()
        best_match = None
        best_confidence = 0.0
        
        for company, keywords in self.company_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    confidence = len(keyword) / len(text_lower) if text_lower else 0
                    confidence = min(confidence * 2, 1.0)
                    
                    if confidence > best_confidence:
                        best_match = company
                        best_confidence = confidence
        
        if best_confidence < Config.COMPANY_DETECTION_THRESHOLD:
            return 'generic', best_confidence
        
        return best_match, best_confidence
    
    def get_extractor_class_name(self, company_name):
        """Get the extractor class name for a company
        
        Args:
            company_name: Company identifier
            
        Returns:
            Class name string
        """
        # Convert snake_case to CamelCase
        parts = company_name.split('_')
        class_name = ''.join(word.capitalize() for word in parts) + 'Extractor'
        return class_name