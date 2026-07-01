# Plan Completo: Pagos Cripto + Licencias Únicas NT8

## Fase 1 — Obfuscación y Sistema de Licencias (prioritario)

### 1.1 Obfuscación de cada indicador (C# .NET)

Cada indicador compila a una DLL (NinjaTrader 8). Hay que ofuscarlas para evitar decompilación.

| Herramienta | Costo | Método |
|---|---|---|
| **ConfuserEx** | Gratuito | Open source, ofuscación básica (renaming, control flow) |
| **.NET Reactor** | ~$249/yr | Ofuscación + encrypt + anti-debug + expiry |
| **SmartAssembly** | ~$499/yr | Ofuscación + embedding + tamper detection |
| **DNGuard** | ~$299/yr | Ofuscación fuerte para NT |

**Recomendación:** .NET Reactor (buen balance costo/seguridad).

Pasos por cada indicador (11 productos ≈ 11 DLLs + dependencias compartidas):

```
1. Compilar DLL de NinjaTrader (Release, Any CPU)
2. Pasar por .NET Reactor:
   - Control Flow Obfuscation
   - Renaming (sobrecarga de nombres)
   - String encryption
   - Anti-debug / Anti-tamper
   - Inhibir decompiladores (dnSpy, ILSpy)
3. Empaquetar DLL ofuscada + archivo de licencia vacío
```

### 1.2 Sistema de licencia por indicador

Cada DLL ofuscada debe incluir validación de una license key única.

**Arquitectura de licencia:**

```
License Key = SHA256(NT8_AccountID + ProductID + SecretSalt)
Formato: GPTR-XXXXX-XXXXX-XXXXX-XXXXX
```

**Flujo de validación en la DLL:**

```
1. Al cargar el indicador, lee C:\Users\<user>\Documents\NinjaTrader 8\bin\Custom\Licenses\<ProductID>.lic
2. Lee el NT8 Account ID desde NinjaTrader (o desde el archivo License.txt de NT8)
3. Desencripta/valida el license key contra el Account ID
4. Si no coincide → muestra mensaje "Licencia inválida" y no dibuja nada
5. Si coincide → funciona normalmente
```

### 1.3 Productos y sus IDs de licencia

| Producto | ProductID | DLL |
|---|---|---|
| TradeSyncer PRO v2.0 | `tradesyncer` | `GpTradeSyncer.dll` |
| GP Firm Copier Pro | `firmcopier` | `GpFirmCopier.dll` |
| GPRiskReward | `riskreward` | `GpRiskReward.dll` |
| OmniFlow GFlow PRO v2.0 | `gflowpro` | `GpGflowPro.dll` |
| OmniFlow GFlow X | `gflowx` | `GpGflowX.dll` |
| OmniFlow Quantum Prime | `quantumprime` | `GpQuantumPrime.dll` |
| GFlow Pro Premium | `gflowpremium` | `GpGflowPremium.dll` |
| GP VWAP Clásico | `vpwap` | `GpVwap.dll` |
| Nexus Trend Engine | `nexus` | `GpNexus.dll` |
| Specter Trend Cloud | `specter` | `GpSpecter.dll` |
| GPCuantum X | `gpcuantum` | `GpCuantumX.dll` |

### 1.4 Tool de generación de licencias (uso interno)

Aplicación interna (console app o webapp privada) para generar licencias:

```
Input:  NT8 Account ID, ProductID, cantidad de días (0 = vitalicia)
Output: License Key (texto para copiar o .lic file)

Algoritmo:
  1. LicenseKey = Base64(HMAC-SHA256(AccountID + ProductID + ExpiryDate, MasterSecret))
  2. Formatear como GPTR-XXXXX-XXXXX-XXXXX-XXXXX
  3. Guardar en BD interna (SQLite o Google Sheets) para auditoría:

     CREATE TABLE licencias (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       license_key TEXT UNIQUE NOT NULL,
       producto TEXT NOT NULL,
       nt8_account_id TEXT NOT NULL,
       customer_email TEXT,
       customer_name TEXT,
       order_id TEXT,
       created_at TEXT DEFAULT (datetime('now')),
       expires_at TEXT,
       revocada INTEGER DEFAULT 0
     );
```

### 1.5 Prevención de duplicados

- Cada license key se genera con el `NT8 Account ID` + `ProductID` como input → único por usuario-producto
- La BD interna registra cada licencia emitida → se puede verificar si ya existe
- Si un usuario intenta usar la misma licencia en otro Account ID → falla la validación
- (Opcional) La DLL puede hacer un chequeo online al cargar (Phone Home) contra un worker para verificar que la licencia no está revocada

