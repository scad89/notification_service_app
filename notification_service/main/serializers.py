from rest_framework import serializers
from .models import Notification, Client, Message


class ClientCreateSerializer(serializers.ModelSerializer):
    """Добавления нового клиента в справочник"""

    class Meta:
        model = Client
        fields = ['phone', 'slug', 'time_zone']

        def save(self):
            mobile_code = self.validated_data['phone'][1:4]


class ClientSerializer(serializers.ModelSerializer):
    """Вывод всех клиентов"""
    class Meta:
        model = Client
        fields = ['pk', 'phone', 'mobile_code', 'slug', 'time_zone']
