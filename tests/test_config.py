"""Tests for MultiFlexi MCP Server configuration."""

import os
import pytest
from unittest.mock import patch

from multiflexi_mcp_server.config import MultiFleXiConfig


class TestMultiFleXiConfig:
    """Test MultiFleXiConfig class."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = MultiFleXiConfig()
        
        assert config.host == "https://virtserver.swaggerhub.com/VitexSoftware/MultiFlexi/1.0.0"
        assert config.username is None
        assert config.password is None
        assert config.verify_ssl is True
        assert config.timeout == 30
        assert config.max_retries == 3
        assert config.debug is False
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = MultiFleXiConfig(
            host="https://custom.example.com",
            username="testuser",
            password="testpass",
            verify_ssl=False,
            timeout=60,
            max_retries=5,
            debug=True
        )
        
        assert config.host == "https://custom.example.com"
        assert config.username == "testuser"
        assert config.password == "testpass"
        assert config.verify_ssl is False
        assert config.timeout == 60
        assert config.max_retries == 5
        assert config.debug is True
    
    def test_host_validation(self):
        """Test host URL validation."""
        # Valid URLs
        config = MultiFleXiConfig(host="https://example.com")
        assert config.host == "https://example.com"
        
        config = MultiFleXiConfig(host="http://example.com")
        assert config.host == "http://example.com"
        
        # Test trailing slash removal
        config = MultiFleXiConfig(host="https://example.com/")
        assert config.host == "https://example.com"
        
        # Invalid URL should raise validation error
        with pytest.raises(ValueError):
            MultiFleXiConfig(host="invalid-url")
    
    def test_has_auth(self):
        """Test authentication credential checking."""
        # No credentials
        config = MultiFleXiConfig()
        assert config.has_auth() is False
        
        # Only username
        config = MultiFleXiConfig(username="testuser")
        assert config.has_auth() is False
        
        # Only password
        config = MultiFleXiConfig(password="testpass")
        assert config.has_auth() is False
        
        # Both credentials
        config = MultiFleXiConfig(username="testuser", password="testpass")
        assert config.has_auth() is True
    
    @patch.dict(os.environ, {
        "MULTIFLEXI_HOST": "https://env.example.com",
        "MULTIFLEXI_USERNAME": "envuser",
        "MULTIFLEXI_PASSWORD": "envpass",
        "MULTIFLEXI_VERIFY_SSL": "false",
        "MULTIFLEXI_TIMEOUT": "45",
        "MULTIFLEXI_MAX_RETRIES": "7",
        "MULTIFLEXI_DEBUG": "true"
    })
    def test_from_env(self):
        """Test configuration from environment variables."""
        config = MultiFleXiConfig.from_env()
        
        assert config.host == "https://env.example.com"
        assert config.username == "envuser"
        assert config.password == "envpass"
        assert config.verify_ssl is False
        assert config.timeout == 45
        assert config.max_retries == 7
        assert config.debug is True
    
    @patch.dict(os.environ, {}, clear=True)
    def test_from_env_defaults(self):
        """Test configuration from environment with defaults."""
        config = MultiFleXiConfig.from_env()
        
        assert config.host == "https://virtserver.swaggerhub.com/VitexSoftware/MultiFlexi/1.0.0"
        assert config.username is None
        assert config.password is None
        assert config.verify_ssl is True
        assert config.timeout == 30
        assert config.max_retries == 3
        assert config.debug is False