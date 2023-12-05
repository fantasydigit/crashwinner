# yourapp/routing.py

from django.urls import re_path

from .consumers import ScrapingConsumer

websocket_urlpatterns = [
    re_path(r'ws/scraping/$', ScrapingConsumer.as_asgi()),
]
