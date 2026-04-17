#!/usr/bin/env bash
set -euo pipefail
python -m pip install -r requirements_native.txt
python -m pip install pyinstaller
pyinstaller --clean --noconfirm ContinuityEngine.spec
printf '\nBuild complete.\n'
printf 'App bundle/executable is in dist/.\n'
