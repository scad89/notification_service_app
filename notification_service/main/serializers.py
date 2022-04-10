from rest_framework import serializers
from .models import Notification, Client, Message


class ClientCreateSerializer(serializers.ModelSerializer):
    """Добавления нового клиента в справочник"""

    class Meta:
        model = Client
        fields = ['name', 'surname', 'phone', 'slug', 'time_zone']

        def save(self):
            mobile_code = self.validated_data['phone'][1:4]


class ClientSerializer(serializers.ModelSerializer):
    """Вывод всех клиентов"""
    class Meta:
        model = Client
        fields = ['pk', 'name', 'surname', 'phone']


class ClientDetailSerializer(serializers.ModelSerializer):
    """Вывод детальной информации о клиенте"""

    class Meta:
        model = Client
        exclude = ['unvisible_client']


class UpdateDetailClientSerializer(serializers.ModelSerializer):
    """Редактирование данных клиента"""
    class Meta:
        model = Client
        exclude = ['unvisible_client']


class DeleteDetailClientSerializer(serializers.ModelSerializer):
    """Удаление клиента"""
    class Meta:
        model = Client
        fields = ['unvisible_client']


class NotificationCreateSerializer(serializers.ModelSerializer):
    """Создание рассылки"""

    class Meta:
        model = Notification
        exclude = ['unvisible_notification']


class NotificationSerializer(serializers.ModelSerializer):
    """Вывод всех рассылок"""
    class Meta:
        model = Notification
        exclude = ['filter', 'start_date',
                   'end_date', 'unvisible_notification']


class NotificationDetailSerializer(serializers.ModelSerializer):
    """Вывод детальной информации о рассылке"""
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Notification
        fields = ['name_notification', 'text',
                  'filter', 'start_date', 'end_date', 'url']


class UpdateDetailNotificationSerializer(serializers.ModelSerializer):
    """Редактирование атрибутов рассылки"""
    class Meta:
        model = Notification
        exclude = ['unvisible_notification']


class DeleteDetailNotificationSerializer(serializers.ModelSerializer):
    """Удаление клиента"""
    class Meta:
        model = Notification
        fields = ['unvisible_notification']
