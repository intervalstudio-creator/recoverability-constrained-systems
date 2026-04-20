#!/usr/bin/env bash
set -e
python3 -m pip install -r build_backend/requirements-backend.txt
pyinstaller   --noconfirm   --clean   --onedir   --name boundary-backend   --add-data "api:api"   --add-data "engine:engine"   --add-data "integrations:integrations"   api/server.py
