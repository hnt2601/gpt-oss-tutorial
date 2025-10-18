"""
Unit tests for GPT-OSS Tutorial examples

Run with: pytest tests/
"""

import pytest
import os
from unittest.mock import Mock, patch

from src.config import Config, get_config
from src.client import create_client


class TestConfig:
    """Test configuration management"""
    
    def test_config_from_env(self):
        """Test config loads from environment"""
        with patch.dict(os.environ, {
            'API_KEY': 'test_key',
            'BASE_URL': 'https://test.com',
            'MODEL_NAME': 'test-model'
        }):
            config = Config()
            assert config.api_key == 'test_key'
            assert config.base_url == 'https://test.com'
            assert config.model_name == 'test-model'
    
    def test_config_requires_api_key(self):
        """Test config validates API key"""
        with patch.dict(os.environ, {'API_KEY': ''}, clear=True):
            with pytest.raises(ValueError, match="API_KEY is required"):
                Config()
    
    def test_config_defaults(self):
        """Test config uses defaults"""
        with patch.dict(os.environ, {'API_KEY': 'test_key'}):
            config = Config()
            assert config.base_url == 'https://mkp-api.fptcloud.com'
            assert config.model_name == 'gpt-oss-20b'


class TestClient:
    """Test client creation"""
    
    def test_create_client(self):
        """Test client can be created"""
        with patch.dict(os.environ, {'API_KEY': 'test_key'}):
            client = create_client()
            assert client is not None
            assert hasattr(client, 'responses')
    
    def test_create_client_custom_params(self):
        """Test client with custom parameters"""
        client = create_client(
            api_key='custom_key',
            base_url='https://custom.url'
        )
        assert client is not None


class TestExamples:
    """Test example modules can be imported"""
    
    def test_import_basic_examples(self):
        """Test basic examples import"""
        from examples.01_basic import instructions
        assert hasattr(instructions, 'main')
    
    def test_import_structured_output_examples(self):
        """Test structured output examples import"""
        from examples.02_structured_output import json_schema
        from examples.02_structured_output import pydantic_parse
        assert hasattr(json_schema, 'main')
        assert hasattr(pydantic_parse, 'main')
    
    def test_import_tools_examples(self):
        """Test tools examples import"""
        from examples.03_tools import function_calling
        from examples.03_tools import web_search
        from examples.03_tools import mcp
        assert hasattr(function_calling, 'main')
        assert hasattr(web_search, 'main')
        assert hasattr(mcp, 'main')
    
    def test_import_multimodal_examples(self):
        """Test multimodal examples import"""
        from examples.04_multimodal import image_url
        from examples.04_multimodal import image_base64
        assert hasattr(image_url, 'main')
        assert hasattr(image_base64, 'main')
    
    def test_import_stateful_examples(self):
        """Test stateful examples import"""
        from examples.05_stateful import store_retrieve
        assert hasattr(store_retrieve, 'main')
    
    def test_import_advanced_examples(self):
        """Test advanced examples import"""
        from examples.06_advanced import rag_pinecone
        assert hasattr(rag_pinecone, 'main')
        assert hasattr(rag_pinecone, 'PineconeRAG')


class TestIntegration:
    """Integration tests (require API key)"""
    
    @pytest.mark.skipif(
        not os.getenv('API_KEY'),
        reason="API_KEY not set"
    )
    def test_simple_api_call(self):
        """Test simple API call works"""
        client = create_client()
        
        response = client.responses.create(
            model='gpt-oss-20b',
            input='Say "test successful"',
        )
        
        assert response is not None
        assert hasattr(response, 'output')
        assert len(response.output) > 0
    
    @pytest.mark.skipif(
        not os.getenv('API_KEY'),
        reason="API_KEY not set"
    )
    def test_embedding_generation(self):
        """Test embedding generation works"""
        client = create_client()
        
        response = client.embeddings.create(
            input=['test text'],
            model='multilingual-e5-large'
        )
        
        assert response is not None
        assert len(response.data) == 1
        assert len(response.data[0].embedding) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

