from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^study/studybutton/$', views.study_button.as_view(), name='study_button'),
    url(r'^study/ten_min_data/$',views.ten_min_data.as_view(), name='ten_min_data'),
    url(r'^study/study_data/$',views.study_data.as_view(), name='study_data'),
    url(r'^study/room_info/$',views.room_info.as_view(), name='room_info'),


]