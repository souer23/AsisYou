from rest_framework.decorators import api_view
from rest_framework.response import Response
from .calculos import calcular_notas
from .asistencia_calculos import calcular_asistencia
from .llm import detectar_intencion
from .simulaciones import responder_simulacion
from django.utils import timezone

from .models import Estudiante, Inscripcion, Evaluacion, Nota
from decimal import Decimal, ROUND_HALF_UP


def formato_nota(valor):
    nota = Decimal(str(valor)).quantize(
        Decimal('0.1'),
        rounding=ROUND_HALF_UP
    )
    return str(nota).replace('.', ',')


def formato_porcentaje(valor):
    porcentaje = Decimal(str(valor)).normalize()
    return format(porcentaje, 'f').replace('.', ',')


@api_view(['POST'])
def chat(request):

    mensaje = request.data.get('message')

    if not isinstance(mensaje, str) or not mensaje.strip():
        return Response(
            {'error': 'Debes enviar un mensaje válido.'},
            status=400
        )

    # Consultas sobre promedios y notas necesarias
    consulta = mensaje.lower()
    intencion = detectar_intencion(mensaje)

    # Simulaciones de notas hipotéticas
    es_simulacion = (
        intencion == "SIMULACION"
        or consulta.lstrip("¿¡ ").startswith((
            "si me saco",
            "si saco",
            "si obtengo",
            "si tengo un",
            "si tuviera"
        ))
    )

    if es_simulacion:
        try:
            estudiante = Estudiante.objects.get(
                usuario__username="alumno_demo"
            )
        except Estudiante.DoesNotExist:
            return Response({
                "reply": "No encontré al estudiante de prueba."
            })

        respuesta = responder_simulacion(
            estudiante,
            mensaje
        )

        return Response({"reply": respuesta})

     # Consultas sobre asistencia
    if intencion == "ASISTENCIA" or any(
    palabra in consulta
    for palabra in ['asist', 'clase', 'faltas', '70%']
    ):

        try:
            estudiante = Estudiante.objects.get(
                usuario__username='alumno_demo'
            )
        except Estudiante.DoesNotExist:
            return Response({
                'reply': 'No encontré al estudiante de prueba.'
            })

        inscripciones = Inscripcion.objects.filter(
            estudiante=estudiante,
            estado='Activa'
        ).select_related('seccion__asignatura')

        # Filtrar por asignatura si el estudiante la menciona
        if 'bases de datos' in consulta:
            inscripciones = inscripciones.filter(
                seccion__asignatura__nombre='Bases de Datos'
            )
        elif 'ingl' in consulta:
            inscripciones = inscripciones.filter(
                seccion__asignatura__nombre='Inglés Online'
            )

        respuestas = []

        for inscripcion in inscripciones:

            resultado = calcular_asistencia(inscripcion)

            if 'error' in resultado:
                respuestas.append(resultado['error'])
                continue

            nombre = resultado['asignatura']

            if not resultado['requiere_asistencia']:
                respuestas.append(
                    f'{nombre}: Esta sección no exige '
                    f'un porcentaje mínimo de asistencia.'
                )
                continue

            presentes = resultado['clases_presentes']
            realizadas = resultado['clases_realizadas']
            restantes = resultado['clases_restantes']

            actual = resultado['porcentaje_actual']
            maximo = resultado['porcentaje_maximo']
            minimo = resultado['asistencia_minima']

            necesarias = resultado['clases_necesarias']
            alcanzable = resultado['alcanzable']

            texto = f'{nombre}\n'

            if actual is not None:
                texto += (
                    f'Asistencia actual: '
                    f'{formato_porcentaje(actual)}% '
                    f'({presentes} de {realizadas} clases).\n'
                )
            else:
                texto += 'Aún no hay clases realizadas.\n'

            texto += (
                f'Clases restantes: {restantes}\n'
                f'Asistencia mínima: '
                f'{formato_porcentaje(minimo)}%\n'
            )

            if maximo is not None:
                texto += (
                    f'Si asistes a todas las clases restantes, '
                    f'alcanzarías un '
                    f'{formato_porcentaje(maximo)}%.\n'
                )

            if alcanzable:
                if necesarias == 0:
                    texto += (
                        'Ya tienes suficientes asistencias '
                        'para cumplir el mínimo al finalizar '
                        'las clases programadas.'
                    )
                else:
                    texto += (
                        f'Necesitas asistir al menos a '
                        f'{necesarias} de las {restantes} '
                        f'clases restantes para cumplir '
                        f'el requisito.'
                    )
            else:
                texto += (
                    'Aunque asistas a todas las clases '
                    'restantes, no alcanzarías el '
                    'mínimo exigido.'
                )

            respuestas.append(texto)

        return Response({
            'reply': '\n\n'.join(respuestas)
            if respuestas else 'No encontré asignaturas.'
        })

    if intencion == "PROMEDIO" or any(
    palabra in consulta
    for palabra in ['promedio', 'necesit', 'aprobar', 'me falta']
    ):

        try:
            estudiante = Estudiante.objects.get(
                usuario__username='alumno_demo'
            )
        except Estudiante.DoesNotExist:
            return Response({
                'reply': 'No encontré al estudiante de prueba.'
            })

        inscripciones = Inscripcion.objects.filter(
            estudiante=estudiante,
            estado='Activa'
        ).select_related('seccion__asignatura')

        # Si menciona una asignatura, mostrar solo esa
        if 'bases de datos' in consulta:
            inscripciones = inscripciones.filter(
                seccion__asignatura__nombre='Bases de Datos'
            )
        elif 'ingl' in consulta:
            inscripciones = inscripciones.filter(
                seccion__asignatura__nombre='Inglés Online'
            )

        respuestas = []

        for inscripcion in inscripciones:
            resultado = calcular_notas(inscripcion)

            if 'error' in resultado:
                respuestas.append(resultado['error'])
                continue

            nombre = resultado['asignatura']
            promedio = resultado['promedio_actual']
            pendiente = resultado['peso_pendiente']
            necesaria = resultado['nota_necesaria']

            if promedio is None:
                texto = f'{nombre}: Aún no tienes notas.'
            else:
                texto = (
                    f'{nombre}\n'
                    f'Promedio actual: '
                    f'{formato_nota(promedio)}\n'
                )

                if necesaria is not None:
                    texto += (
                        f'Tienes pendiente el {formato_porcentaje(pendiente)}% '
                        f'de las evaluaciones.\n'
                        f'Necesitas promediar al menos '
                        f'{formato_nota(necesaria)} '
                        f'en las evaluaciones restantes '
                        f'para alcanzar la nota mínima.'
                    )

                elif resultado['alcanzable'] is False:
                    texto += (
                        'Con las notas pendientes ya no '
                        'alcanzas la nota mínima, '
                        'incluso obteniendo un 7,0.'
                    )

                elif resultado['nota_final'] is not None:
                    texto += (
                        f'Nota final: '
                        f'{resultado["nota_final"].replace(".", ",")}.'
                    )

            respuestas.append(texto)

        return Response({
            'reply': '\n\n'.join(respuestas)
            if respuestas else 'No encontré asignaturas.'
        })

    # Identificar una consulta sobre notas
    if intencion == "NOTAS" or 'nota' in consulta:

        # Temporal: estudiante ficticio de demostración
        try:
            estudiante = Estudiante.objects.get(
                usuario__username='alumno_demo'
            )
        except Estudiante.DoesNotExist:
            return Response({
                'reply': 'No encontré al estudiante de prueba.'
            })

        inscripciones = Inscripcion.objects.filter(
            estudiante=estudiante,
            estado='Activa'
        ).select_related('seccion__asignatura')

        respuesta = ['Estas son tus calificaciones:']

        for inscripcion in inscripciones:

            asignatura = inscripcion.seccion.asignatura.nombre
            respuesta.append(f'\n{asignatura}:')

            evaluaciones = Evaluacion.objects.filter(
                seccion=inscripcion.seccion
            ).order_by('fecha')

            for evaluacion in evaluaciones:

                nota = Nota.objects.filter(
                    inscripcion=inscripcion,
                    evaluacion=evaluacion
                ).first()

                if nota:
                    calificacion = str(nota.calificacion).replace('.', ',')
                else:
                    calificacion = 'Pendiente'

                respuesta.append(
                    f'{evaluacion.nombre}: {calificacion} '
                    f'({formato_porcentaje(evaluacion.ponderacion)}% de ponderación)'
                )

        if len(respuesta) == 1:
            respuesta.append('No hay asignaturas inscritas.')

        return Response({
            'reply': '\n'.join(respuesta)
        })

    # Respuesta temporal para otras preguntas
    return Response({
        'reply': (
            '¡Hola! Soy AsisYou. Por ahora puedes '
            'preguntarme: ¿Qué notas tengo?'
        )
    })

