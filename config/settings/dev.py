from .base import *

# Development-specific settings
DEBUG = True  # Enable debugging during development
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Use SQLite for local development
DATABASES['default'] = env.db('DATABASE_URL', default='sqlite:///db.sqlite3')

# Development-specific static files location
STATICFILES_DIRS = [BASE_DIR / 'static']

# Allow localhost and 127.0.0.1 for development
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
