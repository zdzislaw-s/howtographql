"""
ASGI config for subscriptions project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from graphql_ws.django.consumers import GraphQLSubscriptionConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackernews.settings')

websocket_urlpatterns = [
    path("subscriptions", GraphQLSubscriptionConsumer.as_asgi())
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})
