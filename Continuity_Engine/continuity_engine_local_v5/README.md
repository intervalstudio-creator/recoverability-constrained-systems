# Continuity Engine v4 Local

A local PC application that evaluates whether continuation remains admissible under recoverability constraints.

## Included in v4

- multi-trajectory recovery evaluation
- point-of-no-return detection
- truth-integrity checks for stale, conflicted, or unverifiable signals
- authority reality checks
- downstream propagation effects
- proof output
- dependency graph visualization
- live simulation toggles for delay, pressure, resonance, truth failure, and authority failure
- explicit connection-state handling
- offline-first fallback mode
- certificate-aware execution analysis for local and remote paths
- JSON and PDF export

## Install

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run:

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python -m streamlit run app.py
```

## Offline-first behavior

This package is designed to keep local evaluation admissible when internet-dependent features fail, provided a valid fallback local mode exists.

- local JSON input works offline
- local reports export offline
- remote/network paths are marked non-admissible when connectivity is lost
- certificate-dependent execution is analyzed separately from local fallback

## Certificates

No certificate is required for ordinary local localhost use.

Certificates matter only when the evaluated path depends on them, for example:
- remote API access
- HTTPS/public hosting
- client-auth integration
- signed distribution

The engine treats missing, expired, revoked, or unreachable certificates as continuity-critical only when the evaluated execution path depends on them.


## Native desktop UI (v5)

This package now includes a native desktop UI in addition to the Streamlit app.

### Run native UI

Windows:
```bash
python -m pip install -r requirements_native.txt
python desktop_app.py
```

Mac / Linux:
```bash
python -m pip install -r requirements_native.txt
python desktop_app.py
```

### Build executable

On the target operating system, build the executable locally.

Windows:
```bash
build_windows_exe.bat
```

Mac / Linux:
```bash
./build_mac_app.sh
```

### Important

Executable builds are OS-specific. Build the Windows `.exe` on Windows, and build the macOS app bundle on macOS.
The engine logic is included in this package; the build step only packages it for the target platform.
