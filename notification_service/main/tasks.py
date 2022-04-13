import json
import os
import requests
import pytz
import datetime
from django.utils import timezone
from notification_service.celery import app
from celery.utils.log import get_task_logger
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from models import Notification, Client, Message
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")

logger = get_task_logger(__name__)


@app.task(bind=True, retry_backoff=True)
def send_notification(self, data, id_notification, id_client, url=URL, token=TOKEN):
    notification = Notification.objects.get(pk=id_notification)
    client = Client.objects.get(pk=id_client)
    message = Message.objects.filter(
        id_notification=notification.id).filter(id_client=client.id)
    timezone_client = pytz.timezone(client.time_zone)
    date_and_time_client = datetime.datetime.now(timezone_client)

    if notification.start_date <= date_and_time_client <= notification.end_date and message.status in ['No Sent', 'Waiting', 'Wrong Time']:
        if 3 < int(date_and_time_client.strftime('%H:%M:%S')[:2]) < 16:
            logger.info(
                f"Wrong time to send notification '{data['id']}'. Need to try later")
            Message.objects.filter(pk=data['id']).update(status='Wrong Time')
        else:
            header = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'}
            try:
                requests.post(
                    url=url + str(data['id']), headers=header, json=data)
            except requests.exceptions.RequestException as exc:
                logger.error(
                    f"Notification '{data['id']}' is error. Server has problem.")
                Message.objects.filter(pk=data['id']).update(status='Error')
                raise exc
            else:
                logger.info(f"Notification is '{data['id']}' sent success!")
                Message.objects.filter(pk=data['id']).update(status='Success')
                task_success = PeriodicTask.objects.get(
                    name=f'Create task: {notification.name}')
                task_success.enabled = False
                task_success.save()
    elif date_and_time_client < notification.start_date and message.status != 'No Sent':
        Message.objects.filter(pk=data['id']).update(status='Waiting')

# задать условие, чтобы снимать задачу
