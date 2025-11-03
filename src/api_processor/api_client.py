"""HTTP client and API call handling"""
import asyncio
import logging
from typing import Any

import httpx
import orjson

from .config import Config
from .optimized_parser import LightweightResponseParser
from .performance_decorators import measure_async_performance, measure_performance

logger = logging.getLogger(__name__)


class APIClient:
    """HTTP client with connection pooling and retry logic"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client: httpx.AsyncClient | None = None
        self.parser = LightweightResponseParser()  # Lightweight parser for medium-scale data
    
    @measure_performance(include_memory=True, threshold_ms=5.0)
    def create_client(self) -> httpx.AsyncClient:
        """Create httpx AsyncClient optimized for multi-host environments"""
        http_config = self.config.http
        
        # Multi-host optimized connection limits
        limits = httpx.Limits(
            max_connections=http_config.get("max_connections", 100),
            max_keepalive_connections=http_config.get("max_keepalive_connections", 50),
            keepalive_expiry=http_config.get("keepalive_expiry", 300.0)
        )
        
        # Separate connect and read timeouts for real networks
        timeout = httpx.Timeout(
            connect=http_config.get("connect_timeout", 10.0),
            read=http_config.get("timeout", 30.0),
            write=5.0,
            pool=2.0
        )
        
        client = httpx.AsyncClient(
            limits=limits,
            timeout=timeout,
            http2=True,  # HTTP/2 multiplexing beneficial for multiple requests per host
            follow_redirects=True,  # Handle redirects in production environments
            verify=True  # SSL verification for production HTTPS endpoints
        )
        
        logger.info(
            f"Multi-host HTTP Client initialized: "
            f"max_conn={limits.max_connections}, "
            f"keepalive={limits.max_keepalive_connections}, "
            f"connect_timeout={timeout.connect}s, read_timeout={timeout.read}s"
        )
        
        return client
    
    @measure_async_performance(include_memory=True, threshold_ms=10.0, include_args=True)
    async def call_with_retry(self, url: str, row_id: int, response_type: str, headers: dict = None) -> dict[str, Any]:
        """Call API with optimized retry logic and parsing"""
        if self.client is None:
            raise RuntimeError("API client not initialized. Use async context manager.")

        max_retries = self.config.max_retries
        request_headers = headers or {}
        
        for attempt in range(max_retries):
            try:
                response = await self.client.get(url, headers=request_headers)
                response.raise_for_status()
                
                # Use optimized parser based on response type
                if response_type == 'salary':
                    parsed_data = self.parser.parse_salary_response(response.content)
                    # Extract token from response headers for dependent APIs
                    if 'X-Salary-Token' in response.headers:
                        parsed_data['_salary_token'] = response.headers['X-Salary-Token']
                elif response_type == 'loans':
                    parsed_data = self.parser.parse_loans_response(response.content)
                    # Extract token from response headers for dependent APIs
                    if 'X-Loan-Token' in response.headers:
                        parsed_data['_loan_token'] = response.headers['X-Loan-Token']
                elif response_type == 'awards':
                    parsed_data = self.parser.parse_awards_response(response.content)
                else:
                    # Fallback to original parsing
                    parsed_data = orjson.loads(response.content)
                
                return parsed_data
                    
            except httpx.TimeoutException:
                logger.warning(f"Row {row_id}: Timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    # Reduced exponential backoff: 0.5s, 1s, 2s instead of 1s, 2s, 4s
                    await asyncio.sleep(0.5 * (2 ** attempt))
                else:
                    raise
            except httpx.HTTPStatusError as e:
                logger.warning(f"Row {row_id}: HTTP {e.response.status_code} (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    # Faster retry for HTTP errors (likely server issues, not network)
                    await asyncio.sleep(0.3 * (attempt + 1))
                else:
                    raise
            except Exception as e:
                logger.warning(f"Row {row_id}: {type(e).__name__}: {e} (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    await asyncio.sleep(0.5 * (2 ** attempt))
                else:
                    raise
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.client = self.create_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.aclose()
