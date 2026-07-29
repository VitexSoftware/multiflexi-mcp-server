"""Regression tests for the multiflexi_client cold-start import fix.

Importing ``multiflexi_mcp_server.client`` (and by extension
``multiflexi_mcp_server.server``) must not eagerly import ``multiflexi_client``
-- it's a generated OpenAPI SDK whose ``__init__.py`` eagerly loads ~15 API
classes and every model class, adding ~1.5-2s to every process start. Since
this server is spawned fresh per connection by consumers like mcprack's
per-user HTTP proxy and must answer the MCP ``initialize`` handshake within a
bounded timeout, an eager import here causes handshake timeouts.

Each check runs in a subprocess: ``sys.modules`` is process-global, and other
test modules in this suite import ``multiflexi_client`` themselves, so an
in-process check would always see it already loaded.
"""

import os
import subprocess
import sys
from pathlib import Path

SRC = str(Path(__file__).resolve().parent.parent / "src")


def _run(code: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONPATH=SRC)
    return subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )


def test_importing_client_module_does_not_import_multiflexi_client():
    result = _run(
        "import sys\n"
        "import multiflexi_mcp_server.client\n"
        "assert 'multiflexi_client' not in sys.modules, "
        "'multiflexi_client was imported eagerly by multiflexi_mcp_server.client'\n"
    )
    assert result.returncode == 0, result.stderr


def test_importing_server_module_does_not_import_multiflexi_client():
    result = _run(
        "import sys\n"
        "import multiflexi_mcp_server.server\n"
        "assert 'multiflexi_client' not in sys.modules, "
        "'multiflexi_client was imported eagerly via multiflexi_mcp_server.server'\n"
    )
    assert result.returncode == 0, result.stderr


def test_calling_a_client_method_does_import_multiflexi_client():
    result = _run(
        "import sys\n"
        "from multiflexi_mcp_server.client import MultiFleXiClient\n"
        "from multiflexi_mcp_server.config import MultiFleXiConfig\n"
        "client = MultiFleXiClient(MultiFleXiConfig(host='https://test.example.com'))\n"
        "client.get_configuration()\n"
        "assert 'multiflexi_client' in sys.modules, "
        "'multiflexi_client should be imported once a client method actually runs'\n"
    )
    assert result.returncode == 0, result.stderr
