import { useEffect, useState } from 'react'
import { iniciarSesion, consultarSesion, cerrarSesion } from '../services/auth'
import imagenUTM from '../assets/hero.png'
import './PublicSite.css'

// Navegación hash para mantener el portal sin dependencias adicionales.
function rutaActual() {
  const ruta = window.location.hash.replace(/^#/, '')
  return ruta.startsWith('/') ? ruta : '/'
}

function LogoUTM() {
  return (
    <span className="utm-identidad">
      <span className="utm-simbolo" aria-hidden="true">
        <svg viewBox="0 0 48 48" fill="none" focusable="false">
          <path d="M5 18 24 8l19 10-19 10L5 18Z" stroke="currentColor" strokeWidth="2.8" strokeLinejoin="round" />
          <path d="M13 23v11c8 6 14 6 22 0V23" stroke="currentColor" strokeWidth="2.8" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M42 19v13" stroke="currentColor" strokeWidth="2.8" strokeLinecap="round" />
          <circle cx="42" cy="35" r="2.5" fill="currentColor" />
        </svg>
      </span>
      <span className="utm-identidad-texto">
        <strong>UTM</strong>
        <small>Universidad Tecnológica del Maule</small>
      </span>
    </span>
  )
}

function InicioPublico() {
  function irSobreNosotros() {
    document.getElementById('utm-sobre-nosotros')?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <div className="utm-publico">
      <header className="utm-barra">
        <div className="utm-contenedor utm-barra-interior">
          <a className="utm-logo-enlace" href="#/" aria-label="Ir al inicio de la UTM">
            <LogoUTM />
          </a>
          <nav className="utm-navegacion" aria-label="Navegación principal">
            <button type="button" className="utm-enlace-texto" onClick={irSobreNosotros}>
              Sobre nosotros
            </button>
            <a className="utm-boton utm-boton-amarillo" href="#/login">
              Iniciar sesión <span aria-hidden="true">↗</span>
            </a>
          </nav>
        </div>
      </header>

      <main>
        <section className="utm-portada utm-contenedor" aria-labelledby="utm-titulo">
          <div className="utm-portada-texto">
            <span className="utm-etiqueta"><span className="utm-punto" /> UNIVERSIDAD TECNOLÓGICA DEL MAULE</span>
            <h1 id="utm-titulo">Una experiencia académica <em>más cercana.</em></h1>
            <p>
              Bienvenido a la UTM, una universidad ficticia creada para demostrar
              cómo la tecnología puede facilitar la vida estudiantil en la Región del Maule.
            </p>
            <div className="utm-acciones">
              <a className="utm-boton utm-boton-amarillo utm-boton-grande" href="#/login">
                Acceder al portal estudiantil <span aria-hidden="true">→</span>
              </a>
              <button type="button" className="utm-boton utm-boton-borde" onClick={irSobreNosotros}>
                Conoce la UTM
              </button>
            </div>
            <span className="utm-nota-portada">Portal académico de demostración · Proyecto AsisYou</span>
          </div>
          <div className="utm-portada-visual">
            <img src={imagenUTM} alt="Imagen de presentación del campus universitario UTM" />
            <div className="utm-tarjeta-flotante">
              <span className="utm-estrella" aria-hidden="true">✦</span>
              <span><strong>AsisYou</strong><small>Tu asistente académico virtual</small></span>
            </div>
          </div>
        </section>

        <section className="utm-seccion-sobre" id="utm-sobre-nosotros" aria-labelledby="utm-sobre-titulo">
          <div className="utm-contenedor">
            <div className="utm-seccion-encabezado">
              <span className="utm-etiqueta">SOBRE NOSOTROS</span>
              <h2 id="utm-sobre-titulo">Educación e innovación en un mismo lugar.</h2>
              <p>
                La UTM es el entorno universitario ficticio en el que se desarrolla AsisYou,
                una propuesta para simplificar el acceso a la información académica.
              </p>
            </div>
            <div className="utm-beneficios">
              <article className="utm-beneficio">
                <span className="utm-beneficio-icono" aria-hidden="true">▤</span>
                <h3>Información organizada</h3>
                <p>Consulta asignaturas, calificaciones y asistencia desde un único portal.</p>
              </article>
              <article className="utm-beneficio">
                <span className="utm-beneficio-icono" aria-hidden="true">✦</span>
                <h3>Orientación académica</h3>
                <p>Haz preguntas en lenguaje natural y explora simulaciones con AsisYou.</p>
              </article>
              <article className="utm-beneficio">
                <span className="utm-beneficio-icono" aria-hidden="true">◈</span>
                <h3>Acceso desde cualquier pantalla</h3>
                <p>Una experiencia web diseñada para computadores y teléfonos móviles.</p>
              </article>
            </div>
          </div>
        </section>
      </main>
      <footer className="utm-pie">
        <div className="utm-contenedor utm-pie-interior">
          <span>© 2026 UTM · Proyecto académico ficticio</span>
          <span>Desarrollado como demostración de AsisYou</span>
        </div>
      </footer>
    </div>
  )
}

function LoginPublico({ onSuccess }) {
  const [aviso, setAviso] = useState('')
  const [procesando, setProcesando] = useState(false)

  async function enviarFormulario(evento) {
    evento.preventDefault()
    if (procesando) return
    const campos = new FormData(evento.currentTarget)
    const username = String(campos.get('usuario') || '')
    const password = String(campos.get('clave') || '')
    setProcesando(true)
    setAviso('')
    try {
      const usuario = await iniciarSesion(username, password)
      onSuccess(usuario)
    } catch (error) {
      setAviso(error.message || 'No fue posible iniciar sesión.')
    } finally {
      setProcesando(false)
    }
  }

  return (
    <div className="utm-login-pagina">
      <header className="utm-barra">
        <div className="utm-contenedor utm-barra-interior">
          <a className="utm-logo-enlace" href="#/" aria-label="Volver al inicio">
            <LogoUTM />
          </a>
          <a className="utm-volver" href="#/">← Volver al inicio</a>
        </div>
      </header>
      <main className="utm-login-centro">
        <div className="utm-login-tarjeta">
          <div className="utm-login-emblema" aria-hidden="true">✦</div>
          <span className="utm-etiqueta">PORTAL ESTUDIANTIL UTM</span>
          <h1>Bienvenido de nuevo</h1>
          <p className="utm-login-subtitulo">Ingresa con tu cuenta de demostración para acceder a tu espacio académico.</p>

          <form onSubmit={enviarFormulario} className="utm-login-formulario">
            <label htmlFor="utm-usuario">Usuario</label>
            <input id="utm-usuario" name="usuario" type="text" autoComplete="username" placeholder="Tu usuario de demostración" required disabled={procesando} />
            <label htmlFor="utm-clave">Contraseña</label>
            <input id="utm-clave" name="clave" type="password" autoComplete="current-password" placeholder="Ingresa tu contraseña" required disabled={procesando} />
            <button className="utm-boton utm-boton-amarillo utm-boton-ingresar" type="submit" disabled={procesando}>
              {procesando ? 'Verificando...' : 'Iniciar sesión'} <span aria-hidden="true">→</span>
            </button>
            {aviso && <p role="alert" className="utm-login-aviso">{aviso}</p>}
          </form>
        </div>
        <p className="utm-login-descargo">UTM ficticia · Acceso de demostración</p>
      </main>
    </div>
  )
}

export default function PublicSite({ Portal }) {
  const [ruta, setRuta] = useState(rutaActual)
  const [usuario, setUsuario] = useState(null)
  const [revisando, setRevisando] = useState(true)
  const [errorSesion, setErrorSesion] = useState('')

  useEffect(() => {
    const actualizar = () => setRuta(rutaActual())
    window.addEventListener('hashchange', actualizar)
    return () => window.removeEventListener('hashchange', actualizar)
  }, [])

  useEffect(() => {
    if (ruta !== '/portal') return
    let activo = true
    setRevisando(true)
    setErrorSesion('')
    consultarSesion()
      .then((datos) => {
        if (!activo) return
        setUsuario(datos)
        if (!datos) window.location.hash = '/login'
      })
      .catch((error) => {
        if (activo) setErrorSesion(error.message)
      })
      .finally(() => { if (activo) setRevisando(false) })
    return () => { activo = false }
  }, [ruta])

  async function salir() {
    try {
      await cerrarSesion()
      setUsuario(null)
      window.location.hash = '/login'
    } catch (error) {
      window.alert(error.message || 'No fue posible cerrar sesión.')
    }
  }

  function entrar(datos) {
    setUsuario(datos)
    window.location.hash = '/portal'
  }

  if (ruta === '/login') return <LoginPublico onSuccess={entrar} />
  if (ruta === '/portal') {
    if (revisando) return <p style={{ padding: '3rem' }}>Comprobando sesión...</p>
    if (errorSesion) return <p role="alert" style={{ padding: '3rem' }}>{errorSesion}</p>
    if (!usuario) return null
    return <Portal onLogout={salir} />
  }
  return <InicioPublico />
}
