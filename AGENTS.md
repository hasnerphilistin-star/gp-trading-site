# GP Trading Site — Contexto para el agente

## Stack
- Astro + Tailwind CSS, desplegado en Cloudflare Pages
- Sitio: https://gptradingfx.pages.dev
- GitHub: https://github.com/hasnerphilistin-star/gp-trading-site

## Blog - Sistema de Publicación Automática
- **23 artículos publicados** en `src/pages/blog/`
- **120 drafts totales** en `drafts/` (día 1→120) con prefijo numérico
  - 30 existentes (día 1-30) — empiezan a publicarse el 1 Jul 2026
  - 90 nuevos (día 31-120) — generados el 30 Jun 2026
- `src/data/schedule.json` — plan de 120 artículos con campo `published`
- `src/data/published.json` — artículos ya publicados (con `views`)
- `scripts/publish-today.cjs` — mueve 1 draft/día, actualiza JSON, commit + push (`.cjs` por `"type": "module"` en package.json)
- `.github/workflows/daily-publish.yml` — GitHub Action cron 8am UTC
- **Alternancia**: Herramientas ↔ Educación, con Ventaja Estadística intercalado
- Categorías: "Herramientas", "Educación", "Ventaja Estadística"

## Home (index.astro)
- Sección "Últimos del Blog": data-driven desde `published.json`
  - Muestra el **más visto** (mayor `views`) + los **2 más recientes** (por fecha)
- Productos, combos, videos, FAQ — todo importado desde componentes

## Blog (blog/index.astro)
- Ordenado por **fecha descendente** (más reciente primero)
- Filtros por categoría (Todos, Herramientas, Educación, Ventaja Estadística)

## Productos (11)
1. TradeSyncer PRO v2.0 — `tradesyncer-pro-v2-guia-completa` ✓
2. GP Firm Copier Pro — `gp-firm-copier-pro-guia` ✓
3. GPRiskReward — `gpriskreward-guia-completa` ✓
4. OmniFlow GFlow PRO v2.0 — `omniflow-gflow-pro-v2-guia-completa` ✓
5. OmniFlow GFlow X — `omniflow-gflow-x-guia` ✓
6. OmniFlow Quantum Prime — `omniflow-quantum-prime-guia` ✓
7. GFlow Pro Premium — `gflow-pro-premium-guia` ✓
8. GP VWAP Clásico — `gp-vwap-clasico-guia` ✓
9. Nexus Trend Engine — `nexus-trend-engine-guia` ✓
10. Specter Trend Cloud — `specter-trend-cloud-guia` ✓
11. GPCuantum X — `gpcuantum-x-guia` ✓

## Seguridad
- `public/_headers`: HSTS (1 año), Permissions-Policy (sin cámara/mic/geo), X-Frame-Options: DENY, X-Content-Type-Options: nosniff, Referrer-Policy
- CSP en Layout.astro: solo self, YouTube, Google Fonts
- e.origin validado en postMessage de YouTube
- Sin formularios, sin base de datos, sin servidor (sitio 100% estático)

## SEO
- Google Search Console verificado (meta tag + archivo HTML)
- Sitemap: `sitemap-index.xml` (29 URLs, TEMPLATE excluido)
- robots.txt configurado
- OG tags, canonical, JSON-LD Organization Schema
- **Sitio aún no indexado** — Google tardará 1-2 días
- Google Analytics / Cloudflare Web Analytics: pendiente de configuración

## Build & Deploy
```bash
npm run build
# Auto-deploy via GitHub → Cloudflare Pages (puede fallar, tener token a mano)
# Manual:
CLOUDFLARE_API_TOKEN="<token>" CLOUDFLARE_ACCOUNT_ID="ef1bfef4d6dce5b041f0de5bc1505f84" npx wrangler pages deploy dist --project-name=gptradingfx --branch=main
```

## Cuenta Cloudflare
- Account ID: `ef1bfef4d6dce5b041f0de5bc1505f84`
- Proyecto: `gptradingfx`
- Token: preguntar al usuario (no guardar)

## Estilo de artículos
- Tono: profesional pero accesible, en español
- Keywords: Order Flow, NinjaTrader 8, prop firms, SMC, liquidez, volumen
- Estructura: intro, secciones con h2, subsecciones con h3, listas, CTA al final
- Cada artículo debe conectar con una herramienta de GP Trading al final
- Los artículos de producto siempre enlazan a `/#detalle-{productId}`

