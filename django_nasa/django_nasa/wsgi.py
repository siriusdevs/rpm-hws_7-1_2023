"""WSGI config for django_nasa project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_nasa.settings')

application = get_wsgi_application()
