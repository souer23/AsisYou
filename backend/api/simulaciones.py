from decimal import Decimal, InvalidOperation
import unicodedata

from .models import Inscripcion, Evaluacion, Nota
from .calculos import calcular_notas
from .llm import interpretar_simulacion


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(
        c for c in texto if not unicodedata.combining(c)
    )
    return " ".join(texto.casefold().split())


def formato_nota(valor):
    return str(
        Decimal(str(valor)).quantize(Decimal("0.1"))
    ).replace(".", ",")


def responder_simulacion(estudiante, mensaje):
    datos = interpretar_simulacion(mensaje)

    if not isinstance(datos, dict):
        return "No pude interpretar la simulación. Intenta nuevamente."

    nombre_asignatura = datos.get("asignatura")
    notas_propuestas = datos.get("notas")

    if not nombre_asignatura:
        return "¿En qué asignatura quieres simular las notas?"

    if not isinstance(notas_propuestas, list) or not notas_propuestas:
        return "Indícame la evaluación y la nota que quieres simular."

    # Buscar solamente asignaturas inscritas por este estudiante.
    inscripciones = list(
        Inscripcion.objects.filter(
            estudiante=estudiante,
            estado="Activa"
        ).select_related("seccion__asignatura")
    )

    coincidencias = [
        i for i in inscripciones
        if normalizar(i.seccion.asignatura.nombre)
        == normalizar(nombre_asignatura)
    ]

    if not coincidencias:
        return (
            f"No encontré {nombre_asignatura} entre las "
            "asignaturas inscritas del estudiante."
        )

    if len(coincidencias) > 1:
        return "Tienes varias secciones de esa asignatura. Indica la sección."

    inscripcion = coincidencias[0]

    evaluaciones = list(
        Evaluacion.objects.filter(
            seccion=inscripcion.seccion
        ).exclude(tipo="RECUPERACION")
    )

    ids_con_nota_real = set(
        Nota.objects.filter(
            inscripcion=inscripcion
        ).values_list("evaluacion_id", flat=True)
    )

    simuladas = {}
    nombres_simulados = []

    for propuesta in notas_propuestas:
        if not isinstance(propuesta, dict):
            return "No pude interpretar una de las evaluaciones."

        nombre = propuesta.get("evaluacion")

        if not isinstance(nombre, str) or not nombre.strip():
            return "Debes indicar qué evaluación quieres simular."

        buscada = normalizar(nombre)

        # Primero buscar coincidencia exacta.
        encontradas = [
            e for e in evaluaciones
            if normalizar(e.nombre) == buscada
        ]

        # Permitir "examen" si solo existe "Examen final".
        if not encontradas:
            encontradas = [
                e for e in evaluaciones
                if buscada in normalizar(e.nombre)
            ]

        if len(encontradas) != 1:
            return (
                f"No pude identificar una única evaluación "
                f"llamada '{nombre}' en esa asignatura."
            )

        evaluacion = encontradas[0]

        if evaluacion.id in ids_con_nota_real:
            return (
                f"{evaluacion.nombre} ya tiene una nota registrada. "
                "Esta simulación solo admite evaluaciones pendientes."
            )

        if evaluacion.id in simuladas:
            return "Mencionaste dos veces la misma evaluación."

        try:
            nota = Decimal(
                str(propuesta.get("nota")).replace(",", ".")
            )
        except (InvalidOperation, ValueError):
            return "Una de las notas propuestas no es válida."

        if not nota.is_finite() or not Decimal("1") <= nota <= Decimal("7"):
            return "Las notas deben estar entre 1,0 y 7,0."

        if nota != nota.quantize(Decimal("0.1")):
            return "Las notas deben expresarse con un decimal."

        simuladas[evaluacion.id] = str(nota)
        nombres_simulados.append(
            f"{evaluacion.nombre}: {formato_nota(nota)}"
        )

    resultado = calcular_notas(inscripcion, simuladas)

    if "error" in resultado:
        return resultado["error"]

    introduccion = (
        f"Simulación de {inscripcion.seccion.asignatura.nombre}\n"
        + "\n".join(nombres_simulados)
        + "\n\n"
    )

    pendientes = [
        e for e in evaluaciones
        if e.id not in ids_con_nota_real
        and e.id not in simuladas
    ]

    # Ya se conocen todas las notas.
    if not pendientes:
        nota_final = formato_nota(resultado["nota_final"])

        if resultado["aprueba_por_notas"]:
            mensaje_final = (
                f"Con esas notas, tu promedio final sería "
                f"{nota_final}. Sí alcanzarías la nota mínima."
            )
        else:
            mensaje_final = (
                f"Con esas notas, tu promedio final sería "
                f"{nota_final}. No alcanzarías la nota mínima."
            )

        return introduccion + mensaje_final + (
            "\n\nEsto considera solo las notas, no la asistencia "
            "ni otros requisitos académicos."
        )

    # Probar el peor y el mejor escenario posible en lo pendiente.
    peor_escenario = calcular_notas(
        inscripcion,
        {
            **simuladas,
            **{e.id: "1.0" for e in pendientes}
        }
    )

    mejor_escenario = calcular_notas(
        inscripcion,
        {
            **simuladas,
            **{e.id: "7.0" for e in pendientes}
        }
    )

    if peor_escenario["aprueba_por_notas"]:
        respuesta = (
            "Sí, alcanzarías la nota mínima incluso si "
            "obtienes un 1,0 en todas las evaluaciones "
            "que quedan pendientes.\n"
            "En ese escenario, tu nota final sería "
            f"{formato_nota(peor_escenario['nota_final'])}."
        )

    elif not mejor_escenario["aprueba_por_notas"]:
        respuesta = (
            "No alcanzarías la nota mínima, ni siquiera "
            "obteniendo un 7,0 en todas las evaluaciones "
            "pendientes."
        )

    else:
        necesaria = formato_nota(resultado["nota_necesaria"])

        if len(pendientes) == 1:
            respuesta = (
                f"Todavía podrías aprobar. Necesitarías "
                f"al menos un {necesaria} en "
                f"{pendientes[0].nombre}."
            )
        else:
            respuesta = (
                f"Todavía podrías aprobar. Necesitarías "
                f"promediar al menos {necesaria} en las "
                "evaluaciones pendientes."
            )

    return introduccion + respuesta + (
        "\n\nEsta simulación no modifica tus notas reales. "
        "También debes cumplir los requisitos de asistencia "
        "y cualquier condición especial del examen."
    )