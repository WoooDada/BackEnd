from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [

    url(r'^tdl/monthly/$', views.monthly_tdl.as_view(), name='monthly_tdl'),
    url(r'^tdl/weekly/$',views.weekly_tdl.as_view(), name='weekly_tdl'),
    url(r'^tdl/daily/$',views.daily_tdl.as_view(), name='daily_tdl'),

]