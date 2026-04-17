@echo off
setlocal
python -m pip install -r requirements_native.txt
python -m pip install pyinstaller
pyinstaller --clean --noconfirm --onedir ContinuityEngine.spec
if errorlevel 1 (
  echo Build failed.
  pause
  exit /b 1
)
echo.
echo Portable folder build complete.
echo Folder: dist\ContinuityEngine\
pause
