from django.urls import path
from . import views


urlpatterns = [
    path('create_client/', views.NewClientCreateAPIView.as_view(),
         name='create_client'),
    path('client/', views.GetClientListView.as_view(), name='client'),
    path("client/<int:pk>/", views.GetClientDetailRetrieveAPIView.as_view(),
         name='detail_client'),
    path('client/<int:pk>/update_client/',
         views.UpdateClientRetrieveUpdateAPIView.as_view(), name='update_client'),
    path('client/<int:pk>/delete_client/',
         views.DeleteClientRetrieveUpdateAPIView.as_view(), name='delete_client'),

    path('create_notification/', views.NewNotificationCreateAPIView.as_view(),
         name='create_notification'),
    path('notification/', views.GetNotificationtListView.as_view(),
         name='notification'),
    path("notification/<int:pk>/", views.GetNotificationDetailRetrieveAPIView.as_view(),
         name='detail_notification'),
    path('notification/<int:pk>/update_notification/',
         views.UpdateNotificationRetrieveUpdateAPIView.as_view(), name='update_notification'),
    path('notification/<int:pk>/delete_notification/',
         views.DeleteNotificationRetrieveUpdateAPIView.as_view(), name='delete_notification'),



    #     path("choices/", views.GetChoiceListView.as_view(), name='choices'),
    #     path("create_choice/", views.CreateChoiceApiView.as_view(), name='create_choice'),
    #     path("choice/<int:pk>/", views.GetChoiceDetailListView.as_view(),
    #          name='detail_choice'),
    #     path("choice/<int:pk>/update_choice", views.UpdateChoiceListView.as_view(),
    #          name='update_choice'),
    #     path('question/<int:pk>/answer/',
    #          views.AddAnswerApiView.as_view(), name='answer'),
    #     path('results/', views.VotingResultsApiView.as_view(), name='results'),
]
