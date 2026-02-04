# CalculadoraPrecalculo — Reproducibilidad y OCR

Esta carpeta contiene una calculadora educativa con **OCR integrado (pytesseract)** para extraer datos de imágenes y calcular estadísticas paso a paso.

## Requisitos
- Python 3.10+ (recomendado 3.11)
- Windows (instrucciones para Windows aquí)
- Tesseract-OCR instalado (binario) - no solo el paquete pip

## Pasos para reproducir (Windows)
1. Crear y activar entorno virtual:

   PowerShell:
   ```powershell
   py -3 -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Instalar dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

3. Instalar Tesseract (si no está instalado):

   ```powershell
   winget install tesseract-ocr.tesseract -e --accept-package-agreements --accept-source-agreements
   ```

   Si no puedes usar winget, descarga el instalador desde:
   https://github.com/tesseract-ocr/tesseract/releases


4. Ejecutar demo (genera una imagen de muestra, hace OCR y muestra estadísticas):

   ```powershell
   .\venv\Scripts\python.exe demo_ocr.py
   ```

5. Ejecutar la calculadora interactiva (opción 5.2 para OCR):

   ```powershell
   .\venv\Scripts\python.exe calculadora.py
   ```

---

## Ejecutable Windows (.exe)
El workflow de GitHub Actions genera dos ejecutables en cada release:

- `CalculadoraCLI.exe`
- `calculadora_cli.exe`

Ambos funcionan igual. Descarga cualquiera desde la sección **Releases** en GitHub.

### Uso básico del EXE

```powershell
CalculadoraCLI.exe demo
CalculadoraCLI.exe stats -d "1,2,3,4" -o resultados.csv
CalculadoraCLI.exe stats-image -i sample_numbers.png -o resultados.csv
CalculadoraCLI.exe interactive
```

### Si el EXE se cierra inmediatamente o muestra error
El ejecutable ahora incluye manejo robusto de errores: si ocurre un error inesperado, se mostrará el mensaje y el traceback, y el programa esperará a que presiones ENTER antes de cerrarse. Así puedes ver qué ocurrió y reportar el error.

Si ves un error relacionado con Tesseract, asegúrate de tenerlo instalado y accesible en tu sistema.

## Archivos importantes
- `calculadora.py` — Programa principal con opción OCR (5.2) y estadística.
- `demo_ocr.py` — Demo reproducible que genera imagen, ejecuta OCR y muestra resultados.
- `generate_sample_image.py` — Genera una imagen `sample_numbers.png` para pruebas.
- `requirements.txt` — Dependencias Python.

## Notas
- `pytesseract` es una interfaz Python que requiere la instalación del **ejecutable de Tesseract** en el sistema. `calculadora.py` intenta detectar la ubicación más común (`C:\Program Files\Tesseract-OCR\tesseract.exe`) y configurarla automáticamente.
- Si Tesseract no se encuentra en PATH pero está instalado en `C:\Program Files\Tesseract-OCR`, no necesitas modificar PATH ya que `calculadora.py` la detectará.

---

## Setup rápido (PowerShell)
Puedes ejecutar el script `setup.ps1` para crear el `venv`, instalar dependencias y (opcionalmente) lanzar la instalación de Tesseract via `winget`:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
```

---

## Tests
Instala las dependencias de test (`pytest`) y ejecuta:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

---

## Interfaz CLI
He añadido `calculadora_cli.py` para usar la calculadora desde la línea de comando o lanzar la interfaz interactiva.

Ejemplos:
```powershell
# Demo (genera imagen de muestra y corre OCR+estadística)
.\venv\Scripts\python.exe calculadora_cli.py demo

# Estadística desde datos manuales y guardar resultados
.\venv\Scripts\python.exe calculadora_cli.py stats -d "12,7.5,3,9.25,14" -o resultados.csv

# Estadística desde imagen
.\venv\Scripts\python.exe calculadora_cli.py stats-image -i sample_numbers.png -o resultados.csv

# Interactivo (menú completo)
.\venv\Scripts\python.exe calculadora_cli.py interactive
```

---

Se añadieron las siguientes mejoras recientemente:
- Tests automatizados para OCR y estadísticas
- Script `setup.ps1` para preparar el entorno
- Opción para exportar resultados a CSV desde el menú interactivo
- Interfaz CLI (`calculadora_cli.py`) y salida con `rich` para mejor legibilidad
- Flujo de CI (GitHub Actions) que genera un instalable Windows (.exe) por cada "tag" `v*` y sube el artefacto (dist/CalculadoraCLI.exe)

---

## Cómo crear una release y obtener el ejecutable (Windows)
1. Actualiza `CHANGELOG.md` (add the release notes).

2. Create and push a tag in your local repo, for example `v1.0.0`:

   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

3. Al hacer push de un tag (p. ej. `v1.0.0`), el workflow `Build and Release Windows EXE` se ejecutará automáticamente y creará una GitHub Release.

4. El workflow compila `CalculadoraCLI.exe` y lo adjunta directamente al Release como asset. Ve a la pestaña **Releases** en GitHub para descargar el ejecutable final (más sencillo que descargar artifacts desde Actions).

5. Verificación adicional (opcional): descarga la EXE y ejecuta `CalculadoraCLI.exe demo` en una máquina Windows con Tesseract instalado para comprobar la funcionalidad OCR.

---

## Distribución recomendada
- Para usar todas las funciones (OCR) en la máquina destino, asegúrate de que Tesseract OCR esté instalado (por ejemplo mediante `winget install tesseract-ocr.tesseract` o el instalador oficial). El ejecutable busca `tesseract` en PATH o en `C:\Program Files\Tesseract-OCR\tesseract.exe`.

- Si quieres que yo prepare un instalador (MSI) o un paquete con el instalador de Tesseract incluido, puedo hacerlo, pero requiere más pasos y decisiones sobre empaquetado/licencias.

---

Si quieres, puedo:
- Añadir pruebas en CI (GitHub Actions) para ejecutar `pytest` automáticamente ✅
- Añadir exportación a formatos adicionales (Excel) ✅
- Añadir logging y mejor manejo de errores en todo el proyecto ✅

¿Deseas que añada pruebas de CI (GitHub Actions) para ejecutar `pytest` automáticamente? 🔧