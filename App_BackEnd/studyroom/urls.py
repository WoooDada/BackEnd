from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^studyroom/$', views.studyroom.as_view(), name='studyroom'),
]