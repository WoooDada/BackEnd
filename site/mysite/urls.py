
from django.contrib import admin
from django.urls import path, include

from account.views import (
    signup_view,
    logout_view,
    login_view,
    must_authenticate_view,
    account_view,
)

from homepage.views import (
    home,
)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('mainpage.urls')),
    path('homepage/', home, name="home"),
    path('admin/', admin.site.urls),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('signup/', signup_view, name="register"),
    path('account/', account_view, name="account"),

    path('api/account/', include('account.api.urls', 'account_api')),
]
