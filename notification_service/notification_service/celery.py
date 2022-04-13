import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'notification_service.settings')

app = Celery('notification_service')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# app.conf.beat_schedule = {    # тут задаём расписание
#     'send-spam-every-5-minutes': {    # название раписания/задачи
#         'task': 'main.tasks.send_beat_email',    # задача, с путём в tasks и название функции
#         'shedule': crontab(minute='*/5')    # переодичность
#     }
# }
