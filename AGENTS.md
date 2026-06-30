# GP Trading Site — Contexto para el agente

## Stack
- Astro + Tailwind CSS, desplegado en Cloudflare Pages
- Sitio: https://gptradingfx.pages.dev
- GitHub: https://github.com/hasnerphilistin-star/gp-trading-site

## Blog
- 23 artículos en `/src/pages/blog/` (11 producto, 10 educativo, 2 ventaja estadística)
- Template para nuevos artículos: `src/pages/blog/TEMPLATE.astro`
- Para crear uno: duplicar TEMPLATE.astro, renombrar con slug, editar contenido
- Registrar en `src/pages/blog/index.astro` (agregar al array `posts`)
- Alternar: producto, educativo, producto, educativo...
- Categorías disponibles: "Herramientas", "Educación", "Ventaja Estadística"

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

## Build & Deploy
```bash
npm run build
# Auto-deploy via GitHub → Cloudflare Pages
# También manual:
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
