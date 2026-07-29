"""Ensure tests exercise this repo's source tree, not an installed package.

Without this, ``pytest`` resolves ``multiflexi_mcp_server`` via normal import
machinery, which can pick up an already-installed (e.g. Debian-packaged)
version under ``dist-packages`` instead of ``src/`` -- silently testing stale
code.
"""

import sys
from pathlib import Path

SRC = str(Path(__file__).resolve().parent.parent / "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
