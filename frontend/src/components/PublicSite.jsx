import { useEffect, useState } from 'react'
import { iniciarSesion, consultarSesion, cerrarSesion } from '../services/auth'
import imagenUTMs from '../assets/logo-utm.png'
import frontUTM from '../assets/FrontUTMS.jpg'
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
        <img 
          src={imagenUTMs} 
          alt="" 
          style={{ width: '100%', height: '100%', objectFit: 'contain' }} 
        />
      </span>
      <span className="utm-identidad-texto">
        <strong>UTM</strong>
        <small>Universidad Tecnológica del Maule</small>
      </span>
    </span>
  );
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
            <img src={frontUTM} alt="Imagen de presentación del campus universitario UTM" />
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

  // 1. Comprueba la sesión al iniciar, sin importar en qué ruta esté
  useEffect(() => {
    let activo = true
    consultarSesion()
      .then((datos) => {
        if (!activo) return
        setUsuario(datos)
        if (datos && ruta !== '/portal') {
          window.location.replace('#/portal')
        } else if (!datos && ruta === '/portal') {
          window.location.replace('#/login')
        }
      })
      .catch((error) => {
        if (activo) setErrorSesion(error.message)
      })
      .finally(() => {
        if (activo) setRevisando(false)
      })
    return () => { activo = false }
  }, [])

  // 2. Bloquea el botón "Atrás" o cambios manuales en la URL según el estado de sesión
  useEffect(() => {
    if (revisando) return

    if (usuario && ruta !== '/portal') {
      // Si está logueado e intenta ir a inicio o login, lo devuelve al portal
      window.location.replace('#/portal')
    } else if (!usuario && ruta === '/portal') {
      // Si no está logueado e intenta entrar al portal, lo manda al login
      window.location.replace('#/login')
    }
  }, [ruta, usuario, revisando])

  async function salir() {
    try {
      await cerrarSesion()
      setUsuario(null)
      window.location.replace('#/login')
    } catch (error) {
      window.alert(error.message || 'No fue posible cerrar sesión.')
    }
  }

  function entrar(datos) {
    setUsuario(datos)
    window.location.replace('#/portal')
  }

  // Mientras verifica con Django si hay cookie activa, no muestra pantallas falsas
  if (revisando) return <p style={{ padding: '3rem' }}>Comprobando sesión...</p>
  if (errorSesion) return <p role="alert" style={{ padding: '3rem' }}>{errorSesion}</p>

  // Si ya hay usuario logueado, siempre renderiza el Portal
  if (usuario) {
    return <Portal onLogout={salir} />
  }

  // Si NO hay usuario logueado, muestra Login o Inicio público
  if (ruta === '/login') return <LoginPublico onSuccess={entrar} />
  return <InicioPublico />
}