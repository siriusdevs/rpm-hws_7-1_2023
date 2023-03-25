"""django_nasa URL Configuration."""
from django.contrib import admin
from django.urls import path

from nasa.views import nasa_page, mars_page, user_page, user_image_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", nasa_page, name='home'),
    path("nasa", nasa_page, name='nasa'),
    path("mars", mars_page, name='mars'),
    path("user", user_page, name='user'),
    path("user/image/", user_image_page, name='user_image'),
]
