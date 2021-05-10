from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url(r'^home/badge_profile/$', views.badge_profile.as_view(), name='badge_profile'),
    url(r'^home/concent_graph/$', views.concent_graph.as_view(), name='concent_graph'),
]

