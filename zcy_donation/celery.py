from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zcy_donation.settings')

app = Celery('zcy_donation')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(bind=True, default_retry_delay=5 * 60)
def retry_task(self, text):
    try:
        return text
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


app.conf.beat_schedule = {
    'run-get_statistic_for_jar': {
        'task': 'apps.jars.tasks.get_statistic_for_jar',
        'schedule': crontab(hour=17, minute=57),
    }
}
