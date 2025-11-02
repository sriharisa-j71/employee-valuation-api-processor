"""High-performance API response parsing optimized for medium-scale datasets"""
import orjson
from typing import Any, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)


class LightweightResponseParser:
    """Lightweight, fast API response parser without heavy validation overhead"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize with optional configuration for field mappings"""
        self.config = config or {}
        
        # Default field mappings - can be overridden via config
        self.salary_fields = self.config.get('salary_field_mappings', {
            'base_salary': ['base_salary', 'salary', 'basic_salary'],
            'bonus': ['bonus', 'incentive', 'additional_pay'],
            'years_of_service': ['years_of_service', 'service_years', 'experience_years']
        })
        
        self.loans_fields = self.config.get('loans_field_mappings', {
            'repayment_score': ['repayment_score', 'credit_score', 'payment_rating'],
            'outstanding_amount': ['outstanding_amount', 'outstanding', 'debt_amount']
        })
        
        self.awards_fields = self.config.get('awards_field_mappings', {
            'total_awards': ['total_awards', 'awards_count', 'awards'],
            'recognitions': ['recognitions', 'recognition_count', 'honors'],
            'performance_rating': ['performance_rating', 'rating', 'performance_score']
        })
        
        # Pre-compile defaults for speed
        self.defaults = {
            'salary': {'base_salary': 50000.0, 'bonus': 5000.0, 'years_of_service': 1.0},
            'loans': {'repayment_score': 80.0, 'outstanding_amount': 0.0},
            'awards': {'total_awards': 0.0, 'recognitions': 0.0, 'performance_rating': 3.0}
        }
    
    def _fast_extract(self, data: Dict[str, Any], field_candidates: list, default: float) -> float:
        """Ultra-fast field extraction with fallback chain"""
        # Try each field candidate in order
        for field in field_candidates:
            value = data.get(field)
            if value is not None:
                # Fast numeric conversion
                if isinstance(value, (int, float)):
                    return float(value)
                elif isinstance(value, str):
                    try:
                        return float(value)
                    except ValueError:
                        continue
        return default
    
    def parse_salary_response(self, json_bytes: bytes) -> Dict[str, float]:
        """Parse salary API response - optimized for speed"""
        try:
            data = orjson.loads(json_bytes)
        except orjson.JSONDecodeError:
            return self.defaults['salary'].copy()
        
        return {
            'base_salary': self._fast_extract(data, self.salary_fields['base_salary'], 50000.0),
            'bonus': self._fast_extract(data, self.salary_fields['bonus'], 5000.0),
            'years_of_service': self._fast_extract(data, self.salary_fields['years_of_service'], 1.0)
        }
    
    def parse_loans_response(self, json_bytes: bytes) -> Dict[str, float]:
        """Parse loans API response - optimized for speed"""
        try:
            data = orjson.loads(json_bytes)
        except orjson.JSONDecodeError:
            return self.defaults['loans'].copy()
        
        return {
            'repayment_score': self._fast_extract(data, self.loans_fields['repayment_score'], 80.0),
            'outstanding_amount': self._fast_extract(data, self.loans_fields['outstanding_amount'], 0.0)
        }
    
    def parse_awards_response(self, json_bytes: bytes) -> Dict[str, float]:
        """Parse awards API response - optimized for speed"""
        try:
            data = orjson.loads(json_bytes)
        except orjson.JSONDecodeError:
            return self.defaults['awards'].copy()
        
        return {
            'total_awards': self._fast_extract(data, self.awards_fields['total_awards'], 0.0),
            'recognitions': self._fast_extract(data, self.awards_fields['recognitions'], 0.0),
            'performance_rating': self._fast_extract(data, self.awards_fields['performance_rating'], 3.0)
        }


# Keep the old class name for backward compatibility
OptimizedResponseParser = LightweightResponseParser


class BatchOptimizer:
    """Optimize processing of multiple responses together"""
    
    def __init__(self):
        self.parser = LightweightResponseParser()
    
    def process_employee_responses(self, salary_bytes: bytes, loans_bytes: bytes, awards_bytes: bytes) -> tuple:
        """Process all three API responses for one employee in one go"""
        return (
            self.parser.parse_salary_response(salary_bytes),
            self.parser.parse_loans_response(loans_bytes),
            self.parser.parse_awards_response(awards_bytes)
        )