"""
CALCULADORA UNIVERSAL DE PRECÁLCULO, MATEMÁTICAS Y ESTADÍSTICA
Incluye integración con Tesseract OCR para extraer datos desde imágenes.
"""

import math
import re
import sys
from collections import Counter

import numpy as np

# Optional imports (may not be available in all environments until installed)
try:
    import pytesseract
    from PIL import Image
except Exception:
    pytesseract = None
    Image = None


# ---------------------- UTILIDADES TESSERACT ----------------------

def find_tesseract():
    """Detecta la instalación de Tesseract en Windows y configura pytesseract.
    Devuelve la ruta al ejecutable o None si no se encuentra."""
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]

    # Intentar ejecutar tesseract directamente si está en PATH
    try:
        import subprocess
        proc = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
        if proc.returncode == 0:
            return "tesseract"
    except Exception:
        pass

    # Buscar en rutas comunes
    for p in possible_paths:
        try:
            with open(p, 'rb'):
                if pytesseract:
                    pytesseract.pytesseract.tesseract_cmd = p
                return p
        except Exception:
            continue

    return None


# ---------------------- ESTADÍSTICA (de lista) ----------------------

def estadistica_descriptiva_from_list(datos):
    """Calcula y muestra estadísticas paso a paso para una lista de números."""
    datos = [float(x) for x in datos]
    n = len(datos)

    print(f"\nDATOS: {datos}")
    print(f"Cantidad (n): {n}")

    datos_ordenados = sorted(datos)
    print(f"\n1. DATOS ORDENADOS: {datos_ordenados}")

    suma = sum(datos)
    media = suma / n
    print(f"\n2. MEDIA (PROMEDIO):")
    print(f"   Media = Σx / n = {suma} / {n} = {media:.4f}")

    if n % 2 == 0:
        mediana = (datos_ordenados[n//2 - 1] + datos_ordenados[n//2]) / 2
    else:
        mediana = datos_ordenados[n//2]

    print(f"\n3. MEDIANA: {mediana}")

    frecuencias = Counter(datos)
    moda_frecuencia = max(frecuencias.values())
    modas = [k for k, v in frecuencias.items() if v == moda_frecuencia]

    print(f"\n4. MODA: {modas} (frecuencia: {moda_frecuencia})")

    rango = max(datos) - min(datos)
    print(f"\n5. RANGO: máximo - mínimo = {max(datos)} - {min(datos)} = {rango}")

    suma_cuadrados = sum((x - media) ** 2 for x in datos)
    varianza_pob = suma_cuadrados / n
    desviacion_pob = math.sqrt(varianza_pob)

    print(f"\n6. VARIANZA POBLACIONAL = {varianza_pob:.4f}")
    print(f"   DESVIACIÓN POBLACIONAL = {desviacion_pob:.4f}")

    if n > 1:
        varianza_muestral = suma_cuadrados / (n - 1)
        desviacion_muestral = math.sqrt(varianza_muestral)
        print(f"\n7. VARIANZA MUESTRAL = {varianza_muestral:.4f}")
        print(f"   DESVIACIÓN MUESTRAL = {desviacion_muestral:.4f}")

    q1 = np.percentile(datos, 25)
    q2 = np.percentile(datos, 50)
    q3 = np.percentile(datos, 75)
    print(f"\n8. CUARTILES: Q1={q1:.4f}, Q2={q2:.4f}, Q3={q3:.4f}, IQR={q3 - q1:.4f}")

    print('\n' + '='*50)
    print('RESUMEN:')
    print(f'• n = {n}')
    print(f'• Mínimo = {min(datos):.4f}')
    print(f'• Máximo = {max(datos):.4f}')
    print(f'• Media = {media:.4f}')
    print(f'• Mediana = {mediana:.4f}')
    print(f'• Moda = {modas}')
    print(f'• Desviación estándar = {desviacion_pob:.4f}')


# ---------------------- OCR A ESTADÍSTICA ----------------------

def ocr_to_numbers(img_path):
    """Extrae números desde una imagen usando pytesseract y devuelve lista de floats."""
    if pytesseract is None or Image is None:
        raise RuntimeError("pytesseract o PIL no están instalados en el entorno. Instala las dependencias.")

    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)

    # Buscar números (enteros o decimales, con signo opcional)
    matches = re.findall(r"[-+]?[0-9]*\.?[0-9]+", text)
    numbers = [float(m) for m in matches]
    return numbers, text


def ocr_estadistica(img_path=None):
    """Ejecuta OCR en una imagen y llama a estadistica_descriptiva_from_list.
    Si img_path es None, propone generar/usar una imagen de ejemplo."""
    print('\n' + '='*50)
    print('OCR → ESTADÍSTICA')
    print('='*50)

    if find_tesseract() is None:
        print('❌ Tesseract no encontrado. Instálalo (Windows: "winget install tesseract-ocr.tesseract")')
        return

    if img_path is None:
        img_path = input('Ruta de la imagen (o deja vacío para generar muestra): ').strip()

    if not img_path:
        # Generar imagen de muestra
        from generate_sample_image import generate_sample
        img_path = generate_sample()
        print(f'Imagen de muestra creada en: {img_path}')

    try:
        numbers, raw_text = ocr_to_numbers(img_path)
        print('\nTEXTO EXTRAÍDO:')
        print(raw_text)
        if not numbers:
            print('\n❌ No se encontraron números en la imagen.')
            return

        print(f'\nNúmeros detectados: {numbers}')
        estadistica_descriptiva_from_list(numbers)
    except Exception as e:
        print(f'❌ Error al ejecutar OCR: {e}')


# ---------------------- MENÚ BÁSICO (solo integra OCR y estadísticas) ----------------------

def mostrar_menu():
    print('\n' + '='*60)
    print('CALCULADORA UNIVERSAL - PRECÁLCULO, MATEMÁTICAS, ESTADÍSTICA')
    print('='*60)
    print('\n5. ESTADÍSTICA')
    print('   5.1 Estadística descriptiva manual')
    print('   5.2 Estadística desde imagen (OCR)')
    print('\n0. SALIR')


def main():
    print('\n¡BIENVENIDO A LA CALCULADORA UNIVERSAL!')
    while True:
        mostrar_menu()
        opcion = input('\nSelecciona una opción (ej: "5.1", "5.2", "0"): ').strip()
        if opcion == '0':
            print('\n¡Gracias por usar la calculadora!')
            break
        elif opcion == '5.1':
            datos_str = input('\nIngresa datos separados por comas: ')
            datos = [float(x.strip()) for x in datos_str.split(',') if x.strip()]
            estadistica_descriptiva_from_list(datos)
        elif opcion == '5.2':
            ocr_estadistica()
        else:
            print('\n❌ Opción no válida.')


if __name__ == '__main__':
    main()
