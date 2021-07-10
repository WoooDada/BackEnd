from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^main/studyrank/$', views.studyrank.as_view(), name='studyrank'),
    url(r'^main/playrank/$', views.playrank.as_view(), name='playrank'),
    url(r'^main/random_rooms/$', views.random_rooms.as_view(), name='random_rooms'),
    url(r'^main/my_rooms/$', views.my_rooms.as_view(), name='my_rooms')
]
