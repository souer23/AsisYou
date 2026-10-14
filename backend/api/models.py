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
