import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-daily-alerts-at-8am': {
        'task': 'alerts.tasks.send_daily_job_alerts',
        'schedule': crontab(hour=8, minute=0),
    },
}
