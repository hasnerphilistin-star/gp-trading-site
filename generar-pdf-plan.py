#!/usr/bin/env python3
"""Genera el PDF del Plan de Proteccion de Codigo y Licencias"""

from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font(FONT, 'I', 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, 'GP Trading - Plan de Proteccion de Codigo y Licencias', align='C')
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font(FONT, 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', align='C')

    def title_page(self):
        self.add_page()
        self.ln(60)
        self.set_font(FONT, 'B', 28)
        self.set_text_color(0, 212, 170)
        self.cell(0, 15, 'GP Trading', align='C')
        self.ln(18)
        self.set_font(FONT, 'B', 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, 'Plan de Proteccion de Codigo', align='C')
        self.ln(10)
        self.cell(0, 12, 'y Sistema de Licencias', align='C')
        self.ln(20)
        self.set_font(FONT, '', 13)
        self.set_text_color(200, 200, 200)
        self.cell(0, 8, 'Ofuscacion de DLLs + Licencias unicas por NT8 Account ID', align='C')
        self.ln(8)
        self.cell(0, 8, 'Anti-decompilacion, Anti-duplicacion, Anti-pirateria', align='C')
        self.ln(35)
        self.set_font(FONT, '', 11)
        self.set_text_color(150, 150, 150)
        self.cell(0, 7, 'Documento interno - Confidencial', align='C')
        self.ln(7)
        self.cell(0, 7, 'Junio 2026', align='C')

    def section_title(self, title, num=None):
        self.ln(6)
        if num:
            full = f'{num}. {title}'
        else:
            full = title
        self.set_font(FONT, 'B', 16)
        self.set_text_color(0, 212, 170)
        self.cell(0, 10, full)
        self.ln(12)

    def sub_title(self, title):
        self.ln(4)
        self.set_font(FONT, 'B', 12)
        self.set_text_color(220, 220, 220)
        self.cell(0, 8, title)
        self.ln(10)

    def sub_sub_title(self, title):
        self.ln(2)
        self.set_font(FONT, 'B', 11)
        self.set_text_color(200, 200, 200)
        self.cell(0, 7, title)
        self.ln(8)

    def body_text(self, text):
        self.set_font(FONT, '', 10)
        self.set_text_color(220, 220, 220)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text, indent=10):
        self.set_font(FONT, '', 10)
        self.set_text_color(220, 220, 220)
        x = self.get_x()
        self.cell(indent, 5.5, '')
        self.set_font(FONT, '', 10)
        bullet_char = chr(8226)
        self.cell(5, 5.5, bullet_char)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def code_block(self, text):
        self.ln(2)
        self.set_fill_color(20, 20, 30)
        self.set_text_color(0, 212, 170)
        self.set_font('Courier', '', 9)
        lines = text.split('\n')
        for line in lines:
            self.cell(10, 5, '', fill=True)
            self.cell(0, 5, line, fill=True)
            self.ln()
        self.ln(3)

    def warning_box(self, text):
        self.ln(2)
        self.set_fill_color(50, 30, 0)
        self.set_text_color(255, 200, 50)
        self.set_font(FONT, 'B', 10)
        self.cell(10, 6, '', fill=True)
        self.cell(0, 6, ' IMPORTANTE: ' + text, fill=True)
        self.ln(8)

    def info_box(self, text):
        self.ln(2)
        self.set_fill_color(0, 40, 40)
        self.set_text_color(0, 212, 170)
        self.set_font(FONT, '', 10)
        self.cell(10, 6, '', fill=True)
        self.cell(0, 6, ' ' + text, fill=True)
        self.ln(8)


pdf = PDF('P', 'mm', 'A4')
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.set_draw_color(0, 212, 170)
pdf.set_fill_color(10, 10, 10)

FONT_PATH = '/Library/Fonts/Arial Unicode.ttf'
if os.path.exists(FONT_PATH):
    pdf.add_font('ArialUni', '', FONT_PATH, uni=True)
    pdf.add_font('ArialUni', 'B', FONT_PATH, uni=True)
    pdf.add_font('ArialUni', 'I', FONT_PATH, uni=True)
else:
    print('WARNING: Arial Unicode font not found, using Helvetica')

FONT = 'ArialUni' if os.path.exists(FONT_PATH) else 'Helvetica'


# ---- PORTADA ----
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, 'F')

# Logo area
pdf.ln(50)
pdf.set_font(FONT, 'B', 36)
pdf.set_text_color(0, 212, 170)
pdf.cell(0, 18, 'GP TRADING', align='C')
pdf.ln(14)
pdf.set_font(FONT, '', 11)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 7, 'NinjaTrader 8 Suite Premium', align='C')
pdf.ln(30)

