"""Configuration management for MultiFlexi MCP Server."""

import os
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class MultiFleXiConfig(BaseModel):
    """Configuration for MultiFlexi MCP Server."""
    
    host: str = Field(
        default="https://virtserver.swaggerhub.com/VitexSoftware/MultiFlexi/1.0.0",
        description="MultiFlexi API host URL"
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
        return cls(
            host=os.getenv("MULTIFLEXI_HOST", cls.model_fields['host'].default),
            username=os.getenv("MULTIFLEXI_USERNAME"),
            password=os.getenv("MULTIFLEXI_PASSWORD"),
            verify_ssl=os.getenv("MULTIFLEXI_VERIFY_SSL", "true").lower() == "true",
            timeout=int(os.getenv("MULTIFLEXI_TIMEOUT", "30")),
            max_retries=int(os.getenv("MULTIFLEXI_MAX_RETRIES", "3")),
            debug=os.getenv("MULTIFLEXI_DEBUG", "false").lower() == "true",
        )

    def has_auth(self) -> bool:
        """Check if authentication credentials are available."""
        return bool(self.username and self.password)