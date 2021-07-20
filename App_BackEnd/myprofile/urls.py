from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^myprofile/$', views.myprofile.as_view(), name='myprofile'),
]