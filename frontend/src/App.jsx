import { useEffect, useState } from 'react'
import ChatWidget from './components/ChatWidget'
import { obtenerPerfil } from './services/api'
import './App.css'

const MESES = [
  'ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN',
  'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'
]

const navItems = [
  { id: 'inicio', label: 'Inicio', icon: '⌂' },
  { id: 'asignaturas', label: 'Asignaturas', icon: '▤' },
  { id: 'notas', label: 'Mis notas', icon: '▧' },
  { id: 'asistencia', label: 'Asistencia', icon: '✓' },
  { id: 'evaluaciones', label: 'Evaluaciones', icon: '▦' },
  { id: 'avisos', label: 'Avisos', icon: '♧' },
]

function App() {
  const [activeNav, setActiveNav] = useState('inicio')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [perfil, setPerfil] = useState(null)
  const [errorPerfil, setErrorPerfil] = useState('')

  useEffect(() => {
    let activo = true

    obtenerPerfil()
      .then((datos) => {
        if (activo) setPerfil(datos)
      })
      .catch((error) => {
        if (activo) setErrorPerfil(error.message)
      })

    return () => {
      activo = false
    }
  }, [])

  const asignaturas = perfil?.asignaturas ?? []
  const proximasActividades = perfil?.proximas_actividades ?? []

  const asignaturasDestacadas = [...asignaturas]
    .sort((a, b) => {
      const notaA = a.promedio === null
        ? Infinity : Number(a.promedio.replace(',', '.'))

      const notaB = b.promedio === null
        ? Infinity : Number(b.promedio.replace(',', '.'))

      return notaA - notaB
    })
    .slice(0, 3)

  const primerNombre = perfil?.nombre?.split(' ')[0] ?? 'estudiante'

  const activeLabel = navItems.find((item) => item.id === activeNav)?.label ?? 'Inicio'

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? 'sidebar--open' : ''}`}>
        <a className="brand" href="#inicio" onClick={() => setActiveNav('inicio')}>
          <span className="brand-mark">A</span>
          <span className="brand-copy">
            <strong>UTM</strong>
            <small>Universidad Tecnológica<br />del Maule</small>
          </span>
        </a>

        <div className="sidebar-label">PORTAL ESTUDIANTIL</div>
        <nav className="main-nav" aria-label="Navegación principal">
          {navItems.map((item) => (
            <button
              className={`nav-item ${activeNav === item.id ? 'nav-item--active' : ''}`}
              key={item.id}
              onClick={() => {
                setActiveNav(item.id)
                setSidebarOpen(false)
              }}
              type="button"
            >
              <span className="nav-icon" aria-hidden="true">{item.icon}</span>
              <span>{item.label}</span>
              {item.id === 'avisos' && <span className="nav-dot" aria-label="Nuevo aviso" />}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="help-card">
            <span className="help-card-icon">✦</span>
            <strong>¿Necesitas ayuda?</strong>
            <p>AsisYou puede ayudarte con tus dudas académicas.</p>
            <span className="help-card-hint">Abre el asistente ↘</span>
          </div>
          <div className="sidebar-footer">© 2026 UTM · Portal de demostración</div>
        </div>
      </aside>

      {sidebarOpen && <button className="sidebar-backdrop" aria-label="Cerrar menú" onClick={() => setSidebarOpen(false)} />}

      <main className="main-area">
        <header className="topbar">
          <button className="mobile-menu" type="button" aria-label="Abrir menú" onClick={() => setSidebarOpen((open) => !open)}>☰</button>
          <div className="breadcrumb"><span>Portal estudiantil</span><span className="breadcrumb-separator">/</span><strong>{activeLabel}</strong></div>
          <div className="topbar-actions">
            <button className="icon-button notification-button" aria-label="Notificaciones" type="button">
              ♧<span className="notification-dot" />
            </button>
            <div className="profile">
              <div className="avatar">{perfil?.iniciales ?? '—'}</div>
              <div className="profile-copy"><strong>{perfil?.nombre ?? 'Cargando perfil...'}</strong><span>Estudiante</span></div>
              <span className="profile-chevron">⌄</span>
            </div>
          </div>
        </header>

        <div className="page-content">
          {activeNav === 'inicio' ? (
            <>
              <section className="welcome-row">
                <div>
                  <div className="eyebrow"><span className="eyebrow-line" /> MI ESPACIO ACADÉMICO</div>
                  <h1>¡Hola, {primerNombre}! <span className="wave">✦</span></h1>
                  <p className="welcome-subtitle">Aquí tienes un resumen de tu actividad académica.</p>
                </div>
                <div className="semester-pill"><span /> Segundo semestre 2026</div>
              </section>

              <section className="summary-grid" aria-label="Resumen académico">
                <article className="summary-card">
                  <div className="summary-card-top">
                    <span className="summary-icon summary-icon--yellow">▧</span>
                    <span className="card-overline">PROMEDIO ACTUAL</span>
                  </div>

                  <div className="summary-value">
                    {perfil?.promedio_general ?? '—'}
                  </div>

                  <div className="summary-foot">
                    Media referencial de asignaturas con notas
                  </div>
                </article>

                <article className="summary-card">
                  <div className="summary-card-top">
                    <span className="summary-icon summary-icon--green">✓</span>
                    <span className="card-overline">ASISTENCIA REGISTRADA</span>
                  </div>

                  <div className="summary-value">
                    {perfil?.asistencia_general ?? '—'}
                  </div>

                  <div className="summary-foot">
                    Considera las secciones con asistencia registrada
                  </div>
                </article>

                <article className="summary-card">
                  <div className="summary-card-top">
                    <span className="summary-icon summary-icon--blue">▦</span>
                    <span className="card-overline">ASIGNATURAS</span>
                  </div>

                  <div className="summary-value">
                    {perfil?.total_asignaturas ?? '—'}
                    <span className="summary-unit summary-unit--label">
                      {' '}inscritas
                    </span>
                  </div>

                  <div className="summary-foot">
                    {perfil?.carrera ?? 'Perfil académico de demostración'}
                  </div>
                </article>
              </section>

              <section className="content-grid">
                <div className="panel subjects-panel">
                  <div className="panel-heading">
                    <div><h2>Asignaturas para revisar</h2><p>Ordenadas por promedio actual</p></div>
                    <button className="text-button" onClick={() => setActiveNav('asignaturas')} type="button">Ver todas <span>→</span></button>
                  </div>
                  <div className="subject-list">
                    {asignaturasDestacadas.map((subject, index) => (
                      <article className="subject-row" key={subject.codigo}>
                        <div className={`subject-symbol subject-symbol--${index % 2 === 0 ? 'yellow' : 'blue'
                          }`}>
                          {subject.nombre.slice(0, 1)}
                        </div>

                        <div className="subject-info">
                          <strong>{subject.nombre}</strong>
                          <span>
                            {subject.codigo} · Sección {subject.seccion}
                          </span>
                        </div>

                        <div className="subject-grade">
                          <strong>{subject.promedio ?? '—'}</strong>
                          <span>Promedio actual</span>
                        </div>
                      </article>
                    ))}
                  </div>
                  <div className="demo-note">
                    <span>i</span>
                    Datos académicos ficticios obtenidos desde PostgreSQL.
                  </div>
                </div>

                <div className="panel upcoming-panel">
                  <div className="panel-heading">
                    <div><h2>Próximas actividades</h2><p>Organiza tus pendientes</p></div>
                    <button className="more-button" aria-label="Más opciones" type="button">···</button>
                  </div>
                  <div className="activity-list">
                    {proximasActividades.length === 0 ? (
                      <p>No tienes próximas evaluaciones pendientes.</p>
                    ) : (
                      proximasActividades.map((actividad) => (
                        <article
                          className="activity-row"
                          key={`${actividad.asignatura}-${actividad.titulo}-${actividad.fecha}`}
                        >
                          <div className="date-tile">
                            <strong>
                              {Number(actividad.fecha.slice(8, 10))}
                            </strong>
                            <span>
                              {MESES[Number(actividad.fecha.slice(5, 7)) - 1]}
                            </span>
                          </div>

                          <div className="activity-info">
                            <strong>{actividad.titulo}</strong>
                            <span>{actividad.asignatura}</span>
                            <small>{actividad.tipo}</small>
                          </div>
                        </article>
                      ))
                    )}
                  </div>
                  <button className="activity-footer" type="button" onClick={() => setActiveNav('evaluaciones')}>Ver calendario completo <span>→</span></button>
                </div>
              </section>

              <section className="assistant-banner">
                <div className="assistant-banner-mark">✦</div>
                <div className="assistant-banner-copy"><span>CONOCE A TU ASISTENTE</span><h2>Tu vida académica, más simple.</h2><p>Pregúntale a AsisYou sobre notas, asistencia, evaluaciones y reglamentos.</p></div>
                <div className="assistant-banner-tip">Prueba preguntando<br /><strong>“¿Qué nota necesito para aprobar?”</strong></div>
              </section>
            </>
          ) : activeNav === 'asignaturas' ? (
            <section className="panel" style={{ paddingBottom: 20 }}>
              <div className="panel-heading">
                <div>
                  <h2>Mis asignaturas</h2>
                  <p>Asignaturas inscritas durante el período académico</p>
                </div>
              </div>

              <div className="subject-list">
                {asignaturas.length === 0 ? (
                  <p>No hay asignaturas disponibles.</p>
                ) : (
                  asignaturas.map((subject, index) => (
                    <article
                      className="subject-row"
                      key={`${subject.codigo}-${subject.seccion}`}
                    >
                      <div
                        className={`subject-symbol subject-symbol--${index % 2 === 0 ? 'yellow' : 'blue'
                          }`}
                      >
                        {subject.nombre.charAt(0)}
                      </div>

                      <div className="subject-info">
                        <strong>{subject.nombre}</strong>
                        <span>
                          {subject.codigo} · Sección {subject.seccion}
                        </span>
                        <span>
                          Asistencia: {subject.asistencia ?? 'No disponible'}
                        </span>
                      </div>

                      <div className="subject-grade">
                        <strong>{subject.promedio ?? '—'}</strong>
                        <span>Promedio actual</span>
                      </div>
                    </article>
                  ))
                )}
              </div>
            </section>
          ) : (
            <section className="placeholder-page">
              <div className="placeholder-icon">▤</div>
              <span className="eyebrow">PORTAL ESTUDIANTIL</span>
              <h1>{activeLabel}</h1>
              <p>Esta sección se habilitará en una siguiente etapa del proyecto.</p>
              <div className="placeholder-note">Por ahora, los datos académicos del inicio son ilustrativos. Puedes utilizar AsisYou para probar la experiencia del asistente.</div>
              <button className="primary-button" onClick={() => setActiveNav('inicio')} type="button">Volver al inicio</button>
            </section>
          )}
        </div>
      </main>
      <ChatWidget nombreEstudiante={perfil ? primerNombre : null} />
    </div>
  )
}

export default App