pdf.set_font(FONT, 'B', 22)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, 'Plan de Proteccion de Codigo', align='C')
pdf.ln(10)
pdf.cell(0, 12, 'y Sistema de Licencias', align='C')
pdf.ln(25)

pdf.set_font(FONT, '', 12)
pdf.set_text_color(180, 180, 180)
pdf.cell(0, 7, 'Ofuscacion de DLLs  |  Licencias por NT8 Account ID', align='C')
pdf.ln(7)
pdf.cell(0, 7, 'Anti-decompilacion  |  Anti-duplicacion  |  Anti-pirateria', align='C')
pdf.ln(40)

pdf.set_font(FONT, '', 10)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 7, 'Documento interno - Confidencial', align='C')
pdf.ln(7)
pdf.cell(0, 7, 'GP Trading Academy - gptradingfx.pages.dev', align='C')
pdf.ln(7)
pdf.cell(0, 7, 'Junio 2026', align='C')

# ---- TABLA DE CONTENIDOS ----
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, 'F')

pdf.set_font(FONT, 'B', 18)
pdf.set_text_color(0, 212, 170)
pdf.cell(0, 12, 'Tabla de Contenidos')
pdf.ln(16)

toc = [
    ('1', 'Resumen Ejecutivo'),
    ('2', 'Arquitectura General del Sistema'),
    ('3', 'Ofuscacion de Codigo (Anti-Decompilacion)'),
    ('3.1', '  Que es la ofuscacion y por que es necesaria'),
    ('3.2', '  ConfuserEx: herramienta gratuita recomendada'),
    ('3.3', '  Configuracion paso a paso para NT8'),
    ('3.4', '  Reglas de preservacion para NinjaTrader'),
    ('3.5', '  Prueba de resistencia contra decompiladores'),
    ('4', 'Sistema de Licencias Unicas'),
    ('4.1', '  Algoritmo de generacion de License Key'),
    ('4.2', '  Formato de la clave'),
    ('4.3', '  Almacenamiento en el disco del cliente'),
    ('4.4', '  Validacion en tiempo de carga del indicador'),
    ('4.5', '  Prevencion de duplicados'),
    ('4.6', '  Revocacion de licencias'),
    ('5', 'Tool Interna de Generacion de Licencias'),
    ('5.1', '  Funcionamiento'),
    ('5.2',  '  Base de datos de auditoria'),
    ('6', 'Proceso de Entrega (6-12 horas)'),
    ('6.1', '  Flujo completo paso a paso'),
    ('6.2', '  Plantilla de email al cliente'),
    ('7', 'Planes a Futuro: Automatizacion Total'),
    ('7.1',  '  Integracion con Binance Pay'),
    ('7.2', '  Phone Home opcional'),
    ('8', 'Recomendaciones Finales'),
    ('9', 'Apendice: Configuracion ConfuserEx (.crproj)'),
]

for num, title in toc:
    if num.count('.') == 0 and len(num) <= 2:
        pdf.set_font(FONT, 'B', 11)
    else:
        pdf.set_font(FONT, '', 10)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(10, 6, num)
    pdf.cell(0, 6, title)
    pdf.ln(6.5)

# ---- 1. RESUMEN EJECUTIVO ----
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, 'F')
pdf.section_title('Resumen Ejecutivo', '1')

pdf.body_text(
    'GP Trading distribuye 11 indicadores premium para NinjaTrader 8 en formato DLL (C# .NET). '
    'Al ser codigo .NET compilado en IL (Intermediate Language), cualquier persona con un decompilador '
    'gratuito (dnSpy, ILSpy, dotPeek) puede reconstruir el codigo fuente original casi por completo. '
    'Esto expone la logica de negocio, los algoritmos institucionales y permite la pirateria masiva.')
pdf.ln(2)
pdf.body_text(
    'Este documento detalla un sistema completo de proteccion en tres capas:')
pdf.ln(2)
pdf.bullet('Ofuscacion del codigo (anti-decompilacion): hacer ilegible el IL sin romper la compatibilidad con NT8')
pdf.bullet('Licencias por hardware/identidad (anti-duplicacion): cada copia se ata al Account ID de NinjaTrader del comprador')
pdf.bullet('Auditoria y revocacion (anti-pirateria): base de datos interna que permite rastrear y revocar licencias')
pdf.ln(2)
pdf.info_box('Herramienta principal: ConfuserEx (gratuita, open source) combinada con reglas especificas para NinTrader 8.')

# ---- 2. ARQUITECTURA GENERAL ----
pdf.section_title('Arquitectura General del Sistema', '2')
pdf.body_text(
    'El sistema se compone de 5 elementos que trabajan en conjunto:')
pdf.ln(2)

