import os
import environ
from pathlib import Path

# Set base directory
BASE_DIR = Path(__file__).resolve().parent.parent

django_env = os.getenv('DJANGO_ENV', 'development')
env_file = BASE_DIR.parent / f".env.{django_env}"

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)
environ.Env.read_env(env_file)

# Base settings
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db" / "db.sqlite3"}')
}

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
# Image Processing Settings
PROFILE_PICTURE_WIDTH = 150
PROFILE_PICTURE_HEIGHT = 150
BANNER_IMAGE_WIDTH = 1200
BANNER_IMAGE_HEIGHT = 400
IMAGE_RESIZE_QUALITY = 85  # For JPEG, 0-100

# Policy for original images after successful resize
DELETE_ORIGINAL_AFTER_RESIZE = False # Set to True if you want to delete originals

# Celery settings 
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_DEFAULT_RETRY_DELAY = 60 # seconds (example)

# Static and media files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [BASE_DIR.parent / 'static']
STATIC_ROOT = BASE_DIR.parent / 'staticfiles'
MEDIA_ROOT = BASE_DIR.parent / 'media'
ROOT_URLCONF = 'config.urls'

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'ads',
    'profiles',
    'payments',
    'notifications',
    'reports',
    'collaborations',
]

# Middleware settings
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Logging settings (for development)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
