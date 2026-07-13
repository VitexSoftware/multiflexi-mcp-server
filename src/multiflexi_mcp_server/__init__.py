"""MultiFlexi MCP Server package initialization."""

__version__ = "0.1.0"
__author__ = "CyberVitexus"
__email__ = "info@vitexsoftware.cz"

from .server import app, main

__all__ = ["app", "main"]