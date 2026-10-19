import { useEffect, useRef, useState } from 'react'
import { sendMessage } from '../services/api'
import './ChatWidget.css'

const welcomeMessage = {
  id: 'welcome',
  role: 'assistant',
  content: '¡Hola! Soy AsisYou, tu asistente académico. ¿En qué puedo ayudarte hoy?',
}

const suggestions = [
  '¿Qué promedio llevo?',
  '¿Cuánto llevo de asistencia?',
  '¿Qué evaluaciones tengo pronto?',
]

function ChatWidget({ nombreEstudiante }) {
  const [isOpen, setIsOpen] = useState(false)
  const [isExpanded, setIsExpanded] = useState(false)
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([welcomeMessage])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const inputRef = useRef(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    if (isOpen) inputRef.current?.focus()
  }, [isOpen])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, isLoading])

  async function handleSubmit(event) {
    event.preventDefault()
    const trimmedMessage = message.trim()
    if (!trimmedMessage || isLoading) return

    setMessages((current) => [...current, {
      id: `${Date.now()}-user`,
      role: 'user',
      content: trimmedMessage,
    }])
    setMessage('')
    setError('')
    setIsLoading(true)

    try {
      const reply = await sendMessage(trimmedMessage)
      setMessages((current) => [...current, {
        id: `${Date.now()}-assistant`,
        role: 'assistant',
        content: reply,
      }])
    } catch (requestError) {
      setError(requestError.message || 'No pudimos conectar con AsisYou. Inténtalo nuevamente.')
    } finally {
      setIsLoading(false)
      inputRef.current?.focus()
    }
  }

  function useSuggestion(suggestion) {
    setMessage(suggestion)
    inputRef.current?.focus()
  }

  return (
    <>
      {!isOpen && (
        <button className="chat-launcher" type="button" onClick={() => setIsOpen(true)} aria-label="Abrir chat de AsisYou">
          <span className="launcher-sparkle">✦</span>
          <span className="launcher-label">¿Necesitas ayuda?</span>
          <span className="launcher-icon">☏</span>
        </button>
      )}

      {isOpen && (
        <section className={`chat-window ${isExpanded ? 'chat-window--expanded' : ''}`} aria-label="Asistente AsisYou">
          <header className="chat-header">
            <div className="chat-brand-icon">✦</div>
            <div className="chat-header-copy"><strong>AsisYou</strong><span><i /> Asistente académico</span></div>
            <div className="chat-header-actions">
              <button type="button" onClick={() => setIsExpanded((expanded) => !expanded)} aria-label={isExpanded ? 'Reducir chat' : 'Ampliar chat'} title={isExpanded ? 'Reducir' : 'Ampliar'}>{isExpanded ? '⤢' : '⛶'}</button>
              <button type="button" onClick={() => setIsOpen(false)} aria-label="Cerrar chat" title="Cerrar">×</button>
            </div>
          </header>

          <div className="chat-context"><span>✦</span> Tu compañero para la vida universitaria</div>

          <div className="chat-messages" aria-live="polite">
            <div className="chat-day-label">HOY</div>
            {messages.map((item) => (
              <div className={`message-row message-row--${item.role}`} key={item.id}>
                {item.role === 'assistant' && <span className="message-avatar">✦</span>}
                <div className="message-bubble">
                  <p>
                    {item.id === 'welcome' && nombreEstudiante
                      ? `¡Hola, ${nombreEstudiante}! Soy AsisYou, tu asistente académico. ¿En qué puedo ayudarte hoy?`
                      : item.content}
                  </p>
                  <span className="message-time">{item.role === 'assistant' ? 'AsisYou' : 'Tú'}</span>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message-row message-row--assistant">
                <span className="message-avatar">✦</span>
                <div className="message-bubble typing-bubble"><span /><span /><span /><small>AsisYou está pensando…</small></div>
              </div>
            )}
            {error && <div className="chat-error" role="alert"><strong>No se pudo enviar el mensaje.</strong><span>{error}</span><button type="button" onClick={() => setError('')}>Cerrar</button></div>}
            <div ref={messagesEndRef} />
          </div>

          {messages.length === 1 && !isLoading && (
            <div className="suggestions">
              <span>PUEDES PREGUNTARME</span>
              {suggestions.map((suggestion) => <button type="button" key={suggestion} onClick={() => useSuggestion(suggestion)}>{suggestion}<span>↗</span></button>)}
            </div>
          )}

          <form className="chat-composer" onSubmit={handleSubmit}>
            <label className="sr-only" htmlFor="asisyou-message">Escribe tu pregunta</label>
            <textarea
              id="asisyou-message"
              ref={inputRef}
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter' && !event.shiftKey) {
                  event.preventDefault()
                  event.currentTarget.form?.requestSubmit()
                }
              }}
              placeholder="Escribe tu pregunta..."
              rows={1}
              disabled={isLoading}
            />
            <button className="send-button" type="submit" disabled={!message.trim() || isLoading} aria-label="Enviar mensaje">↑</button>
            <div className="composer-footnote">AsisYou puede cometer errores. Verifica la información importante.</div>
          </form>
        </section>
      )}
    </>
  )
}

export default ChatWidget
