import { useState } from 'react'
import ChatWidget from './components/ChatWidget'
import './App.css'

const subjects = [
  { code: 'INF-302', name: 'Bases de Datos', teacher: 'Prof. Marcela Soto', grade: '5,6', progress: 76, color: 'yellow' },
  { code: 'INF-305', name: 'Ingeniería de Software', teacher: 'Prof. Rodrigo Pérez', grade: '6,1', progress: 88, color: 'blue' },
  { code: 'MAT-204', name: 'Estadística', teacher: 'Prof. Camila Rojas', grade: '4,9', progress: 64, color: 'green' },
]

const upcoming = [
  { day: '16', month: 'OCT', title: 'Control de Bases de Datos', subject: 'Bases de Datos', type: 'Evaluación' },
  { day: '20', month: 'OCT', title: 'Entrega proyecto grupal', subject: 'Ingeniería de Software', type: 'Entrega' },
  { day: '23', month: 'OCT', title: 'Prueba unidad 2', subject: 'Estadística', type: 'Evaluación' },
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
              <div className="avatar">GP</div>
              <div className="profile-copy"><strong>Gonzalo Peredo</strong><span>Estudiante</span></div>
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
                  <h1>¡Hola, Gonzalo! <span className="wave">✦</span></h1>
                  <p className="welcome-subtitle">Aquí tienes un resumen de tu actividad académica.</p>
                </div>
                <div className="semester-pill"><span /> Segundo semestre 2026</div>
              </section>

              <section className="summary-grid" aria-label="Resumen académico">
                <article className="summary-card">
                  <div className="summary-card-top"><span className="summary-icon summary-icon--yellow">▧</span><span className="card-overline">PROMEDIO GENERAL</span></div>
                  <div className="summary-value">5,5 <span className="value-trend">↗</span></div>
                  <div className="summary-foot">Escala de notas de 1,0 a 7,0</div>
                </article>
                <article className="summary-card">
                  <div className="summary-card-top"><span className="summary-icon summary-icon--green">✓</span><span className="card-overline">ASISTENCIA</span></div>
                  <div className="summary-value">87<span className="summary-unit">%</span></div>
                  <div className="progress-track"><span style={{ width: '87%' }} /></div>
                  <div className="summary-foot">Vas por buen camino</div>
                </article>
                <article className="summary-card">
                  <div className="summary-card-top"><span className="summary-icon summary-icon--blue">▦</span><span className="card-overline">ASIGNATURAS</span></div>
                  <div className="summary-value">5 <span className="summary-unit summary-unit--label">inscritas</span></div>
                  <div className="summary-foot">3 con actividad próxima</div>
                </article>
              </section>

              <section className="content-grid">
                <div className="panel subjects-panel">
                  <div className="panel-heading">
                    <div><h2>Mis asignaturas</h2><p>Un vistazo a tu semestre</p></div>
                    <button className="text-button" onClick={() => setActiveNav('asignaturas')} type="button">Ver todas <span>→</span></button>
                  </div>
                  <div className="subject-list">
                    {subjects.map((subject) => (
                      <article className="subject-row" key={subject.code}>
                        <div className={`subject-symbol subject-symbol--${subject.color}`}>{subject.name.slice(0, 1)}</div>
                        <div className="subject-info"><strong>{subject.name}</strong><span>{subject.code} · {subject.teacher}</span><div className="subject-progress"><span style={{ width: `${subject.progress}%` }} /></div></div>
                        <div className="subject-grade"><strong>{subject.grade}</strong><span>Promedio</span></div>
                      </article>
                    ))}
                  </div>
                  <div className="demo-note"><span>i</span> Datos ilustrativos para la demostración del frontend.</div>
                </div>

                <div className="panel upcoming-panel">
                  <div className="panel-heading">
                    <div><h2>Próximas actividades</h2><p>Organiza tus pendientes</p></div>
                    <button className="more-button" aria-label="Más opciones" type="button">···</button>
                  </div>
                  <div className="activity-list">
                    {upcoming.map((activity) => (
                      <article className="activity-row" key={activity.title}>
                        <div className="date-tile"><strong>{activity.day}</strong><span>{activity.month}</span></div>
                        <div className="activity-info"><strong>{activity.title}</strong><span>{activity.subject}</span><small>{activity.type}</small></div>
                      </article>
                    ))}
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
      <ChatWidget />
    </div>
  )
}

export default App
