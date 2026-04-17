# PyInstaller spec for native Continuity Engine v5
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

project_dir = Path(__file__).resolve().parent

datas = []
datas += collect_data_files('matplotlib')
datas += [
    (str(project_dir / 'sample_cases'), 'sample_cases'),
    (str(project_dir / 'templates'), 'templates'),
    (str(project_dir / 'continuity_engine'), 'continuity_engine'),
]

block_cipher = None

a = Analysis(
    ['desktop_app.py'],
    pathex=[str(project_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=['PySide6', 'matplotlib.backends.backend_qtagg'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ContinuityEngine',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
