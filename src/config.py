"""
Configuration management for GPT-OSS Tutorial

This module handles environment variables and configuration settings
for all examples in the tutorial.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for GPT-OSS API"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        embedding_model: Optional[str] = None,
    ):
        """
        Initialize configuration
        
        Args:
            api_key: API key for authentication (defaults to env variable)
            base_url: Base URL for API (defaults to env variable)
            model_name: Default model name (defaults to env variable)
            embedding_model: Default embedding model (defaults to env variable)
        """
        self.api_key = api_key or os.getenv("API_KEY")
        self.base_url = base_url or os.getenv("BASE_URL", "https://mkp-api.fptcloud.com")
        self.model_name = model_name or os.getenv("MODEL_NAME", "gpt-oss-20b")
        self.embedding_model = embedding_model or os.getenv(
            "EMBEDDING_MODEL", "multilingual-e5-large"
        )
        
        # Optional configurations
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        
        # Validate required fields
        if not self.api_key:
            raise ValueError(
                "API_KEY is required. Set it in .env file or pass it to Config()"
            )
    
    def __repr__(self) -> str:
        return (
            f"Config("
            f"base_url='{self.base_url}', "
            f"model_name='{self.model_name}', "
            f"api_key={'***' if self.api_key else None})"
        )


# Global default config instance
_default_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get or create the default configuration instance
    
    Returns:
        Config: The default configuration
    """
    global _default_config
    if _default_config is None:
        _default_config = Config()
    return _default_config


def set_config(config: Config) -> None:
    """
    Set the default configuration instance
    
    Args:
        config: The configuration to set as default
    """
    global _default_config
    _default_config = config

