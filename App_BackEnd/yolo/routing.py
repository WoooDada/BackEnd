from django.urls import re_path
from .consumers import sendConsumer

websocket_urlpatterns=[
    re_path(r'yolo/getmessage/$', sendConsumer.as_asgi()),
]
