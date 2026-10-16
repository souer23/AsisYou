from django.conf import settings
from django.db import models


class Carrera(models.Model):
    nombre = models.CharField(max_length=120)
    codigo = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre


class Estudiante(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.PROTECT
    )
    numero_matricula = models.CharField(
        max_length=20,
        unique=True
    )
    semestre_actual = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"Estudiante {self.numero_matricula}"

class Asignatura(models.Model):
    nombre = models.CharField(max_length=120)
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Seccion(models.Model):
    asignatura = models.ForeignKey(
        Asignatura,
        on_delete=models.PROTECT
    )
    nombre_seccion = models.CharField(max_length=20)
    periodo = models.CharField(max_length=20)
    modalidad = models.CharField(
        max_length=20,
        default='Presencial'
    )

    nota_minima = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=4.0
    )
    asistencia_minima = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=70
    )
    requiere_asistencia = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.asignatura.nombre} - {self.nombre_seccion}"

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.PROTECT
    )

    seccion = models.ForeignKey(
        Seccion,
        on_delete=models.PROTECT
    )

    fecha_inscripcion = models.DateField(auto_now_add=True)

    estado = models.CharField(
        max_length=20,
        default='Activa'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['estudiante', 'seccion'],
                name='inscripcion_unica'
            )
        ]

    def __str__(self):
        return f"{self.estudiante} - {self.seccion}"
