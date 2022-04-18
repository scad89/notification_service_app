from inspect import ArgSpec
from django.http import response
import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertRedirects, assertFormError, assertRaisesMessage
from main.models import Notification, Client, Message


@pytest.mark.django_db
def test_published_post_create_notification(create_new_notification, client):
    url = reverse('create_notification')
    data = {
        'name_notification': create_new_notification.name_notification,
        'text': create_new_notification.text,
        'filter': create_new_notification.filter,
        'start_date': create_new_notification.start_date,
        'end_date': create_new_notification.end_date,
        'unvisible_notification': create_new_notification.unvisible_notification
    }
    response = client.post(url, data)
    assert str(
        create_new_notification.name_notification) == response['name_notification'].data
