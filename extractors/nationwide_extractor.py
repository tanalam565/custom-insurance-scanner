from extractors.base_extractor import BaseExtractor

class NationwideExtractor(BaseExtractor):
    """Extractor for Nationwide insurance documents"""
    
    def get_company_name(self):
        return 'nationwide'
    
    def extract_custom_fields(self, img):
        """Extract Nationwide-specific fields"""
        custom_data = {}
        
        # Agent name
        agent_coords = (103, 330, 200, 20)
        try:
            roi = self.processor.extract_roi(img, agent_coords)
            processed = self.processor.preprocess_roi(roi)
            text = self.ocr.extract_text(processed)
            custom_data['agent_name'] = self.ocr.clean_name(text)
        except Exception as e:
            custom_data['agent_name'] = ''
        
        # Agent number
        agent_num_coords = (103, 347, 150, 20)
        try:
            roi = self.processor.extract_roi(img, agent_num_coords)
            processed = self.processor.preprocess_roi(roi)
            text = self.ocr.extract_text(processed)
            custom_data['agent_number'] = text.strip()
        except Exception as e:
            custom_data['agent_number'] = ''
        
        return custom_data
    
    def post_process(self, data):
        """Post-process Nationwide data"""
        # Clean up company name
        if 'insurance_company' in data:
            data['insurance_company'] = 'Nationwide'
        
        # Ensure proper formatting for policy number
        if data.get('policy_number'):
            # Nationwide format: typically alphanumeric with spaces
            policy = data['policy_number'].strip()
            data['policy_number'] = policy
        
        return data