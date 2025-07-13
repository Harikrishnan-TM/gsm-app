from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gsm_backend.settings')

app = Celery('gsm_backend')

# Load config from Django settings, using CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in your apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
