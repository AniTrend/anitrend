#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def __get_base_dir() -> str:
    """
    Returns the root project directory
    :return:
    """
    current_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(current_path, '..')


def main():
    """Run administrative tasks."""
    sys.path.append(__get_base_dir())
    # TODO: Change settings to production when ready for deployment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.development')
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
