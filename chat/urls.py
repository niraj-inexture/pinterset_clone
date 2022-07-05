from django.urls import path
from . import views

urlpatterns = [
    path('chat-page/', views.ChatClassView.as_view(),name='chat-page'),
    path('delete-chat/',views.DeleteChatClassView.as_view(),name='delete-chat')
]