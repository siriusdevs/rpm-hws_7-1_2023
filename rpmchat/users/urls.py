from django.urls import path
from users import views


app_name = 'users'
urlpatterns = [
    path("registration", views.register, name="register"),
    path('', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout')
]
