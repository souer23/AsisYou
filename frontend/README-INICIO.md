# AsisYou — primer frontend

## Qué incluye
- Dashboard inicial del portal estudiantil UTM.
- Navegación lateral adaptable.
- Widget de chat con abrir/cerrar y ampliar.
- Estados de carga y errores.
- Servicio independiente `src/services/api.js`.
- Modo simulado para trabajar mientras Django no esté disponible.

## Cómo aplicar
1. Haz una copia de seguridad de `src/App.jsx`, `src/App.css` y `src/index.css`.
2. Copia los archivos de esta carpeta a tu proyecto `frontend/`, respetando las rutas.
3. No reemplaces `src/main.jsx`; el que tienes actualmente puede quedarse igual.
4. Conserva tu `vite.config.js` actual. El proxy se configura después de revisar ese archivo y acordar el puerto de Django.
5. Ejecuta `npm run dev`.

## Modo simulado y modo real
- En `.env.development`, `VITE_USE_MOCK_API=true` usa una respuesta claramente identificada como simulada.
- Cuando Django esté listo, cambia a `VITE_USE_MOCK_API=false` y reinicia Vite.
- La petición real usa `POST /api/chat/`, envía `{ "message": "..." }` y espera `{ "reply": "..." }`.
- Para que `/api/chat/` llegue al servidor Django durante el desarrollo, debe existir una regla proxy en `vite.config.js`. No se incluyó una regla con un puerto inventado.

## Importante
Las notas, asistencia, evaluaciones y nombre de estudiante de esta pantalla son datos de demostración, no datos reales.
