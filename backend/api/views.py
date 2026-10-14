from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def chat(request):
    mensaje = request.data.get('message')

    if not isinstance(mensaje, str) or not mensaje.strip():
        return Response(
            {'error': 'Debes enviar un mensaje válido.'},
            status=400
        )

    return Response({
        'reply': '¡Hola! Soy AsisYou, tu asistente académico.'
    })