pdf.sub_title('Componentes')
pdf.bullet('DLL ofuscada: cada indicador compilado + ofuscado con ConfuserEx. Incluye la logica de validacion de licencia.')
pdf.bullet('License Key unico: string de 32 caracteres generado con el NT8 Account ID + una clave maestra secreta.')
pdf.bullet('Archivo .lic: archivo de texto plano en el disco del cliente con su license key.')
pdf.bullet('Tool de generacion (interna): aplicacion que recibe un Account ID + Product ID y genera el License Key.')
pdf.bullet('Base de datos de auditoria: registro de todas las licencias emitidas para detectar duplicados o abusos.')
pdf.ln(3)

pdf.warning_box(
    'El Account ID de NinjaTrader 8 es el identificador unico de cada cuenta de simulacion/real '
    '(ej: "sim-xxxxx" o "real-xxxxx"). Esto hace que cada licencia este atada a UNA SOLA cuenta de NT8.')

# ---- 3. OFUSCACION ----
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, 'F')
pdf.section_title('Ofuscacion de Codigo (Anti-Decompilacion)', '3')

pdf.sub_title('3.1 Que es la ofuscacion y por que es necesaria')
pdf.body_text(
    'El codigo .NET no se compila a codigo maquina, sino a IL (Intermediate Language). '
    'IL conserva nombres de clases, metodos, propiedades, strings y la estructura logica completa. '
    'Herramientas como dnSpy permiten a cualquiera abrir una DLL y ver:')
pdf.ln(2)

pdf.code_block(
    '// Ejemplo: codigo visible en dnSpy SIN ofuscacion\n'
    'public class GpTradeSyncer : Indicator\n'
    '{\n'
    '  private double CalculateEntryPrice()\n'
    '  {\n'
    '    double vwap = GetVWAP(14);\n'
    '    double fairValue = vwap * 1.005;\n'
    '    return fairValue;\n'
    '  }\n'
    '}')

pdf.body_text(
    'La ofuscacion transforma ese codigo en algo como esto:')
pdf.code_block(
    '// Ejemplo: mismo codigo DESPUES de ofuscacion\n'
    'public class A : B\n'
    '{\n'
    '  private double X()\n'
    '  {\n'
    '    double a = C(\"\\\\u0003\\\\u0019\\\\u0005...\");  // string encriptado\n'
    '    double b = a * Y.Z();  // control flow ofuscado\n'
    '    return b;\n'
    '  }\n'
    '}')

pdf.body_text(
    'Sigue siendo funcionalmente identico, pero un humano no puede entenderlo '
    'ni reconstruir la logica original facilmente.')

# ---- 3.2 CONFUSEREX ----
pdf.sub_title('3.2 ConfuserEx: herramienta gratuita recomendada')
pdf.body_text(
    'ConfuserEx es un ofuscador open source para .NET, mantenido por la comunidad, '
    'sin costo y ampliamente utilizado en el ecosistema NinjaTrader.')
pdf.ln(2)
pdf.bullet('Licencia: MIT (completamente gratuito)')
pdf.bullet('Plataforma: Windows (GUI + CLI)')
pdf.bullet('Soporte: .NET Framework 4.8 (compatible con NT8)')
pdf.ln(2)

pdf.sub_sub_title('Protecciones que ofrece ConfuserEx:')

prots = [
    ('Renaming', 'Cambia nombres de clases, metodos y variables a nombres ilegibles (a, b, c, A1, B2...)'),
    ('Control Flow', 'Ofusca la estructura de control (if, for, while) en saltos opacos ilegibles'),
    ('Constants / Strings', 'Encripta strings literales (URLs, claves, mensajes) para que no sean visibles'),
    ('Anti Debug', 'Detecta si la DLL se esta ejecutando bajo un decompilador y altera su comportamiento'),
    ('Anti Tamper', 'Verifica la integridad de la DLL; si fue modificada, deja de funcionar'),
    ('Anti Dump', 'Dificulta el volcado de la memoria del proceso para extraer la DLL limpia'),
    ('Ref Proxy', 'Desv铆a llamadas a metodos a traves de proxies dificiles de seguir'),
]

for name, desc in prots:
    pdf.set_font(FONT, 'B', 10)
    pdf.set_text_color(0, 212, 170)
    pdf.cell(45, 6, name)
    pdf.set_font(FONT, '', 10)
    pdf.set_text_color(220, 220, 220)
    pdf.cell(0, 6, desc)
    pdf.ln(7)

# ---- 3.3 CONFIG CONFUSEREX ----
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, 'F')
pdf.sub_title('3.3 Configuracion paso a paso para NinjaTrader 8')

