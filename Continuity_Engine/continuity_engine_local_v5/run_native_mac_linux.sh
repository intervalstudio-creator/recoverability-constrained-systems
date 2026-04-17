#!/usr/bin/env bash
set -euo pipefail
python -m pip install -r requirements_native.txt
python desktop_app.py
