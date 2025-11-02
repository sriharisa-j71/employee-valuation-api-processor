"""Ultra-fast JSON parsing using simdjson and JSONPath"""
import logging
from typing import Dict, Any, Optional

try:
    import simdjson
    SIMDJSON_AVAILABLE = True
except ImportError:
    import orjson
    SIMDJSON_AVAILABLE = False

logger = logging.getLogger(__name__)


class UltraFastParser:
    """Ultra-fast JSON parsing using simdjson for maximum performance"""
    
    def __init__(self):
        self.use_simdjson = SIMDJSON_AVAILABLE
        if self.use_simdjson:
            logger.info("Using simdjson for ultra-fast parsing")
        else:
            logger.info("Using orjson fallback parsing")
    
    def parse_json_fast(self, json_bytes: bytes) -> Dict[str, Any]:
        """Parse JSON with fastest available method"""
        if self.use_simdjson:
            try:
                return simdjson.loads(json_bytes)
            except Exception as e:
                logger.warning(f"simdjson failed, falling back to orjson: {e}")
                return orjson.loads(json_bytes)
        else:
            return orjson.loads(json_bytes)
    
    def extract_salary_fields(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Extract salary fields with compiled field accessors"""
        # Pre-compiled field extraction for maximum speed
        result = {}
        
        # Direct field access (fastest)
        result['base_salary'] = self._fast_float_extract(data, 'base_salary', 50000.0)
        result['bonus'] = self._fast_float_extract(data, 'bonus', 5000.0)
        result['years_of_service'] = self._fast_float_extract(data, 'years_of_service', 1.0)
        
        return result
    
    def extract_loans_fields(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Extract loans fields with compiled field accessors"""
        result = {}
        
        result['repayment_score'] = self._fast_float_extract(data, 'repayment_score', 80.0)
        result['outstanding_amount'] = self._fast_float_extract(data, 'outstanding_amount', 0.0)
        
        return result
    
    def extract_awards_fields(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Extract awards fields with compiled field accessors"""
        result = {}
        
        result['total_awards'] = self._fast_float_extract(data, 'total_awards', 0.0)
        result['recognitions'] = self._fast_float_extract(data, 'recognitions', 0.0)
        result['performance_rating'] = self._fast_float_extract(data, 'performance_rating', 3.0)
        
        return result
    
    def _fast_float_extract(self, data: Dict[str, Any], key: str, default: float) -> float:
        """Ultra-fast float extraction with minimal overhead"""
        try:
            value = data.get(key)
            if value is None:
                return default
            
            # Fast path for already numeric values
            if isinstance(value, (int, float)):
                return float(value)
            
            # String conversion
            if isinstance(value, str):
                return float(value)
            
            return default
        except (TypeError, ValueError):
            return default


class BatchResponseProcessor:
    """Process multiple API responses in batches for improved throughput"""
    
    def __init__(self):
        self.ultra_parser = UltraFastParser()
    
    def process_response_batch(self, responses: list[tuple[bytes, str]]) -> list[Dict[str, float]]:
        """Process multiple responses in a single batch operation"""
        results = []
        
        for response_content, response_type in responses:
            try:
                data = self.ultra_parser.parse_json_fast(response_content)
                
                if response_type == 'salary':
                    parsed = self.ultra_parser.extract_salary_fields(data)
                elif response_type == 'loans':
                    parsed = self.ultra_parser.extract_loans_fields(data)
                elif response_type == 'awards':
                    parsed = self.ultra_parser.extract_awards_fields(data)
                else:
                    parsed = {}
                
                results.append(parsed)
                
            except Exception as e:
                logger.error(f"Failed to process {response_type} response: {e}")
                results.append({})
        
        return results