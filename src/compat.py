"""
Compatibility layer for GPT-OSS API

This module provides workarounds for compatibility issues between
the OpenAI SDK and GPT-OSS API response formats.
"""

import functools
from typing import Any, Callable
import openai
from openai import OpenAI


def handle_response_validation_error(func: Callable) -> Callable:
    """
    Decorator to handle response validation errors
    
    GPT-OSS API may return responses in a slightly different format
    than standard OpenAI API, causing validation errors in newer SDK versions.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except openai.BadRequestError as e:
            error_msg = str(e)
            
            # Check if it's a logprobs validation error
            if "logprobs" in error_msg and "iterable" in error_msg:
                raise RuntimeError(
                    "Response validation error: The GPT-OSS API response format "
                    "is incompatible with this OpenAI SDK version.\n\n"
                    "Solutions:\n"
                    "1. Downgrade OpenAI SDK: pip install openai==1.12.0\n"
                    "2. Or contact API provider about response format compatibility\n\n"
                    f"Original error: {error_msg}"
                ) from e
            
            # Re-raise other errors
            raise
    
    return wrapper


def create_compatible_client(*args, **kwargs) -> OpenAI:
    """
    Create OpenAI client with compatibility patches
    
    This wraps the standard OpenAI client and adds error handling
    for known compatibility issues.
    """
    client = OpenAI(*args, **kwargs)
    
    # Wrap the responses.create method
    original_create = client.responses.create
    client.responses.create = handle_response_validation_error(original_create)
    
    return client


def check_sdk_version():
    """
    Check OpenAI SDK version and warn if incompatible
    
    Returns:
        tuple: (version_string, is_compatible, warning_message)
    """
    import openai
    from packaging import version as pkg_version
    
    version = openai.__version__
    
    try:
        v = pkg_version.parse(version)
        # Need >= 1.50.0 for responses API, < 2.0.0 for compatibility
        min_version = pkg_version.parse("1.50.0")
        max_version = pkg_version.parse("2.0.0")
        
        is_compatible = min_version <= v < max_version
        
        if not is_compatible:
            if v < min_version:
                warning = (
                    f"⚠️  OpenAI SDK version {version} is too old.\n"
                    f"   The responses API requires version >= 1.50.0\n"
                    f"   To fix: uv pip install 'openai>=1.50.0,<2.0.0'"
                )
            else:
                warning = (
                    f"⚠️  OpenAI SDK version {version} may have breaking changes.\n"
                    f"   Recommended: 1.50.0 <= version < 2.0.0\n"
                    f"   To fix: uv pip install 'openai>=1.50.0,<2.0.0'"
                )
        else:
            warning = None
            
    except Exception as e:
        # Fallback if version parsing fails
        is_compatible = True
        warning = None
    
    return version, is_compatible, warning

