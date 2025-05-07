from .base import *

# Production-specific settings
DEBUG = False  # Disable debugging in production

# Use PostgreSQL for production
DATABASES['default'] = env.db('DATABASE_URL')

# Allow only your production domain for hosts
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['yourdomain.com'])

CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')

# Optional hardening:
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_TIME_LIMIT = 300  # 5 mins timeout


# Enable secure connections and cookies
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True  # Ensure all traffic uses HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Static and media files settings for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = '/var/www/mooshak/media'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_STORAGE_BUCKET_NAME = 'your-s3-bucket-name'
# AWS_ACCESS_KEY_ID = 'your-access-key'
# AWS_SECRET_ACCESS_KEY = 'your-secret-key'

# Set up logging for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
