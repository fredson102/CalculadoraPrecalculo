"""
Calculadora completa: ÁLGEBRA, FUNCIONES, TRIGONOMETRÍA, APLICACIONES y ESTADÍSTICA
Incluye integración con Tesseract OCR. Ejecuta `python calculadora_completa.py --demo`
para ejecutar el demo (genera imagen de ejemplo → OCR → estadísticas) y salir.
"""

import math
import sys
from collections import Counter
import numpy as np

# Intentar importar módulos opcionales
try:
    import pytesseract
    from PIL import Image
except Exception:
    pytesseract = None
    Image = None

# Import demo helpers si existen
try:
    from generate_sample_image import generate_sample
except Exception:
    generate_sample = None


# ---------------------- UTILIDADES ----------------------

def find_tesseract():
    """Detecta la instalación de Tesseract y configura pytesseract si está presente."""
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]

    try:
        import subprocess
        proc = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
        if proc.returncode == 0:
            if pytesseract:
                pytesseract.pytesseract.tesseract_cmd = "tesseract"
            return "tesseract"
    except Exception:
        pass

    for p in possible_paths:
        try:
            with open(p, 'rb'):
                if pytesseract:
                    pytesseract.pytesseract.tesseract_cmd = p
                return p
        except Exception:
            continue

    return None


# ---------------------- ÁLGEBRA ----------------------

def resolver_ecuacion_lineal():
    print("\n" + "="*50)
    print("ECUACIÓN LINEAL: ax + b = c")
    print("="*50)
    a = float(input("Coeficiente a: "))
    b = float(input("Término independiente b: "))
    c = float(input("Lado derecho c: "))
    print(f"\nPASO A PASO:")
    print(f"1. Ecuación original: {a}x + {b} = {c}")
    print(f"2. Restar {b} en ambos lados:")
    print(f"   {a}x = {c} - {b} = {c - b}")
    print(f"3. Dividir entre {a}:")
    print(f"   x = {c - b} / {a}")
    solucion = (c - b) / a
    print(f"4. Solución: x = {solucion}")
    return solucion


def resolver_ecuacion_cuadratica():
    print("\n" + "="*50)
    print("ECUACIÓN CUADRÁTICA: ax² + bx + c = 0")
    print("="*50)
    a = float(input("Coeficiente a: "))
    b = float(input("Coeficiente b: "))
    c = float(input("Coeficiente c: "))
    discriminante = b**2 - 4*a*c
    print(f"Discriminante: D = {discriminante}")
    if discriminante > 0:
        x1 = (-b + math.sqrt(discriminante)) / (2*a)
        x2 = (-b - math.sqrt(discriminante)) / (2*a)
        print(f"x1 = {x1}, x2 = {x2}")
        return [x1, x2]
    elif discriminante == 0:
        x = -b / (2*a)
        print(f"x = {x}")
        return [x]
    else:
        real = -b / (2*a)
        imag = math.sqrt(-discriminante) / (2*a)
        print(f"x1 = {real} + {imag}i, x2 = {real} - {imag}i")
        return [complex(real, imag), complex(real, -imag)]


def sistema_ecuaciones_lineales():
    print("\nSISTEMA 2x2")
    a1 = float(input("a₁: "))
    b1 = float(input("b₁: "))
    c1 = float(input("c₁: "))
    a2 = float(input("a₂: "))
    b2 = float(input("b₂: "))
    c2 = float(input("c₂: "))
    det = a1*b2 - a2*b1
    if det != 0:
        x = (c1*b2 - c2*b1) / det
        y = (a1*c2 - a2*c1) / det
        print(f"SOLUCIÓN: x = {x:.4f}, y = {y:.4f}")
        return x, y
    else:
        print("Sistema sin solución única (determinante=0)")
        return None


# ---------------------- FUNCIONES ----------------------

def funcion_exponencial():
    a = float(input("Coeficiente a: "))
    b = float(input("Base b (b>0, b≠1): "))
    h = float(input("Desplazamiento horizontal h: "))
    k = float(input("Desplazamiento vertical k: "))
    print(f"f(x) = {a}*{b}^(x-{h}) + {k}")
    for x in np.linspace(-2, 4, 7):
        y = a * (b ** (x - h)) + k
        print(f"x={x:.2f} → {y:.4f}")


def funcion_logaritmica():
    a = float(input("Coeficiente a: "))
    b = float(input("Base b (b>0, b≠1): "))
    h = float(input("Desplazamiento horizontal h: "))
    k = float(input("Desplazamiento vertical k: "))
    start = max(h + 0.1, 0.1)
    for x in np.linspace(start, start + 5, 6):
        y = a * math.log(x - h, b) + k
        print(f"x={x:.2f} → {y:.4f}")


# ---------------------- TRIGONOMETRÍA ----------------------

