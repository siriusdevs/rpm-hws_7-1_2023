from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('main_page/', views.main_page, name='main_page'),
    path('places/', views.places, name='places'),
    path('find_place/', views.find_place, name='find_place'),
    path('update_place/', views.PlacesList.as_view(), name='update_place'),
    path('update_place/<int:p_id>', views.PlacesList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
