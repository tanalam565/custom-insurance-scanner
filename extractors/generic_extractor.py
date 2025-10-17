from extractors.base_extractor import BaseExtractor

class GenericExtractor(BaseExtractor):
    """Generic extractor for unknown insurance companies"""
    
    def get_company_name(self):
        return 'generic'
    
    def extract_custom_fields(self, img):
        """No custom fields for generic extractor"""
        return {}
    
    def post_process(self, data):
        """Minimal post-processing for generic extraction"""
        # Try to clean up insurance company name if present
        if data.get('insurance_company'):
            company = data['insurance_company'].strip()
            # Capitalize words
            company = ' '.join(word.capitalize() for word in company.split())
            data['insurance_company'] = company
        else:
            data['insurance_company'] = 'Unknown'
        
        return data