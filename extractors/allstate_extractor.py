from extractors.base_extractor import BaseExtractor

class AllstateExtractor(BaseExtractor):
    """Allstate specific patterns."""
    
    def __init__(self):
        super().__init__()
        self.company_name = "Allstate"
    
    def get_patterns(self):
        return {
            'policy_number': [
                r'Policy\s*(?:Number|#)\s*:?\s*([A-Z0-9\-]+)',
                r'Policy\s*:?\s*([A-Z]{2,3}\d{7,})',
            ],
            'policyholder_name': [
                r'Named\s*Insured\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'Policyholder\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            ],
            'property_address': [
                r'Property\s*Address\s*:?\s*(.+?)(?:\n|$)',
                r'Location\s*:?\s*(.+?)(?:\n|$)',
            ],
            'coverage_amount': [
                r'Personal\s*Property\s*:?\s*\$?\s*([\d,]+)',
                r'Contents\s*:?\s*\$?\s*([\d,]+)',
            ],
            'liability_coverage': [
                r'Family\s*Liability\s*:?\s*\$?\s*([\d,]+)',
                r'Personal\s*Liability\s*:?\s*\$?\s*([\d,]+)',
            ],
            'deductible': [
                r'Deductible\s*:?\s*\$?\s*([\d,]+)',
            ],
            'effective_date': [
                r'Policy\s*Period\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'Effective\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            ],
            'expiration_date': [
                r'(?:to|through)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'Expiration\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            ],
            'premium_amount': [
                r'Total\s*Premium\s*:?\s*\$?\s*([\d,]+\.?\d*)',
            ],
            'insurance_company': [
                r'(Allstate[^\n]*)',
            ],
        }