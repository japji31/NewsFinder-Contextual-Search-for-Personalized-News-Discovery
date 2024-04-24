from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.consumers import ChatConsumer
from django.core.asgi import get_asgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_search_django.settings')

# Define HTTP and WebSocket applications
http_application = get_asgi_application()

websocket_application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/chatbot/', ChatConsumer.as_asgi()),
    ]),
})

# Main application routing
application = ProtocolTypeRouter({
    'http': http_application,
    'websocket': websocket_application,
})
