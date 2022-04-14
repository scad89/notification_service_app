from django.urls import path
from . import views


urlpatterns = [
    path('create_client/', views.NewClientCreateAPIView.as_view(),
         name='create_client'),
    path('clients/', views.GetClientListView.as_view(), name='clients'),
    path("client/<int:pk>/", views.GetClientDetailRetrieveAPIView.as_view(),
         name='detail_client'),
    path('client/<int:pk>/update_client/',
         views.UpdateClientRetrieveUpdateAPIView.as_view(), name='update_client'),
    path('client/<int:pk>/delete_client/',
         views.DeleteClientRetrieveUpdateAPIView.as_view(), name='delete_client'),

    path('create_notification/', views.NewNotificationCreateAPIView.as_view(),
         name='create_notification'),
    path('notifications/', views.GetNotificationtListView.as_view(),
         name='notifications'),
    path("notification/<int:pk>/", views.GetNotificationDetailRetrieveAPIView.as_view(),
         name='detail_notification'),
    path('notification/<int:pk>/update_notification/',
         views.UpdateNotificationRetrieveUpdateAPIView.as_view(), name='update_notification'),
    path('notification/<int:pk>/delete_notification/',
         views.DeleteNotificationRetrieveUpdateAPIView.as_view(), name='delete_notification'),
]
