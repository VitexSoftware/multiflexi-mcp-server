"""Ensure tests exercise this repo's source tree, not an installed package.

Without this, ``pytest`` resolves ``multiflexi_mcp_server`` via normal import
machinery, which can pick up an already-installed (e.g. Debian-packaged)
version under ``dist-packages`` instead of ``src/`` -- silently testing stale
code.
"""

import os
import sys
from pathlib import Path

SRC = str(Path(__file__).resolve().parent.parent / "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

# server.py builds a module-level MultiFleXiConfig.from_env() at import time,
# and MULTIFLEXI_HOST has no default (by design - see config.py). Give test
# collection a placeholder so importing the module doesn't require a real
# MultiFlexi instance to be configured.
os.environ.setdefault(
    "MULTIFLEXI_HOST", "https://test.invalid/api/VitexSoftware/MultiFlexi/1.0.0"
)
