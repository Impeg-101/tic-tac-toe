from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', consumers.GameConsumer.as_asgi())
]