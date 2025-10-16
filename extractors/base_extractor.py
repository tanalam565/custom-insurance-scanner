from abc import ABC, abstractmethod
from typing import Dict, Any
import re
import logging

logger = logging.getLogger(__name__)

class BaseExtractor(ABC):
    def __init__(self):
        self.company_name = "Unknown"
    
    @abstractmethod
    def get_patterns(self) -> Dict[str, list]:
        pass
    
    def extract(self, text: str) -> Dict[str, Any]:
        patterns = self.get_patterns()
        data = {}
        
        for field, pattern_list in patterns.items():
            data[field] = self._extract_field(text, pattern_list)
        
        data['detected_company'] = self.company_name
        data['confidence_score'] = self._calculate_confidence(data)
        data['raw_text_preview'] = text[:500]
        
        return data
    
    def _extract_field(self, text: str, patterns: list) -> Any:
        for pattern in patterns:
            try:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    value = match.group(1).strip()
                    value = ' '.join(value.split())
                    return self._format_value(pattern, value)
            except Exception as e:
                logger.warning(f"Pattern error: {e}")
                continue
        return None
    
    def _format_value(self, pattern: str, value: str) -> str:
        if any(word in pattern.lower() for word in ['premium', 'coverage', 'liability', 'deductible', 'amount']):
            if not value.startswith('$') and value[0].isdigit():
                return f"${value}"
        return value
    
    def _calculate_confidence(self, data: Dict[str, Any]) -> float:
        """
        Calculate extraction confidence score (0-100).
        Fixed to ensure result never exceeds 100.
        """
        # Fields to exclude from calculation
        exclude = ['detected_company', 'confidence_score', 'raw_text_preview']
        
        # Get all data fields (excluding metadata)
        data_fields = {k: v for k, v in data.items() if k not in exclude}
        
        total = len(data_fields)
        
        if total == 0:
            return 0.0
        
        # Count successfully extracted fields (not None, not empty, not '-')
        extracted = sum(
            1 for v in data_fields.values() 
            if v is not None and v != '' and v != '-'
        )
        
        # Calculate percentage
        confidence = (extracted / total) * 100
        
        # Ensure it never exceeds 100
        confidence = min(confidence, 100.0)
        
        return round(confidence, 2)