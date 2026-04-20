# Standalone Installers

This release flow packages the backend into an executable bundle before building the Electron installers.

## Result
Users no longer need Python installed just to run the desktop app.

## Current behavior
- Windows installer includes packaged backend executable
- macOS disk image includes packaged backend binary
- Electron launches the packaged backend automatically

## Remaining optional hardening
- Windows code signing
- Apple signing + notarization
- hidden-import tuning if future Python dependencies change
