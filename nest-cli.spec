# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('tools', 'tools'), ('/home/khaled/nest-cli/venv/lib/python3.13/site-packages/whois/data/public_suffix_list.dat', 'whois/data')],
    hiddenimports=['runtime_patch', 'tools.nix.management', 'tools.domains.management', 'tools.databases.management', 'tools.github.management', 'tools.caddy.management', 'ai', 'utils', 'colorama', 'requests', 'questionary', 'psycopg2', 'cryptography', 'whois', 'whois.parser'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='nest-cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
