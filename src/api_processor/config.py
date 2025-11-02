"""Configuration management"""
import tomllib
from pathlib import Path
from typing import Any


class Config:
    """Application configuration"""
    
    def __init__(self, config_path: str = "config.toml"):
        self.config_path = Path(config_path)
        self._config: dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from TOML file"""
        with open(self.config_path, "rb") as f:
            self._config = tomllib.load(f)
    
    @property
    def processing(self) -> dict[str, Any]:
        return self._config.get("processing", {})
    
    @property
    def api(self) -> dict[str, Any]:
        return self._config.get("api", {})
    
    @property
    def http(self) -> dict[str, Any]:
        return self._config.get("http", {})
    
    @property
    def database(self) -> dict[str, Any]:
        return self._config.get("database", {})
    
    @property
    def concurrency(self) -> int:
        return self.processing.get("concurrency", 10)
    
    @property
    def max_retries(self) -> int:
        return self.processing.get("max_retries", 3)
    
    @property
    def max_failures(self) -> int:
        return self.processing.get("max_failures", 20)
    
    @property
    def db_path(self) -> str:
        return self.database.get("path", "db.duckdb")
