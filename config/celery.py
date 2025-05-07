# config/celery.py
import os
from celery import Celery
from django.conf import settings # Import Django settings

# Set the default Django settings module for the 'celery' program.
# This MUST come before creating the Celery app instance.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
redis_url = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
app = Celery('mooshak',broker=redis_url, backend=redis_url) # 'mooshak' or your project name

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Optional: Example debug task
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')