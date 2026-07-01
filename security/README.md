# Sistema de Protección y Licencias — GP Trading

## Estructura

| Archivo | Propósito |
|---|---|
| `LicenseValidatorTemplate.cs` | Template C# para integrar en cada DLL de NT8 |
| `license-generator.html` | Página web admin para generar licencias (abrir en navegador) |
| `confuserex-config.crproj` | Configuración de ConfuserEx para ofuscar DLLs |
| `gen-license.py` | Script CLI para generar licencias desde terminal |

## Integración en cada Indicador NT8

### 1. Agregar el template a tu proyecto

Copia `LicenseValidatorTemplate.cs` a tu proyecto de Visual Studio.
Cambia `__PRODUCT_ID__` por el ID del producto:

| Producto | PRODUCT_ID |
|---|---|
| TradeSyncer PRO v2.0 | `tradesyncer` |
| GP Firm Copier Pro | `firmcopier` |
| GPRiskReward | `riskreward` |
| OmniFlow GFlow PRO v2.0 | `gflowpro` |
| OmniFlow GFlow X | `gflowx` |
| OmniFlow Quantum Prime | `quantumprime` |
| GFlow Pro Premium | `gflowpremium` |
| GP VWAP Clásico | `vpwap` |
| Nexus Trend Engine | `nexus` |
| Specter Trend Cloud | `specter` |
| GPCuantum X | `gpcuantum` |

### 2. Modificar tu indicador

En tu clase de indicador, agrega la validación en `OnStateChange()`:

```csharp
private LicenseStatus _licenseStatus = LicenseStatus.Invalid;
private int _trialDaysLeft;

protected override void OnStateChange()
{
    if (State == State.SetDefaults)
    {
        // ... tus defaults existentes ...
    }
    else if (State == State.Configure)
    {
        _licenseStatus = LicenseValidator.Validate(out _trialDaysLeft);
    }
}
```

En `OnBarUpdate()`, al inicio:

```csharp
protected override void OnBarUpdate()
{
    switch (_licenseStatus)
    {
        case LicenseStatus.Valid:
            LicenseValidator.RemoveLockScreen(this);
            break;

        case LicenseStatus.Trial:
            LicenseValidator.DrawTrialBanner(this, _trialDaysLeft);
            break;

        case LicenseStatus.Expired:
        case LicenseStatus.Invalid:
            LicenseValidator.DrawLockScreen(this);
            return;
    }

    // ... tu lógica del indicador aquí ...
}
```

### 3. Compilar

Compila en **Release**, **Any CPU**.

### 4. Ofuscar con ConfuserEx

Usa `confuserex-config.crproj`. Cambia `TuIndicador.dll` por tu DLL.
La DLL ofuscada se genera en la carpeta `Confused/`.

### 5. Probar en NT8

- Copia la DLL ofuscada a `Documents\NinjaTrader 8\bin\Custom`
- Inicia NT8, agrega el indicador
- Sin archivo `.lic`: debe mostrar "Prueba: 3 días restantes" (banner gold arriba a la derecha)
- Después de 3 días: debe mostrar pantalla de bloqueo centrada con datos de contacto
- Con archivo `.lic` válido: funciona normalmente

## Generar Licencias

### Opción 1: Página Web Admin (recomendado)

Abre `license-generator.html` en cualquier navegador.
Interfaz profesional con la identidad visual de GP Trading.

### Opción 2: Script CLI

```bash
python gen-license.py --account sim-12345678 --product tradesyncer
```

## Archivo .lic

El usuario crea `...\NinjaTrader 8\bin\Custom\Licenses\<product>.lic`
con el contenido del License Key (una línea, texto plano).

## Seguridad

- El `MASTER_SECRET` se reemplaza en cada DLL compilada manualmente
- La validación es offline (no requiere internet)
- El archivo `.trial` se crea automáticamente en la carpeta Licenses
- Ofuscación con ConfuserEx protege contra decompilación
- Anti-debug y anti-tamper activados en la configuración de ConfuserEx
