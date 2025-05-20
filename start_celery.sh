# Set environment variables
export DJANGO_ENV=${DJANGO_ENV:-development}
export DJANGO_SETTINGS_MODULE=config.settings.settings

# Start Celery worker
celery -A config.celery worker --loglevel=info