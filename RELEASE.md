Release checklist — CalculadoraPrecalculo

This document lists the recommended steps to create a release and publish the Windows executable using the project's CI.

1) Ensure code is committed and tests pass locally
   - .\venv\Scripts\python.exe -m pytest -q

2) Update version and CHANGELOG
   - Edit `CHANGELOG.md` with the new version and notes.

3) Create a signed tag and push to GitHub
   - git tag -a vX.Y.Z -m "Release vX.Y.Z"
   - git push origin vX.Y.Z

4) Verify the GitHub Actions `Build and Release Windows EXE` runs successfully
   - Go to the repository -> Actions -> select "Build and Release Windows EXE" run for the tag.

5) Download the release asset
   - After the workflow completes, a Release will be created and `CalculadoraCLI.exe` will be attached as an asset. Download from GitHub Releases.

6) Verify the downloaded EXE on a clean Windows machine
   - Ensure Tesseract OCR is installed (winget install tesseract-ocr.tesseract) before running OCR features.

7) Publish release notes and mark the release as a stable release (if applicable)

Optional extras
- Code-signing: sign the EXE with a code signing certificate to avoid SmartScreen warnings.
- MSI installer: create an MSI if you want a richer installer experience for end-users.

Notes
- The CI build runs tests before building; if tests fail the build is aborted.
- If you prefer to keep the release private, create a draft release and upload the EXE manually from the Actions run artifacts.