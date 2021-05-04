from django.urls import path
from account.api.views import (
	signup_view,
)


app_name = 'account'

urlpatterns = [
	path('signup', signup_view, name="signup"),
]
