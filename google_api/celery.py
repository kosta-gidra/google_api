import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'google_api.settings')

app = Celery('google_api')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'sheets.tasks.get_google_sheet',
        'schedule': 15.0  # задача выполняется каждые 15 секунд
        # 'schedule': crontab(),  # по умолчанию, задача выполняется раз в минуту
    },
}
