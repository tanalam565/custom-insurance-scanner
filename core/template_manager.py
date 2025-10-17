class TemplateManager:
    """Manages coordinate templates for different insurance companies"""
    
    def __init__(self):
        self.templates = self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize coordinate templates for all companies"""
        return {
            'nationwide': {
                'insurance_company': (190, 42, 150, 30),  # "Nationwide" logo text
                'policy_number': (530, 84, 150, 20),  # "78 42 HS 027914"
                'date_prepared': (720, 84, 150, 20),  # "AUG 21, 2024"
                'insurer_name': (518, 242, 250, 20),  # "CHRISTINA NOLDEN"
                'insurer_address': (518, 260, 300, 20),  # "13555 BRETON RIDGE ST APT 118"
                'insurer_city_state': (518, 277, 300, 20),  # "HOUSTON TX 77070-5819"
                'insurance_amount': (830, 741, 60, 20),  # "$285.24"
                'property_address': (518, 260, 300, 40),  # Full address
                'effective_date': (150, 450, 150, 20),  # From policy declarations
                'expiration_date': (150, 470, 150, 20),  # From policy declarations
                'agent_name': (103, 330, 200, 20),  # "KATHYE CARPENTER"
                'agent_number': (103, 347, 150, 20),  # "00068474"
            },
            
            'state_farm': {
                'insurance_company': (100, 40, 200, 35),
                'policy_number': (400, 85, 150, 22),
                'date_prepared': (580, 85, 100, 22),
                'insurer_name': (400, 210, 280, 22),
                'insurer_address': (400, 235, 280, 22),
                'insurer_city_state': (400, 260, 280, 22),
                'insurance_amount': (600, 640, 160, 22),
                'property_address': (130, 310, 320, 22),
                'effective_date': (420, 160, 130, 22),
                'expiration_date': (580, 160, 130, 22),
            },
            
            'allstate': {
                'insurance_company': (120, 30, 180, 40),
                'policy_number': (430, 80, 140, 20),
                'date_prepared': (600, 80, 95, 20),
                'insurer_name': (420, 200, 270, 20),
                'insurer_address': (420, 220, 270, 20),
                'insurer_city_state': (420, 240, 270, 20),
                'insurance_amount': (620, 625, 155, 20),
                'property_address': (140, 295, 310, 20),
                'effective_date': (435, 155, 125, 20),
                'expiration_date': (590, 155, 125, 20),
            },
            
            'progressive': {
                'insurance_company': (140, 35, 170, 35),
                'policy_number': (445, 82, 135, 21),
                'date_prepared': (605, 82, 98, 21),
                'insurer_name': (430, 205, 265, 21),
                'insurer_address': (430, 227, 265, 21),
                'insurer_city_state': (430, 249, 265, 21),
                'insurance_amount': (630, 635, 158, 21),
                'property_address': (145, 305, 315, 21),
                'effective_date': (440, 158, 128, 21),
                'expiration_date': (595, 158, 128, 21),
            },
            
            'usaa': {
                'insurance_company': (130, 38, 160, 32),
                'policy_number': (440, 78, 130, 19),
                'date_prepared': (595, 78, 93, 19),
                'insurer_name': (425, 203, 260, 19),
                'insurer_address': (425, 224, 260, 19),
                'insurer_city_state': (425, 245, 260, 19),
                'insurance_amount': (625, 628, 153, 19),
                'property_address': (135, 298, 305, 19),
                'effective_date': (433, 153, 123, 19),
                'expiration_date': (588, 153, 123, 19),
            },
            
            'travelers': {
                'insurance_company': (145, 32, 175, 38),
                'policy_number': (450, 84, 138, 22),
                'date_prepared': (608, 84, 97, 22),
                'insurer_name': (435, 208, 268, 22),
                'insurer_address': (435, 232, 268, 22),
                'insurer_city_state': (435, 256, 268, 22),
                'insurance_amount': (635, 638, 160, 22),
                'property_address': (148, 308, 318, 22),
                'effective_date': (443, 161, 130, 22),
                'expiration_date': (600, 161, 130, 22),
            },
            
            'liberty_mutual': {
                'insurance_company': (125, 36, 185, 34),
                'policy_number': (442, 79, 133, 20),
                'date_prepared': (600, 79, 94, 20),
                'insurer_name': (428, 204, 263, 20),
                'insurer_address': (428, 226, 263, 20),
                'insurer_city_state': (428, 248, 263, 20),
                'insurance_amount': (628, 630, 155, 20),
                'property_address': (138, 300, 308, 20),
                'effective_date': (436, 155, 125, 20),
                'expiration_date': (590, 155, 125, 20),
            },
            
            'farmers': {
                'insurance_company': (135, 34, 165, 36),
                'policy_number': (448, 81, 136, 21),
                'date_prepared': (603, 81, 96, 21),
                'insurer_name': (432, 206, 266, 21),
                'insurer_address': (432, 229, 266, 21),
                'insurer_city_state': (432, 252, 266, 21),
                'insurance_amount': (632, 633, 157, 21),
                'property_address': (143, 303, 313, 21),
                'effective_date': (440, 157, 127, 21),
                'expiration_date': (593, 157, 127, 21),
            },
            
            'geico': {
                'insurance_company': (150, 37, 155, 33),
                'policy_number': (455, 83, 125, 20),
                'date_prepared': (607, 83, 92, 20),
                'insurer_name': (437, 207, 255, 20),
                'insurer_address': (437, 230, 255, 20),
                'insurer_city_state': (437, 253, 255, 20),
                'insurance_amount': (637, 636, 152, 20),
                'property_address': (150, 306, 305, 20),
                'effective_date': (445, 159, 122, 20),
                'expiration_date': (595, 159, 122, 20),
            },
            
            'generic': {
                'insurance_company': (150, 35, 160, 35),
                'policy_number': (450, 80, 130, 20),
                'date_prepared': (600, 80, 95, 20),
                'insurer_name': (430, 205, 260, 20),
                'insurer_address': (430, 227, 260, 20),
                'insurer_city_state': (430, 249, 260, 20),
                'insurance_amount': (630, 632, 155, 20),
                'property_address': (145, 302, 310, 20),
                'effective_date': (438, 156, 125, 20),
                'expiration_date': (590, 156, 125, 20),
            }
        }
    
    def get_template(self, company_name):
        """Get coordinate template for a company
        
        Args:
            company_name: Company identifier
            
        Returns:
            Dictionary of field coordinates
        """
        return self.templates.get(company_name, self.templates['generic'])
    
    def add_template(self, company_name, template):
        """Add or update a company template
        
        Args:
            company_name: Company identifier
            template: Dictionary of field coordinates
        """
        self.templates[company_name] = template
    
    def get_field_coords(self, company_name, field_name):
        """Get coordinates for a specific field
        
        Args:
            company_name: Company identifier
            field_name: Field name
            
        Returns:
            Tuple of (x, y, w, h) or None
        """
        template = self.get_template(company_name)
        return template.get(field_name)
    
    def get_all_fields(self, company_name):
        """Get all available fields for a company
        
        Args:
            company_name: Company identifier
            
        Returns:
            List of field names
        """
        template = self.get_template(company_name)
        return list(template.keys())
    
    def has_field(self, company_name, field_name):
        """Check if a company template has a specific field
        
        Args:
            company_name: Company identifier
            field_name: Field name
            
        Returns:
            Boolean
        """
        template = self.get_template(company_name)
        return field_name in template