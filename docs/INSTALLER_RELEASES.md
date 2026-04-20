# Installer Releases

Boundary can publish installable releases through GitHub Actions.

## Release flow
1. Commit the Electron wrapper and workflow.
2. Push to `main`.
3. Create a version tag:
   - `git tag v3.2.0`
   - `git push origin v3.2.0`
4. Wait for the `Release Installers` workflow.
5. Download `.exe` and `.dmg` from the GitHub Release.

## Outputs
- Windows: NSIS installer (`.exe`)
- macOS: disk image (`.dmg`)

## Signing
Unsigned builds are supported.
For trusted installs later, add:
- Windows code-signing certificate
- Apple Developer signing + notarization
