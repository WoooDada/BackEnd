from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^api/signup/$', views.signup.as_view(), name='signup'),
    url(r'^api/login/$',views.login.as_view(), name='login'),

]

