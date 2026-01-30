import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
print('tesseract_cmd:', pytesseract.pytesseract.tesseract_cmd)
from pytesseract import get_tesseract_version
print('tesseract version from pytesseract:', get_tesseract_version())