## Preferencias del usuario
- Dark theme (#0a0a0a, #00d4aa accent, #f59e0b gold)
- Sin garantías/warranties
- WhatsApp: https://wa.link/rzdnzn
- Soporte vía Discord
- Videos de YouTube sin branding, auto-avance
- Alternar producto/educativo en nueva tanda de artículos

## Historial de sesiones
### 30 Jun 2026 — Sesión masiva
- **90 artículos nuevos** generados (día 31→120) con script `scripts/generate-90-articles.cjs`
- Home ahora data-driven: muestra más visto + 2 últimos artículos
- Blog ordenado por fecha descendente
- FAQ: añadidos Header + Footer
- Seguridad: HSTS, Permissions-Policy, _headers file
- Google Search Console: verificación completada, sitemap enviado
- Build: 30 páginas, 0 errores
- Deploy manual necesario (auto-deploy de GitHub inestable)

### 30 Jun 2026 — Fix scroll + highlight "Ver precios"
- Bug: clic en "Ver precios" no siempre scrolleaba ni animaba el precio correcto
- Causa: event listener genérico en `document` con `closest('[data-precio]')` interfería con otros handlers del carrusel
- Fix: cada link ahora usa `onclick="goToPrice('producto');return false;"` y la función global `window.goToPrice` definida en Pricing.astro
- `data-precio` eliminado de los links; ya no es necesario
- Deploy manual exitoso a Cloudflare Pages

### 30 Jun 2026 — Plan de protección de código + licencias NT8
- PDF generado: `~/Downloads/Plan_Proteccion_Codigo_Licencias_GP_Trading.pdf` (17 págs, 98 KB)
- Ofuscación con **ConfuserEx** (gratuito, open source) con reglas de preservación para NT8
- Sistema de **License Key único** por indicador: `SHA256(NT8 Account ID + Product ID + SecretSalt)`
- Formato: `GPTR-XXXXX-XXXXX-XXXXX-XXXXX`, almacenado en `...\NinjaTrader 8\bin\Custom\Licenses\<product>.lic`
- Cada DLL valida la licencia al cargar vs el Account ID de NT8; si falla, no dibuja nada
- Tool interna de generación (console app) + BD SQLite de auditoría para prevenir duplicados
- Proceso manual de 6-12h: pago → alerta Discord → generar licencia → email al cliente con DLL + .lic
- Plan a futuro: automatizar con Binance Pay + Cloudflare Worker + Phone Home opcional

### 1 Jul 2026 — Sistema completo de protección y licencias
- **`security/`** — Nuevo directorio con el sistema de licencias completo
- `security/LicenseValidatorTemplate.cs` — Template C# para integrar en cada DLL:
  - Validación offline contra archivo `.lic` en `...\Licenses\<product>.lic`
  - **3 días de prueba** automáticos al primer uso (crea archivo `.trial`)
  - Banner "Prueba: X días restantes" en gold (arriba derecha) durante el trial
  - Pantalla de bloqueo centrada con logo GP Trading, mensaje de contacto,
    email, Discord, Instagram, Telegram, YouTube (sin WhatsApp)
  - Colores corporativos: accent `#00d4aa`, gold `#f59e0b`, bg `#0a0a0a`
- `security/license-generator.html` — Página web admin para generar licencias:
  - Interfaz profesional dark con glassmorphism, animaciones, stats
  - Dropdown de los 11 productos, inputs para Account ID, email, nombre
  - Genera License Key con SHA-256, animación de caracteres
  - Copia al portapapeles, descarga `.lic`, historial persistente (localStorage)
  - Footer con todas las redes sociales (sin WhatsApp)
- `security/confuserex-config.crproj` — Config de ConfuserEx con reglas de preservación NT8:
  - Renaming, Control Flow, Constants/strings encryption, Anti Debug, Anti Tamper, Ref Proxy
  - Preserva: clase Indicator, OnStateChange, OnBarUpdate, OnRender, propiedades, atributos
  - Preserva LicenseValidator para no romper instanciación
- `security/gen-license.py` — Script CLI Python:
  - `--account`, `--product`, `--email`, `--name`, `--list`, `--revoke`
  - Guarda en SQLite (`licencias.db`), genera archivo `.lic`
  - Modo --no-save para solo mostrar
  - Variable de entorno `GPT_LICENSE_SECRET` para el master secret
- `security/license-db-schema.sql` — Esquema SQLite con tablas `licencias` y `orders`
- `security/README.md` — Guía completa de integración paso a paso
- **Flujo**: DLL sin licencia → 3 días trial → pantalla de bloqueo con branding → contacto
- **Master secret** reemplazable en cada DLL compilada; nunca va en código cliente
