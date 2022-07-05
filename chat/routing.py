from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('chat/chat-page/',consumers.ChatConsumer.as_asgi()),
]