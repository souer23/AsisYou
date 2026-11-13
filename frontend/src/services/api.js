import { obtenerCsrfToken } from './auth'

const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === 'true'

export async function sendMessage(message) {
  if (!message?.trim()) throw new Error('Escribe una pregunta antes de enviarla.')

  if (USE_MOCK_API) {
    await new Promise((resolve) => setTimeout(resolve, 700))
    return 'Modo de demostración: esta respuesta no consulta Django.'
  }

  let respuesta
  try {
    const csrf = await obtenerCsrfToken()
    respuesta = await fetch('/api/chat/', {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
      body: JSON.stringify({ message }),
    })
  } catch {
    throw new Error('No se pudo conectar con Django. Comprueba que el servidor esté ejecutándose.')
  }

  if (!respuesta.ok) {
    throw new Error(`El servidor respondió con un error (${respuesta.status}).`)
  }

  const data = await respuesta.json()
  if (typeof data.reply !== 'string') throw new Error('La API no devolvió una respuesta válida.')
  return data.reply
}

export async function obtenerPerfil() {
  const respuesta = await fetch('/api/perfil/', { credentials: 'same-origin' })
  if (!respuesta.ok) throw new Error('No se pudo cargar el perfil del estudiante.')
  return await respuesta.json()
}
