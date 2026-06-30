#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const SCHEDULE_PATH = 'src/data/schedule.json';
const DRAFTS_DIR = 'drafts';

const articles = [
  // ============ HERRAMIENTAS (30) ============
  { day:31, slug:'tradesyncer-latencia-optimizacion', title:'TradeSyncer PRO v2.0 — Optimización de latencia para operar en vivo', excerpt:'La latencia es el enemigo silencioso del copiador de trades. Aprende a configurar TradeSyncer PRO para minimizar el retardo entre cuentas.', category:'Herramientas', readTime:'5 min' },
  { day:32, slug:'order-flow-liquidez-intraday', title:'Liquidez intradiaria: dónde están realmente los stops', excerpt:'Los stops se agrupan en zonas predecibles. Aprende a identificar dónde está la liquidez intradiaria usando Order Flow.', category:'Educación', readTime:'7 min' },
  { day:33, slug:'firm-copier-risk-distribution', title:'GP Firm Copier Pro — Distribución de riesgo entre cuentas', excerpt:'Cómo distribuir el riesgo uniformemente entre 5, 10 o 20 cuentas de prop firms usando GP Firm Copier Pro.', category:'Herramientas', readTime:'6 min' },
  { day:34, slug:'drawdown-psicologia-gestion', title:'Drawdown: cómo gestionarlo en lo emocional y lo técnico', excerpt:'El drawdown es inevitable. Lo que diferencia a un profesional es cómo lo gestiona. Estrategias técnicas y psicológicas.', category:'Educación', readTime:'7 min' },
  { day:35, slug:'gpriskreward-oco-avanzado', title:'GPRiskReward — Estrategias OCO avanzadas para scalpers', excerpt:'Más allá del One-Click básico. Configuraciones OCO avanzadas con GPRiskReward para escalar posiciones.', category:'Herramientas', readTime:'5 min' },
  { day:36, slug:'fvg-trade-management', title:'Fair Value Gaps: cómo gestionar el trade después de la entrada', excerpt:'Entrar en un FVG es solo el inicio. Aprende a gestionar el trade: targets parciales, trailing y re-entradas.', category:'Educación', readTime:'6 min' },
  { day:37, slug:'gflow-pro-zonas-verificadas', title:'OmniFlow GFlow PRO v2.0 — Zonas Verificadas en profundidad', excerpt:'Las Zonas Verificadas son el filtro más potente de GFlow PRO. Cómo se calculan, cómo leerlas y cómo operarlas.', category:'Herramientas', readTime:'7 min' },
  { day:38, slug:'divergencias-rsi-volume', title:'Divergencias: cómo detectarlas con RSI y Volumen en NT8', excerpt:'Las divergencias son señales de agotamiento. Aprende a identificarlas combinando RSI y análisis de volumen.', category:'Educación', readTime:'6 min' },
  { day:39, slug:'gflow-x-kinetic-patrones', title:'OmniFlow GFlow X — Patrones de Kinetic Singularity más rentables', excerpt:'Los 3 patrones de Kinetic Singularity con mayor tasa de acierto según datos de backtesting en NQ y ES.', category:'Herramientas', readTime:'6 min' },
  { day:40, slug:'correlacion-mercados-futuros', title:'Correlación entre mercados: cómo usar el NQ, ES y YM juntos', excerpt:'Los índices no se mueven en el vacío. Aprende a leer la correlación entre NQ, ES y YM para anticipar movimientos.', category:'Educación', readTime:'7 min' },
  { day:41, slug:'quantum-prime-volatility-setups', title:'OmniFlow Quantum Prime — Setups para alta y baja volatilidad', excerpt:'Un mismo algoritmo, dos configuraciones. Cómo ajustar Quantum Prime para mercados volátiles y laterales.', category:'Herramientas', readTime:'5 min' },
  { day:42, slug:'session-breakout-strategy', title:'Estrategia de breakout en las primeras 30 minutos de cada sesión', excerpt:'Las aperturas de sesión generan los movimientos más potentes. Estrategia completa para operar breakouts en primeros 30 min.', category:'Educación', readTime:'6 min' },
  { day:43, slug:'gflow-premium-mapa-calor', title:'GFlow Pro Premium — Cómo interpretar el mapa de calor institucional', excerpt:'El mapa de calor de GFlow Pro Premium muestra dónde están los muros de oferta y demanda. Guía de interpretación.', category:'Herramientas', readTime:'6 min' },
  { day:44, slug:'iceberg-orders-detectarlos', title:'Órdenes Iceberg: qué son y cómo detectarlas con Order Flow', excerpt:'Las instituciones esconden su verdadera intención con órdenes Iceberg. Aprende a detectarlas en el tape.', category:'Educación', readTime:'7 min' },
  { day:45, slug:'gp-vwap-multitimeframe', title:'GP VWAP Clásico — Estrategia multi-timeframe para day trading', excerpt:'Un VWAP en múltiples timeframes te da una visión completa. Estrategia para operar con VWAP de 5min, 15min y 60min.', category:'Herramientas', readTime:'5 min' },
  { day:46, slug:'win-rate-vs-rr-ecuacion', title:'Win Rate vs Risk-Reward: la ecuación que todo trader debe entender', excerpt:'Ganar el 90% de las operaciones no te hace rentable. La relación Win Rate-R:R es lo único que importa.', category:'Ventaja Estadística', readTime:'6 min' },
  { day:47, slug:'nexus-trend-momentum-filtros', title:'Nexus Trend Engine — Filtros de momentum para evitar falsas señales', excerpt:'Cómo configurar los filtros de momentum de Nexus Trend Engine para reducir señales falsas en mercados laterales.', category:'Herramientas', readTime:'6 min' },
  { day:48, slug:'trading-reversiones-soporte-resistencia', title:'Trading de reversiones en soporte y resistencia con volumen', excerpt:'No todo soporte o resistencia es válido. El volumen te dice cuáles van a romperse y cuáles van a sostenerse.', category:'Educación', readTime:'7 min' },
  { day:49, slug:'specter-cloud-alertas', title:'Specter Trend Cloud — Configuración de alertas inteligentes', excerpt:'Las alertas de Specter Trend Cloud te avisan antes de que el mercado cambie. Configuración óptima para cada sesión.', category:'Herramientas', readTime:'5 min' },
  { day:50, slug:'fomo-trading-como-evitarlo', title:'FOMO en trading: cómo detectarlo y evitarlo con reglas objetivas', excerpt:'El FOMO es el mayor destructor de cuentas. Reglas objetivas para mantener la disciplina cuando el mercado se acelera.', category:'Educación', readTime:'6 min' },
  { day:51, slug:'gpcuantum-confluencia', title:'GPCuantum X — Cómo interpretar la confluencia multi-timeframe', excerpt:'GPCuantum X analiza 3 timeframes simultáneamente. Aprende a leer las señales de confluencia y alineación temporal.', category:'Herramientas', readTime:'6 min' },
  { day:52, slug:'absorption-patterns-order-flow', title:'Patrones de absorción en Order Flow: cómo identificarlos', excerpt:'La absorción es la firma de la manipulación institucional. Patrones y configuraciones para detectarla en el DOM.', category:'Educación', readTime:'7 min' },
  { day:53, slug:'tradesyncer-filtros-seguridad', title:'TradeSyncer PRO v2.0 — Filtros de seguridad para evitar pérdidas', excerpt:'Los filtros de seguridad de TradeSyncer PRO te protegen de errores. Daily Loss Limit, Max Drawdown y Kill Switch.', category:'Herramientas', readTime:'5 min' },
  { day:54, slug:'estadisticas-por-sesion', title:'¿En qué sesión es más rentable operar? Datos y estadísticas', excerpt:'Analizamos datos de miles de operaciones para determinar qué sesión ofrece las mejores oportunidades estadísticas.', category:'Ventaja Estadística', readTime:'6 min' },
  { day:55, slug:'firm-copier-evaluacion-multi', title:'GP Firm Copier Pro — Gestión de múltiples evaluaciones simultáneas', excerpt:'Opera 10+ evaluaciones al mismo tiempo con GP Firm Copier Pro. Sincronización, límites individuales y panel centralizado.', category:'Herramientas', readTime:'6 min' },
  { day:56, slug:'vwap-desviacion-estandar', title:'VWAP y desviación estándar: la base estadística del precio justo', excerpt:'El VWAP no es solo una línea. Entiende la estadística detrás de las bandas de desviación y cómo usarlas.', category:'Educación', readTime:'6 min' },
  { day:57, slug:'gpriskreward-auto-lotaje-avanzado', title:'GPRiskReward — Auto-Lotaje avanzado con riesgo por cuenta', excerpt:'Configura el Auto-Lotaje de GPRiskReward para gestionar el riesgo individual por cada cuenta de prop firm.', category:'Herramientas', readTime:'5 min' },
  { day:58, slug:'reversal-trading-estrategia', title:'Estrategia de reversión con Order Flow: cuándo ir contra la tendencia', excerpt:'Ir contra la tendencia es peligroso, pero el Order Flow te dice cuándo es seguro hacerlo. Señales y reglas.', category:'Educación', readTime:'7 min' },
  { day:59, slug:'gflow-pro-vs-quantum-prime-cual', title:'GFlow PRO v2.0 vs Quantum Prime — ¿Cuál necesitas según tu perfil?', excerpt:'Dos herramientas de Order Flow, dos perfiles distintos. Comparativa detallada para que elijas la correcta.', category:'Herramientas', readTime:'5 min' },
  { day:60, slug:'top-prop-firms-julio-2026', title:'Top 5 prop firms para traders de futuros en Julio 2026', excerpt:'Selección actualizada de las mejores prop firms para traders de futuros: evaluación, payout y reglas.', category:'Educación', readTime:'7 min' },

  // ============ SEGUNDO MES (61-90) ============
  { day:61, slug:'order-flow-claves-operativas', title:'Order Flow: 5 claves operativas que transformarán tu trading', excerpt:'Después de años operando con Order Flow, estas 5 claves son las que realmente hacen la diferencia.', category:'Educación', readTime:'6 min' },
  { day:62, slug:'nexus-trend-personalizacion', title:'Nexus Trend Engine — Personalización avanzada de parámetros', excerpt:'Cada mercado tiene su personalidad. Cómo ajustar los parámetros de Nexus Trend Engine para NQ, ES, CL y GC.', category:'Herramientas', readTime:'6 min' },
  { day:63, slug:'manipulacion-precio-smc', title:'Manipulación del precio: cómo identificar la trampa institucional', excerpt:'Las instituciones mueven el precio para cazar stops. Aprende a identificar la manipulación con SMC y Order Flow.', category:'Educación', readTime:'7 min' },
  { day:64, slug:'specter-cloud-personalizacion', title:'Specter Trend Cloud — Personalización visual y parámetros', excerpt:'Ajusta los colores, la sensibilidad y las alertas de Specter Trend Cloud para adaptarlo a tu estilo de trading.', category:'Herramientas', readTime:'5 min' },
  { day:65, slug:'backtesting-estrategias-nt8', title:'Cómo hacer backtesting de estrategias en NinjaTrader 8', excerpt:'Guía completa de backtesting en NT8: Strategy Analyzer, parámetros, optimización y pitfalls comunes.', category:'Educación', readTime:'8 min' },
  { day:66, slug:'tradesyncer-sync-bidireccional', title:'TradeSyncer PRO v2.0 — Sincronización bidireccional al detalle', excerpt:'Cómo funciona la sincronización bidireccional de TradeSyncer PRO y por qué es superior a la unidireccional.', category:'Herramientas', readTime:'5 min' },
  { day:67, slug:'estadisticas-breakout-apertura', title:'Estadísticas de breakouts en apertura de mercado: datos reveladores', excerpt:'Analizamos cientos de aperturas de mercado para determinar la probabilidad real de continuación tras un breakout.', category:'Ventaja Estadística', readTime:'6 min' },
  { day:68, slug:'consistency-prop-firms', title:'Consistency en prop firms: cómo lograrla sin sacrificar rentabilidad', excerpt:'Las prop firms exigen consistencia, no rentabilidad máxima. Cómo equilibrar ambos sin volverse loco.', category:'Educación', readTime:'6 min' },
  { day:69, slug:'gflow-pro-parametros-mercados', title:'OmniFlow GFlow PRO v2.0 — Parámetros recomendados por mercado', excerpt:'Configuraciones específicas de GFlow PRO para NQ, ES, CL, GC y YM. Ajustes finos para cada instrumento.', category:'Herramientas', readTime:'7 min' },
  { day:70, slug:'order-flow-vs-indicadores', title:'Order Flow vs Indicadores tradicionales: por qué el primero gana', excerpt:'Los indicadores tradicionales miran al pasado. El Order Flow mira al presente. Comparativa directa.', category:'Educación', readTime:'6 min' },
  { day:71, slug:'gpcuantum-alineacion-temporal', title:'GPCuantum X — Señales de alineación temporal y cómo operarlas', excerpt:'Cuando los 3 timeframes de GPCuantum X se alinean, la probabilidad se dispara. Estrategia de alineación.', category:'Herramientas', readTime:'6 min' },
  { day:72, slug:'correlacion-volumen-volatilidad', title:'Correlación volumen-volatilidad: anticipa los movimientos fuertes', excerpt:'Cuando el volumen sube y la volatilidad baja, algo se está gestando. Patrón para anticipar expansiones.', category:'Educación', readTime:'5 min' },
  { day:73, slug:'gp-vwap-bandas-dinamicas', title:'GP VWAP Clásico — Bandas dinámicas para trailing de posiciones', excerpt:'Usa las bandas de desviación del VWAP como trailing stop dinámico. Estrategia para capturar tendencias.', category:'Herramientas', readTime:'5 min' },
  { day:74, slug:'diario-trader-que-registrar', title:'Diario de trading: qué registrar y cómo analizar los datos', excerpt:'No es solo anotar ganancias y pérdidas. Qué datos registrar para mejorar tu operativa mes a mes.', category:'Educación', readTime:'6 min' },
  { day:75, slug:'firm-copier-daily-loss', title:'GP Firm Copier Pro — Daily Loss Limit avanzado y protección', excerpt:'Configuración avanzada del Daily Loss Limit de GP Firm Copier Pro con stops por cuenta y global.', category:'Herramientas', readTime:'5 min' },
  { day:76, slug:'prop-firm-evaluation-tips-2026', title:'Prop Firms 2026: 10 consejos para pasar la evaluación al primer intento', excerpt:'10 consejos prácticos basados en cientos de evaluaciones exitosas usando herramientas GP Trading.', category:'Educación', readTime:'7 min' },
  { day:77, slug:'quantum-prime-parametros-ajuste', title:'OmniFlow Quantum Prime — Ajuste de parámetros en vivo', excerpt:'Cómo ajustar los parámetros de Quantum Prime en tiempo real según cambia la volatilidad del mercado.', category:'Herramientas', readTime:'6 min' },
  { day:78, slug:'estadisticas-trade-management', title:'El impacto del trade management en tu expectativa estadística', excerpt:'Cómo el trailing, los targets parciales y el scaling afectan tu expectativa matemática. Datos reales.', category:'Ventaja Estadística', readTime:'6 min' },
  { day:79, slug:'gflow-x-proyecciones-tp', title:'OmniFlow GFlow X — Proyecciones TP1-TP4 y targets dinámicos', excerpt:'Las proyecciones de GFlow X no son fijas. Aprende cómo se calculan y cómo ajustar targets dinámicamente.', category:'Herramientas', readTime:'6 min' },
  { day:80, slug:'risk-management-avanzado-portafolio', title:'Risk Management avanzado: gestión de riesgo por portafolio', excerpt:'No gestiones el riesgo operación por operación. Aprende a gestionarlo a nivel de portafolio completo.', category:'Educación', readTime:'7 min' },
  { day:81, slug:'tradesyncer-log-depuracion', title:'TradeSyncer PRO v2.0 — Logs y depuración de errores', excerpt:'Cómo usar los logs de TradeSyncer PRO para diagnosticar problemas de conexión, sincronización y latencia.', category:'Herramientas', readTime:'4 min' },
  { day:82, slug:'operar-noticias-economicas', title:'Cómo operar noticias económicas con Order Flow', excerpt:'NFP, CPI, FOMC: cómo prepararse y operar eventos de alta volatilidad usando herramientas de Order Flow.', category:'Educación', readTime:'7 min' },
  { day:83, slug:'gflow-premium-casos-uso', title:'GFlow Pro Premium — Casos de uso reales en NQ y ES', excerpt:'Ejemplos reales de operaciones con GFlow Pro Premium en NQ y ES. Análisis pre-trade, ejecución y resultado.', category:'Herramientas', readTime:'6 min' },
  { day:84, slug:'order-flow-momentum-indicators', title:'Indicadores de momentum basados en Order Flow: crea los tuyos', excerpt:'El Order Flow es materia prima para indicadores personalizados. Conceptos para crear tus propios filtros.', category:'Educación', readTime:'7 min' },
  { day:85, slug:'nexus-trend-optimizacion', title:'Nexus Trend Engine — Optimización de parámetros con backtesting', excerpt:'Cómo optimizar los parámetros de Nexus Trend Engine usando datos históricos de NQ y ES.', category:'Herramientas', readTime:'6 min' },
  { day:86, slug:'daily-loss-limit-psicologia', title:'Daily Loss Limit: la herramienta psicológica más poderosa', excerpt:'El DDL no solo protege tu capital, protege tu mente. Por qué es la regla más importante del trading.', category:'Educación', readTime:'5 min' },
  { day:87, slug:'gpcuantum-personalizacion-timeframes', title:'GPCuantum X — Personalización de timeframes y alertas', excerpt:'Configura los 3 timeframes de GPCuantum X según tu estilo de trading. Alertas personalizadas por timeframe.', category:'Herramientas', readTime:'5 min' },
  { day:88, slug:'estadisticas-fvg-nt8', title:'Estadísticas de Fair Value Gaps en NQ y ES: datos de 6 meses', excerpt:'Analizamos 6 meses de FVGs en NQ y ES: tasa de relleno, distancia media y mejores configuraciones.', category:'Ventaja Estadística', readTime:'7 min' },
  { day:89, slug:'gpriskreward-monedas-futuros', title:'GPRiskReward — Calculando riesgo en futuros y divisas', excerpt:'GPRiskReward no es solo para futuros. Cómo configurarlo para operar Forex y CFDs con precisión.', category:'Herramientas', readTime:'5 min' },
  { day:90, slug:'overconfidence-trading-evitarlo', title:'Overconfidence: el mayor riesgo después de una racha ganadora', excerpt:'Después de 10 operaciones ganadoras consecutivas, el riesgo más grande eres tú. Cómo mantener la humildad.', category:'Educación', readTime:'6 min' },

  // ============ TERCER MES (91-120) ============
  { day:91, slug:'order-flow-avanzado-imbalance', title:'Order Flow Avanzado: Imbalance y Exceso en el tape', excerpt:'El imbalance entre compradores y vendedores es la señal más pura del Order Flow. Cómo leerlo en el tape.', category:'Educación', readTime:'7 min' },
  { day:92, slug:'tradesyncer-vps-config', title:'TradeSyncer PRO v2.0 — Configuración en VPS para máxima velocidad', excerpt:'Ejecutar TradeSyncer PRO en un VPS reduce la latencia al mínimo. Guía de configuración paso a paso.', category:'Herramientas', readTime:'6 min' },
  { day:93, slug:'volume-profile-poc-value-area', title:'Volume Profile Avanzado: POC, Value Area y perfiles de sesión', excerpt:'Más allá de lo básico. Cómo leer un perfil de volumen completo: POC, Value Area, perfiles de sesión.', category:'Educación', readTime:'7 min' },
  { day:94, slug:'firm-copier-modo-prop-firm', title:'GP Firm Copier Pro — Modo Prop Firm: configuración y límites', excerpt:'El Modo Prop Firm de GP Copier Pro ajusta automáticamente el comportamiento para cumplir reglas de fondeo.', category:'Herramientas', readTime:'5 min' },
  { day:95, slug:'trading-pausas-pre-meditadas', title:'El poder de las pausas pre-meditadas en tu operativa diaria', excerpt:'Las pausas no son tiempo perdido. Cómo programar descansos estratégicos mejora tu toma de decisiones.', category:'Educación', readTime:'5 min' },
  { day:96, slug:'gflow-pro-v2-modo-dios-parametros', title:'OmniFlow GFlow PRO v2.0 — Modo Dios: parámetros y ajustes finos', excerpt:'El Modo Dios no es magia, es matemática. Ajusta sus parámetros para filtrar solo las mejores configuraciones.', category:'Herramientas', readTime:'6 min' },
  { day:97, slug:'acumulacion-distribucion-order-flow', title:'Acumulación y distribución: cómo detectarlas con Order Flow', excerpt:'Las fases de acumulación y distribución institucional duran horas. El Order Flow te permite verlas en tiempo real.', category:'Educación', readTime:'7 min' },
  { day:98, slug:'quantum-prime-estadisticas', title:'OmniFlow Quantum Prime — Estadísticas de rendimiento en scalping', excerpt:'Datos reales de operaciones con Quantum Prime: win rate por hora del día, pares más rentables y drawdown.', category:'Ventaja Estadística', readTime:'6 min' },
  { day:99, slug:'gflow-x-hud-panel', title:'OmniFlow GFlow X — Panel HUD: toda la información de un vistazo', excerpt:'El panel HUD de GFlow X concentra la información crítica del Order Flow. Guía de lectura rápida.', category:'Herramientas', readTime:'5 min' },
  { day:100, slug:'maximo-diario-operaciones', title:'¿Cuántas operaciones al día es óptimo? Datos y recomendaciones', excerpt:'Operar demasiado es tan malo como operar muy poco. Datos sobre el número óptimo de operaciones diarias.', category:'Educación', readTime:'6 min' },
  { day:101, slug:'gp-vwap-divergencias-volumen', title:'GP VWAP Clásico — Divergencias entre precio y VWAP', excerpt:'Cuando el precio se separa del VWAP sin volumen de respaldo, la reversión es inminente. Cómo detectarlo.', category:'Herramientas', readTime:'5 min' },
  { day:102, slug:'revenue-per-trade-metrica', title:'Revenue per Trade: la métrica que ningún trader principiante mira', excerpt:'La mayoría mira el win rate. Los profesionales miran el revenue por operación. Cómo calcularlo y mejorarlo.', category:'Ventaja Estadística', readTime:'6 min' },
  { day:103, slug:'specter-cloud-estrategia-tendencia', title:'Specter Trend Cloud — Estrategia completa para mercados en tendencia', excerpt:'Cuando el mercado está en tendencia, Specter Trend Cloud brilla. Estrategia de entrada, trailing y salida.', category:'Herramientas', readTime:'5 min' },
  { day:104, slug:'gestion-stops-trailing-avanzado', title:'Gestión de stops: trailing dinámico con estructura de mercado', excerpt:'No uses trailing stops fijos. Aprende a mover tu stop basándote en la estructura del mercado y el volumen.', category:'Educación', readTime:'6 min' },
  { day:105, slug:'gpcuantum-deteccion-temprana', title:'GPCuantum X — Detección temprana de cambios de tendencia', excerpt:'Los cambios de tendencia no ocurren de la noche a la mañana. GPCuantum X los detecta en etapas tempranas.', category:'Herramientas', readTime:'6 min' },
  { day:106, slug:'fomo-venganza-trading', title:'Venganza trading: por qué ocurre y cómo romper el ciclo', excerpt:'Después de una pérdida grande, el 90% de los traders intenta recuperarla inmediatamente. Cómo romper el ciclo.', category:'Educación', readTime:'6 min' },
  { day:107, slug:'tradesyncer-failover-respaldo', title:'TradeSyncer PRO v2.0 — Failover y respaldo de conexión', excerpt:'Configuración de failover en TradeSyncer PRO para que nunca pierdas la conexión entre cuentas.', category:'Herramientas', readTime:'4 min' },
  { day:108, slug:'niveles-clave-soporte-resistencia', title:'Niveles clave de soporte y resistencia: cómo trazarlos correctamente', excerpt:'No todos los niveles importan. Cómo identificar soportes y resistencias relevantes con criterios objetivos.', category:'Educación', readTime:'6 min' },
  { day:109, slug:'gpriskreward-multi-cuenta', title:'GPRiskReward — Gestión de riesgo multi-cuenta centralizada', excerpt:'Controla el riesgo de todas tus cuentas desde un solo panel con GPRiskReward. Configuración y ejemplos.', category:'Herramientas', readTime:'5 min' },
  { day:110, slug:'plan-trading-diario', title:'Tu plan de trading diario: estructura para operar sin emociones', excerpt:'Un plan de trading no es una estrategia. Es la estructura que te mantiene operando sin importar cómo te sientas.', category:'Educación', readTime:'6 min' },
  { day:111, slug:'firm-copier-comparativa', title:'GP Firm Copier Pro vs TradeSyncer PRO — Comparativa y casos de uso', excerpt:'Dos copiadores, dos enfoques. Cuándo usar cada uno y por qué a veces necesitas ambos.', category:'Herramientas', readTime:'5 min' },
  { day:112, slug:'mejores-horas-operar-futuros', title:'Las mejores horas para operar futuros según el instrumento', excerpt:'Cada futuro tiene horas óptimas de operación. Tabla comparativa con spreads, volumen y volatilidad por hora.', category:'Educación', readTime:'6 min' },
  { day:113, slug:'order-flow-scope-datos', title:'El Order Flow en tu scope de datos: lo que necesitas saber', excerpt:'No todos los datos de Order Flow son iguales. Qué incluir y qué omitir en tu scope de NinjaTrader.', category:'Educación', readTime:'5 min' },
  { day:114, slug:'nexus-trend-multi-mercado', title:'Nexus Trend Engine — Aplicación multi-mercado: NQ, ES, CL y GC', excerpt:'Nexus Trend Engine funciona en cualquier mercado. Parámetros específicos y estrategias para cada instrumento.', category:'Herramientas', readTime:'6 min' },
  { day:115, slug:'diario-emocional-trader', title:'Diario emocional: la herramienta subestimada del trader profesional', excerpt:'Además del diario de operaciones, necesitas un diario emocional. Cómo registrar y analizar tus estados.', category:'Educación', readTime:'5 min' },
  { day:116, slug:'gflow-premium-confluencia', title:'GFlow Pro Premium — Confluencia de señales para máxima probabilidad', excerpt:'Cuando el mapa de calor, las zonas de liquidez y la tendencia se alinean, la probabilidad se multiplica.', category:'Herramientas', readTime:'6 min' },
  { day:117, slug:'eeuu-china-trading-impacto', title:'La relación EEUU-China y su impacto en los futuros globales', excerpt:'Los titulares geopolíticos mueven los mercados. Cómo anticipar y operar eventos entre las dos potencias.', category:'Educación', readTime:'7 min' },
  { day:118, slug:'quantum-prime-personalizacion-parametros', title:'OmniFlow Quantum Prime — Guía completa de personalización', excerpt:'Cada parámetro de Quantum Prime tiene un propósito. Guía completa para personalizar el algoritmo a tu medida.', category:'Herramientas', readTime:'6 min' },
  { day:119, slug:'estadisticas-cierre-mercado', title:'Estadísticas del cierre de mercado: patrones en los últimos 30 minutos', excerpt:'Los últimos 30 minutos de la sesión tienen patrones repetitivos. Datos y estrategias para operarlos.', category:'Ventaja Estadística', readTime:'6 min' },
  { day:120, slug:'camino-trader-profesional', title:'El camino del trader profesional: de principiante a consistente', excerpt:'El viaje del trading no es lineal. Las etapas, los obstáculos y lo que realmente funciona para volverse consistente.', category:'Educación', readTime:'7 min' },
];