pdf.body_text(
    'NinjaTrader 8 descubre los indicadores mediante reflexion: busca clases publicas que hereden '
    'de NinjaTrader.Gui.NinjaScript.Indicator. Si ConfuserEx renombra la clase principal, '
    'NT8 no podra cargar el indicador.')
pdf.ln(2)
pdf.body_text('Por eso la configuracion debe incluir REGLAS DE PRESERVACION.')

pdf.sub_sub_title('Paso 1: Compilar la DLL en modo Release')
pdf.bullet('Abrir el proyecto en Visual Studio')
pdf.bullet('Configurar: Solution Config = Release, Platform = Any CPU')
pdf.bullet('Compilar (Build > Build Solution)')
pdf.bullet('La DLL se genera en bin/Release/NombreIndicador.dll')

pdf.sub_sub_title('Paso 2: Crear proyecto ConfuserEx')
pdf.bullet('Descargar ConfuserEx desde https://github.com/ConfuserEx/ConfuserEx/releases')
pdf.bullet('Abrir ConfuserEx GUI')
pdf.bullet('Arrastrar la DLL a la ventana')
pdf.bullet('Ir a la pestana "Settings"')

pdf.sub_sub_title('Paso 3: Aplicar reglas de preservacion')
pdf.body_text('Agregar reglas para que NT8 pueda cargar el indicador:')

pdf.code_block(
    '<rule pattern="true" inherit="false">\n'
    '  <protection action="remove" module="rename" />\n'
    '  <protection action="remove" module="ctrl flow" />\n'
    '</rule>\n'
    '<rule pattern="public class *Indicator">\n'
    '  <protection action="remove" module="rename" />\n'
    '</rule>\n'
    '<rule pattern="public class * : NinjaTrader.Gui.NinjaScript.Indicator">\n'
    '  <protection action="remove" module="rename" />\n'
    '</rule>')

pdf.sub_sub_title('Paso 4: Activar protecciones internas')
pdf.body_text('Para el resto del codigo (metodos privados, propiedades, strings), activar:')
pdf.bullet('Renaming: si (con reglas arriba)')
pdf.bullet('Control Flow: si (fuerte)')
pdf.bullet('Constants / Strings: si')
pdf.bullet('Anti Debug: si')
pdf.bullet('Anti Tamper: si')
pdf.bullet('Ref Proxy: si')

pdf.sub_sub_title('Paso 5: Ofuscar')
pdf.bullet('Ir a la pestana "Protect"')
pdf.bullet('Click "Protect"')
pdf.bullet('La DLL ofuscada se genera en la carpeta Confused/')
pdf.bullet('Probar la DLL en NinjaTrader 8 antes de distribuir')

# ---- 3.4 REGLAS DETALLADAS ----
pdf.sub_title('3.4 Reglas de preservacion detalladas para NT8')

pdf.body_text('NinjaTrader 8 requiere que los siguientes elementos NO sean renombrados:')
pdf.ln(2)
pdf.bullet('La clase principal del indicador (debe heredar de Indicator)')
pdf.bullet('Propiedades publicas (las usa NT8 para la UI: Browsable, DisplayName, etc.)')
pdf.bullet('Metodos sobreescritos: OnStateChange(), OnBarUpdate(), Initialize(), Terminate()')
pdf.bullet('Atributos (DisplayName, Description, XmlIgnore...)')
pdf.ln(2)

pdf.body_text('Regla general: ofuscar TODO lo interno, preservar TODO lo publico que NT8 necesita.')
pdf.ln(2)

pdf.info_box('En la seccion "Apendice" (final del documento) se incluye el archivo .crproj completo listo para usar.')

# ---- 3.5 PRUEBA ----
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, 'F')
pdf.sub_title('3.5 Prueba de resistencia contra decompiladores')

pdf.body_text('Despues de ofuscar, hay que verificar que la proteccion sea efectiva:')

pdf.sub_sub_title('Test 1: dnSpy / ILSpy')
pdf.bullet('Abrir la DLL ofuscada en dnSpy')
pdf.bullet('Verificar que los nombres de clases internas sean ilegibles (A, B, C, a1, b2...)')
pdf.bullet('Verificar que los strings aparezcan encriptados (\\u0000\\u0001...)')
pdf.bullet('Intentar navegar el control flow: debe ser un "arbol de decision" ilegible')

pdf.sub_sub_title('Test 2: Carga en NinjaTrader 8')
pdf.bullet('Copiar la DLL ofuscada a: Documents\\NinjaTrader 8\\bin\\Custom')
pdf.bullet('Reiniciar NinjaTrader 8')
pdf.bullet('Abrir el panel de indicadores (New > Indicators)')
pdf.bullet('Verificar que el indicador aparezca con su nombre correcto')
pdf.bullet('Arrastrarlo a un grafico: debe funcionar sin errores')

