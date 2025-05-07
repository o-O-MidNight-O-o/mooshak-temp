from .base import *

# Development-specific settings
DEBUG = True  # Enable debugging during development
BASE_DIR = Path(__file__).resolve().parent.parent
# Use SQLite for local development
DATABASES['default'] = env.db('DATABASE_URL', default='sqlite:///db.sqlite3')

# Development-specific static files location
STATICFILES_DIRS = [BASE_DIR.parent / 'static']

# Allow localhost and 127.0.0.1 for development
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_TASK_ALWAYS_EAGER = False  # Set to True only for unit testing

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'azinmalekiazin@gmail.com'
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