def trigonometria_basica():
    print("1: Resolver triángulo; 2: Convertir; 3: Valores trig")
    opcion = input("Selecciona (1-3): ")
    if opcion == "1":
        lado1 = float(input("Cateto 1: "))
        lado2 = float(input("Cateto 2: "))
        hip = math.sqrt(lado1**2 + lado2**2)
        ang1 = math.degrees(math.atan2(lado1, lado2))
        ang2 = 90 - ang1
        print(f"Hipotenusa={hip:.4f}, ángulos={ang1:.2f}°, {ang2:.2f}°")
    elif opcion == "2":
        valor = float(input("Valor: "))
        tipo = input("Es grados (G) o radianes (R)? ").upper()
        if tipo == 'G':
            print(f"{valor}° = {math.radians(valor):.4f} rad")
        else:
            print(f"{valor} rad = {math.degrees(valor):.2f}°")
    else:
        ang = float(input("Ángulo en grados: "))
        r = math.radians(ang)
        print(f"sen={math.sin(r):.4f}, cos={math.cos(r):.4f}, tan={math.tan(r):.4f}")


# ---------------------- APLICACIONES ----------------------

def interes_compuesto():
    P = float(input("Capital inicial (P): "))
    i = float(input("Tasa anual (i) en decimal: "))
    t = float(input("Tiempo (t) en años: "))
    n = int(input("Capitalizaciones por año (ej: 1,2,4,12): "))
    factor = (1 + i/n) ** (n*t)
    A = P * factor
    print(f"Monto final A={A:.2f}, interés={A-P:.2f}")


# ---------------------- ESTADÍSTICA ----------------------

def estadistica_descriptiva():
    datos_str = input("Ingresa datos separados por comas: ")
    datos = [float(x.strip()) for x in datos_str.split(',') if x.strip()]
    estadistica_descriptiva_from_list(datos)


def compute_statistics(datos):
    """Devuelve un dict con estadísticas calculadas para una lista numérica."""
    datos = [float(x) for x in datos]
    n = len(datos)
    if n == 0:
        return None

    datos_ordenados = sorted(datos)
    suma = sum(datos)
    media = suma / n

    suma_cuad = sum((x - media) ** 2 for x in datos)
    var_p = suma_cuad / n
    sd_p = math.sqrt(var_p)

    var_s = suma_cuad / (n - 1) if n > 1 else float('nan')
    sd_s = math.sqrt(var_s) if n > 1 else float('nan')

    q1 = np.percentile(datos, 25)
    q2 = np.percentile(datos, 50)
    q3 = np.percentile(datos, 75)
    iqr = q3 - q1

    return {
        'n': n,
        'data': datos,
        'sorted': datos_ordenados,
        'sum': suma,
        'mean': media,
        'var_p': var_p,
        'sd_p': sd_p,
        'var_s': var_s,
        'sd_s': sd_s,
        'q1': q1,
        'q2': q2,
        'q3': q3,
        'iqr': iqr,
    }


def estadistica_descriptiva_from_list(datos, verbose=True):
    """Imprime estadísticas paso a paso y devuelve el diccionario de estadísticas."""
    stats = compute_statistics(datos)
    if stats is None:
        print("No hay datos para analizar.")
        return None

    if verbose:
        print(f"\nDATOS: {stats['data']}")
        print(f"Cantidad (n): {stats['n']}")
        print(f"\n1. DATOS ORDENADOS: {stats['sorted']}")
        print(f"\n2. MEDIA (PROMEDIO):")
        print(f"   Media = Σx / n = {stats['sum']} / {stats['n']} = {stats['mean']:.4f}")
        print(f"\n3. MEDIANA: {stats['q2']:.4f}")
        print(f"\n4. MODA: (para simplicidad se omite cálculo exacto aquí)")
        print(f"\n5. RANGO: máximo - mínimo = {max(stats['data'])} - {min(stats['data'])} = {max(stats['data']) - min(stats['data'])}")
        print(f"\n6. VARIANZA POBLACIONAL = {stats['var_p']:.4f}")
        print(f"   DESVIACIÓN POBLACIONAL = {stats['sd_p']:.4f}")
        if stats['n'] > 1:
            print(f"\n7. VARIANZA MUESTRAL = {stats['var_s']:.4f}")
            print(f"   DESVIACIÓN MUESTRAL = {stats['sd_s']:.4f}")
        print(f"\n8. CUARTILES: Q1={stats['q1']:.4f}, Q2={stats['q2']:.4f}, Q3={stats['q3']:.4f}, IQR={stats['iqr']:.4f}")
        print('\n' + '='*50)
        print('RESUMEN:')
        print(f"• n = {stats['n']}")
        print(f"• Mínimo = {min(stats['data']):.4f}")
        print(f"• Máximo = {max(stats['data']):.4f}")
        print(f"• Media = {stats['mean']:.4f}")
        print(f"• Mediana = {stats['q2']:.4f}")
        print(f"• Desviación estándar = {stats['sd_p']:.4f}")

    return stats


