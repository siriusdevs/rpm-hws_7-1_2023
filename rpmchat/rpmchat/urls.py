from django.contrib import admin
from django.urls import path, include
from rpmchat.views import home_run

urlpatterns = [
    path('', home_run),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('account/', include('users.urls')),
]
