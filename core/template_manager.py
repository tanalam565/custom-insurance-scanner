from extractors.base_extractor import BaseExtractor
from extractors.state_farm_extractor import StateFarmExtractor
from extractors.allstate_extractor import AllstateExtractor
from extractors.progressive_extractor import ProgressiveExtractor
from extractors.usaa_extractor import USAAExtractor
from extractors.nationwide_extractor import NationwideExtractor
from extractors.travelers_extractor import TravelersExtractor
from extractors.liberty_mutual_extractor import LibertyMutualExtractor
from extractors.farmers_extractor import FarmersExtractor
from extractors.geico_extractor import GEICOExtractor
from extractors.american_family_extractor import AmericanFamilyExtractor
from extractors.erie_extractor import ErieExtractor
from extractors.amica_extractor import AmicaExtractor
from extractors.csaa_extractor import CSAAExtractor
from extractors.chubb_extractor import ChubbExtractor
from extractors.hartford_extractor import HartfordExtractor
from extractors.country_financial_extractor import CountryFinancialExtractor
from extractors.lemonade_extractor import LemonadeExtractor
from extractors.hanover_extractor import HanoverExtractor
from extractors.generic_extractor import GenericExtractor
import logging

logger = logging.getLogger(__name__)

class TemplateManager:
    """Route extraction to appropriate company-specific extractor."""
    
    EXTRACTOR_MAP = {
        'state_farm': StateFarmExtractor,
        'allstate': AllstateExtractor,
        'progressive': ProgressiveExtractor,
        'usaa': USAAExtractor,
        'nationwide': NationwideExtractor,
        'travelers': TravelersExtractor,
        'liberty_mutual': LibertyMutualExtractor,
        'farmers': FarmersExtractor,
        'geico': GEICOExtractor,
        'american_family': AmericanFamilyExtractor,
        'erie': ErieExtractor,
        'amica': AmicaExtractor,
        'csaa': CSAAExtractor,
        'chubb': ChubbExtractor,
        'hartford': HartfordExtractor,
        'country_financial': CountryFinancialExtractor,
        'lemonade': LemonadeExtractor,
        'hanover': HanoverExtractor,
        'generic': GenericExtractor,
    }
    
    @staticmethod
    def get_extractor(company_name: str, confidence: float) -> BaseExtractor:
        """
        Get appropriate extractor based on detected company.
        Falls back to generic if confidence < 70% or company not found.
        """
        # Use company-specific extractor if high confidence
        if confidence >= 0.70 and company_name in TemplateManager.EXTRACTOR_MAP:
            extractor_class = TemplateManager.EXTRACTOR_MAP[company_name]
            logger.info(f"Using {company_name} extractor (confidence: {confidence:.2f})")
            return extractor_class()
        
        # Fallback to generic extractor
        logger.info(f"Using generic extractor (company: {company_name}, confidence: {confidence:.2f})")
        return GenericExtractor()