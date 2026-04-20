# Boundary Electron Wrapper (Standalone Backend Edition)

This wrapper launches the packaged backend executable and then opens the Boundary UI.

## CI packaging flow
1. Package backend with PyInstaller
2. Stage backend bundle into `dist-backend`
3. Build Electron installer
4. Publish Release artifacts
