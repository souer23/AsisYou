const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === 'true'

/**
 * Envía una pregunta al asistente.
 * Contrato acordado con backend:
 * POST /api/chat/  { message: string } -> { reply: string }
 */
export async function sendMessage(message) {
  if (!message?.trim()) {
    throw new Error('Escribe una pregunta antes de enviarla.')
  }

  if (USE_MOCK_API) {
    // Modo de demostración: esta respuesta NO viene de Django.
    await new Promise((resolve) => setTimeout(resolve, 700))
    return 'Estoy en modo de demostración, así que todavía no puedo consultar tus datos reales. Cuando conectemos Django podré ayudarte con información académica.'
  }

  let response
  try {
    response = await fetch('/api/chat/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    })
  } catch {
    throw new Error('No se pudo conectar con el servidor. Comprueba que Django esté ejecutándose.')
  }

  if (!response.ok) {
    throw new Error(`El servidor respondió con un error (${response.status}). Inténtalo nuevamente.`)
  }

  let data
  try {
    data = await response.json()
  } catch {
    throw new Error('El servidor respondió con un formato que no pudimos leer.')
  }

  if (typeof data.reply !== 'string') {
    throw new Error('La respuesta del servidor no contiene la propiedad "reply" esperada.')
  }

  return data.reply
}
