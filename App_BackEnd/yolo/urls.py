from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^yolo/testimage/$', views.testimage.as_view(), name='testimage'),
]
