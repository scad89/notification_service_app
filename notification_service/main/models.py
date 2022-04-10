from concurrent.futures.thread import _worker
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Notification(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)
    filter = models.CharField(max_length=3)
    end_date = models.DateTimeField()


class Client(models.Model):
    class Slug(models.TextChoices):
        CHILD = 'CH'
        SCHOOLBOY = 'SC'
        STUDENT = 'ST'
        WORKER = 'WR'
        RETIREE = 'RT'

    class RussiaTimeZone(models.TextChoices):
        KALININGRA = 'MSK-1'
        MOSCOW = 'MSK '
        SAMARA = 'MSK+1'
        YEKATERINBURG = 'MSK+2'
        OMSK = 'MSK+3'
        KRASNOYARSK = 'MSK+4'
        IRKUTSK = 'MSK+5'
        YAKUTSK = 'MSK+6'
        VLADIVOSTOK = 'MSK+7'
        SREDNEKOLYMSK = 'MSK+8'
        KAMCHATKA = 'MSK+9'

    phone = PhoneNumberField(unique=True, region='RU')
    mobile_code = models.CharField(max_length=3)
    slug = models.CharField(
        choices=Slug.choices, max_length=2)
    time_zone = models.CharField(
        choices=RussiaTimeZone.choices, max_length=5)


class Message(models.Model):
    class Status(models.TextChoices):
        Success = 'Success'
        Waiting = 'Waiting'
        Fail = 'Fail'
        Error = 'Error'

    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=Status.choices, max_length=10)
    id_notification = models.ForeignKey(
        Notification, on_delete=models.DO_NOTHING, related_name='to_notifiacation')
    id_client = models.ForeignKey(
        Client, on_delete=models.DO_NOTHING, related_name='to_client')
