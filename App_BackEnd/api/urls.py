from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^accounts/$', views.AccountListView.as_view(), name='Account List'),
    url(r'^api/signup/$', views.signup.as_view(), name='signup'),
    url(r'^api/login/$',views.login.as_view(), name='login')
]