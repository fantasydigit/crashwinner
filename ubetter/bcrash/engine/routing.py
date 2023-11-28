# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from consumers import DatabaseChangeConsumer

websocket_urlpatterns = [
    path('/ws/database/', DatabaseChangeConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
