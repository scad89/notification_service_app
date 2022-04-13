import json

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from models import Notification, Client, Message


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('notification_id', nargs=1, type=int)

    def handle(self, *args, **options):
        notification = Notification.objects.filter(
            unvisible_notification=False).filter(id=options['notification_id'][0]).first()
        clients = Client.objects.filter(unvisible_client=False).filter(
            slug=notification.slug).all()

        for client in clients:
            Message.objects.create(
                status="No Sent",
                id_notification=notification.id,
                id_client=client.id
            )
            message = Message.objects.filter(
                id_notification=notification.id, id_client=client.id).first()
            data = {
                'id': message.id,
                "phone": client.phone,
                "text": notification.text
            }
            id_notification = notification.id
            id_client = client.id

            PeriodicTask.objects.create(
                name=f'Create task: {notification.name}',
                task='send_notification',
                interval=IntervalSchedule.objects.get(
                    every=60, period='seconds'),
                args=json.dumps([options['notification_id'][0]], data,
                                id_notification, id_client),
                start_time=timezone.now(),
            )