pdf.sub_sub_title('Test 3: Anti-Debug')
pdf.bullet('Abrir la DLL en dnSpy y ejecutarla (Debug > Start)')
pdf.bullet('Si Anti Debug funciona, el indicador debe detectar el debugger y alterar su comportamiento o fallar')

pdf.warning_box(
    'Ninguna ofuscacion es 100% inquebrantable. Un atacante determinado con semanas de '
    'trabajo puede revertir cualquier proteccion. El objetivo es que el esfuerzo necesario '
    'supere el valor de la herramienta, disuadiendo al 99% de los piratas.')

# ---- 4. SISTEMA DE LICENCIAS ----
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, 'F')
pdf.section_title('Sistema de Licencias Unicas', '4')

pdf.sub_title('4.1 Algoritmo de generacion de License Key')
pdf.body_text(
    'El License Key se genera combinando el NT8 Account ID del comprador con una clave maestra secreta '
    'que solo tu conoces. Esto asegura que cada licencia es UNICA y no transferible a otra cuenta.')
pdf.ln(2)

pdf.code_block(
    '// Pseudocodigo de generacion\n'
    'function GenerateLicenseKey(accountId, productId, masterSecret):\n'
    '    data = accountId + "|" + productId + "|" + masterSecret\n'
    '    hash = SHA256(data)\n'
    '    // Tomar primeros 20 bytes -> 40 caracteres hex\n'
    '    key = "GPTR-" + FormatearEnGrupos(hash[0:20])\n'
    '    return key')

pdf.sub_sub_title('Componentes del algoritmo:')
pdf.bullet('accountId: el NT8 Account ID del comprador (ej: "sim-12345678")')
pdf.bullet('productId: identificador interno del producto (ej: "tradesyncer")')
pdf.bullet('masterSecret: string aleatorio conocido SOLO por GP Trading (ej: 64 caracteres hex)')
pdf.bullet('SHA256: funcion hash unidireccional (no se puede obtener el Account ID desde la key)')
pdf.ln(2)
pdf.warning_box(
    'El masterSecret debe ser unico, largo (min 32 caracteres), generado con un generador '
    'criptografico seguro y almacenado JAMAS en el codigo de la DLL ni en el repositorio.')

pdf.sub_title('4.2 Formato de la clave')
pdf.body_text('Cada License Key sigue el formato:')
pdf.code_block('GPTR-XXXXX-XXXXX-XXXXX-XXXXX')
pdf.body_text(
    'Donde cada grupo son caracteres hexadecimales (0-9, A-F). '
    'Ejemplo real: GPTR-A3F8-1C92-4B7D-E05A')

pdf.sub_title('4.3 Almacenamiento en el disco del cliente')
pdf.body_text('El archivo de licencia se almacena en:')
pdf.code_block(
    'C:\\Users\\<NOMBRE>\\Documents\\NinjaTrader 8\\bin\\Custom\\Licenses\\')
pdf.body_text('Con el nombre del producto:')
pdf.code_block(
    'Ejemplo: ...\\Licenses\\tradesyncer.lic')
pdf.ln(2)
pdf.body_text('Contenido del archivo .lic (una sola linea):')
pdf.code_block('GPTR-A3F8-1C92-4B7D-E05A')
pdf.ln(2)
pdf.info_box(
    'Ventaja de usar archivos .lic: no requieren instalacion adicional. '
    'El usuario solo copia un archivo de texto a la carpeta correcta.')

# ---- 4.4 VALIDACION ----
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, 'F')
pdf.sub_title('4.4 Validacion en tiempo de carga del indicador')

pdf.body_text(
    'Cada DLL ofuscada incluye codigo de validacion que se ejecuta en OnStateChange() '
    'cuando el estado es State.SetDefaults o State.Configure.')
pdf.ln(2)

pdf.code_block(
    '// Pseudocodigo de validacion DENTRO de la DLL\n'
    'function OnStateChange():\n'
    '    if state == State.SetDefaults:\n'
    '        licenseKey = LeerArchivo("...\\\\Licenses\\\\<ProductID>.lic")\n'
    '        if licenseKey == null:\n'
    '            MostrarError("Licencia no encontrada")\n'
    '            return\n'
    '        accountId = ObtenerNT8AccountId()\n'
    '        expected = GenerateLicenseKey(accountId, productId, masterSecret)\n'
    '        if licenseKey != expected:\n'
    '            MostrarError("Licencia invalida para esta cuenta")\n'
    '            return\n'
    '    // Si pasa la validacion -> continua carga normal')

