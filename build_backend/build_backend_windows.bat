@echo off
setlocal
python -m pip install -r build_backend\requirements-backend.txt
pyinstaller ^
  --noconfirm ^
  --clean ^
  --onedir ^
  --name boundary-backend ^
  --add-data "api;api" ^
  --add-data "engine;engine" ^
  --add-data "integrations;integrations" ^
  api\server.py
