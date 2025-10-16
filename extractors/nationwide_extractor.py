from extractors.base_extractor import BaseExtractor

class NationwideExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        self.company_name = "Nationwide"
    
    def get_patterns(self):
        return {
            'policy_number': [
                # Specific pattern for "78 42 HS 027914" format with spaces
                r'Policy\s+Number\s+(\d{2}\s+\d{2}\s+[A-Z]{2}\s+\d{6})',
                r'Policy\s+Number:\s*\n\s*(\d{2}\s+\d{2}\s+[A-Z]{2}\s+\d{6})',
                # Try without spaces as fallback
                r'(\d{2}\s?\d{2}\s?[A-Z]{2}\s?\d{6})',
            ],
            'policyholder_name': [
                # Matches all-caps name format
                r'Policyholder:\s*\(Named\s+Insured\)\s*([A-Z]{2,}\s+[A-Z]{2,}(?:\s+[A-Z]{2,})?)',
                r'Named\s+Insured\)\s*([A-Z]{2,}\s+[A-Z]{2,}(?:\s+[A-Z]{2,})?)',
                r'\(Named\s+Insured\)\s*([A-Z\s]{10,}?)(?:\d|\n)',
            ],
            'property_address': [
                # Multi-line address pattern - captures number, street, apt, city state zip
                r'(\d{5}\s+[A-Z\s]+(?:ST|STREET|AVE|AVENUE|BLVD|BOULEVARD|RD|ROAD|DR|DRIVE|LN|LANE|WAY|CT|COURT)\s+(?:APT|UNIT|STE|#)?\s*\d+[A-Z]?\s*\n?\s*[A-Z]+\s+[A-Z]{2}\s+\d{5}(?:-\d{4})?)',
                # Single line with apt
                r'(\d{5}\s+[A-Z\s]+(?:ST|AVE|BLVD|RD|DR)\s+(?:APT|UNIT)\s+\d+)',
                # Full address in residence info section
                r'(\d{5}\s+[A-Z\s]+\n?[A-Z\s]+\n?[A-Z]+\s+TX\s+\d{5}-\d{4})',
            ],
            'coverage_amount': [
                r'COVERAGE-C-PERSONAL\s+PROPERTY\s+\$(\d{1,3}(?:,\d{3})*)',
                r'Personal\s+Property\s+\$(\d{1,3}(?:,\d{3})*)',
            ],
            'liability_coverage': [
                r'COVERAGE-E-PERSONAL\s+LIABILITY[^\$]*\$(\d{1,3}(?:,\d{3})*)',
                r'Personal\s+Liability[^\$]*\$(\d{1,3}(?:,\d{3})*)',
            ],
            'deductible': [
                r'Deductible:\s*\$(\d{1,3}(?:,\d{3})*)\s+ALL',
                r'Deductible\s+\$(\d{1,3}(?:,\d{3})*)',
            ],
            'effective_date': [
                # Get date from "Policy Period From: OCT 04, 2024"
                r'Policy\s+Period\s+From:\s*([A-Z]{3}\s+\d{1,2},\s+\d{4})',
                # Avoid "Issued:" date
                r'OCT\s+\d{2},\s+\d{4}\s+to\s+OCT',
            ],
            'expiration_date': [
                r'to\s+([A-Z]{3}\s+\d{1,2},\s+\d{4})',
                r'Policy\s+Period.*?to\s+([A-Z]{3}\s+\d{1,2},\s+\d{4})',
            ],
            'premium_amount': [
                r'Annual\s+Renewal\s+Premium\s+\$(\d{1,3}(?:,\d{3})*\.?\d{0,2})',
                r'BILLING\s+ACCOUNT\s+\$(\d{1,3}(?:,\d{3})*\.?\d{0,2})',
            ],
            'insurance_company': [
                r'(NATIONWIDE\s+MUTUAL\s+INSURANCE\s+COMPANY)',
                r'Issued\s+By:\s+(NATIONWIDE[^\n]+)',
            ],
        }