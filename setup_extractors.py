#!/usr/bin/env python3
# FILE: setup_extractors.py

import os
from pathlib import Path

def create_extractor_files():
    '''
    Automatically create all 16 extractor files.
    Run this script to generate all missing extractors.
    '''
    
    extractors_dir = Path('extractors')
    extractors_dir.mkdir(exist_ok=True)
    
    # Create __init__.py if it doesn't exist
    init_file = extractors_dir / '__init__.py'
    if not init_file.exists():
        init_file.write_text('# Auto-generated\\n')
    
    extractors = {
        'progressive': 'Progressive',
        'usaa': 'USAA',
        'nationwide': 'Nationwide',
        'travelers': 'Travelers',
        'liberty_mutual': 'Liberty Mutual',
        'farmers': 'Farmers Insurance',
        'geico': 'GEICO',
        'american_family': 'American Family',
        'erie': 'Erie Insurance',
        'amica': 'Amica Mutual',
        'csaa': 'CSAA Insurance Group (AAA)',
        'chubb': 'Chubb',
        'hartford': 'The Hartford',
        'country_financial': 'Country Financial',
        'lemonade': 'Lemonade',
        'hanover': 'The Hanover',
    }
    
    for key, name in extractors.items():
        filename = f'{key}_extractor.py'
        filepath = extractors_dir / filename
        
        if filepath.exists():
            print(f'✓ {filename} already exists')
            continue
        
        class_name = ''.join(word.capitalize() for word in key.split('_')) + 'Extractor'
        
        content = f'''from extractors.base_extractor import BaseExtractor

class {class_name}(BaseExtractor):
    def __init__(self):
        super().__init__()
        self.company_name = "{name}"
    
    def get_patterns(self):
        return {{
            'policy_number': [
                r'Policy\\s*(?:Number|#)\\s*:?\\s*([A-Z0-9\\-]+)',
            ],
            'policyholder_name': [
                r'Named\\s*Insured\\s*:?\\s*([A-Z][a-z]+(?:\\s+[A-Z][a-z]+)+)',
            ],
            'property_address': [
                r'Property\\s*Address\\s*:?\\s*(.+?)(?:\\n|$)',
            ],
            'coverage_amount': [
                r'Personal\\s*Property\\s*:?\\s*\\$?\\s*([\\d,]+)',
            ],
            'liability_coverage': [
                r'Personal\\s*Liability\\s*:?\\s*\\$?\\s*([\\d,]+)',
            ],
            'deductible': [
                r'Deductible\\s*:?\\s*\\$?\\s*([\\d,]+)',
            ],
            'effective_date': [
                r'Effective\\s*Date\\s*:?\\s*(\\d{{1,2}}[/-]\\d{{1,2}}[/-]\\d{{2,4}})',
            ],
            'expiration_date': [
                r'Expiration\\s*Date\\s*:?\\s*(\\d{{1,2}}[/-]\\d{{1,2}}[/-]\\d{{2,4}})',
            ],
            'premium_amount': [
                r'Total\\s*Premium\\s*:?\\s*\\$?\\s*([\\d,]+\\.?\\d*)',
            ],
            'insurance_company': [
                r'({name}[^\\n]*)',
            ],
        }}
'''
        
        filepath.write_text(content)
        print(f'✓ Created {filename}')
    
    print('\\n All extractors created successfully!')
    print('\\nNext steps:')
    print('1. Review and customize patterns for each company')
    print('2. Update core/template_manager.py with all imports')
    print('3. Test with real insurance documents')

if __name__ == '__main__':
    create_extractor_files()