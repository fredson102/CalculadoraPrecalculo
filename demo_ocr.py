"""Demo rápido: genera una imagen de ejemplo, detecta Tesseract, ejecuta OCR y muestra estadísticas."""

from generate_sample_image import generate_sample
from calculadora import find_tesseract, ocr_to_numbers, estadistica_descriptiva_from_list


def run_demo():
    print('1) Buscando Tesseract...')
    t = find_tesseract()
    if t is None:
        print('   ❌ Tesseract no encontrado. Instálalo con: winget install tesseract-ocr.tesseract')
        return
    print('   ✅ Encontrado:', t)

    print('\n2) Generando imagen de ejemplo...')
    img = generate_sample()
    print('   Imagen:', img)

    print('\n3) Ejecutando OCR...')
    numbers, text = ocr_to_numbers(img)
    print('   Texto extraído:')
    print(text)
    print('   Números detectados:', numbers)

    print('\n4) Estadística:')
    estadistica_descriptiva_from_list(numbers)


if __name__ == '__main__':
    run_demo()
