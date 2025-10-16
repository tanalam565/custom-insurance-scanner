from extractors.base_extractor import BaseExtractor

class HanoverExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        self.company_name = "The Hanover"
    
    def get_patterns(self):
        return {
            'policy_number': [
                r'Policy\s*(?:Number|#)\s*:?\s*([A-Z0-9\-]+)',
                r'Policy\s*:?\s*([A-Z]{2}\d{7,})',
            ],
            'policyholder_name': [
                r'Named\s*Insured\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'Insured\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
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
                r'Personal\s*Liability\s*:?\s*\$?\s*([\d,]+)',
                r'Liability\s*:?\s*\$?\s*([\d,]+)',
            ],
            'deductible': [
                r'Deductible\s*:?\s*\$?\s*([\d,]+)',
            ],
            'effective_date': [
                r'Effective\s*Date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            ],
            'expiration_date': [
                r'Expiration\s*Date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            ],
            'premium_amount': [
                r'Total\s*Premium\s*:?\s*\$?\s*([\d,]+\.?\d*)',
            ],
            'insurance_company': [
                r'(The\s*Hanover[^\n]*)',
                r'(Hanover[^\n]*)',
            ],
        }