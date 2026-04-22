@echo off
echo ============================================
echo  RECOVS â€” Windows Installer
echo ============================================

echo.
echo [1/3] Checking Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found. Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo [2/3] Installing dependencies...
python -m pip install -r requirements.txt --quiet

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo [3/3] Starting Boundary API server...
echo.
echo  Backend:  http://127.0.0.1:8787
echo  UI:       Open web\index.html in your browser
echo.
echo  Press Ctrl+C to stop.
echo.

start "" web\index.html
python -m uvicorn api.server:app --host 127.0.0.1 --port 8787 --reload

pause