pdf.sub_sub_title('Comportamiento cuando la licencia falla:')
pdf.bullet('El indicador se carga en NT8 pero NO dibuja nada en el grafico')
pdf.bullet('Muestra un mensaje de error en la ventana de Output de NT8')
pdf.bullet('Puede mostrar una ventana emergente (Draw.TextFixed) con "Licencia no valida - GP Trading"')
pdf.ln(2)

pdf.warning_box(
    'NUNCA incluyas el masterSecret directamente como string en la DLL, ni siquiera ofuscado. '
    'En su lugar, genera el License Key por adelantado (en la tool interna) y embedelo en la DLL '
    'o en el archivo .lic. La validacion en cliente solo compara el hash, no necesita el secreto.')

# ---- 4.5 PREVENCION DUPLICADOS ----
pdf.sub_title('4.5 Prevencion de duplicados')

pdf.body_text('El sistema previene duplicacion en tres niveles:')
pdf.ln(2)

pdf.sub_sub_title('Nivel 1: Ataque por hardware (Account ID)')
pdf.body_text(
    'Cada License Key se genera con el NT8 Account ID del comprador. Si el usuario '
    'copia su archivo .lic a otro PC con otra cuenta de NT8, la validacion falla porque '
    'el Account ID no coincide.')

pdf.sub_sub_title('Nivel 2: Base de datos de auditoria')
pdf.body_text(
    'Cada licencia emitida se registra en una base de datos interna con: '
    'License Key, Account ID, Product ID, email del comprador y fecha. '
    'Si detectas que un mismo Account ID genera multiples solicitudes, puedes bloquearlo manualmente.')

pdf.sub_sub_title('Nivel 3: Phone Home (opcional, futuro)')
pdf.body_text(
    'Al cargar, la DLL puede hacer una peticion HTTP a un servidor central para verificar que '
    'la licencia sigue activa y no ha sido revocada. Esto requiere conectividad a internet.')

# ---- 4.6 REVOCACION ----
pdf.sub_title('4.6 Revocacion de licencias')

pdf.body_text(
    'Si un usuario infringe los terminos (comparte su licencia, la publica, etc.), '
    'puedes revocarla de dos maneras:')
pdf.ln(2)
pdf.bullet('Sin Phone Home: agregas el License Key a una "lista negra" interna y en la proxima version '
           'de la DLL, ese key sera rechazado. El usuario necesitara actualizar la DLL para seguir usando el indicador.')
pdf.bullet('Con Phone Home: la DLL consulta un endpoint central; si la licencia esta revocada, '
           'el indicador deja de funcionar inmediatamente en todos los PCs donde este instalada.')

pdf.info_box('Para empezar, el Nivel 1 + Nivel 2 son suficientes. Phone Home se puede agregar despues.')

# ---- 5. TOOL INTERNA ----
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, 'F')
pdf.section_title('Tool Interna de Generacion de Licencias', '5')

pdf.sub_title('5.1 Funcionamiento')
pdf.body_text(
    'La tool de generacion es una aplicacion interna (console app o web app protegida) '
    'que solo tu puedes ejecutar. Recibe 3 parametros y devuelve el License Key.')
pdf.ln(2)

pdf.code_block(
    '// Ejemplo de uso (CLI)\n'
    '> gpt-license-gen --account sim-12345678 --product tradesyncer\n'
    '\n'
    'Licencia generada:\n'
    '  Producto:     TradeSyncer PRO v2.0\n'
    '  Account ID:   sim-12345678\n'
    '  License Key:  GPTR-A3F8-1C92-4B7D-E05A\n'
    '  Archivo:      tradesyncer.lic')

pdf.sub_sub_title('Requisitos de la tool:')
pdf.bullet('Ejecutable portable (C# console app o script de Python)')
pdf.bullet('El masterSecret se ingresa al iniciar o se lee de una variable de entorno')
pdf.bullet('Genera el archivo .lic directamente')
pdf.bullet('Opcional: genera tambien el email para el cliente')
pdf.ln(2)

pdf.sub_title('5.2 Base de datos de auditoria')
pdf.body_text('Cada licencia emitida se registra automaticamente en una base de datos SQLite:')

pdf.code_block(
    'CREATE TABLE licencias (\n'
    '  id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
    '  license_key TEXT UNIQUE NOT NULL,\n'
    '  producto TEXT NOT NULL,\n'
    '  nt8_account_id TEXT NOT NULL,\n'
    '  customer_email TEXT,\n'
    '  customer_name TEXT,\n'
    '  order_id TEXT,\n'
    '  created_at TEXT DEFAULT (datetime("now")),\n'
    '  revocada INTEGER DEFAULT 0\n'
    ');')

pdf.body_text('Esto permite:')
pdf.bullet('Consultar cuantas licencias tiene un Account ID')
pdf.bullet('Detectar si un mismo Account ID solicita el mismo producto dos veces')
pdf.bullet('Revocar licencias marcando revocada = 1')
pdf.bullet('Exportar reportes de ventas')

