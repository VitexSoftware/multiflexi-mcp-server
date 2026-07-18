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
        Resource(
            uri="multiflexi://credentials",
            name="Credentials",
            description="List of MultiFlexi credentials",
            mimeType="application/json",
        ),
        Resource(
            uri="multiflexi://credential_types",
            name="Credential Types",
            description="List of MultiFlexi credential types",
            mimeType="application/json",
        ),
        Resource(
            uri="multiflexi://topics",
            name="Topics",
            description="List of MultiFlexi topics (capability contracts)",
            mimeType="application/json",
        ),
        Resource(
            uri="multiflexi://eventsources",
            name="Event Sources",
            description="List of MultiFlexi event sources",
            mimeType="application/json",
        ),
        Resource(
            uri="multiflexi://eventrules",
            name="Event Rules",
            description="List of MultiFlexi event rules",
            mimeType="application/json",
        ),
        Resource(
            uri="multiflexi://tasks",
            name="Tasks",
            description="List of MultiFlexi tasks (per-window fulfilment obligations)",
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

        elif uri == "multiflexi://credentials":
            result = client.list_credentials()
            return json.dumps(result, indent=2)

        elif uri == "multiflexi://credential_types":
            result = client.list_credential_types()
            return json.dumps(result, indent=2)

        elif uri == "multiflexi://topics":
            result = client.list_topics()
            return json.dumps(result, indent=2)

        elif uri == "multiflexi://eventsources":
            result = client.list_event_sources()
            return json.dumps(result, indent=2)

        elif uri == "multiflexi://eventrules":
            result = client.list_event_rules()
            return json.dumps(result, indent=2)

        elif uri == "multiflexi://tasks":
            result = client.list_tasks()
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
            description="Schedule a job from a RunTemplate (mirrors 'run-template:schedule')",
            inputSchema={
                "type": "object",
                "properties": {
                    "runtemplate_id": {
                        "type": "integer",
                        "description": "ID of the RunTemplate to schedule"
                    },
                    "scheduled": {
                        "type": "string",
                        "description": "'now' or a 'Y-m-d H:i:s' timestamp",
                        "default": "now"
                    },
                    "executor": {
                        "type": "string",
                        "description": "Overrides the RunTemplate executor (e.g. Native, Docker)"
                    },
                    "env": {
                        "type": "object",
                        "description": "Environment variable overrides (KEY=>VALUE) injected into the job",
                        "additionalProperties": {"type": "string"}
                    }
                },
                "required": ["runtemplate_id"]
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
        ),
        # Company
        Tool(
            name="list_companies",
            description="List all MultiFlexi companies",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum number of results"},
                    "offset": {"type": "integer", "description": "Number of records to skip"},
                    "order": {"type": "string", "description": "Field to order by ('-' prefix for descending)"}
                }
            }
        ),
        Tool(
            name="list_company_users",
            description="List users assigned to a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "company_id": {"type": "integer", "description": "ID of the company"},
                    "limit": {"type": "integer", "description": "Maximum number of results"}
                },
                "required": ["company_id"]
            }
        ),
        Tool(
            name="assign_user_to_company",
            description="Assign a user to a company with an access role",
            inputSchema={
                "type": "object",
                "properties": {
                    "company_id": {"type": "integer", "description": "ID of the company"},
                    "user_id": {"type": "integer", "description": "ID of the user to assign"},
                    "role": {
                        "type": "string",
                        "description": "Access role in the company",
                        "default": "viewer"
                    }
                },
                "required": ["company_id", "user_id"]
            }
        ),
        Tool(
            name="unassign_user_from_company",
            description="Remove a user's assignment from a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "company_id": {"type": "integer", "description": "ID of the company"},
                    "user_id": {"type": "integer", "description": "ID of the user to remove"}
                },
                "required": ["company_id", "user_id"]
            }
        ),
        # User / roles
        Tool(
            name="list_users",
            description="List all MultiFlexi users",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum number of results"}
                }
            }
        ),
        Tool(
            name="get_user_roles",
            description="Get the RBAC roles assigned to a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "ID of the user"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="set_user_roles",
            description="Assign RBAC roles to a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "ID of the user"},
                    "roles": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of RBAC role names to assign"
                    },
                    "replace": {
                        "type": "boolean",
                        "description": "When true (default), existing roles not in the list are removed",
                        "default": True
                    }
                },
                "required": ["user_id", "roles"]
            }
        ),
        # Credential / CredentialType
        Tool(
            name="list_credentials",
            description="List all credentials visible to the authenticated user",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum number of results"}
                }
            }
        ),
        Tool(
            name="get_credential",
            description="Get a credential by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "credential_id": {"type": "integer", "description": "ID of the credential"}
                },
                "required": ["credential_id"]
            }
        ),
        Tool(
            name="list_credential_types",
            description="List all credential types",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum number of results"}
                }
            }
        ),
        Tool(
            name="get_credential_type",
            description="Get a credential type by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "credential_type_id": {"type": "integer", "description": "ID of the credential type"}
                },
                "required": ["credential_type_id"]
            }
        ),
        # Topic
        Tool(
            name="list_topics",
            description="List all topics (capability contracts required by apps / provided by credentials)",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum number of results"}
                }
            }
        ),
        Tool(
            name="get_topic",
            description="Get a topic by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic_id": {"type": "integer", "description": "ID of the topic"}
                },
                "required": ["topic_id"]
            }
        ),
        # EventSource
        Tool(
            name="list_event_sources",
            description="List all event sources (webhook adapters feeding EventRules)",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum number of results"}
                }
            }
        ),
        Tool(
            name="get_event_source",
            description="Get an event source by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_source_id": {"type": "integer", "description": "ID of the event source"}
                },
                "required": ["event_source_id"]
            }
        ),
        Tool(
            name="set_event_source",
            description="Create or update an event source (omit event_source_id to create)",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_source_id": {"type": "integer", "description": "ID to update; omit to create"},
                    "name": {"type": "string", "description": "Human-readable name"},
                    "adapter_type": {"type": "string", "description": "Type of webhook adapter"},
                    "db_connection": {"type": "string", "description": "Database driver"},
                    "db_host": {"type": "string", "description": "Database host"},
                    "db_port": {"type": "string", "description": "Database port"},
                    "db_database": {"type": "string", "description": "Database name"},
                    "db_username": {"type": "string", "description": "Database username"},
                    "db_password": {"type": "string", "description": "Database password"},
                    "poll_interval": {"type": "integer", "description": "Poll interval in seconds"},
                    "enabled": {"type": "boolean", "description": "Whether this source is active"}
                }
            }
        ),
        Tool(
            name="delete_event_source",
            description="Delete an event source by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_source_id": {"type": "integer", "description": "ID of the event source"}
                },
                "required": ["event_source_id"]
            }
        ),
        Tool(
            name="test_event_source_connection",
            description="Live-test connectivity/credentials for an event source",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_source_id": {"type": "integer", "description": "ID of the event source to test"}
                },
                "required": ["event_source_id"]
            }
        ),
        # EventRule
        Tool(
            name="list_event_rules",
            description="List all event rules (bindings from EventSource changes to RunTemplate triggers)",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum number of results"}
                }
            }
        ),
        Tool(
            name="get_event_rule",
            description="Get an event rule by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_rule_id": {"type": "integer", "description": "ID of the event rule"}
                },
                "required": ["event_rule_id"]
            }
        ),
        Tool(
            name="set_event_rule",
            description="Create or update an event rule (omit event_rule_id to create)",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_rule_id": {"type": "integer", "description": "ID to update; omit to create"},
                    "event_source_id": {"type": "integer", "description": "References the EventSource"},
                    "evidence": {"type": "string", "description": "Evidence type pattern to match (omit for any)"},
                    "operation": {"type": "string", "description": "Operation to match", "default": "any"},
                    "runtemplate_id": {"type": "integer", "description": "RunTemplate to trigger when rule matches"},
                    "priority": {"type": "integer", "description": "Higher priority rules are evaluated first"},
                    "enabled": {"type": "boolean", "description": "Whether this rule is active"},
                    "env_mapping": {"type": "string", "description": "JSON mapping of change fields to environment variables"}
                },
                "required": ["runtemplate_id"]
            }
        ),
        Tool(
            name="delete_event_rule",
            description="Delete an event rule by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_rule_id": {"type": "integer", "description": "ID of the event rule"}
                },
                "required": ["event_rule_id"]
            }
        ),
        # Task
        Tool(
            name="list_tasks",
            description="List tasks (per-window fulfilment obligations spawned from RunTemplates)",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "Filter by task state",
                        "enum": ["open", "running", "fulfilled", "fulfilled_late", "failed", "missed"]
                    },
                    "runtemplate_id": {"type": "integer", "description": "Filter by RunTemplate"},
                    "limit": {"type": "integer", "description": "Maximum number of results"}
                }
            }
        ),
        Tool(
            name="get_task",
            description="Get a task by ID, including its job attempt history",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "ID of the task"}
                },
                "required": ["task_id"]
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
            result = client.create_job(
                runtemplate_id=arguments["runtemplate_id"],
                scheduled=arguments.get("scheduled", "now"),
                executor=arguments.get("executor"),
                env=arguments.get("env"),
            )
            
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

        elif name == "list_companies":
            result = client.list_companies(
                limit=arguments.get("limit"),
                offset=arguments.get("offset"),
                order=arguments.get("order"),
            )

        elif name == "list_company_users":
            result = client.list_company_users(arguments["company_id"], limit=arguments.get("limit"))

        elif name == "assign_user_to_company":
            result = client.assign_user_to_company(
                arguments["company_id"], arguments["user_id"], arguments.get("role", "viewer")
            )

        elif name == "unassign_user_from_company":
            result = client.unassign_user_from_company(arguments["company_id"], arguments["user_id"])

        elif name == "list_users":
            result = client.list_users(limit=arguments.get("limit"))

        elif name == "get_user_roles":
            result = client.get_user_roles(arguments["user_id"])

        elif name == "set_user_roles":
            result = client.set_user_roles(
                arguments["user_id"], arguments["roles"], arguments.get("replace", True)
            )

        elif name == "list_credentials":
            result = client.list_credentials(limit=arguments.get("limit"))

        elif name == "get_credential":
            result = client.get_credential(arguments["credential_id"])

        elif name == "list_credential_types":
            result = client.list_credential_types(limit=arguments.get("limit"))

        elif name == "get_credential_type":
            result = client.get_credential_type(arguments["credential_type_id"])

        elif name == "list_topics":
            result = client.list_topics(limit=arguments.get("limit"))

        elif name == "get_topic":
            result = client.get_topic(arguments["topic_id"])

        elif name == "list_event_sources":
            result = client.list_event_sources(limit=arguments.get("limit"))

        elif name == "get_event_source":
            result = client.get_event_source(arguments["event_source_id"])

        elif name == "set_event_source":
            event_source_data = {k: v for k, v in arguments.items() if k != "event_source_id"}
            result = client.set_event_source(event_source_data, event_source_id=arguments.get("event_source_id"))

        elif name == "delete_event_source":
            result = client.delete_event_source(arguments["event_source_id"])

        elif name == "test_event_source_connection":
            result = client.test_event_source_connection(arguments["event_source_id"])

        elif name == "list_event_rules":
            result = client.list_event_rules(limit=arguments.get("limit"))

        elif name == "get_event_rule":
            result = client.get_event_rule(arguments["event_rule_id"])

        elif name == "set_event_rule":
            event_rule_data = {k: v for k, v in arguments.items() if k != "event_rule_id"}
            result = client.set_event_rule(event_rule_data, event_rule_id=arguments.get("event_rule_id"))

        elif name == "delete_event_rule":
            result = client.delete_event_rule(arguments["event_rule_id"])

        elif name == "list_tasks":
            result = client.list_tasks(
                state=arguments.get("state"),
                runtemplate_id=arguments.get("runtemplate_id"),
                limit=arguments.get("limit"),
            )

        elif name == "get_task":
            result = client.get_task(arguments["task_id"])

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