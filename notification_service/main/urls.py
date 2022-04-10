from django.urls import path
from . import views


urlpatterns = [
    path('create_client/', views.NewClientListView.as_view(), name='create_client'),
    path('client/', views.GetClientListView.as_view(), name='client'),
    #     path("question/<int:pk>/", views.GetQuestionDetailListView.as_view(),
    #          name='detail_question'),
    #     path('question/<int:pk>/update_question/', views.UpdateQuestionListView.as_view(),
    #          name='update_question'),

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