### 1.6 Entregables Fase 1

| Tarea | Tiempo |
|---|---|
| Ofuscar 11 DLLs con .NET Reactor | 1 día |
| Implementar sistema de validación en cada DLL | 2-3 días |
| Crear tool interna de generación de licencias | 1 día |
| Setup BD de licencias (SQLite) | 0.5 día |
| Testing: intentar decompilar + probar licencias | 1 día |
| **Total Fase 1** | **~5-6 días** |

---

## Fase 2 — Página de Checkout + Binance Pay

### 2.1 Flujo completo

```
Usuario en web
  ↓  elige producto + "Comprar Ahora"
Checkout (email obligatorio + NT8 Account ID + Discord opcional)
  ↓
Cloudflare Worker crea orden en Binance Pay
  ↓
Usuario paga con Binance (USDT, BTC, BNB)
  ↓
Webhook de Binance → Worker (confirmación)
  ↓
Notificación a Discord interno: "NUEVA VENTA - TradeSyncer - 599 USDT"
  ↓
GP Trading manualmente:
   1. Abre tool de licencias
   2. Ingresa NT8 Account ID del comprador
   3. Genera license key
   4. Envía por email al comprador (o se entrega automático)
  ────────────────────────────────────
  ⌛ 6-12 horas (proceso manual)
  ────────────────────────────────────
  ↓
Usuario recibe DLL ofuscada + license key por email
  ↓
Usuario copia DLL a NinjaTrader 8\bin\Custom
  ↓
Usuario coloca license key en ...\Licenses\<ProductID>.lic
  ↓
Indicador funciona validado contra su NT8 Account ID
```

### 2.2 Página de checkout (`/checkout`)

Campos del formulario:
- **Email** (obligatorio) — para entregar la licencia
- **NT8 Account ID** (obligatorio) — obtenido desde NinjaTrader 8 (Accounts tab → Account ID)
- **Discord username** (opcional) — para soporte
- **Producto seleccionado** + precio

Validación:
- El NT8 Account ID se guarda como input del usuario (no se puede verificar automáticamente)
- El license key se genera a partir de este ID

### 2.3 Página de éxito + instrucciones

Después del pago:
- "Recibirás tu licencia en 6-12 horas hábiles al email ingresado"
- "Tu orden: ORD-20260701-XXXXX"
- Recordatorio de NT8 Account ID ingresado
- Links a Discord / contacto

### 2.4 Webhook interno para notificar

Cuando el worker recibe confirmación de Binance:
```
POST a Discord webhook:
  "🟢 NUEVA VENTA 🟢
   Producto: TradeSyncer PRO v2.0
   Monto: 599 USDT
   Email: cliente@email.com
   NT8 Account: sim-xxxxx
   Orden: ORD-20260701-XXXXX

   → https://admin.gptradingfx.pages.dev/generar-licencia?order=ORD-20260701-XXXXX"
```

### 2.5 Panel admin simple (Cloudflare Worker + páginas protegidas)

Mini-dashboard para GP Trading:
- Ver órdenes pendientes de generar licencia
- Generar license key (con un clic)
- Marcar como "licencia entregada"
- Historial de ventas
- Protegido con Basic Auth o Cloudflare Access

---

## Fase 3 — Automatización total (post-MVP)

Cuando quieras eliminar el proceso manual de 6-12h:

1. **Generación automática de licencias** — el worker genera el license key inmediatamente después del webhook de Binance
2. **Entrega automática por email** — sin intervención manual
3. **Phone Home opcional** — las DLL verifican online si la licencia sigue activa antes de cargar

Pero esto requiere tener la tool de licencias integrada con el worker y el master secreto en Cloudflare, no local.

---

## Stack completo

| Capa | Tecnología |
|---|---|
| Frontend | Astro + Tailwind (existente) |
| Backend API | Cloudflare Workers |
| DB de órdenes | Cloudflare D1 (SQLite) |
| DB de licencias | SQLite local (tool manual) → luego migrar a D1 |
| Pagos | Binance Pay API |
| Obfuscación | .NET Reactor |
| Notificaciones | Discord webhook |
| Email | Resend o SendGrid |
| Admin panel | Cloudflare Worker + páginas protegidas |

## Tiempo total estimado

| Fase | Tiempo |
|---|---|
| **Fase 1** — Obfuscación + licencias | **5-6 días** |
| **Fase 2** — Checkout + Binance + admin | **5-7 días** |
| **Fase 3** — Automatización total (opcional) | +3 días |
| **Total** | **~10-13 días** |
