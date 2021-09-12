from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^', include('api.urls')),         #login, signup
    url(r'^', include('home.urls')),        #badge_profile
    url(r'^', include('tdl.urls')),         #monthly/weekly/dialy
    url(r'^', include('study.urls')),
    url(r'^', include('main.urls')),
    url(r'^', include('myprofile.urls')),
    url(r'^', include('studyroom.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


