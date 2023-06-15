from django.urls import path, re_path
from .consumer import ReserveConsumer, MyCafeConsumer

websocket_urlpatterns = [
    path('ws/dynamic/', ReserveConsumer.as_asgi()),
    path('ws/dynamicMycafe/', MyCafeConsumer.as_asgi()),
]