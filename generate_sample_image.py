from PIL import Image, ImageDraw, ImageFont
import os


def generate_sample(path='sample_numbers.png'):
    """Genera una imagen simple con números separados por comas para pruebas OCR."""
    text = '12, 7.5, 3, 9.25, 14'
    width, height = 800, 200
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        # Intentar cargar una fuente del sistema
        font = ImageFont.truetype('arial.ttf', 48)
    except Exception:
        font = ImageFont.load_default()

    try:
        # Pillow >= 8.0: textbbox disponible
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except AttributeError:
        # Fallback para versiones antiguas
        text_w, text_h = font.getsize(text)

    x = (width - text_w) // 2
    y = (height - text_h) // 2
    draw.text((x, y), text, font=font, fill=(0, 0, 0))

    image.save(path)
    return os.path.abspath(path)


if __name__ == '__main__':
    p = generate_sample()
    print('Generated sample image:', p)
