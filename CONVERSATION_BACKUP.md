# GP Trading - Historial de Desarrollo

## Resumen del Proyecto
Landing page premium para GP Trading (NinjaTrader 8 suite) con catálogo de productos, carrusel de videos, precios, contacto y páginas legales. Optimizada para mobile-first y conversión vía WhatsApp.

## Stack Técnico
- **Framework:** Astro 4.5
- **CSS:** Tailwind CSS 3.4
- **Hosting:** Cloudflare Pages (`https://gp-trading.pages.dev`)
- **Idioma:** Español

## Preferencias del Cliente
- Tema dark profesional (#0a0a0a base, #00d4aa accent, #f59e0b gold)
- Sin garantías ni warranties mencionados
- Sin Facebook/Snapchat
- "Comprar Ahora" → WhatsApp `https://wa.link/rzdnzn`
- Social: Instagram, Discord, YouTube, Telegram
- Email: `gptradingacademy@proton.me`
- YouTube bg video Hero: `https://youtu.be/YzwUEKikqtg`
- Cada indicador necesita su precio individual
- Los videos del carrusel NO deben mostrar branding de YouTube
- Los videos NO se pueden pausar
- Los videos empiezan desde cero cada vez que se visita el slide
- Los videos avanzan automáticamente al siguiente slide al terminar

---

## Videos Configurados en Carrusel

| # | Slide ID | Producto | Video YouTube ID | Duración |
|---|---|---|---|---|
| 4 | `gflowx` | OmniFlow GFlow X | `KDofJ-ADrJo` | 69s |
| 6 | `gflowpro` | GFlow Pro Premium | `Mce88WjenQM` | 69s |
| 7 | `vpwap` | GP VWAP Clásico | `4ncuwWvAPJ0` | 69s |
| 10 | `gpcuantum` | GPCuantum X | `4g_3zghj2lA` | 69s |

**Slides 1, 2, 3, 5, 8, 9:** Sin video (placeholder SVG) — duración 8 segundos cada uno.

---

## Sistema de Videos del Carrusel

### Configuración por producto (VideoCarousel.astro)
Cada producto tiene campos:
```javascript
{
  id: 'gflowpro',
  video: 'Mce88WjenQM',    // ID del video de YouTube
  duration: 69               // Duración en segundos
}
```

### Cómo funciona el sistema de video

1. **Iframe YouTube** con parámetros restrictivos:
   - `autoplay=1&mute=1` — reproduce automático en mute (requerido para autoplay en navegadores)
   - `controls=0` — sin controles de YouTube
   - `showinfo=0` — sin info del video
   - `modestbranding=1` — logo mínimo
   - `disablekb=1` — sin atajos de teclado
   - `iv_load_policy=3` — sin anotaciones
   - `rel=0` — sin videos relacionados
   - `enablejsapi=1` — habilita API para detectar fin del video
   - `_t={timestamp}` — fuerza recarga desde cero

2. **Video Blocker** (`div.video-blocker`):
   - Cubre el iframe completamente
   - `pointer-events: all !important` — bloquea todos los touches/clicks
   - `z-index: 9999 !important` — siempre encima del iframe
   - Fondo transparente (se ve el video pero no se puede interactuar)
   - Nunca se desvanece — permanece activo todo el tiempo
   - Al salir del slide → se vuelve opaco (`background: #0a0a0a`)

3. **Reproducción desde cero**:
   - Al entrar al slide: `iframe.src = ''` (limpia) luego `iframe.src = '...'&_t={timestamp}'` (recarga)
   - Al salir del slide: `iframe.src = ''` (detiene completamente)

4. **Avance automático al terminar**:
   - Listener de `window.addEventListener('message')` detecta YouTube `playerState === 0` (ended)
   - Ejecuta `next()` para avanzar al siguiente slide
   - Timer de respaldo también avanza después de `duration` segundos

5. **Control por slide**:
   - Cada slide tiene `data-duration` con su duración en segundos
   - El timer de autoplay usa la duración del slide actual
   - Al cambiar de slide → se reinicia el timer con la nueva duración

### Funciones JS clave
```javascript
// Detener video al salir del slide
function stopVideo(slide) {
  iframe.src = '';           // Detiene reproducción
  blocker.style.background = '#0a0a0a';  // Bloquea visualmente
}

// Iniciar video al entrar al slide
function startVideo(slide) {
  blocker.style.background = 'transparent';  // Muestra video
  iframe.src = '...&_t=' + Date.now();       // Recarga desde cero
}

// Detectar fin del video
window.addEventListener('message', function(e) {
  // YouTube envía playerState === 0 cuando termina
  if (data.event === 'infoDelivery' && data.info.playerState === 0) {
    next();  // Avanza al siguiente slide
  }
});
```

---

## Cambios Realizados

### Carrusel de Videos
- **Bolitas animadas**: Se iluminan en accent con glow al estar activas
- **Auto-scroll corregido**: Autoplay no hace scroll, solo interacción del usuario
- **Touch states**: Feedback visual en mobile para glass-card y links
- **Flechas responsivas**: Más pequeñas y transparentes en móvil (`w-8 h-8 bg-black/40`)
- **Video blocker**: Bloquea interacción completa con el iframe de YouTube
- **Duración por slide**: Cada slide tiene su propio temporizador

### Productos y Precios
- **10 enlaces "Ver precios" corregidos**: Cada uno apunta a su ID correcto en Pricing
- **10 enlaces "Ver detalle" corregidos**: Apuntan a slides correctos del carrusel
- **GP VWAP link corregido**: `#detalle-vwap` → `#detalle-vpwap`

### Touch States para Móvil
- Removidas clases inline redundantes de articles
- `.glass-card:active` con transición `0.15s` en mobile
- `.glass-card a:active` con `opacity: 0.7` y `scale(0.97)`
- `touch-action: manipulation` en links de acción

### Menú Móvil
- Links más grandes (`py-3` + `touch-manipulation`)
- `aria-expanded` en botón hamburger
- Menú se cierra al tocar cualquier link

### Seguridad Estricta
- **`_headers`**: X-Frame-Options DENY, X-Content-Type-Options nosniff, HSTS, CSP, COOP, CORP, Permissions-Policy
- **`robots.txt`**: Bloquea rutas sensibles
- **`security.txt`**: Contacto para vulnerabilidades
- **Meta tags**: CSP, X-Frame-Options, X-XSS-Protection, Referrer-Policy

### CSS Accessibility
- `prefers-reduced-motion` desactiva animaciones
- `.skip-link` para navegación por teclado
- `.focus-visible-ring` con outline accent
- ARIA roles en carrusel

---

## Mapeo de IDs

### ProductsSection → VideoCarousel (Ver detalle)
| Producto | Link Ver detalle | Slide ID |
|---|---|---|
| TradeSyncer PRO | `#detalle-tradesyncer` | `tradesyncer` |
| GP Firm Copier | `#detalle-firmcopier` | `firmcopier` |
| RiskRewardSniper | `#detalle-riskreward` | `riskreward` |
| OmniFlow GFlow X | `#detalle-gflowx` | `gflowx` |
| Quantum Prime | `#detalle-quantumprime` | `quantumprime` |
| GFlow Pro | `#detalle-gflowpro` | `gflowpro` |
| GP VWAP | `#detalle-vpwap` | `vpwap` |
| Nexus Trend | `#detalle-nexus` | `nexus` |
| Specter Cloud | `#detalle-specter` | `specter` |
| GPCuantum X | `#detalle-gpcuantum` | `gpcuantum` |

### ProductsSection → Pricing (Ver precios)
| Producto | Link Ver precios | Precio ID |
|---|---|---|
| TradeSyncer PRO | `#precio-tradesyncer` | `precio-tradesyncer` |
| GP Firm Copier | `#precio-firmcopier` | `precio-firmcopier` |
| RiskRewardSniper | `#precio-riskreward` | `precio-riskreward` |
| OmniFlow GFlow X | `#precio-gflowx` | `precio-gflowx` |
| Quantum Prime | `#precio-quantumprime` | `precio-quantumprime` |
| GFlow Pro | `#precio-gflowpro` | `precio-gflowpro` |
| GP VWAP | `#precio-vwap` | `precio-vwap` |
| Nexus Trend | `#precio-nexus` | `precio-nexus` |
| Specter Cloud | `#precio-specter` | `precio-specter` |
| GPCuantum X | `#precio-gpcuantum` | `precio-gpcuantum` |

---

## Estructura de Archivos
```
gp-trading-site/
├── public/
│   ├── logo.svg
│   ├── _headers                    # Security headers (Cloudflare Pages)
│   ├── robots.txt
│   └── .well-known/security.txt
├── src/
│   ├── components/
│   │   ├── Header.astro            # Nav + menú móvil
│   │   ├── Hero.astro              # Hero con video YouTube bg
│   │   ├── VideoCarousel.astro     # Carrusel con videos embebidos
│   │   ├── ProductsSection.astro   # 10 productos con precios
│   │   ├── Pricing.astro           # Sección de precios individuales
│   │   └── Footer.astro            # Footer con social links
│   ├── layouts/Layout.astro        # HTML head + meta tags seguridad
│   ├── pages/
│   │   ├── index.astro             # Página principal
│   │   ├── privacidad.astro        # Política de privacidad
│   │   └── riesgos.astro           # Aviso de riesgos trading
│   └── styles/global.css           # Animaciones, video-blocker, glass-card
├── astro.config.mjs                # Static output, site URL
├── package.json                    # Astro 4.5, Tailwind 3.4
├── wrangler.toml                   # Cloudflare Pages config
└── CONVERSATION_BACKUP.md          # Este archivo
```

## Pendiente
- [ ] Grabar videos para los 6 slides restantes (tradesyncer, firmcopier, riskreward, quantumprime, nexus, specter)
- [ ] Agregar campo `video` y `duration` a cada producto faltante
- [ ] Deploy final a Cloudflare Pages (`npm run deploy`)

## Comandos Útiles
- `npm run dev` — servidor local en `localhost:4321`
- `npm run build` — verificar build
- `npm run deploy` — deploy a Cloudflare Pages
- `ipconfig getifaddr en0` — obtener IP local para acceso desde celular
- Servidor accesible desde celular: `http://TU_IP:4321`
