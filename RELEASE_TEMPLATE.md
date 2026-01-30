Release title: vX.Y.Z

Short summary
- One-line summary of the release.

Changes
- Added: feature 1
- Fixed: bug 2
- Improved: CLI usability

Assets
- CalculadoraCLI.exe (Windows single-file executable)

Testing notes
- Tests passed: pytest -q
- Manual test: demo (runs OCR + statistics) successful

How to install (Windows)
1. Download `CalculadoraCLI.exe` from the Release assets.
2. Ensure `Tesseract-OCR` is installed on the system (winget install tesseract-ocr.tesseract).
3. Run `CalculadoraCLI.exe demo` or `CalculadoraCLI.exe stats -d "1,2,3"`.