from extractors.base_extractor import BaseExtractor

class StateFarmExtractor(BaseExtractor):
    """Extractor for State Farm insurance documents"""
    
    def get_company_name(self):
        return 'state_farm'
    
    def extract_custom_fields(self, img):
        """Extract State Farm-specific fields"""
        custom_data = {}
        
        # State Farm specific fields
        # Agent information
        agent_coords = (420, 280, 200, 20)
        try:
            roi = self.processor.extract_roi(img, agent_coords)
            processed = self.processor.preprocess_roi(roi)
            text = self.ocr.extract_text(processed)
            custom_data['agent_name'] = self.ocr.clean_name(text)
        except Exception as e:
            custom_data['agent_name'] = ''
        
        return custom_data
    
    def post_process(self, data):
        """Post-process State Farm data"""
        if 'insurance_company' in data:
            data['insurance_company'] = 'State Farm'
        
        # State Farm policy numbers are typically numeric
        if data.get('policy_number'):
            policy = data['policy_number'].replace('-', '').replace(' ', '')
            data['policy_number'] = policy
        
        return data