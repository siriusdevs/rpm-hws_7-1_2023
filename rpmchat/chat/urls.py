from django.urls import path
from chat.views import run_chat, send_request, logout_request

app_name = 'chat'
urlpatterns = [
    path('', run_chat, name='client'),
    path('send/', view=send_request, name='send'),
    path('logout/', view=logout_request, name='logout')
]
