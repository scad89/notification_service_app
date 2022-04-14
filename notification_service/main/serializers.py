from attr import field
from rest_framework import serializers
from .models import Notification, Client, Message


class MessageSerializer(serializers.ModelSerializer):
    """Статусы сообщений для вывода в статистике"""
    class Meta:
        model = Message
        fields = ['status']


class AllMessageSerializer(serializers.ModelSerializer):
    """Вывод всех сообщений"""
    id_notification = serializers.SlugRelatedField(
        slug_field='name_notification', read_only=True)
    id_client = serializers.SlugRelatedField(
        slug_field='surname', read_only=True)

    class Meta:
        model = Message
        fields = ['pk', 'status', 'id_notification', 'id_client']


class MessageDetailSerializer(serializers.ModelSerializer):
    """Вывод детальной информации о клиенте"""
    id_notification = serializers.SlugRelatedField(
        slug_field='name_notification', read_only=True)
    id_client = serializers.SlugRelatedField(
        slug_field='surname', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


class MessageDeatailSerializer(serializers.ModelSerializer):
    """Статусы сообщений для вывода в статистике"""
    id_client = serializers.SlugRelatedField(
        slug_field='surname', read_only=True)

    class Meta:
        model = Message
        fields = ['pk', 'create_date', 'status',
                  'id_client']


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
        fields = ['id', 'name', 'surname', 'phone']


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
    to_notification = MessageSerializer(many=True)
    count_status = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['name_notification', 'to_notification', 'count_status']

    def get_count_status(self, obj):
        return obj.to_notification.count()


class NotificationDetailSerializer(serializers.ModelSerializer):
    """Вывод детальной информации о рассылке"""
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    to_notification = MessageDeatailSerializer(many=True)

    class Meta:
        model = Notification
        fields = ['name_notification', 'text',
                  'filter', 'start_date', 'end_date', 'url', 'to_notification']


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


class MessageCreateSerializer(serializers.ModelSerializer):    # для теста
    """Добавления нового сообщения"""

    class Meta:
        model = Message
        fields = ['status', 'id_notification', 'id_client']


class MessageSerializer(serializers.ModelSerializer):    # в общей
    """Статусы сообщений для вывода в статистике"""
    class Meta:
        model = Message
        fields = ['pk', 'status']


class ResultsSerializer(serializers.ModelSerializer):
    """Вывод результатов завершённых опросов"""
    to_notification = MessageSerializer(many=True)
    count_status = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['name_notification', 'to_notification', 'count_status']

    def get_count_status(self, obj):
        return obj.to_notification.count()
