from django.urls import re_path
from .consumers import sendMate

websocket_urlpatterns=[
    re_path(r'study/study_mate/$', sendMate.as_asgi()),
    ]
