import json
import os
import requests
import pytz
import datetime
from django.utils import timezone
from notification_service.celery import app
from celery.utils.log import get_task_logger
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .models import Notification, Client, Message
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")

logger = get_task_logger(__name__)


def complete_task(task):
    task.enabled = False
    return task.save()


def check_periodic_task(notification_name):
    return PeriodicTask.objects.get(
        name=f'Create task: {notification_name}')


def create_periodic_task(notification_name, phone, id_notification, id_client, time, data):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=time,
        period=IntervalSchedule.SECONDS,
    )
    return PeriodicTask.objects.create(
        name=f'Create task: {notification_name} for {phone}',
        task='send_notification',
        interval=schedule,
        args=json.dumps([id_notification, id_client, data]),
        start_time=timezone.now(),
    )


@app.task(bind=True, retry_backoff=5)
def send_notification(self, notification_id, client_id, data, url=URL, token=TOKEN):
    notification = Notification.objects.get(pk=notification_id)
    client = Client.objects.get(pk=client_id)
    message = Message.objects.filter(
        id_notification=notification.id).filter(id_client=client.id)
    timezone_client = pytz.timezone(client.time_zone)
    date_and_time_client = datetime.datetime.now(timezone_client)

    if notification.start_date <= date_and_time_client <= notification.end_date:
        if 22 < int(date_and_time_client.strftime('%H:%M:%S')[:2]) or int(date_and_time_client.strftime('%H:%M:%S')[:2]) < 8:
            logger.info(
                f"Wrong time to send notification '{data['id']}'. Need to try later")
            Message.objects.filter(pk=data['id']).update(status='Wrong Time')
            create_periodic_task(notification.name_notification,
                                 client.phone,
                                 notification.id,
                                 client.id,
                                 60*60,
                                 data)
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
                task_error = PeriodicTask.objects.filter(
                    name=f'Create task: {notification.name_notification}').exists()
                if task_error:
                    complete_task(task_error)
                create_periodic_task(notification.name_notification,
                                     client.phone,
                                     notification.id,
                                     client.id,
                                     20,
                                     data)
                raise exc
            else:
                logger.info(f"Notification is '{data['id']}' sent success!")
                Message.objects.filter(pk=data['id']).update(status='Success')
                task_success = PeriodicTask.objects.filter(
                    name=f'Create task: {notification.name_notification}').exists()
                if task_success:
                    complete_task(task_success)

    elif date_and_time_client < notification.start_date:
        Message.objects.filter(pk=data['id']).update(status='Waiting')
        create_periodic_task(notification.name_notification,
                             client.phone,
                             notification.id,
                             client.id,
                             60*60*24,
                             data)
