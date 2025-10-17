"""
Additional insurance company extractors
Copy these to individual files as needed
"""
from extractors.base_extractor import BaseExtractor

class AllstateExtractor(BaseExtractor):
    def get_company_name(self):
        return 'allstate'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'Allstate'
        return data

class ProgressiveExtractor(BaseExtractor):
    def get_company_name(self):
        return 'progressive'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'Progressive'
        return data

class UsaaExtractor(BaseExtractor):
    def get_company_name(self):
        return 'usaa'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'USAA'
        return data

class TravelersExtractor(BaseExtractor):
    def get_company_name(self):
        return 'travelers'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'Travelers'
        return data

class LibertyMutualExtractor(BaseExtractor):
    def get_company_name(self):
        return 'liberty_mutual'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'Liberty Mutual'
        return data

class FarmersExtractor(BaseExtractor):
    def get_company_name(self):
        return 'farmers'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'Farmers Insurance'
        return data

class GeicoExtractor(BaseExtractor):
    def get_company_name(self):
        return 'geico'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'GEICO'
        return data

class AmericanFamilyExtractor(BaseExtractor):
    def get_company_name(self):
        return 'american_family'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'American Family'
        return data

class ErieExtractor(BaseExtractor):
    def get_company_name(self):
        return 'erie'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'Erie Insurance'
        return data

class AmicaExtractor(BaseExtractor):
    def get_company_name(self):
        return 'amica'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'Amica Mutual'
        return data

class CsaaExtractor(BaseExtractor):
    def get_company_name(self):
        return 'csaa'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'CSAA Insurance Group'
        return data

class ChubbExtractor(BaseExtractor):
    def get_company_name(self):
        return 'chubb'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'Chubb'
        return data

class HartfordExtractor(BaseExtractor):
    def get_company_name(self):
        return 'hartford'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'The Hartford'
        return data

class CountryFinancialExtractor(BaseExtractor):
    def get_company_name(self):
        return 'country_financial'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'COUNTRY Financial'
        return data

class LemonadeExtractor(BaseExtractor):
    def get_company_name(self):
        return 'lemonade'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'Lemonade'
        return data

class HanoverExtractor(BaseExtractor):
    def get_company_name(self):
        return 'hanover'
    
    def post_process(self, data):
        if 'insurance_company' in data:
            data['insurance_company'] = 'The Hanover'
        return data