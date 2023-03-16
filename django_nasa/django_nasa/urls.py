"""django_nasa URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/

Examples:
    Function views:
        1. Add an import:  from my_app import views.
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
