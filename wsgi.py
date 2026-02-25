"""Top-level WSGI wrapper to load the inner Django project's WSGI application.

This file makes it easy for process managers (like gunicorn on Render)
to import `wsgi:application` regardless of nested project layout.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Ensure the inner Django package (studyconnect/studyconnect) is on sys.path
inner_pkg_path = ROOT / 'studyconnect'
if inner_pkg_path.exists():
    sys.path.insert(0, str(inner_pkg_path))
# Also keep project root for manage.py parity
sys.path.insert(0, str(ROOT))

# Import the real WSGI application
try:
    from importlib import import_module
    mod = import_module('studyconnect.wsgi')
    application = mod.application
except Exception:
    # If import fails, raise a clear error so Render logs show it.
    raise
