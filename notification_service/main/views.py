import datetime
from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from .models import Notification, Client, Message
from .serializers import (
    ClientCreateSerializer,
    ClientSerializer
)


class NewClientListView(generics.CreateAPIView):
    """Создание клиента"""
    queryset = Client.objects.all()
    serializer_class = ClientCreateSerializer

    def perform_create(self, serializer):
        serializer.save(mobile_code=serializer.validated_data['phone'][2:5])


class GetClientListView(generics.ListAPIView):
    """Вывод списка клиентов"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
