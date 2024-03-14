#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
#import json


#def load_environment_variables_from_json(json_files):
#    """Load environment variables from JSON files."""
#    try:
#        for json_file in json_files:
#            with open(json_file, 'r') as file:
#                variables = json.load(file)
#                for key, value in variables['data'].items():
#                    os.environ.setdefault(key, str(value))
#    except Exception as e:
#        print(f"Error loading environment variables from JSON: {e}")

# Lista de nombres de archivos JSON que contienen las variables de entorno
#json_files = ['login_secrets.json', 'tools_secrets.json', 'jwt_secrets.json']

# Load environment variables from JSON
#load_environment_variables_from_json(json_files)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcendence.settings')
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
