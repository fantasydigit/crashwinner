"""
ASGI config for ubet project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubet.settings')

# application = get_asgi_application()

# asgi.py


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, re_path
import django_eventstream

from bcrash.routing import websocket_urlpatterns  # Update with your actual app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubet.settings')

# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket": AuthMiddlewareStack(
#             URLRouter(
#                 websocket_urlpatterns
#             )
#         ),
#     }
# )

application = ProtocolTypeRouter({
    'http': URLRouter([
        path('events/', AuthMiddlewareStack(
            URLRouter(django_eventstream.routing.urlpatterns)
        ), { 'channels': ['test'] }),
        re_path(r'', get_asgi_application()),
    ]),
})

# from bcrash.routing import websocket_urlpatterns  # Update with your actual app name


# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from channels.auth import AuthMiddlewareStack
# import bcrash.routing
# from bcrash.consumers import ScrapingConsumer
# from django.urls import path
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubet.settings')

# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket": #AllowedHostsOriginValidator (
#             AuthMiddlewareStack(
#                 URLRouter(
#                     # websocket_urlpatterns
#                     # bcrash.routing.websocket_urlpatterns
#                     [
#                         path("ws/scraping/", ScrapingConsumer.as_asgi()),
#                     ]
#                 )
#             ),
#         #),
#     }
# )
