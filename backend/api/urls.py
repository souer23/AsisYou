from django.urls import path
from .views import chat, perfil_demo

urlpatterns = [
    path('chat/', chat, name='chat'),
    path('perfil/', perfil_demo, name='perfil_demo'),
]