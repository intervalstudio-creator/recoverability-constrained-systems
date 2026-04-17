# Continuity Engine v6 Deployment Pack

This release adds a desktop deployment path for Windows with:
- native desktop UI
- no terminal window in the packaged app
- one-folder portable build
- installer script for Inno Setup
- local icon asset
- offline-first and certificate-aware runtime preserved

## Run directly from source

```bash
python -m pip install -r requirements_native.txt
python desktop_app.py
```

## Build portable Windows app

Run:

```bat
build_windows_portable.bat
```

Expected output:
- `dist\ContinuityEngine\ContinuityEngine.exe`

## Build Windows installer

1. Install Inno Setup.
2. Run:

```bat
build_windows_installer.bat
```

Expected output:
- `installer_dist\ContinuityEngineInstaller_v6.exe`

## Notes

- Build the Windows release on Windows.
- The packaged app is local-first and does not require Wi-Fi for local execution.
- Remote features remain dependency-aware and can be blocked independently when network or certificate conditions fail.
