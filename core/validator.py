from typing import Dict, Any, List, Tuple
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataValidator:
    """Validate extracted insurance data for accuracy and completeness."""
    
    @staticmethod
    def validate_policy_number(policy_number: str) -> Tuple[bool, str]:
        """Validate policy number format."""
        if not policy_number or policy_number == '-':
            return False, "Policy number is missing"
        
        # Should be alphanumeric with possible hyphens
        if not re.match(r'^[A-Z0-9\-]{5,20}$', policy_number, re.IGNORECASE):
            return False, "Policy number format appears invalid"
        
        return True, "Valid"
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Validate policyholder name."""
        if not name or name == '-':
            return False, "Name is missing"
        
        # Should have at least first and last name
        parts = name.strip().split()
        if len(parts) < 2:
            return False, "Name should include first and last name"
        
        # Check if contains numbers (likely OCR error)
        if re.search(r'\d', name):
            return False, "Name contains numbers (possible OCR error)"
        
        return True, "Valid"
    
    @staticmethod
    def validate_address(address: str) -> Tuple[bool, str]:
        """Validate property address."""
        if not address or address == '-':
            return False, "Address is missing"
        
        if len(address) < 10:
            return False, "Address appears incomplete"
        
        return True, "Valid"
    
    @staticmethod
    def validate_currency(amount: str, field_name: str) -> Tuple[bool, str]:
        """Validate currency amounts."""
        if not amount or amount == '-':
            return False, f"{field_name} is missing"
        
        # Remove $ and commas
        clean_amount = amount.replace('$', '').replace(',', '')
        
        try:
            value = float(clean_amount)
            
            # Sanity checks for insurance amounts
            if field_name == "coverage_amount" and (value < 1000 or value > 1000000):
                return False, f"{field_name} outside typical range ($1k-$1M)"
            
            if field_name == "liability_coverage" and (value < 10000 or value > 10000000):
                return False, f"{field_name} outside typical range ($10k-$10M)"
            
            if field_name == "deductible" and (value < 100 or value > 10000):
                return False, f"{field_name} outside typical range ($100-$10k)"
            
            if field_name == "premium_amount" and (value < 50 or value > 10000):
                return False, f"{field_name} outside typical range ($50-$10k)"
            
            return True, "Valid"
            
        except ValueError:
            return False, f"{field_name} is not a valid number"
    
    @staticmethod
    def validate_date(date_str: str, field_name: str) -> Tuple[bool, str]:
        """Validate date format."""
        if not date_str or date_str == '-':
            return False, f"{field_name} is missing"
        
        # Try common date formats
        formats = ['%m/%d/%Y', '%m-%d-%Y', '%m/%d/%y', '%m-%d-%y']
        
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                
                # Check if date is reasonable (between 1990 and 2050)
                if parsed_date.year < 1990 or parsed_date.year > 2050:
                    return False, f"{field_name} year appears incorrect"
                
                return True, "Valid"
            except ValueError:
                continue
        
        return False, f"{field_name} format is invalid"
    
    @staticmethod
    def validate_date_range(effective_date: str, expiration_date: str) -> Tuple[bool, str]:
        """Validate that expiration date is after effective date."""
        if not effective_date or not expiration_date:
            return True, "Cannot validate - dates missing"
        
        formats = ['%m/%d/%Y', '%m-%d-%Y', '%m/%d/%y', '%m-%d-%y']
        
        for fmt in formats:
            try:
                eff = datetime.strptime(effective_date, fmt)
                exp = datetime.strptime(expiration_date, fmt)
                
                if exp <= eff:
                    return False, "Expiration date must be after effective date"
                
                # Typical policy is 6 months to 1 year
                days_diff = (exp - eff).days
                if days_diff < 30 or days_diff > 400:
                    return False, f"Policy duration ({days_diff} days) seems unusual"
                
                return True, "Valid"
            except ValueError:
                continue
        
        return True, "Cannot validate - date format unknown"
    
    @staticmethod
    def validate_all(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate all fields in extracted data.
        Returns validation results with issues flagged.
        """
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'field_validations': {}
        }
        
        # Validate policy number
        if data.get('policy_number'):
            is_valid, msg = DataValidator.validate_policy_number(data['policy_number'])
            validation_results['field_validations']['policy_number'] = {
                'valid': is_valid,
                'message': msg
            }
            if not is_valid:
                validation_results['errors'].append(f"Policy Number: {msg}")
                validation_results['is_valid'] = False
        
        # Validate name
        if data.get('policyholder_name'):
            is_valid, msg = DataValidator.validate_name(data['policyholder_name'])
            validation_results['field_validations']['policyholder_name'] = {
                'valid': is_valid,
                'message': msg
            }
            if not is_valid:
                validation_results['warnings'].append(f"Policyholder Name: {msg}")
        
        # Validate address
        if data.get('property_address'):
            is_valid, msg = DataValidator.validate_address(data['property_address'])
            validation_results['field_validations']['property_address'] = {
                'valid': is_valid,
                'message': msg
            }
            if not is_valid:
                validation_results['warnings'].append(f"Property Address: {msg}")
        
        # Validate currency amounts
        currency_fields = {
            'coverage_amount': 'coverage_amount',
            'liability_coverage': 'liability_coverage',
            'deductible': 'deductible',
            'premium_amount': 'premium_amount'
        }
        
        for field_key, field_name in currency_fields.items():
            if data.get(field_key):
                is_valid, msg = DataValidator.validate_currency(
                    data[field_key], 
                    field_name
                )
                validation_results['field_validations'][field_key] = {
                    'valid': is_valid,
                    'message': msg
                }
                if not is_valid:
                    validation_results['warnings'].append(f"{field_name.replace('_', ' ').title()}: {msg}")
        
        # Validate dates
        if data.get('effective_date'):
            is_valid, msg = DataValidator.validate_date(
                data['effective_date'], 
                'effective_date'
            )
            validation_results['field_validations']['effective_date'] = {
                'valid': is_valid,
                'message': msg
            }
            if not is_valid:
                validation_results['warnings'].append(f"Effective Date: {msg}")
        
        if data.get('expiration_date'):
            is_valid, msg = DataValidator.validate_date(
                data['expiration_date'], 
                'expiration_date'
            )
            validation_results['field_validations']['expiration_date'] = {
                'valid': is_valid,
                'message': msg
            }
            if not is_valid:
                validation_results['warnings'].append(f"Expiration Date: {msg}")
        
        # Validate date range
        if data.get('effective_date') and data.get('expiration_date'):
            is_valid, msg = DataValidator.validate_date_range(
                data['effective_date'],
                data['expiration_date']
            )
            validation_results['field_validations']['date_range'] = {
                'valid': is_valid,
                'message': msg
            }
            if not is_valid:
                validation_results['errors'].append(f"Date Range: {msg}")
                validation_results['is_valid'] = False
        
        # Check completeness
        required_fields = [
            'policy_number', 
            'policyholder_name', 
            'property_address',
            'coverage_amount'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not data.get(field) or data.get(field) == '-':
                missing_fields.append(field.replace('_', ' ').title())
        
        if missing_fields:
            validation_results['warnings'].append(
                f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # Overall confidence check
        if data.get('confidence_score', 0) < 50:
            validation_results['warnings'].append(
                f"Low extraction confidence: {data.get('confidence_score', 0)}%"
            )
        
        logger.info(f"Validation complete: {len(validation_results['errors'])} errors, "
                   f"{len(validation_results['warnings'])} warnings")
        
        return validation_results
    
    @staticmethod
    def should_flag_for_review(data: Dict[str, Any], validation_results: Dict[str, Any]) -> bool:
        """
        Determine if extracted data should be flagged for human review.
        """
        # Flag if validation failed
        if not validation_results['is_valid']:
            return True
        
        # Flag if low confidence
        if data.get('confidence_score', 0) < 70:
            return True
        
        # Flag if multiple warnings
        if len(validation_results['warnings']) >= 3:
            return True
        
        # Flag if critical fields missing
        critical_fields = ['policy_number', 'policyholder_name', 'coverage_amount']
        missing_critical = sum(
            1 for field in critical_fields 
            if not data.get(field) or data.get(field) == '-'
        )
        
        if missing_critical >= 2:
            return True
        
        return False