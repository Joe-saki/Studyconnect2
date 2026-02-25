"""Top-level WSGI wrapper to load the inner Django project's WSGI application.

This file makes it easy for process managers (like gunicorn on Render)
to import `wsgi:application` regardless of nested project layout.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Try adding the most likely parent directories to sys.path so
# `import studyconnect.wsgi` will succeed.
candidates = [ROOT, ROOT / 'studyconnect']
for c in candidates:
    if (c / 'studyconnect' / 'wsgi.py').exists():
        sys.path.insert(0, str(c))
        break

# Import the real WSGI application
try:
    from importlib import import_module
    mod = import_module('studyconnect.wsgi')
    application = mod.application
except Exception:
    # If import fails, raise a clear error so Render logs show it.
    raise
