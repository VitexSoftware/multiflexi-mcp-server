"""Tests for MultiFlexi MCP Server configuration."""

import os
import pytest
from unittest.mock import patch

from multiflexi_mcp_server.config import MultiFleXiConfig


class TestMultiFleXiConfig:
    """Test MultiFleXiConfig class."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = MultiFleXiConfig(host="https://example.com")

        assert config.username is None
        assert config.password is None
        assert config.verify_ssl is True
        assert config.timeout == 30
        assert config.max_retries == 3
        assert config.debug is False
        assert config.read_only is True

    def test_host_is_required(self):
        """host has no default - MultiFleXiConfig() without it must fail."""
        with pytest.raises(ValueError):
            MultiFleXiConfig()
    
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
        config = MultiFleXiConfig(host="https://example.com", username=None, password=None)
        assert config.has_auth() is False

        # Only username
        config = MultiFleXiConfig(host="https://example.com", username="testuser", password=None)
        assert config.has_auth() is False

        # Only password
        config = MultiFleXiConfig(host="https://example.com", username=None, password="testpass")
        assert config.has_auth() is False

        # No auth by default (no username/password default)
        config = MultiFleXiConfig(host="https://example.com")
        assert config.has_auth() is False

        # Both credentials
        config = MultiFleXiConfig(host="https://example.com", username="testuser", password="testpass")
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
    def test_from_env_requires_host(self):
        """from_env() must raise a clear error when MULTIFLEXI_HOST is unset."""
        with pytest.raises(RuntimeError, match="MULTIFLEXI_HOST"):
            MultiFleXiConfig.from_env()

    @patch.dict(os.environ, {"MULTIFLEXI_HOST": "https://env.example.com"}, clear=True)
    def test_from_env_defaults(self):
        """Test configuration from environment with defaults besides host."""
        config = MultiFleXiConfig.from_env()

        assert config.host == "https://env.example.com"
        assert config.username is None
        assert config.password is None
        assert config.verify_ssl is True
        assert config.timeout == 30
        assert config.max_retries == 3
        assert config.debug is False
        assert config.read_only is True