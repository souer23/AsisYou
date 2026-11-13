// Las cookies de sesión son administradas por Django; nunca guardamos contraseñas.
let csrfToken = null

async function jsonSeguro(respuesta) {
  try { return await respuesta.json() }
  catch { return {} }
}

export async function obtenerCsrfToken() {
  if (csrfToken) return csrfToken
  const respuesta = await fetch('/api/auth/csrf/', {
    credentials: 'same-origin', cache: 'no-store',
  })
  const datos = await jsonSeguro(respuesta)
  if (!respuesta.ok || !datos.csrfToken) throw new Error('No se pudo preparar la sesión segura.')
  csrfToken = datos.csrfToken
  return csrfToken
}

export async function iniciarSesion(username, password) {
  const token = await obtenerCsrfToken()
  const respuesta = await fetch('/api/auth/login/', {
    method: 'POST', credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': token },
    body: JSON.stringify({ username, password }),
  })
  const datos = await jsonSeguro(respuesta)
  if (!respuesta.ok) throw new Error(datos.error || `Error de acceso (${respuesta.status}).`)
  csrfToken = datos.csrfToken || null // Django rota CSRF al iniciar sesión.
  return datos.user
}

export async function consultarSesion() {
  const respuesta = await fetch('/api/auth/me/', { credentials: 'same-origin', cache: 'no-store' })
  if (respuesta.status === 401) return null
  const datos = await jsonSeguro(respuesta)
  if (!respuesta.ok) throw new Error(datos.error || 'No se pudo comprobar la sesión.')
  return datos.user
}

export async function cerrarSesion() {
  const token = await obtenerCsrfToken()
  const respuesta = await fetch('/api/auth/logout/', {
    method: 'POST', credentials: 'same-origin',
    headers: { 'X-CSRFToken': token },
  })
  const datos = await jsonSeguro(respuesta)
  if (!respuesta.ok) throw new Error(datos.error || 'No se pudo cerrar sesión.')
  csrfToken = datos.csrfToken || null
}