@api_view(['GET'])
def perfil_demo(request):
    try:
        estudiante = Estudiante.objects.select_related(
            'usuario', 'carrera'
        ).get(usuario__username='alumno_demo')

    except Estudiante.DoesNotExist:
        return Response(
            {'error': 'No encontré al estudiante de prueba.'},
            status=404
        )

    inscripciones = Inscripcion.objects.filter(
        estudiante=estudiante,
        estado='Activa'
    ).select_related('seccion__asignatura')

    asignaturas = []
    promedios = []
    clases_presentes = 0
    clases_realizadas = 0

    for inscripcion in inscripciones:
        seccion = inscripcion.seccion

        notas = calcular_notas(inscripcion)
        asistencia = calcular_asistencia(inscripcion)

        promedio = notas.get('promedio_actual')
        porcentaje = None

        if promedio is not None:
            promedios.append(Decimal(str(promedio)))

        if (
            asistencia.get('requiere_asistencia')
            and 'error' not in asistencia
        ):
            actual = asistencia.get('porcentaje_actual')

            if actual is not None:
                porcentaje = (
                    formato_porcentaje(actual) + '%'
                )

            clases_presentes += asistencia['clases_presentes']
            clases_realizadas += asistencia['clases_realizadas']

        asignaturas.append({
            'codigo': seccion.asignatura.codigo,
            'nombre': seccion.asignatura.nombre,
            'seccion': seccion.nombre_seccion,
            'promedio': (
                formato_nota(promedio)
                if promedio is not None else None
            ),
            'asistencia': porcentaje
        })

    promedio_general = None

    if promedios:
        promedio_general = formato_nota(
            sum(promedios) / len(promedios)
        )

    asistencia_general = None

    if clases_realizadas > 0:
        asistencia_general = (
            formato_porcentaje(
                Decimal(clases_presentes)
                * 100 / Decimal(clases_realizadas)
            ) + '%'
        )
     # Obtener próximas evaluaciones pendientes
    proximas = []
    hoy = timezone.localdate()

    for inscripcion in inscripciones:
        notas_registradas = Nota.objects.filter(
            inscripcion=inscripcion
        ).values_list("evaluacion_id", flat=True)

        evaluaciones = Evaluacion.objects.filter(
            seccion=inscripcion.seccion,
            fecha__gte=hoy
        ).exclude(
            id__in=notas_registradas
        ).order_by("fecha")

        for evaluacion in evaluaciones:
            proximas.append({
                "fecha": evaluacion.fecha.isoformat(),
                "titulo": evaluacion.nombre,
                "asignatura": inscripcion.seccion.asignatura.nombre,
                "tipo": evaluacion.get_tipo_display()
            })

    proximas.sort(key=lambda actividad: actividad["fecha"])
    usuario = estudiante.usuario
    nombre = usuario.get_full_name().strip() or usuario.username

    iniciales = ''.join(
        parte[0].upper()
        for parte in nombre.split()[:2]
    )

    return Response({
        'nombre': nombre,
        'iniciales': iniciales,
        'carrera': estudiante.carrera.nombre,
        'semestre': estudiante.semestre_actual,
        'total_asignaturas': len(asignaturas),
        'promedio_general': promedio_general,
        'asistencia_general': asistencia_general,
        'asignaturas': asignaturas,
        'proximas_actividades': proximas[:3]
    })