# ---- 6. PROCESO DE ENTREGA ----
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, 'F')
pdf.section_title('Proceso de Entrega (6-12 horas)', '6')

pdf.sub_title('6.1 Flujo completo paso a paso')

steps = [
    ('1. Compra', 'El usuario compra en la web (Binance Pay / WhatsApp) y proporciona su email + NT8 Account ID.'),
    ('2. Notificacion', 'Te llega una alerta a Discord: "NUEVA VENTA - Producto - Monto - Account ID - Email"'),
    ('3. Validacion manual', 'Verificas que el pago haya sido recibido correctamente.'),
    ('4. Generar licencia', 'Abres la tool interna -> ingresas Account ID + Producto -> obtienes el License Key + archivo .lic'),
    ('5. Registrar en BD', 'La tool registra automaticamente la licencia en la base de datos de auditoria.'),
    ('6. Preparar DLL', 'Tomas la DLL ofuscada correspondiente al producto (ya pre-ofuscada y lista).'),
    ('7. Empaquetar', 'Zip con: DLL ofuscada + archivo .lic + instrucciones de instalacion en PDF'),
    ('8. Enviar al cliente', 'Email automatico o manual con el zip adjunto y las instrucciones.'),
    ('9. Confirmacion', 'El cliente instala y confirma que funciona. Soporte via Discord si es necesario.'),
    ('10. Archivar', 'La orden queda marcada como "completada" en la BD de auditoria.'),
]

for title, desc in steps:
    pdf.set_font(FONT, 'B', 10)
    pdf.set_text_color(0, 212, 170)
    pdf.cell(0, 6, title)
    pdf.ln(6)
    pdf.set_font(FONT, '', 10)
    pdf.set_text_color(220, 220, 220)
    pdf.multi_cell(0, 5.5, desc)
    pdf.ln(3)

# ---- 6.2 PLANTILLA EMAIL ----
pdf.sub_title('6.2 Plantilla de email al cliente')

pdf.set_font('Courier', '', 9)
pdf.set_text_color(0, 212, 170)
pdf.set_fill_color(20, 20, 30)
email_template = (
    'Asunto: [GP Trading] Tu licencia de TradeSyncer PRO v2.0\n'
    '\n'
    'Hola [Nombre],\n'
    '\n'
    'Gracias por tu compra en GP Trading. Adjunto encuentras:\n'
    '\n'
    '  - TradeSyncer PRO v2.0.dll (ofuscada, lista para instalar)\n'
    '  - tradesyncer.lic (tu licencia unica)\n'
    '  - Instrucciones de instalacion.pdf\n'
    '\n'
    'Tu NT8 Account ID registrado: [Account ID]\n'
    'License Key: [GPTR-XXXXX-XXXXX-XXXXX-XXXXX]\n'
    '\n'
    'Pasos para instalar:\n'
    '1. Cierra NinjaTrader 8\n'
    '2. Copia la DLL a: Documents\\NinjaTrader 8\\bin\\Custom\n'
    '3. Crea la carpeta Licenses en: ...\\bin\\Custom\\Licenses\n'
    '4. Copia tradesyncer.lic a esa carpeta\n'
    '5. Abre NinjaTrader 8 y agrega el indicador al grafico\n'
    '\n'
    'Si tienes dudas, responde a este email o escribe a nuestro Discord.\n'
    '\n'
    'Saludos,\n'
    'GP Trading Team')
for line in email_template.split('\n'):
    pdf.cell(10, 4.5, '', fill=True)
    pdf.cell(0, 4.5, line, fill=True)
    pdf.ln()

# ---- 7. FUTURO ----
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, 'F')
pdf.section_title('Planes a Futuro: Automatizacion Total', '7')

pdf.sub_title('7.1 Integracion con Binance Pay')
pdf.body_text(
    'Una vez que el sistema manual de licencias funcione, el siguiente paso es automatizar el proceso '
    'completo desde el pago hasta la entrega de la licencia:')
pdf.ln(2)
pdf.bullet('El usuario paga con Binance Pay en la web')
pdf.bullet('Un Cloudflare Worker recibe el webhook de confirmacion')
pdf.bullet('El worker genera automaticamente el License Key usando el Account ID que ingreso el usuario')
pdf.bullet('El worker envia el email con la DLL + licencia adjunta')
pdf.bullet('El proceso se reduce de 6-12 horas a 1-2 minutos')

pdf.sub_title('7.2 Phone Home opcional')
pdf.body_text(
    'Para proteccion adicional a futuro, cada DLL puede hacer una peticion HTTP al cargar:')
