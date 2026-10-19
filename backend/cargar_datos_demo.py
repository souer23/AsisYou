from datetime import date, time, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model

from api.models import (
    Carrera, Estudiante, Asignatura,
    Seccion, Inscripcion, Evaluacion,
    Nota, Clase, Asistencia, Aviso
)

# 1. Crear estudiante ficticio

Usuario = get_user_model()

usuario, creado = Usuario.objects.get_or_create(
    username="alumno_demo",
    defaults={
        "first_name": "Camila",
        "last_name": "Rojas",
        "email": "camila@utm.test"
    }
)

if creado:
    usuario.set_unusable_password()
    usuario.save()

carrera, _ = Carrera.objects.get_or_create(
    codigo="INF",
    defaults={"nombre": "Ingeniería en Informática"}
)

estudiante, _ = Estudiante.objects.get_or_create(
    usuario=usuario,
    defaults={
        "carrera": carrera,
        "numero_matricula": "UTM2026001",
        "semestre_actual": 4
    }
)

# 2. Crear asignaturas

bases, _ = Asignatura.objects.get_or_create(
    codigo="BDD101",
    defaults={"nombre": "Bases de Datos"}
)

ingles, _ = Asignatura.objects.get_or_create(
    codigo="ING101",
    defaults={"nombre": "Inglés Online"}
)

# 3. Configurar secciones con reglas diferentes

seccion_bases, _ = Seccion.objects.update_or_create(
    asignatura=bases,
    nombre_seccion="001",
    periodo="2026-2",
    defaults={
        "modalidad": "Presencial",
        "nota_minima": Decimal("4.0"),
        "requiere_asistencia": True,
        "asistencia_minima": Decimal("70.00"),
        "tipo_examen": "FINAL",
        "ponderacion_examen": Decimal("20.00"),
        "promedio_min_recuperacion": None
    }
)

seccion_ingles, _ = Seccion.objects.update_or_create(
    asignatura=ingles,
    nombre_seccion="001",
    periodo="2026-2",
    defaults={
        "modalidad": "Online",
        "nota_minima": Decimal("4.0"),
        "requiere_asistencia": False,
        "asistencia_minima": None,
        "tipo_examen": "SIN_EXAMEN",
        "ponderacion_examen": None,
        "promedio_min_recuperacion": None
    }
)

ins_bases, _ = Inscripcion.objects.get_or_create(
    estudiante=estudiante,
    seccion=seccion_bases
)

ins_ingles, _ = Inscripcion.objects.get_or_create(
    estudiante=estudiante,
    seccion=seccion_ingles
)

# 4. Crear evaluaciones y notas

evaluaciones = [
    (seccion_bases, ins_bases, "Prueba 1", "PRUEBA",
     date(2026, 10, 1), "25.00", "5.0"),

    (seccion_bases, ins_bases, "Prueba 2", "PRUEBA",
     date(2026, 10, 9), "25.00", "4.0"),

    (seccion_bases, ins_bases, "Proyecto", "TRABAJO",
     date(2026, 10, 23), "30.00", None),

    (seccion_bases, ins_bases, "Examen final", "EXAMEN",
     date(2026, 10, 30), "20.00", None),

    (seccion_ingles, ins_ingles, "Actividad 1", "TAREA",
     date(2026, 10, 8), "50.00", "6.0"),

    (seccion_ingles, ins_ingles, "Actividad 2", "TAREA",
     date(2026, 10, 28), "50.00", None),
]

for seccion, inscripcion, nombre, tipo, fecha, peso, nota in evaluaciones:

    evaluacion, _ = Evaluacion.objects.update_or_create(
        seccion=seccion,
        nombre=nombre,
        defaults={
            "tipo": tipo,
            "fecha": fecha,
            "ponderacion": Decimal(peso)
        }
    )

    if nota is not None:
        Nota.objects.update_or_create(
            inscripcion=inscripcion,
            evaluacion=evaluacion,
            defaults={"calificacion": Decimal(nota)}
        )

# 5. Crear clases y registros de asistencia

# Diez clases realizadas
for i in range(10):
    fecha = date(2026, 9, 15) + timedelta(days=i * 3)

    clase, _ = Clase.objects.update_or_create(
        seccion=seccion_bases,
        fecha=fecha,
        hora_inicio=time(10, 0),
        defaults={
            "hora_fin": time(11, 30),
            "modalidad": "Presencial",
            "estado": "REALIZADA"
        }
    )

    Asistencia.objects.update_or_create(
        inscripcion=ins_bases,
        clase=clase,
        defaults={
            "estado": "PRESENTE" if i < 6 else "AUSENTE"
        }
    )

# Cuatro clases futuras
for i in range(4):
    fecha = date(2026, 10, 20) + timedelta(days=i * 3)

    Clase.objects.update_or_create(
        seccion=seccion_bases,
        fecha=fecha,
        hora_inicio=time(10, 0),
        defaults={
            "hora_fin": time(11, 30),
            "modalidad": "Presencial",
            "estado": "PROGRAMADA"
        }
    )

# 6. Crear aviso

Aviso.objects.get_or_create(
    seccion=seccion_bases,
    titulo="Recordatorio del proyecto",
    defaults={
        "contenido": "El proyecto se entrega el 23 de octubre.",
        "remitente": "Docente de Bases de Datos",
        "prioridad": "ALTA",
        "estado": "PUBLICADO"
    }
)

print("DATOS DE PRUEBA CARGADOS CORRECTAMENTE")
print("Estudiante: Camila Rojas")
print("Asignaturas: Bases de Datos e Inglés Online")
print("Evaluaciones: 6")
print("Clases de Bases de Datos: 14")