function generateAstroContent(article) {
  const sections = {
    Herramientas: [
      { h2:'¿Qué es ' + article.title.split(' —')[0] + '?', p:'Esta herramienta de GP Trading está diseñada específicamente para traders que buscan llevar su operativa al siguiente nivel. En este artículo exploraremos a fondo sus características, configuración y aplicaciones prácticas en el mercado de futuros.' },
      { h2:'Características principales', p:'La herramienta incluye funcionalidades avanzadas que la diferencian de otras soluciones del mercado. A continuación analizamos cada una y cómo aprovecharlas al máximo en tu operativa diaria con NinjaTrader 8.' },
      { h2:'Configuración recomendada', p:'Para obtener el máximo rendimiento, te recomendamos la siguiente configuración inicial. Estos parámetros han sido optimizados tras cientos de horas de operativa real en NQ y ES. Ajusta según tu estilo y tolerancia al riesgo.' },
      { h2:'Casos de uso en mercado real', p:'Veamos ejemplos concretos de cómo aplicar esta herramienta en diferentes escenarios de mercado. Cada caso incluye el contexto, la configuración utilizada y el resultado obtenido.' },
      { h2:'Errores comunes y cómo evitarlos', p:'Incluso los traders experimentados cometen errores al usar herramientas avanzadas. Estos son los más frecuentes y cómo evitarlos para mantener una operativa consistente.' },
    ],
    Educación: [
      { h2:'¿Qué es y por qué es importante?', p:'Este concepto es fundamental para cualquier trader que busque operar con ventaja real. Entenderlo a fondo marca la diferencia entre operar por intuición y operar con convicción basada en datos.' },
      { h2:'Los fundamentos', p:'Antes de profundizar en estrategias avanzadas, es crucial dominar los fundamentos. Aquí desglosamos los conceptos base que todo trader debe conocer antes de aplicarlos en el mercado.' },
      { h2:'Cómo aplicarlo en tu operativa', p:'La teoría es importante, pero la aplicación práctica es lo que realmente importa. Veamos cómo llevar este conocimiento a tus gráficos de NinjaTrader 8 en tiempo real.' },
      { h2:'Ejemplos prácticos con Order Flow', p:'Combinando estos conceptos con herramientas de Order Flow de GP Trading, podemos identificar oportunidades con alta probabilidad de éxito. Ejemplos paso a paso.' },
      { h2:'Conclusión y próximos pasos', p:'Dominar este concepto requiere práctica y dedicación. Te recomendamos integrarlo gradualmente en tu operativa y combinarlo con las herramientas adecuadas.' },
    ],
    'Ventaja Estadística': [
      { h2:'Los datos detrás de la estrategia', p:'En este artículo analizamos datos reales de operaciones para determinar la ventaja estadística de diferentes enfoques. Los números no mienten.' },
      { h2:'Metodología de análisis', p:'Explicamos cómo recopilamos y procesamos los datos, los filtros aplicados y el tamaño de la muestra. La transparencia es clave para que puedas replicar el análisis.' },
      { h2:'Resultados y hallazgos principales', p:'Los datos revelan patrones claros que pueden mejorar significativamente tu expectativa estadística. Aquí presentamos los hallazgos más relevantes.' },
      { h2:'Implicaciones para tu trading', p:'¿Cómo traducir estos datos en reglas operativas concretas? Te mostramos cómo aplicar estos hallazgos en tu operativa diaria con NT8.' },
      { h2:'Limitaciones del estudio', p:'Todo estudio tiene limitaciones. Es importante entenderlas para no sobreestimar los resultados. Discutimos las variables no controladas.' },
    ],
  };

  const categorySections = sections[article.category] || sections['Educación'];
  const paragraphs = categorySections;

  const content = `---
import Layout from '../../layouts/Layout.astro';
import Header from '../../components/Header.astro';
import Footer from '../../components/Footer.astro';
---
<Layout title="${article.title.replace(/"/g, '&quot;')} — GP Trading Academy" description="${article.excerpt.replace(/"/g, '&quot;')}">
  <Header />
  <div id="main-content">
  <main class="pt-24 md:pt-32 pb-16 md:pb-24">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <a href="/blog" class="inline-flex items-center gap-1 text-sm text-accent hover:underline">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
          Volver al blog
        </a>
      </div>
      <div class="flex items-center gap-3 text-xs text-gray-500 mb-4">
        <span class="px-2 py-0.5 text-accent bg-accent/10 border border-accent/20 rounded-full">${article.category}</span>
        <span id="publish-date">Hoy</span>
        <span>· ${article.readTime} lectura</span>
      </div>
      <h1 class="text-3xl md:text-5xl font-bold tracking-tight mb-6">${article.title}</h1>
      <p class="text-lg text-gray-300 leading-relaxed mb-8">${article.excerpt}</p>
      <div class="glass-card p-8 md:p-12 space-y-6 text-gray-300 text-sm leading-relaxed">
${paragraphs.map((s, i) => `        <section>
          <h2 class="text-xl font-bold text-white mb-4">${s.h2}</h2>
          <p>${s.p}</p>
${i < paragraphs.length - 2 ? `          <p class="mt-3">Para los traders que usan la suite GP Trading en NinjaTrader 8, este conocimiento se traduce directamente en mejores entradas, salidas más precisas y una gestión de riesgo más efectiva. La clave está en la práctica constante y en la revisión objetiva de cada operación.</p>` : ''}
        </section>`).join('\n')}
        <div class="border-t border-white/10 pt-6 mt-8">
          <p class="text-sm text-gray-400">¿Quieres profundizar en este tema? <a href="/blog" class="text-accent hover:underline">Explora más artículos</a> o visita nuestra <a href="/" class="text-accent hover:underline">tienda</a> para conocer las herramientas de GP Trading.</p>
        </div>
      </div>
    </div>
  </main>
  </div>
  <Footer />
</Layout>`;

  return content;
}

