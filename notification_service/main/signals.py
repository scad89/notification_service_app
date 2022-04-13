from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, Client, Message
from tasks import send_notification


@receiver(post_save, sender=Notification, dispatch_uid="create_message")
def create_message(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.filter(id=instance.id).first()
        clients = Client.objects.filter(unvisible_client=False).filter(
            slug=notification.slug).all()

        for client in clients:
            Message.objects.create(
                status="No Sent",
                id_notification=instance.id,
                id_client=client.id
            )
            message = Message.objects.filter(
                id_notification=instance.id, id_client=client.id).first()
            data = {
                'id': message.id,
                "phone": client.phone,
                "text": notification.text
            }
            send_notification.delay(notification.id, client.id, data)
