from django.conf import settings
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator


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

    TIPOS_EXAMEN = [
        ('SIN_EXAMEN', 'Sin examen'),
        ('FINAL', 'Examen final'),
        ('RECUPERACION', 'Recuperación'),
        ('AMBOS', 'Final y recuperación'),
    ]

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

    # Reglas de aprobación
    nota_minima = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=4.0
    )

    # Reglas de asistencia
    requiere_asistencia = models.BooleanField(default=True)

    asistencia_minima = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Reglas de examen
    tipo_examen = models.CharField(
        max_length=20,
        choices=TIPOS_EXAMEN,
        default='SIN_EXAMEN'
    )

    ponderacion_examen = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Reglas de recuperación
    promedio_min_recuperacion = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True
    )

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

class Evaluacion(models.Model):

    TIPOS_EVALUACION = [
        ('PRUEBA', 'Prueba'),
        ('TAREA', 'Tarea'),
        ('TRABAJO', 'Trabajo'),
        ('EXAMEN', 'Examen final'),
        ('RECUPERACION', 'Recuperación'),
    ]

    seccion = models.ForeignKey(
        Seccion,
        on_delete=models.PROTECT
    )

    nombre = models.CharField(max_length=120)

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_EVALUACION
    )

    fecha = models.DateField()

    ponderacion = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0')),
            MaxValueValidator(Decimal('100'))
        ]
    )

    def __str__(self):
        return f"{self.nombre} - {self.seccion}"

class Nota(models.Model):

    inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.PROTECT
    )

    evaluacion = models.ForeignKey(
        Evaluacion,
        on_delete=models.PROTECT
    )

    calificacion = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('1.0')),
            MaxValueValidator(Decimal('7.0'))
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['inscripcion', 'evaluacion'],
                name='nota_unica_por_evaluacion'
            )
        ]

    def __str__(self):
        return f"{self.inscripcion} - {self.calificacion}"

class Clase(models.Model):

    ESTADOS_CLASE = [
        ('PROGRAMADA', 'Programada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    ]

    seccion = models.ForeignKey(
        Seccion,
        on_delete=models.PROTECT
    )

    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    modalidad = models.CharField(
        max_length=20,
        default='Presencial'
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_CLASE,
        default='PROGRAMADA'
    )

    def __str__(self):
        return f"{self.seccion} - {self.fecha}"

class Asistencia(models.Model):

    ESTADOS_ASISTENCIA = [
        ('PRESENTE', 'Presente'),
        ('AUSENTE', 'Ausente'),
        ('JUSTIFICADA', 'Ausencia justificada'),
    ]

    inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.PROTECT
    )

    clase = models.ForeignKey(
        Clase,
        on_delete=models.PROTECT
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_ASISTENCIA
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['inscripcion', 'clase'],
                name='asistencia_unica_por_clase'
            )
        ]

    def __str__(self):
        return f"{self.inscripcion} - {self.estado}"

class Aviso(models.Model):

    PRIORIDADES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
    ]

    ESTADOS_AVISO = [
        ('PUBLICADO', 'Publicado'),
        ('ARCHIVADO', 'Archivado'),
    ]

    seccion = models.ForeignKey(
        Seccion,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    titulo = models.CharField(max_length=150)

    contenido = models.TextField()

    remitente = models.CharField(max_length=120)

    fecha_publicacion = models.DateTimeField(
        auto_now_add=True
    )

    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDADES,
        default='MEDIA'
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_AVISO,
        default='PUBLICADO'
    )

    def __str__(self):
        return self.titulo

class DocumentoInstitucional(models.Model):

    TIPOS_DOCUMENTO = [
        ('REGLAMENTO', 'Reglamento'),
        ('PROTOCOLO', 'Protocolo'),
        ('GUIA', 'Guía'),
        ('OTRO', 'Otro'),
    ]

    ESTADOS_DOCUMENTO = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    titulo = models.CharField(max_length=200)

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_DOCUMENTO
    )

    ruta_archivo = models.CharField(
        max_length=255
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_DOCUMENTO,
        default='ACTIVO'
    )

    def __str__(self):
        return self.titulo
