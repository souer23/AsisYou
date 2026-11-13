"""Crea un segundo estudiante ficticio para demostrar el aislamiento de datos.
No genera ni guarda contraseñas; establécelas con 'manage.py changepassword'.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from api.models import (
    Carrera, Estudiante, Asignatura, Seccion, Inscripcion,
    Evaluacion, Nota, Clase, Asistencia,
)


class Command(BaseCommand):
    help = 'Crea la cuenta ficticia alumno2 y una inscripción con notas distintas.'

    def handle(self, *args, **options):
        try:
            carrera = Carrera.objects.get(codigo='INF')
            seccion = Seccion.objects.get(asignatura__codigo='BDD101', nombre_seccion='001', periodo='2026-2')
            prueba1 = Evaluacion.objects.get(seccion=seccion, nombre='Prueba 1')
        except (Carrera.DoesNotExist, Seccion.DoesNotExist, Evaluacion.DoesNotExist) as exc:
            raise CommandError('Primero debes cargar los datos de Camila con cargar_datos_demo.py.') from exc

        Usuario = get_user_model()
        usuario, nuevo = Usuario.objects.get_or_create(
            username='alumno2',
            defaults={
                'first_name': 'Tomás', 'last_name': 'Vera', 'email': 'tomas@utm.test'
            },
        )
        if nuevo:
            usuario.set_unusable_password()
            usuario.save(update_fields=['password'])

        estudiante, _ = Estudiante.objects.get_or_create(
            usuario=usuario,
            defaults={
                'carrera': carrera, 'numero_matricula': 'UTM2026002', 'semestre_actual': 4,
            },
        )
        inscripcion, _ = Inscripcion.objects.get_or_create(
            estudiante=estudiante, seccion=seccion, defaults={'estado': 'Activa'}
        )
        Nota.objects.update_or_create(
            inscripcion=inscripcion, evaluacion=prueba1,
            defaults={'calificacion': Decimal('6.5')},
        )
        clases = Clase.objects.filter(seccion=seccion, estado='REALIZADA').order_by('fecha', 'id')
        for indice, clase in enumerate(clases):
            Asistencia.objects.update_or_create(
                inscripcion=inscripcion, clase=clase,
                defaults={'estado': 'PRESENTE' if indice < 8 else 'AUSENTE'},
            )

        self.stdout.write(self.style.SUCCESS('Alumno 2 preparado: alumno2 (Tomás Vera), solo Bases de Datos.'))
        self.stdout.write('Asigna una clave local: python manage.py changepassword alumno2')
