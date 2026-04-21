#!/usr/bin/env bash
set -e

echo "============================================"
echo " Boundary Platform v4.0 — Mac/Linux Installer"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Install from https://python.org"
    exit 1
fi

echo "[1/3] Python found: $(python3 --version)"

echo "[2/3] Installing dependencies..."
python3 -m pip install -r requirements.txt --quiet

echo "[3/3] Starting Boundary API server..."
echo ""
echo "  Backend:  http://127.0.0.1:8787"
echo "  UI:       Open app/index.html in your browser"
echo ""
echo "  Press Ctrl+C to stop."
echo ""

# Open UI in browser
if command -v open &> /dev/null; then
    open app/index.html
elif command -v xdg-open &> /dev/null; then
    xdg-open app/index.html
fi

python3 -m uvicorn api.server:app --host 127.0.0.1 --port 8787 --reload
