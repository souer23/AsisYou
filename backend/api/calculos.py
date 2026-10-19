from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING

from .models import Evaluacion, Nota


def redondear_nota(valor):
    """Redondeo académico provisional a un decimal."""
    return valor.quantize(
        Decimal('0.1'),
        rounding=ROUND_HALF_UP
    )


def calcular_notas(inscripcion, simuladas=None):
    """
    Calcula notas reales o simula escenarios.

    simuladas es un diccionario:
    {id_evaluacion: nota_hipotetica}
    """
    if simuladas is None:
        simuladas = {}

    seccion = inscripcion.seccion

    evaluaciones = list(
        Evaluacion.objects.filter(
            seccion=seccion
        ).exclude(
            tipo='RECUPERACION'
        ).order_by('fecha', 'id')
    )

    if not evaluaciones:
        return {"error": "No hay evaluaciones configuradas."}

    peso_total = sum(
        (e.ponderacion for e in evaluaciones),
        Decimal('0')
    )

    if peso_total != Decimal('100'):
        return {"error": "Las ponderaciones no suman 100%."}

    if any(e.ponderacion < 0 for e in evaluaciones):
        return {"error": "Hay ponderaciones negativas."}

    notas = {
        nota.evaluacion_id: nota.calificacion
        for nota in Nota.objects.filter(
            inscripcion=inscripcion,
            evaluacion__seccion=seccion
        )
    }

    ids_validos = {e.id for e in evaluaciones}

    if any(id_eval not in ids_validos for id_eval in simuladas):
        return {"error": "La simulación contiene una evaluación inválida."}

    aporte = Decimal('0')
    peso_considerado = Decimal('0')
    peso_pendiente = Decimal('0')

    for evaluacion in evaluaciones:

        if evaluacion.id in notas:
            if evaluacion.id in simuladas:
                return {
                    "error": "No puedes reemplazar una nota real en esta simulación."
                }
            calificacion = notas[evaluacion.id]

        elif evaluacion.id in simuladas:
            try:
                calificacion = Decimal(
                    str(simuladas[evaluacion.id])
                )
            except Exception:
                return {"error": "La nota simulada no es válida."}

            if not (
                Decimal('1.0') <= calificacion <= Decimal('7.0')
            ):
                return {"error": "La nota debe estar entre 1,0 y 7,0."}

            if calificacion != calificacion.quantize(Decimal('0.1')):
                return {"error": "Las notas deben tener un decimal."}

        else:
            peso_pendiente += evaluacion.ponderacion
            continue

        aporte += (
            calificacion
            * evaluacion.ponderacion
            / Decimal('100')
        )

        peso_considerado += evaluacion.ponderacion

    promedio_actual = None

    if peso_considerado > 0:
        promedio_actual = (
            aporte / (peso_considerado / Decimal('100'))
        )

    resultado = {
        "asignatura": seccion.asignatura.nombre,
        "promedio_actual": (
            str(promedio_actual.quantize(Decimal('0.01')))
            if promedio_actual is not None else None
        ),
        "peso_considerado": str(peso_considerado),
        "peso_pendiente": str(peso_pendiente),
        "nota_minima": str(seccion.nota_minima),
        "nota_necesaria": None,
        "alcanzable": None,
        "nota_final": None,
        "aprueba_por_notas": None
    }

    if peso_pendiente == 0:
        nota_final = redondear_nota(aporte)

        resultado["nota_final"] = str(nota_final)
        resultado["aprueba_por_notas"] = (
            nota_final >= seccion.nota_minima
        )

    else:
        # Para aprobar con redondeo a un decimal,
        # 3.95 puede convertirse en 4.0.
        minimo_sin_redondear = (
            seccion.nota_minima - Decimal('0.05')
        )

        requerida = (
            minimo_sin_redondear - aporte
        ) / (peso_pendiente / Decimal('100'))

        requerida = max(
            Decimal('1.0'),
            (
                requerida * 10
            ).to_integral_value(
                rounding=ROUND_CEILING
            ) / Decimal('10')
        )

        resultado["alcanzable"] = (
            requerida <= Decimal('7.0')
        )

        if resultado["alcanzable"]:
            resultado["nota_necesaria"] = str(requerida)

    return resultado