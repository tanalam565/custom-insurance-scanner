from extractors.base_extractor import BaseExtractor

class GenericExtractor(BaseExtractor):
    """Fallback extractor for unknown insurance companies."""
    
    def __init__(self):
        super().__init__()
        self.company_name = "Unknown/Generic"
    
    def get_patterns(self):
        """Comprehensive patterns covering all terminology variations."""
        return {
            'policy_number': [
                r'Policy\s*(?:Number|#|No\.?|ID)\s*:?\s*([A-Z0-9\-]+)',
                r'POL\s*#?\s*:?\s*([A-Z0-9\-]+)',
                r'Contract\s*(?:Number|#)\s*:?\s*([A-Z0-9\-]+)',
            ],
            'policyholder_name': [
                r'(?:Named\s*)?Insured\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'Policyholder\s*(?:Name)?\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'Name\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'Customer\s*Name\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            ],
            'property_address': [
                r'Property\s*Address\s*:?\s*(.+?)(?:\n|$)',
                r'Insured\s*(?:Location|Address)\s*:?\s*(.+?)(?:\n|$)',
                r'Location\s*:?\s*(.+?)(?:\n|$)',
                r'Address\s*:?\s*(.+?)(?:\n|$)',
                r'Premises\s*:?\s*(.+?)(?:\n|$)',
            ],
            'coverage_amount': [
                r'Personal\s*Property\s*(?:Coverage)?\s*:?\s*\$?\s*([\d,]+)',
                r'Contents\s*(?:Coverage)?\s*:?\s*\$?\s*([\d,]+)',
                r'Coverage\s*C\s*:?\s*\$?\s*([\d,]+)',
                r'Personal\s*Belongings\s*:?\s*\$?\s*([\d,]+)',
                r'Renter\'s\s*Property\s*Coverage\s*:?\s*\$?\s*([\d,]+)',
            ],
            'liability_coverage': [
                r'Personal\s*Liability\s*:?\s*\$?\s*([\d,]+)',
                r'Liability\s*Coverage\s*:?\s*\$?\s*([\d,]+)',
                r'Coverage\s*E\s*:?\s*\$?\s*([\d,]+)',
                r'Family\s*Liability\s*:?\s*\$?\s*([\d,]+)',
            ],
            'deductible': [
                r'Deductible\s*:?\s*\$?\s*([\d,]+)',
                r'All\s*Perils\s*Deductible\s*:?\s*\$?\s*([\d,]+)',
            ],
            'effective_date': [
                r'Effective\s*Date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'Policy\s*(?:Start|Begin)\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'Inception\s*Date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            ],
            'expiration_date': [
                r'Expir(?:ation|y)\s*Date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'Policy\s*(?:End|Expiry)\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(?:to|through)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            ],
            'premium_amount': [
                r'Total\s*Premium\s*:?\s*\$?\s*([\d,]+\.?\d*)',
                r'Annual\s*Premium\s*:?\s*\$?\s*([\d,]+\.?\d*)',
                r'Premium\s*:?\s*\$?\s*([\d,]+\.?\d*)',
                r'Amount\s*Due\s*:?\s*\$?\s*([\d,]+\.?\d*)',
            ],
            'insurance_company': [
                r'Insurance\s*Company\s*:?\s*([A-Za-z\s&]+?)(?:\n|$)',
                r'Carrier\s*:?\s*([A-Za-z\s&]+?)(?:\n|$)',
                r'Insurer\s*:?\s*([A-Za-z\s&]+?)(?:\n|$)',
            ],
        }