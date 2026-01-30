import pytest
from generate_sample_image import generate_sample

pytest.importorskip('pytesseract')

from calculadora_completa import ocr_to_numbers, find_tesseract


def test_ocr_extracts_numbers(tmp_path):
    if find_tesseract() is None:
        pytest.skip("Tesseract not found on system")

    img = generate_sample(str(tmp_path / "sample.png"))
    nums, text = ocr_to_numbers(img)
    # comparar con redondeo a 2 decimales para robustez
    nums_rounded = [round(n, 2) for n in nums]
    assert nums_rounded == [12.0, 7.5, 3.0, 9.25, 14.0]
