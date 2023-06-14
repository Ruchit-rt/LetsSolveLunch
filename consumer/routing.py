from django.urls import path
from .consumer import ReserveConsumer

websocket_urlpatterns = [
    path('ws/dynamic/', ReserveConsumer.as_asgi())
]