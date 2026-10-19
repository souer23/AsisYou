import json
from urllib.request import Request, urlopen
from urllib.error import URLError


MODELO = "qwen3:4b-instruct"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

INTENCIONES = {
    "NOTAS",
    "PROMEDIO",
    "ASISTENCIA",
    "SIMULACION",
    "OTRA"
}
def interpretar_simulacion(mensaje):
    instrucciones = """
    Eres un extractor de información para AsisYou.

    Tu tarea es analizar preguntas de estudiantes sobre
    notas hipotéticas.

    Extrae:
    - asignatura: nombre de la asignatura mencionada.
    - notas: lista de evaluaciones y notas hipotéticas.

    Devuelve solamente un objeto JSON con esta estructura:

    {
      "asignatura": "Bases de Datos",
      "notas": [
        {"evaluacion": "Proyecto", "nota": "7.0"}
      ]
    }

    Reglas:
    - No calcules promedios.
    - No inventes notas ni evaluaciones.
    - Si no se menciona asignatura, utiliza null.
    - Si no se especifica una evaluación, devuelve notas [].
    - Una pregunta puede mencionar varias evaluaciones.
    - Usa punto decimal en las notas.
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
            "num_predict": 180
        }
    }

    solicitud = Request(
        OLLAMA_URL,
        data=json.dumps(datos).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urlopen(solicitud, timeout=45) as respuesta:
            contenido = json.load(respuesta)

        texto = contenido["message"]["content"]
        resultado = json.loads(texto)

        if not isinstance(resultado, dict):
            return None

        if not isinstance(resultado.get("notas"), list):
            return None

        return resultado

    except (
        URLError,
        TimeoutError,
        ValueError,
        KeyError,
        AttributeError
    ):
        return None

def detectar_intencion(mensaje):

    instrucciones = """
    Eres el clasificador de preguntas de AsisYou,
    un asistente universitario.

    Clasifica la pregunta en una sola categoría:

    NOTAS: consultar calificaciones individuales.
    PROMEDIO: consultar promedios, aprobación o notas necesarias, sin proponer notas hipotéticas.
    ASISTENCIA: asistencia, faltas o clases restantes.
    SIMULACION: el estudiante propone una o más notas hipotéticas para evaluaciones, como "si me saco un 7 en el proyecto, ¿apruebo?".
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