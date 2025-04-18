import os
from django.core.wsgi import get_wsgi_application

# This should point to your settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.settings')  # Correct path here

application = get_wsgi_application()
