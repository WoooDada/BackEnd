from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^tdl/studybutton/$', views.study_button.as_view(), name='study_button'),
    url(r'^tdl/ten_min_data/$',views.ten_min_data.as_view(), name='ten_min_data'),
    url(r'^tdl/study_data/$',views.study_data.as_view(), name='study_data'),

]