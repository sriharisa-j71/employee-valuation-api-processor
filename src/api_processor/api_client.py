"""HTTP client and API call handling"""
import asyncio
import logging
from typing import Any

import httpx
import orjson

from .config import Config

logger = logging.getLogger(__name__)


class APIClient:
    """HTTP client with connection pooling and retry logic"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client: httpx.AsyncClient | None = None
    
    def create_client(self) -> httpx.AsyncClient:
        """Create httpx AsyncClient with connection pool configuration"""
        http_config = self.config.http
        
        limits = httpx.Limits(
            max_connections=http_config.get("max_connections", 50),
            max_keepalive_connections=http_config.get("max_keepalive_connections", 20),
            keepalive_expiry=http_config.get("keepalive_expiry", 30.0)
        )
        
        timeout = httpx.Timeout(http_config.get("timeout", 30.0))
        
        client = httpx.AsyncClient(
            limits=limits,
            timeout=timeout,
            http2=True
        )
        
        logger.info(
            f"HTTP Client initialized: "
            f"max_conn={limits.max_connections}, "
            f"keepalive={limits.max_keepalive_connections}, "
            f"timeout={timeout.read}s"
        )
        
        return client
    
    async def call_with_retry(self, url: str, row_id: int) -> dict[str, Any]:
        """Call API with exponential backoff retry logic"""
        if self.client is None:
            raise RuntimeError("API client not initialized. Use async context manager.")
        
        max_retries = self.config.max_retries
        
        for attempt in range(max_retries):
            try:
                response = await self.client.get(url)
                response.raise_for_status()
                return orjson.loads(response.content)
            except httpx.TimeoutException:
                logger.warning(f"Row {row_id}: Timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise
            except httpx.HTTPStatusError as e:
                logger.warning(f"Row {row_id}: HTTP {e.response.status_code} (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise
            except Exception as e:
                logger.warning(f"Row {row_id}: {type(e).__name__}: {e} (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
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
