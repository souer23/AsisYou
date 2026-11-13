"""Inicio de sesión para el portal ficticio AsisYou (Django Sessions + CSRF)."""
import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from .models import Estudiante


def info_usuario(usuario):
    estudiante = Estudiante.objects.select_related('carrera').filter(usuario=usuario).first()
    if estudiante is None:
        return None
    return {
        'username': usuario.username,
        'nombre': usuario.get_full_name().strip() or usuario.username,
        'carrera': estudiante.carrera.nombre,
    }


@require_GET
@ensure_csrf_cookie
def obtener_csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


@require_POST
@csrf_protect
def iniciar_sesion(request):
    try:
        datos = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError, TypeError):
        return JsonResponse({'error': 'Solicitud inválida.'}, status=400)

    username = datos.get('username', '')
    password = datos.get('password', '')
    if not isinstance(username, str) or not isinstance(password, str):
        return JsonResponse({'error': 'Credenciales inválidas.'}, status=400)

    usuario = authenticate(request, username=username.strip(), password=password)
    if usuario is None:
        return JsonResponse({'error': 'Usuario o contraseña incorrectos.'}, status=401)

    datos_usuario = info_usuario(usuario)
    if datos_usuario is None:
        return JsonResponse({'error': 'El usuario no tiene un perfil de estudiante.'}, status=403)

    login(request, usuario)
    # login() rota el token CSRF. Enviar el token actualizado para el próximo POST.
    return JsonResponse({'user': datos_usuario, 'csrfToken': get_token(request)})


@require_GET
def sesion_actual(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Debes iniciar sesión.'}, status=401)
    datos_usuario = info_usuario(request.user)
    if datos_usuario is None:
        return JsonResponse({'error': 'Perfil no disponible.'}, status=403)
    return JsonResponse({'user': datos_usuario})


@require_POST
@csrf_protect
def cerrar_sesion(request):
    logout(request)
    return JsonResponse({'ok': True, 'csrfToken': get_token(request)})
