
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^', include('api.urls')),         #login, signup
    url(r'^', include('home.urls')),        #badge_profile
    url(r'^', include('tdl.urls')),         #monthly/weekly/dialy
    url(r'^', include('study.urls')),
    url(r'^', include('main.urls')),
    url(r'^', include('myprofile.urls')),
    url(r'^', include('studyroom.urls')),
  #  url(r'^', include('yolo.urls')),
]
