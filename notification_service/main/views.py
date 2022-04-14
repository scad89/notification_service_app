from rest_framework import generics
from .models import Notification, Client, Message
from django.db.models import Prefetch
from .serializers import (
    ClientCreateSerializer,
    ClientSerializer,
    ClientDetailSerializer,
    UpdateDetailClientSerializer,
    DeleteDetailClientSerializer,
    NotificationCreateSerializer,
    NotificationSerializer,
    NotificationDetailSerializer,
    UpdateDetailNotificationSerializer,
    DeleteDetailNotificationSerializer,
    AllMessageSerializer,
    MessageDetailSerializer,
)


class NewClientCreateAPIView(generics.CreateAPIView):
    """Создание клиента"""
    queryset = Client.objects.all()
    serializer_class = ClientCreateSerializer

    def perform_create(self, serializer):
        serializer.save(mobile_code=serializer.validated_data['phone'][2:5])


class GetClientListView(generics.ListAPIView):
    """Вывод списка клиентов"""
    queryset = Client.objects.filter(unvisible_client=False)
    serializer_class = ClientSerializer


class GetClientDetailRetrieveAPIView(generics.RetrieveAPIView):
    """Вывод детальной информации о клиенте"""
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer
    lookup_field = 'pk'


class UpdateClientRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Редактирование данных клиента"""
    queryset = Client.objects.all()
    serializer_class = UpdateDetailClientSerializer


class DeleteClientRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Удаление клиента"""
    queryset = Client.objects.all()
    serializer_class = DeleteDetailClientSerializer


class NewNotificationCreateAPIView(generics.CreateAPIView):
    """Создание рассылки"""
    queryset = Notification.objects.all()
    serializer_class = NotificationCreateSerializer


class GetNotificationtListView(generics.ListAPIView):
    """Вывод списка рассылок"""
    queryset = queryset = Notification.objects.filter(unvisible_notification=False).prefetch_related(
        Prefetch('to_notification', queryset=Message.objects.order_by('status')))
    serializer_class = NotificationSerializer


class GetNotificationDetailRetrieveAPIView(generics.RetrieveAPIView):
    """Вывод детальной информации о рассылке"""
    queryset = Notification.objects.prefetch_related(
        Prefetch('to_notification', queryset=Message.objects.order_by('status')))
    serializer_class = NotificationDetailSerializer
    lookup_field = 'pk'


class UpdateNotificationRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Редактирование атрибутов рассылки"""
    queryset = Notification.objects.all()
    serializer_class = UpdateDetailNotificationSerializer


class DeleteNotificationRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Удаление рассылки"""
    queryset = Notification.objects.all()
    serializer_class = DeleteDetailNotificationSerializer


class GetMessagestListView(generics.ListAPIView):
    """Вывод всех сообщений статуса"""
    queryset = Message.objects.all().order_by('-create_date')
    serializer_class = AllMessageSerializer


class GetMessageDetailRetrieveAPIView(generics.RetrieveAPIView):
    """Вывод детальной информации о сообщении"""
    queryset = Message.objects.all()
    serializer_class = MessageDetailSerializer
    lookup_field = 'pk'
