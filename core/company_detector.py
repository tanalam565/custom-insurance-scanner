import re
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class CompanyDetector:
    COMPANY_PATTERNS = {
        'state_farm': {
            'patterns': [
                r'State\s*Farm',
                r'statefarm\.com',
                r'Like\s*a\s*good\s*neighbor',
            ],
            'confidence': 0.95
        },
        'allstate': {
            'patterns': [
                r'Allstate',
                r'allstate\.com',
                r'You\'re\s*in\s*good\s*hands',
            ],
            'confidence': 0.95
        },
        'progressive': {
            'patterns': [
                r'Progressive',
                r'progressive\.com',
            ],
            'confidence': 0.95
        },
        'usaa': {
            'patterns': [
                r'USAA',
                r'usaa\.com',
            ],
            'confidence': 0.95
        },
        'nationwide': {
            'patterns': [
                r'Nationwide',
                r'nationwide\.com',
            ],
            'confidence': 0.95
        },
        'travelers': {
            'patterns': [
                r'Travelers',
                r'travelers\.com',
            ],
            'confidence': 0.95
        },
        'liberty_mutual': {
            'patterns': [
                r'Liberty\s*Mutual',
                r'libertymutual\.com',
            ],
            'confidence': 0.95
        },
        'farmers': {
            'patterns': [
                r'Farmers\s*Insurance',
                r'farmers\.com',
            ],
            'confidence': 0.95
        },
        'geico': {
            'patterns': [
                r'GEICO',
                r'geico\.com',
            ],
            'confidence': 0.95
        },
        'american_family': {
            'patterns': [
                r'American\s*Family',
                r'amfam\.com',
            ],
            'confidence': 0.95
        },
        'erie': {
            'patterns': [
                r'Erie\s*Insurance',
                r'erieinsurance\.com',
            ],
            'confidence': 0.95
        },
        'amica': {
            'patterns': [
                r'Amica\s*Mutual',
                r'amica\.com',
            ],
            'confidence': 0.95
        },
        'csaa': {
            'patterns': [
                r'CSAA\s*Insurance',
                r'AAA\s*Insurance',
                r'csaa-ig\.com',
            ],
            'confidence': 0.95
        },
        'chubb': {
            'patterns': [
                r'Chubb',
                r'chubb\.com',
            ],
            'confidence': 0.95
        },
        'hartford': {
            'patterns': [
                r'The\s*Hartford',
                r'thehartford\.com',
            ],
            'confidence': 0.95
        },
        'country_financial': {
            'patterns': [
                r'Country\s*Financial',
                r'countryfinancial\.com',
            ],
            'confidence': 0.95
        },
        'lemonade': {
            'patterns': [
                r'Lemonade\s*Insurance',
                r'lemonade\.com',
            ],
            'confidence': 0.95
        },
        'hanover': {
            'patterns': [
                r'The\s*Hanover',
                r'hanover\.com',
            ],
            'confidence': 0.95
        },
    }
    
    @staticmethod
    def detect_company(text: str) -> Tuple[str, float]:
        text_sample = text[:2000]
        best_match = ('generic', 0.0)
        
        for company, data in CompanyDetector.COMPANY_PATTERNS.items():
            match_count = 0
            for pattern in data['patterns']:
                if re.search(pattern, text_sample, re.IGNORECASE):
                    match_count += 1
            
            if match_count > 0:
                confidence = data['confidence'] * (match_count / len(data['patterns']))
                if confidence > best_match[1]:
                    best_match = (company, confidence)
        
        logger.info(f"Detected: {best_match[0]} ({best_match[1]:.2f})")
        return best_match