from django.urls import path
from .views import chat, perfil_demo
from .auth_views import obtener_csrf, iniciar_sesion, sesion_actual, cerrar_sesion

urlpatterns = [
    path('chat/', chat, name='chat'),
    path('perfil/', perfil_demo, name='perfil_demo'),
    path('auth/csrf/', obtener_csrf, name='auth_csrf'),
    path('auth/login/', iniciar_sesion, name='auth_login'),
    path('auth/me/', sesion_actual, name='auth_me'),
    path('auth/logout/', cerrar_sesion, name='auth_logout'),
]
