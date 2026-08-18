"""Configuration management for MultiFlexi MCP Server."""

import os
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class MultiFleXiConfig(BaseModel):
    """Configuration for MultiFlexi MCP Server."""
    
    host: str = Field(
        description=(
            "MultiFlexi API host URL. Must include the full API base path "
            "(e.g. https://your-instance.example.com/api/VitexSoftware/MultiFlexi/1.0.0) "
            "- the /VitexSoftware/MultiFlexi/1.0.0 segment is required by the "
            "server's routing, it is not optional SwaggerHub boilerplate."
        )
    )
    username: Optional[str] = Field(
        default=None,
        description="Username for basic authentication"
    )
    password: Optional[str] = Field(
        default=None,
        description="Password for basic authentication"
    )
    verify_ssl: bool = Field(
        default=True,
        description="Whether to verify SSL certificates"
    )
    timeout: int = Field(
        default=30,
        description="Request timeout in seconds"
    )
    max_retries: int = Field(
        default=3,
        description="Maximum number of API request retries"
    )
    debug: bool = Field(
        default=False,
        description="Enable debug logging"
    )
    read_only: bool = Field(
        default=True,
        description=(
            "When true (the default), all mutating tools (create/update/set/"
            "delete/assign/unassign) are rejected before any API call is made. "
            "Set MULTIFLEXI_READONLY=false to allow writes."
        )
    )

    @field_validator('host')
    @classmethod
    def validate_host(cls, v):
        """Validate host URL format."""
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Host must be a valid HTTP/HTTPS URL')
        return v.rstrip('/')

    @classmethod
    def from_env(cls) -> 'MultiFleXiConfig':
        """Create configuration from environment variables."""
        host = os.getenv("MULTIFLEXI_HOST")

        if not host:
            raise RuntimeError(
                "MULTIFLEXI_HOST is required - set it to your MultiFlexi "
                "instance's full API base path, e.g. "
                "https://your-host/api/VitexSoftware/MultiFlexi/1.0.0"
            )

        return cls(
            host=host,
            username=os.getenv("MULTIFLEXI_USERNAME"),
            password=os.getenv("MULTIFLEXI_PASSWORD"),
            verify_ssl=os.getenv("MULTIFLEXI_VERIFY_SSL", "true").lower() == "true",
            timeout=int(os.getenv("MULTIFLEXI_TIMEOUT", "30")),
            max_retries=int(os.getenv("MULTIFLEXI_MAX_RETRIES", "3")),
            debug=os.getenv("MULTIFLEXI_DEBUG", "false").lower() == "true",
            read_only=os.getenv("MULTIFLEXI_READONLY", "true").lower() == "true",
        )

    def has_auth(self) -> bool:
        """Check if authentication credentials are available."""
        return bool(self.username and self.password)