pdf.code_block(
    'GET https://api.gptradingfx.com/validate-license?key=GPTR-XXXXX&product=tradesyncer\n'
    'Respuesta: { "valid": true, "revoked": false }')
pdf.body_text('Si la licencia fue revocada, el indicador muestra error y no funciona.')
pdf.ln(2)
pdf.warning_box(
    'Phone Home requiere que el usuario tenga internet al cargar el indicador. '
    'No recomendado para la version inicial; agregar como capa opcional mas adelante.')

# ---- 8. RECOMENDACIONES ----
pdf.section_title('Recomendaciones Finales', '8')
pdf.ln(2)

recs = [
    'Ofuscar CADA UNA de las 11 DLLs con ConfuserEx antes de distribuir. No saltarse ninguna.',
    'Usar el mismo masterSecret para todas las licencias, pero mantenerlo en un lugar seguro (gestor de contrasenas, variable de entorno).',
    'Probar cada DLL ofuscada en NT8 antes de enviarla al cliente. Errores de ofuscacion pueden romper el indicador.',
    'Comenzar con el proceso manual (6-12h) y automatizar solo cuando el volumen de ventas lo justifique.',
    'No incluir NUNCA el masterSecret en la DLL. La validacion en cliente solo compara hashes, no necesita el secreto.',
    'Tener UNA SOLA BASE DE DATOS de licencias centralizada (SQLite o Google Sheets) para evitar confusiones.',
    'Hacer backups semanales de la base de datos de licencias.',
    'No prometer entrega inmediata: el proceso manual de 6-12h da margen para validacion anti-fraude.',
    'Si un cliente pierde su archivo .lic, puedes regenerarlo (tiene el mismo Account ID -> mismo License Key).',
    'Documentar internamente cada paso del proceso para que otra persona pueda reemplazarte si es necesario.',
]

for i, rec in enumerate(recs, 1):
    pdf.set_font(FONT, '', 10)
    pdf.set_text_color(0, 212, 170)
    pdf.cell(8, 6, f'{i}.')
    pdf.set_text_color(220, 220, 220)
    pdf.multi_cell(0, 6, rec)
    pdf.ln(2)

# ---- 9. APENDICE ----
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, 'F')
pdf.section_title('Apendice: Configuracion ConfuserEx (.crproj)', '9')

pdf.body_text(
    'Este es el archivo de proyecto completo de ConfuserEx para ofuscar indicadores de NinjaTrader 8. '
    'Cambia "TuIndicador.dll" por el nombre real de tu DLL.')
pdf.ln(4)

crproj_content = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<project>\n'
    '  <baseDir>.</baseDir>\n'
    '  <outputDir>Confused</outputDir>\n'
    '  <module path="TuIndicador.dll">\n'
    '    <rule pattern="true" inherit="false">\n'
    '      <protection action="remove" module="rename" />\n'
    '      <protection action="remove" module="ctrl flow" />\n'
    '    </rule>\n'
    '    <rule pattern="public class *Indicator" />\n'
    '    <rule pattern="public class * : NinjaTrader.Gui.NinjaScript.Indicator">\n'
    '      <protection action="remove" module="rename" />\n'
    '    </rule>\n'
    '    <rule pattern="property *">\n'
    '      <protection action="remove" module="rename" />\n'
    '    </rule>\n'
    '    <rule pattern="method *(OnStateChange|OnBarUpdate|Initialize|Terminate)">\n'
    '      <protection action="remove" module="rename" />\n'
    '    </rule>\n'
    '  </module>\n'
    '  <module path="DependenciasCompartidas.dll">\n'
    '    <!-- Si tienes DLLs compartidas, ofuscalas con reglas similares -->\n'
    '  </module>\n'
    '</project>')

pdf.set_font('Courier', '', 8.5)
pdf.set_text_color(0, 212, 170)
pdf.set_fill_color(20, 20, 30)
for line in crproj_content.split('\n'):
    pdf.cell(8, 4.5, '', fill=True)
    pdf.cell(0, 4.5, line, fill=True)
    pdf.ln()

pdf.ln(8)
pdf.body_text(
    'Instrucciones: guarda este contenido como "proyecto.crproj", abrelo con ConfuserEx GUI, '
    'ajusta la ruta de la DLL y haz clic en "Protect". La DLL ofuscada aparecera en la carpeta Confused/.')

pdf.ln(10)
pdf.set_font(FONT, 'I', 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 7, 'Fin del documento - GP Trading Academy - Junio 2026', align='C')

# ---- GUARDAR ----
output_path = os.path.expanduser('~/Downloads/Plan_Proteccion_Codigo_Licencias_GP_Trading.pdf')
pdf.output(output_path)
print(f'PDF generado: {output_path}')
