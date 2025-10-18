"""
OpenAI client wrapper for GPT-OSS Tutorial

This module provides a convenient wrapper around the OpenAI client
with default configuration for GPT-OSS API.
"""

from typing import Optional
from openai import OpenAI
from .config import Config, get_config
from .compat import check_sdk_version


def create_client(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    config: Optional[Config] = None,
    check_version: bool = True,
) -> OpenAI:
    """
    Create an OpenAI client configured for GPT-OSS API
    
    Args:
        api_key: API key (overrides config)
        base_url: Base URL (overrides config)
        config: Custom configuration object
        check_version: Check SDK version compatibility (default: True)
        
    Returns:
        OpenAI: Configured OpenAI client
        
    Example:
        >>> from src.client import create_client
        >>> client = create_client()
        >>> response = client.responses.create(
        ...     model="gpt-oss-20b",
        ...     input="Hello!"
        ... )
    """
    # Check SDK version compatibility
    if check_version:
        version, is_compatible, warning = check_sdk_version()
        if not is_compatible and warning:
            import warnings
            warnings.warn(warning, UserWarning, stacklevel=2)
    
    if config is None:
        config = get_config()
    
    # Override config values if provided
    final_api_key = api_key or config.api_key
    final_base_url = base_url or config.base_url
    
    return OpenAI(
        api_key=final_api_key,
        base_url=final_base_url,
    )


def get_default_model() -> str:
    """
    Get the default model name from configuration
    
    Returns:
        str: Default model name
    """
    return get_config().model_name


def get_embedding_model() -> str:
    """
    Get the default embedding model name from configuration
    
    Returns:
        str: Default embedding model name
    """
    return get_config().embedding_model

