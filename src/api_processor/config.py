"""Configuration management"""
import sys
import tomllib
from pathlib import Path
from typing import Any


class ConfigError(Exception):
    """Configuration related errors"""
    pass


class Config:
    """Application configuration"""
    
    def __init__(self, config_path: str = "config.toml"):
        self.config_path = Path(config_path)
        self._config: dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from TOML file"""
        try:
            if not self.config_path.exists():
                raise ConfigError(f"Configuration file not found: {self.config_path}")
            
            with open(self.config_path, "rb") as f:
                self._config = tomllib.load(f)
                
            # Validate required sections
            required_sections = ["processing", "api", "http", "database", "valuation", "sql_queries"]
            missing_sections = [section for section in required_sections if section not in self._config]
            if missing_sections:
                raise ConfigError(f"Missing required configuration sections: {missing_sections}")
                
        except tomllib.TOMLDecodeError as e:
            raise ConfigError(f"Invalid TOML syntax in {self.config_path}: {e}")
        except (OSError, IOError) as e:
            raise ConfigError(f"Failed to read configuration file {self.config_path}: {e}")
    
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
    def sql_queries(self) -> dict[str, str]:
        return self._config.get("sql_queries", {})
    
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