# ---------------------- OCR → ESTADÍSTICA ----------------------

def ocr_to_numbers(img_path):
    if pytesseract is None or Image is None:
        raise RuntimeError('pytesseract o PIL no instalados.')
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    import re
    matches = re.findall(r"[-+]?[0-9]*\.?[0-9]+", text)
    numbers = [float(m) for m in matches]
    return numbers, text


def save_stats_to_csv(stats, path):
    """Guarda los datos y resumen estadístico en CSV."""
    import csv
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['value'])
        for v in stats['data']:
            writer.writerow([v])
        writer.writerow([])
        writer.writerow(['n', stats['n']])
        writer.writerow(['mean', stats['mean']])
        writer.writerow(['var_p', stats['var_p']])
        writer.writerow(['sd_p', stats['sd_p']])
    print(f"Guardado en {path}")


def ocr_estadistica(img_path=None):
    print('\nOCR → ESTADÍSTICA')
    if find_tesseract() is None:
        print('Tesseract no encontrado. Instala el ejecutable y vuelve a intentarlo.')
        return
    if img_path is None:
        if generate_sample is None:
            print('No hay función de muestra para generar imagen. Instala Pillow.')
            return
        img_path = generate_sample()
        print('Imagen de muestra generada en:', img_path)
    numbers, text = ocr_to_numbers(img_path)
    print('\nTEXTO EXTRAÍDO:')
    print(text)
    if not numbers:
        print('No se detectaron números en la imagen.')
        return
    print('Números:', numbers)
    stats = estadistica_descriptiva_from_list(numbers)

    # Preguntar si guardar
    guardar = input('\n¿Deseas guardar los resultados a CSV? (S/N): ').strip().lower()
    if guardar == 's':
        path = input('Nombre de archivo (ej: resultados.csv): ').strip()
        if not path:
            path = 'resultados.csv'
        save_stats_to_csv(stats, path)
    return stats


# ---------------------- MENÚ COMPLETO ----------------------

def mostrar_menu():
    print('\n' + '='*60)
    print('CALCULADORA UNIVERSAL - PRECÁLCULO, MATEMÁTICAS, ESTADÍSTICA')
    print('='*60)
    print('1.1 Ecuación lineal')
    print('1.2 Ecuación cuadrática')
    print('1.3 Sistema 2x2')
    print('2.1 Función exponencial')
    print('2.2 Función logarítmica')
    print('3.1 Trigonometría básica')
    print('4.1 Interés compuesto')
    print('5.1 Estadística manual')
    print('5.2 Estadística desde imagen (OCR)')
    print('5.3 Exportar datos a CSV (ingresa datos manualmente)')
    print('0. Salir')


def main():
    print('\n¡BIENVENIDO A LA CALCULADORA COMPLETA!')
    print('Si quieres demo rápido ejecuta: python calculadora_completa.py --demo')
    while True:
        mostrar_menu()
        opc = input('\nSelecciona opción (ej: 1.1, 5.2, 0): ').strip()
        if opc == '0':
            print('Hasta luego')
            break
        elif opc == '1.1':
            resolver_ecuacion_lineal()
        elif opc == '1.2':
            resolver_ecuacion_cuadratica()
        elif opc == '1.3':
            sistema_ecuaciones_lineales()
        elif opc == '2.1':
            funcion_exponencial()
        elif opc == '2.2':
            funcion_logaritmica()
        elif opc == '3.1':
            trigonometria_basica()
        elif opc == '4.1':
            interes_compuesto()
        elif opc == '5.1':
            estadistica_descriptiva()
        elif opc == '5.2':
            ocr_estadistica()
        elif opc == '5.3':
            datos_str = input('\nIngresa datos separados por comas: ')
            datos = [float(x.strip()) for x in datos_str.split(',') if x.strip()]
            stats = estadistica_descriptiva_from_list(datos)
            if stats:
                path = input('Nombre de archivo para guardar (ej: datos.csv), dejar vacío para omitir: ').strip()
                if path:
                    save_stats_to_csv(stats, path)
        else:
            print('Opción no válida')


# ---------------------- EJECUCIÓN / DEMO ----------------------

if __name__ == '__main__':
    if '--demo' in sys.argv:
        print('Demo: OCR → estadísticas (generando imagen de ejemplo)')
        # Detect tesseract
        t = find_tesseract()
        if t is None:
            print('Tesseract no encontrado. Instálalo antes de ejecutar demo.')
            sys.exit(1)
        if generate_sample is None:
            print('Falta generate_sample (Pillow). No puedo crear imagen generada.')
            sys.exit(1)
        img = generate_sample()
        print('Imagen generada:', img)
        numbers, text = ocr_to_numbers(img)
        print('\nTexto extraído:')
        print(text)
        print('\nNúmeros detectados:', numbers)
        estadistica_descriptiva_from_list(numbers)
        sys.exit(0)

    # Si no demo, ejecutar el menú interactivo
    main()
