"""MultiFlexi MCP Server package initialization."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("multiflexi-mcp-server")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

__author__ = "CyberVitexus"
__email__ = "info@vitexsoftware.cz"

from .server import app, main

__all__ = ["app", "main"]