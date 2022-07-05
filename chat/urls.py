from django.urls import path
from . import views

urlpatterns = [
    path('chat-page/', views.ChatClassView.as_view(),name='chat-page'),
]