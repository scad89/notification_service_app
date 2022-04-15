from django.urls import reverse
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import pytz


class Slug(models.TextChoices):
    CHILD = 'CH'
    SCHOOLBOY = 'SC'
    STUDENT = 'ST'
    WORKER = 'WR'
    RETIREE = 'RT'


class Notification(models.Model):
    name_notification = models.CharField(max_length=25, default='title')
    text = models.CharField(max_length=1000)
    filter = models.CharField(choices=Slug.choices, max_length=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    unvisible_notification = models.BooleanField(
        verbose_name='Do you want to delete a notification?', default=False)

    def get_absolute_url(self):
        return reverse('detail_notification', kwargs={'pk': self.id})

    def __str__(self):
        return self.name_notification

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    name = models.CharField(max_length=15, default='name')
    surname = models.CharField(max_length=15, default='surname')
    phone = PhoneNumberField(unique=True, region='RU')
    mobile_code = models.CharField(max_length=3)
    slug = models.CharField(
        choices=Slug.choices, max_length=2)
    time_zone = models.CharField(
        choices=TIMEZONES, max_length=32)
    unvisible_client = models.BooleanField(
        verbose_name='Do you want to delete a client?', default=False)

    def __str__(self):
        return f'{self.surname} {self.name}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Message(models.Model):
    class Status(models.TextChoices):
        Success = 'Success'
        Waiting = 'Waiting'
        No_Sent = 'No Sent'
        Error = 'Error'
        Wrong_Time = 'Wrong Time'

    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=Status.choices, max_length=10)
    id_notification = models.ForeignKey(
        Notification, on_delete=models.DO_NOTHING, related_name='to_notification')
    id_client = models.ForeignKey(
        Client, on_delete=models.DO_NOTHING, related_name='to_client')

    def __str__(self):
        return f'{self.id_client}, {self.status} {self.create_date}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
