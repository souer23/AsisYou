from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Estudiante, Inscripcion, Evaluacion, Nota


@api_view(['POST'])
def chat(request):

    mensaje = request.data.get('message')

    if not isinstance(mensaje, str) or not mensaje.strip():
        return Response(
            {'error': 'Debes enviar un mensaje válido.'},
            status=400
        )

    # Identificar una consulta sobre notas
    if 'nota' in mensaje.lower():

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
                    f'({evaluacion.ponderacion}% de ponderación)'
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