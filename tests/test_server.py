"""Tests for MultiFlexi MCP Server main module."""

import json
import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock

from mcp.types import TextContent

import inspect

from multiflexi_mcp_server.server import app, list_resources, read_resource, list_tools, call_tool, main


def test_main_is_sync_entry_point():
    """The `multiflexi-mcp-server` console script calls main() without awaiting
    it, so main must be a plain sync function (previously it was `async def`,
    which meant the console script printed an unawaited-coroutine
    RuntimeWarning and exited immediately without starting the server)."""
    assert not inspect.iscoroutinefunction(main)


class TestMCPServer:
    """Test MCP Server functionality."""
    
    @pytest.mark.asyncio
    async def test_list_resources(self):
        """Test resource listing."""
        resources = await list_resources()
        
        assert len(resources) == 5
        resource_uris = [str(r.uri) for r in resources]

        assert "multiflexi://apps" in resource_uris
        assert "multiflexi://jobs" in resource_uris
        assert "multiflexi://companies" in resource_uris
        assert "multiflexi://users" in resource_uris
        assert "multiflexi://runtemplates" in resource_uris
    
    @pytest.mark.asyncio
    @patch('multiflexi_mcp_server.server.client')
    async def test_read_resource_apps(self, mock_client):
        """Test reading apps resource."""
        mock_client.get_apps.return_value = {"apps": [{"id": 1, "name": "test"}]}
        
        result = await read_resource("multiflexi://apps")
        parsed_result = json.loads(result)
        
        assert parsed_result == {"apps": [{"id": 1, "name": "test"}]}
        mock_client.get_apps.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('multiflexi_mcp_server.server.client')
    async def test_read_resource_jobs(self, mock_client):
        """Test reading jobs resource."""
        mock_client.get_jobs.return_value = {"jobs": [{"id": 1, "name": "test"}]}
        
        result = await read_resource("multiflexi://jobs")
        parsed_result = json.loads(result)
        
        assert parsed_result == {"jobs": [{"id": 1, "name": "test"}]}
        mock_client.get_jobs.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_read_resource_unknown(self):
        """Test reading unknown resource."""
        result = await read_resource("multiflexi://unknown")
        assert result == "Resource not found: multiflexi://unknown"
    
    @pytest.mark.asyncio
    @patch('multiflexi_mcp_server.server.client')
    async def test_read_resource_exception(self, mock_client):
        """Test reading resource with exception."""
        mock_client.get_apps.side_effect = Exception("Test error")
        
        result = await read_resource("multiflexi://apps")
        assert "Unexpected error: Test error" in result
    
    @pytest.mark.asyncio
    async def test_list_tools(self):
        """Test tool listing."""
        tools = await list_tools()
        
        assert len(tools) == 10
        tool_names = [t.name for t in tools]
        
        expected_tools = [
            "get_app", "get_job", "create_job", "get_job_status",
            "get_company", "get_user", "get_runtemplate", "update_runtemplate",
            "request_data_export", "get_export_status"
        ]
        
        for tool_name in expected_tools:
            assert tool_name in tool_names
    
    @pytest.mark.asyncio
    @patch('multiflexi_mcp_server.server.client')
    async def test_call_tool_get_app(self, mock_client):
        """Test get_app tool call."""
        mock_client.get_app_by_id.return_value = {"id": 1, "name": "test"}
        
        result = await call_tool("get_app", {"app_id": 1, "format": "json"})
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        parsed_result = json.loads(result[0].text)
        assert parsed_result == {"id": 1, "name": "test"}
        
        mock_client.get_app_by_id.assert_called_once_with(1, "json")
    
    @pytest.mark.asyncio
    @patch('multiflexi_mcp_server.server.client')
    async def test_call_tool_create_job(self, mock_client):
        """Test create_job tool call."""
        mock_client.create_job.return_value = {"id": 1, "app_id": 1, "company_id": 1}
        
        result = await call_tool("create_job", {
            "app_id": 1,
            "company_id": 1,
            "job_data": {"name": "test"}
        })
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        parsed_result = json.loads(result[0].text)
        assert parsed_result == {"id": 1, "app_id": 1, "company_id": 1}
        
        mock_client.create_job.assert_called_once_with({
            "app_id": 1,
            "company_id": 1,
            "name": "test"
        })
    
    @pytest.mark.asyncio
    async def test_call_tool_unknown(self):
        """Test unknown tool call."""
        result = await call_tool("unknown_tool", {})
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        parsed_result = json.loads(result[0].text)
        assert parsed_result["error"] is True
        assert "Unknown tool: unknown_tool" in parsed_result["message"]
    
    @pytest.mark.asyncio
    @patch('multiflexi_mcp_server.server.client')
    async def test_call_tool_exception(self, mock_client):
        """Test tool call with exception."""
        mock_client.get_app_by_id.side_effect = Exception("Test error")
        
        result = await call_tool("get_app", {"app_id": 1})
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        parsed_result = json.loads(result[0].text)
        assert parsed_result["error"] is True
        assert "Test error" in parsed_result["message"]
        assert parsed_result["tool"] == "get_app"
    
    @pytest.mark.asyncio
    @patch('multiflexi_mcp_server.server.client')
    async def test_call_tool_get_job_status(self, mock_client):
        """Test get_job_status tool call."""
        mock_client.get_job_status.return_value = {"job_id": 1, "status": "running"}
        
        result = await call_tool("get_job_status", {"job_id": 1})
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        parsed_result = json.loads(result[0].text)
        assert parsed_result == {"job_id": 1, "status": "running"}
        
        mock_client.get_job_status.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    @patch('multiflexi_mcp_server.server.client')
    async def test_call_tool_request_data_export(self, mock_client):
        """Test request_data_export tool call."""
        mock_client.request_data_export.return_value = {"export_id": "123", "status": "pending"}
        
        result = await call_tool("request_data_export", {
            "export_type": "personal_data",
            "format": "json"
        })
        
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        parsed_result = json.loads(result[0].text)
        assert parsed_result == {"export_id": "123", "status": "pending"}
        
        mock_client.request_data_export.assert_called_once_with("personal_data", "json")