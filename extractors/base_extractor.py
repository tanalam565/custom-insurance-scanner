from abc import ABC, abstractmethod
from typing import Dict, Any
import re
import logging

logger = logging.getLogger(__name__)

class BaseExtractor(ABC):
    """Base class for all company-specific extractors."""
    
    def __init__(self):
        self.company_name = "Unknown"
    
    @abstractmethod
    def get_patterns(self) -> Dict[str, list]:
        """
        Return company-specific regex patterns.
        Override this in each extractor.
        """
        pass
    
    def extract(self, text: str) -> Dict[str, Any]:
        """Main extraction method."""
        patterns = self.get_patterns()
        data = {}
        
        for field, pattern_list in patterns.items():
            data[field] = self._extract_field(text, pattern_list)
        
        # Add metadata
        data['detected_company'] = self.company_name
        data['confidence_score'] = self._calculate_confidence(data)
        data['raw_text_preview'] = text[:500]
        
        return data
    
    def _extract_field(self, text: str, patterns: list) -> Any:
        """Extract single field using multiple patterns."""
        for pattern in patterns:
            try:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    value = match.group(1).strip()
                    value = ' '.join(value.split())  # Clean whitespace
                    return self._format_value(pattern, value)
            except Exception as e:
                logger.warning(f"Pattern error: {e}")
                continue
        return None
    
    def _format_value(self, pattern: str, value: str) -> str:
        """Format extracted value based on field type."""
        # Add $ for currency fields
        if any(word in pattern.lower() for word in ['premium', 'coverage', 'liability', 'deductible', 'amount']):
            if not value.startswith('$') and value[0].isdigit():
                return f"${value}"
        return value
    
    def _calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate extraction confidence."""
        total_fields = len([k for k in data.keys() if k not in ['detected_company', 'confidence_score', 'raw_text_preview']])
        extracted_fields = sum(1 for v in data.values() if v not in [None, ''] and not isinstance(v, (int, float)))
        
        if total_fields == 0:
            return 0.0
        
        return round((extracted_fields / total_fields) * 100, 2)