// Load existing schedule
let schedule = [];
if (fs.existsSync(SCHEDULE_PATH)) {
  schedule = JSON.parse(fs.readFileSync(SCHEDULE_PATH, 'utf8'));
}

// Find the max existing day
const maxDay = schedule.reduce((max, e) => Math.max(max, e.day), 0);
console.log(`Existing schedule has ${schedule.length} entries, max day: ${maxDay}`);

// Add new articles that don't exist yet
let added = 0;
for (const article of articles) {
  if (!schedule.find(e => e.day === article.day)) {
    schedule.push(article);
    added++;
  }
}

// Sort by day
schedule.sort((a, b) => a.day - b.day);
fs.writeFileSync(SCHEDULE_PATH, JSON.stringify(schedule, null, 2));
console.log(`Added ${added} entries to schedule.json. Total: ${schedule.length}`);

// Generate draft files
if (!fs.existsSync(DRAFTS_DIR)) {
  fs.mkdirSync(DRAFTS_DIR, { recursive: true });
}

const newArticles = articles.filter(a => {
  const filename = `${String(a.day).padStart(2, '0')}-${a.slug}.astro`;
  return !fs.existsSync(path.join(DRAFTS_DIR, filename));
});

let generated = 0;
for (const article of articles) {
  const filename = `${String(article.day).padStart(2, '0')}-${article.slug}.astro`;
  const filepath = path.join(DRAFTS_DIR, filename);
  
  if (!fs.existsSync(filepath)) {
    const content = generateAstroContent(article);
    fs.writeFileSync(filepath, content);
    generated++;
    console.log(`  [${article.day}/120] ${filename}`);
  }
}

console.log(`\nGenerated ${generated} new draft files. Total drafts: ${fs.readdirSync(DRAFTS_DIR).filter(f => f.endsWith('.astro')).length}`);
console.log('Done!');
