import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings.prod')

# create a celery app instance
celery = Celery('storefront')

# specify where celery will look for configuration settings
celery.config_from_object('django.conf:settings', namespace='CELERY') # the namespace 'CELERY' means all celery-related settings in Django settings.py should start with 'CELERY_'

# auto-discover tasks from all registered Django app configs
celery.autodiscover_tasks()