import json
from urllib.request import Request, urlopen
from urllib.error import URLError


MODELO = "qwen3:4b-instruct"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

INTENCIONES = {
    "NOTAS",
    "PROMEDIO",
    "ASISTENCIA",
    "OTRA"
}


def detectar_intencion(mensaje):

    instrucciones = """
    Eres el clasificador de preguntas de AsisYou,
    un asistente universitario.

    Clasifica la pregunta en una sola categoría:

    NOTAS: consultar calificaciones individuales.
    PROMEDIO: promedios, aprobación o notas necesarias.
    ASISTENCIA: asistencia, faltas o clases restantes.
    OTRA: cualquier consulta diferente.

    Responde exclusivamente con un objeto JSON:
    {"intencion": "CATEGORIA"}

    No inventes información académica.
    """

    datos = {
        "model": MODELO,
        "messages": [
            {
                "role": "system",
                "content": instrucciones
            },
            {
                "role": "user",
                "content": mensaje
            }
        ],
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "num_predict": 50
        }
    }

    solicitud = Request(
        OLLAMA_URL,
        data=json.dumps(datos).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urlopen(solicitud, timeout=30) as respuesta:
            contenido = json.load(respuesta)

        texto = contenido["message"]["content"]
        resultado = json.loads(texto)

        intencion = resultado.get("intencion", "").upper()

        if intencion in INTENCIONES:
            return intencion

    except (
        URLError,
        TimeoutError,
        ValueError,
        KeyError,
        AttributeError
    ):
        pass

    # Si Ollama falla, Django puede usar las reglas anteriores
    return None