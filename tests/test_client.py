"""Tests for MultiFlexi MCP Server client."""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock

import multiflexi_client
from multiflexi_client.rest import ApiException

from multiflexi_mcp_server.config import MultiFleXiConfig
from multiflexi_mcp_server.client import MultiFleXiClient


class TestMultiFleXiClient:
    """Test MultiFleXiClient class."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return MultiFleXiConfig(
            host="https://test.example.com",
            username="testuser",
            password="testpass"
        )
    
    @pytest.fixture
    def client(self, config):
        """Create test client."""
        return MultiFleXiClient(config)
    
    def test_initialization(self, client, config):
        """Test client initialization."""
        assert client.config == config
    
    def test_get_configuration(self, client):
        """Test API configuration creation."""
        configuration = client.get_configuration()
        
        assert configuration.host == "https://test.example.com"
        assert configuration.username == "testuser"
        assert configuration.password == "testpass"
        assert configuration.verify_ssl is True
    
    def test_get_configuration_no_auth(self):
        """Test API configuration without authentication."""
        config = MultiFleXiConfig(host="https://test.example.com")
        client = MultiFleXiClient(config)
        configuration = client.get_configuration()
        
        assert configuration.host == "https://test.example.com"
        assert not hasattr(configuration, 'username') or configuration.username is None
        assert not hasattr(configuration, 'password') or configuration.password is None
    
    def test_format_response_dict(self, client):
        """Test response formatting with to_dict method."""
        mock_response = Mock()
        mock_response.to_dict.return_value = {"id": 1, "name": "test"}
        
        result = client.format_response(mock_response)
        assert result == {"id": 1, "name": "test"}
    
    def test_format_response_dict_attribute(self, client):
        """Test response formatting with __dict__ attribute."""
        mock_response = Mock()
        del mock_response.to_dict  # Remove to_dict method
        mock_response.__dict__ = {"id": 1, "name": "test"}
        
        result = client.format_response(mock_response)
        assert result == {"id": 1, "name": "test"}
    
    def test_format_response_string(self, client):
        """Test response formatting with string fallback."""
        mock_response = "test response"
        
        result = client.format_response(mock_response)
        assert result == {"response": "test response"}
    
    def test_handle_api_error(self, client):
        """Test API error handling."""
        error = ApiException(status=404, reason="Not Found")
        error.body = '{"message": "Resource not found"}'
        
        result = client.handle_api_error(error, "test_operation")
        
        assert result["error"] is True
        assert result["operation"] == "test_operation"
        assert result["status"] == 404
        assert result["reason"] == "Not Found"
        assert result["details"] == {"message": "Resource not found"}
    
    def test_handle_api_error_no_body(self, client):
        """Test API error handling without body."""
        error = ApiException(status=500, reason="Server Error")
        
        result = client.handle_api_error(error, "test_operation")
        
        assert result["error"] is True
        assert result["operation"] == "test_operation"
        assert result["status"] == 500
        assert result["reason"] == "Server Error"
        assert result["body"] is None
    
    @patch('multiflexi_client.ApiClient')
    def test_get_apps_success(self, mock_api_client_class, client):
        """Test successful get_apps call."""
        # Setup mocks
        mock_api_client = MagicMock()
        mock_api_client_class.return_value.__enter__.return_value = mock_api_client

        mock_app_api = Mock()
        mock_response = Mock()
        mock_response.to_dict.return_value = {"apps": [{"id": 1, "name": "test"}]}
        mock_app_api.list_apps.return_value = mock_response

        with patch('multiflexi_client.AppApi', return_value=mock_app_api):
            result = client.get_apps()

        assert result == {"apps": [{"id": 1, "name": "test"}]}
        mock_app_api.list_apps.assert_called_once_with("json", limit=None)
    
    @patch('multiflexi_client.ApiClient')
    def test_get_apps_api_error(self, mock_api_client_class, client):
        """Test get_apps with API error."""
        # Setup mocks
        mock_api_client = MagicMock()
        mock_api_client_class.return_value.__enter__.return_value = mock_api_client
        
        mock_app_api = Mock()
        mock_app_api.list_apps.side_effect = ApiException(status=500, reason="Server Error")

        with patch('multiflexi_client.AppApi', return_value=mock_app_api):
            result = client.get_apps()
        
        assert result["error"] is True
        assert result["operation"] == "get_apps"
        assert result["status"] == 500
    
    @patch('multiflexi_client.ApiClient')
    def test_get_app_by_id_success(self, mock_api_client_class, client):
        """Test successful get_app_by_id call."""
        # Setup mocks
        mock_api_client = MagicMock()
        mock_api_client_class.return_value.__enter__.return_value = mock_api_client
        
        mock_app_api = Mock()
        mock_response = Mock()
        mock_response.to_dict.return_value = {"id": 1, "name": "test"}
        mock_app_api.get_app_by_id.return_value = mock_response
        
        with patch('multiflexi_client.AppApi', return_value=mock_app_api):
            result = client.get_app_by_id(1)
        
        assert result == {"id": 1, "name": "test"}
        mock_app_api.get_app_by_id.assert_called_once_with(1, "json", limit=None)
    
    def test_create_job_not_supported(self, client):
        """create_job is a documented no-op: multiflexi-client 1.1.0's
        create/update job endpoint has no request-body parameter, so job_data
        can never reach the server. It must fail loudly instead of silently
        creating an empty job."""
        result = client.create_job({"app_id": 1, "company_id": 1, "name": "test"})

        assert result["error"] is True
        assert result["reason"] == "not_supported_by_client_sdk"

    @patch('multiflexi_client.ApiClient')
    def test_get_job_status_derives_from_job(self, mock_api_client_class, client):
        """get_job_status has no dedicated per-job endpoint on the real API;
        it derives status from the Job's begin/end/exitcode fields."""
        mock_api_client = MagicMock()
        mock_api_client_class.return_value.__enter__.return_value = mock_api_client

        mock_job_api = Mock()
        mock_response = Mock()
        mock_response.to_dict.return_value = {
            "id": 1,
            "begin": "2026-01-01T00:00:00Z",
            "end": "2026-01-01T00:01:00Z",
            "exitcode": 0,
        }
        mock_job_api.getjob_by_id.return_value = mock_response

        with patch('multiflexi_client.JobApi', return_value=mock_job_api):
            result = client.get_job_status(1)

        assert result == {
            "job_id": 1,
            "status": "success",
            "begin": "2026-01-01T00:00:00Z",
            "end": "2026-01-01T00:01:00Z",
            "exitcode": 0,
        }
        mock_job_api.getjob_by_id.assert_called_once_with(1, "json")