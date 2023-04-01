from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, signals
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config',
    broker='redis://redis:6379',
    backend='redis://redis:6379')
    
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))