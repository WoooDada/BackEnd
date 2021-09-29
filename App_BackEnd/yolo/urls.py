from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [

    url(r'^yolo/getmessage/$', views.getmessage.as_view(), name='getmessage'),

]