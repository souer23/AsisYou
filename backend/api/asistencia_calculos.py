from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING

from .models import Clase, Asistencia


def calcular_asistencia(inscripcion):
    seccion = inscripcion.seccion
    nombre = seccion.asignatura.nombre

    # Algunas secciones no exigen asistencia
    if not seccion.requiere_asistencia:
        return {
            "asignatura": nombre,
            "requiere_asistencia": False,
            "mensaje": "Esta sección no exige asistencia mínima."
        }

    if seccion.asistencia_minima is None:
        return {
            "error": "La asistencia mínima no está configurada."
        }

    # Clases que ya se realizaron
    clases_realizadas = Clase.objects.filter(
        seccion=seccion,
        estado="REALIZADA"
    )

    realizadas = clases_realizadas.count()

    # Clases pendientes (no incluye canceladas)
    futuras = Clase.objects.filter(
        seccion=seccion,
        estado="PROGRAMADA"
    ).count()

    registros = Asistencia.objects.filter(
        inscripcion=inscripcion,
        clase__in=clases_realizadas
    )

    # Evitar porcentajes engañosos si faltan registros
    if registros.count() != realizadas:
        return {
            "error": "Faltan registros de asistencia."
        }

    presentes = registros.filter(
        estado="PRESENTE"
    ).count()

    minimo = Decimal(str(seccion.asistencia_minima))

    # Porcentaje actual
    porcentaje_actual = None

    if realizadas > 0:
        porcentaje_actual = (
            Decimal(presentes) * 100 / Decimal(realizadas)
        )

    # Máximo posible asistiendo a todas las futuras
    total = realizadas + futuras

    porcentaje_maximo = None

    if total > 0:
        porcentaje_maximo = (
            Decimal(presentes + futuras)
            * 100 / Decimal(total)
        )

    # Cuántas clases futuras necesita asistir
    clases_necesarias = 0

    if total > 0:
        clases_necesarias = max(
            0,
            int(
                (
                    minimo * Decimal(total) / 100
                    - Decimal(presentes)
                ).to_integral_value(
                    rounding=ROUND_CEILING
                )
            )
        )

    alcanzable = clases_necesarias <= futuras

    def porcentaje(valor):
        if valor is None:
            return None

        return str(valor.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        ))

    return {
        "asignatura": nombre,
        "requiere_asistencia": True,
        "clases_realizadas": realizadas,
        "clases_presentes": presentes,
        "clases_restantes": futuras,
        "porcentaje_actual": porcentaje(porcentaje_actual),
        "porcentaje_maximo": porcentaje(porcentaje_maximo),
        "asistencia_minima": str(minimo),
        "clases_necesarias": clases_necesarias,
        "alcanzable": alcanzable
    }