from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qtechcode.settings')
app = Celery('qtechcode')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.now = timezone.now

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


