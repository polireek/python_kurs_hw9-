import os
from celery import Celery
from celery.schedules import crontab

from datetime import timedelta
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMS.settings')

app = Celery('LMS')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes
app.config_from_object('django.conf:settings', namespace='CELERY')
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, exchanger.tasks.get_exchange_rates.s(), name='add every 10')
    print("good")

app.conf.beat_schedule = {
    'clear-log': {
        'task': 'academy.tasks.clear_log',
        'schedule': crontab(minute=0, hour=0),
    },
    'get_exchange_rates': {
        'task': 'exchanger.tasks.get_exchange_rates',
        'schedule': crontab(minute='*/30'),
    }
}

app.conf.timezone = 'UTC'
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
