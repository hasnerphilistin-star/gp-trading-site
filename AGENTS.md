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
- `scripts/publish-today.js` — mueve 1 draft/día, actualiza JSON, commit + push
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
