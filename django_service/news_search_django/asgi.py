from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.consumers import ChatConsumer
from django.core.asgi import get_asgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_search_django.settings')
application = get_asgi_application()

application = ProtocolTypeRouter({
    'websocket': URLRouter([
            path('ws/chatbot/', ChatConsumer),
        ])
})