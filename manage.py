#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    # Ensure inner project package is importable when manage.py is run from repository root
    repo_root = Path(__file__).resolve().parent
    inner_project = repo_root / 'studyconnect'
    if str(inner_project) not in sys.path:
        sys.path.insert(0, str(inner_project))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyconnect.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
