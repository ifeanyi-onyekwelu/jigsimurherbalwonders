"""
Passenger WSGI file for cPanel deployment
This file is required by cPanel's Python application hosting
"""

import os
import sys

# Add your project directory to the sys.path
# Update the path to match your cPanel Python application name and version
INTERP = os.path.expanduser("~/virtualenv/jigsimurherbalwonders.com/3.11/bin/python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Add the project path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jigsimurherbal.settings")

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
