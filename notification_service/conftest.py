import pytest
from main.models import Notification, Client, Message
from decimal import Decimal
from datetime import datetime
from django.utils.timezone import now


@pytest.fixture()
def create_new_notification():
    return Notification.objects.create(
        name_notification='Для школьников',
        text='Дети! Пора в школу!',
        filter='CH',
        start_date=now(),
        end_date=now(),
        unvisible_notification=False
    )


@pytest.fixture()
def create_new_client():
    return Client.objects.create(
        name='Вася',
        surname='Пупкин',
        phone='+79221110500',
        mobile_code='922',
        slug='CH',
        time_zone='Europe/Moscow',
        unvisible_client=False
    )


@pytest.fixture()
def create_new_message(create_new_notification, create_new_client):
    return Message.objects.create(
        create_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status='Success',
        id_notification=create_new_notification,
        id_client=create_new_client
    )
