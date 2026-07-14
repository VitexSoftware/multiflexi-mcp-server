"""MultiFlexi MCP Server main implementation."""

import json
import logging
import os
from typing import Any, Dict, List, Optional, Union

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
)

from .config import MultiFleXiConfig
from .client import MultiFleXiClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP Server instance
app = Server("multiflexi-mcp-server")

# Global configuration and client
config = MultiFleXiConfig.from_env()
client = MultiFleXiClient(config)


@app.list_resources()
async def list_resources() -> List[Resource]:
    """List available MultiFlexi resources."""
    return [
        Resource(
            uri="multiflexi://apps",
            name="Applications",
            description="List of MultiFlexi applications",
            mimeType="application/json",
        ),
        Resource(
            uri="multiflexi://jobs",
            name="Jobs",
            description="List of MultiFlexi jobs",
            mimeType="application/json",
        ),
        Resource(
            uri="multiflexi://companies",
            name="Companies",
            description="List of MultiFlexi companies",
            mimeType="application/json",
        ),
        Resource(
            uri="multiflexi://users",
            name="Users",
            description="List of MultiFlexi users",
            mimeType="application/json",
        ),
        Resource(
            uri="multiflexi://runtemplates",
            name="Run Templates",
            description="List of MultiFlexi run templates",
            mimeType="application/json",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific MultiFlexi resource."""
    # The mcp SDK invokes this with a pydantic AnyUrl instance despite the `str`
    # annotation. AnyUrl("multiflexi://apps") == "multiflexi://apps" is False even
    # though str(...) matches, so every branch below silently fell through to
    # "Resource not found" for real MCP clients (unit tests missed this because
    # they call read_resource() directly with a plain str, bypassing the SDK).
    uri = str(uri)
    try:
        if uri == "multiflexi://apps":
            result = client.get_apps()
            return json.dumps(result, indent=2)
        
        elif uri == "multiflexi://jobs":
            result = client.get_jobs()
            return json.dumps(result, indent=2)
        
        elif uri == "multiflexi://companies":
            result = client.get_companies()
            return json.dumps(result, indent=2)
        
        elif uri == "multiflexi://users":
            result = client.get_users()
            return json.dumps(result, indent=2)
        
        elif uri == "multiflexi://runtemplates":
            result = client.get_runtemplates()
            return json.dumps(result, indent=2)
        
        else:
            return f"Resource not found: {uri}"
    
    except Exception as e:
        logger.error(f"Unexpected error reading resource {uri}: {e}")
        return f"Unexpected error: {e}"


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available MultiFlexi tools."""
    return [
        Tool(
            name="get_app",
            description="Get a specific MultiFlexi application by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {
                        "type": "integer",
                        "description": "ID of the application to retrieve"
                    },
                    "format": {
                        "type": "string",
                        "description": "Response format (json, html, xml)",
                        "default": "json"
                    }
                },
                "required": ["app_id"]
            }
        ),
        Tool(
            name="get_job",
            description="Get a specific MultiFlexi job by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "integer",
                        "description": "ID of the job to retrieve"
                    },
                    "format": {
                        "type": "string",
                        "description": "Response format (json, html, xml)",
                        "default": "json"
                    }
                },
                "required": ["job_id"]
            }
        ),
        Tool(
            name="create_job",
            description="Create a new MultiFlexi job",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_id": {
                        "type": "integer",
                        "description": "ID of the application to run"
                    },
                    "company_id": {
                        "type": "integer",
                        "description": "ID of the company"
                    },
                    "job_data": {
                        "type": "object",
                        "description": "Job configuration data",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Job name"
                            },
                            "description": {
                                "type": "string",
                                "description": "Job description"
                            },
                            "schedule": {
                                "type": "string",
                                "description": "Cron schedule expression"
                            }
                        }
                    }
                },
                "required": ["app_id", "company_id"]
            }
        ),
        Tool(
            name="get_job_status",
            description="Get the status of a MultiFlexi job",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "integer",
                        "description": "ID of the job to check"
                    }
                },
                "required": ["job_id"]
            }
        ),
        Tool(
            name="get_company",
            description="Get a specific MultiFlexi company by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "company_id": {
                        "type": "integer",
                        "description": "ID of the company to retrieve"
                    },
                    "format": {
                        "type": "string",
                        "description": "Response format (json, html, xml)",
                        "default": "json"
                    }
                },
                "required": ["company_id"]
            }
        ),
        Tool(
            name="get_user",
            description="Get a specific MultiFlexi user by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "ID of the user to retrieve"
                    },
                    "format": {
                        "type": "string",
                        "description": "Response format (json, html, xml)",
                        "default": "json"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="get_runtemplate",
            description="Get a specific MultiFlexi run template by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_id": {
                        "type": "integer",
                        "description": "ID of the run template to retrieve"
                    },
                    "format": {
                        "type": "string",
                        "description": "Response format (json, html, xml)",
                        "default": "json"
                    }
                },
                "required": ["template_id"]
            }
        ),
        Tool(
            name="update_runtemplate",
            description="Update a MultiFlexi run template",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_id": {
                        "type": "integer",
                        "description": "ID of the run template to update"
                    },
                    "template_data": {
                        "type": "object",
                        "description": "Updated template data",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Template name"
                            },
                            "description": {
                                "type": "string",
                                "description": "Template description"
                            },
                            "command": {
                                "type": "string",
                                "description": "Command to execute"
                            },
                            "environment": {
                                "type": "object",
                                "description": "Environment variables"
                            }
                        }
                    }
                },
                "required": ["template_id", "template_data"]
            }
        ),
        Tool(
            name="request_data_export",
            description="Request GDPR data export for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "export_type": {
                        "type": "string",
                        "description": "Type of data export to request",
                        "enum": ["personal_data", "activity_logs", "audit_trail"]
                    },
                    "format": {
                        "type": "string",
                        "description": "Export format",
                        "enum": ["json", "csv", "xml"],
                        "default": "json"
                    }
                },
                "required": ["export_type"]
            }
        ),
        Tool(
            name="get_export_status",
            description="Get the status of a data export request",
            inputSchema={
                "type": "object",
                "properties": {
                    "export_id": {
                        "type": "string",
                        "description": "ID of the export request"
                    }
                },
                "required": ["export_id"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls for MultiFlexi operations."""
    try:
        if name == "get_app":
            app_id = arguments["app_id"]
            format_type = arguments.get("format", "json")
            result = client.get_app_by_id(app_id, format_type)
            
        elif name == "get_job":
            job_id = arguments["job_id"]
            format_type = arguments.get("format", "json")
            result = client.get_job_by_id(job_id, format_type)
            
        elif name == "create_job":
            app_id = arguments["app_id"]
            company_id = arguments["company_id"]
            job_data = arguments.get("job_data", {})
            
            # Merge required fields with job data
            full_job_data = {
                "app_id": app_id,
                "company_id": company_id,
                **job_data
            }
            result = client.create_job(full_job_data)
            
        elif name == "get_job_status":
            job_id = arguments["job_id"]
            result = client.get_job_status(job_id)
            
        elif name == "get_company":
            company_id = arguments["company_id"]
            format_type = arguments.get("format", "json")
            result = client.get_company_by_id(company_id, format_type)
            
        elif name == "get_user":
            user_id = arguments["user_id"]
            format_type = arguments.get("format", "json")
            result = client.get_user_by_id(user_id, format_type)
            
        elif name == "get_runtemplate":
            template_id = arguments["template_id"]
            format_type = arguments.get("format", "json")
            result = client.get_runtemplate_by_id(template_id, format_type)
            
        elif name == "update_runtemplate":
            template_id = arguments["template_id"]
            template_data = arguments["template_data"]
            result = client.update_runtemplate(template_id, template_data)
            
        elif name == "request_data_export":
            export_type = arguments["export_type"]
            format_type = arguments.get("format", "json")
            result = client.request_data_export(export_type, format_type)
            
        elif name == "get_export_status":
            export_id = arguments["export_id"]
            result = client.get_export_status(export_id)
            
        else:
            result = {"error": True, "message": f"Unknown tool: {name}"}
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    except Exception as e:
        logger.error(f"Unexpected error in tool {name}: {e}")
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": True,
                "message": f"Unexpected error: {e}",
                "tool": name
            }, indent=2)
        )]


async def run_server() -> None:
    """Run the MultiFlexi MCP Server over stdio."""
    logger.info(f"Starting MultiFlexi MCP Server")
    logger.info(f"Host: {config.host}")
    logger.info(f"Authentication: {'enabled' if config.has_auth() else 'disabled'}")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="multiflexi-mcp-server",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                ),
            ),
        )


def main() -> None:
    """Synchronous entry point used by the ``multiflexi-mcp-server`` console script.

    The generated console-script wrapper calls ``main()`` directly (it does not
    await it), so this must not itself be a coroutine function -- previously
    ``main`` was ``async def``, which meant running ``multiflexi-mcp-server``
    just printed an unawaited-coroutine RuntimeWarning and exited immediately
    without starting the server.
    """
    import asyncio

    asyncio.run(run_server())


if __name__ == "__main__":
    main()