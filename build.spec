# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('tools', 'tools'),  # Include all tool modules
        ('./venv/lib/python3.12/site-packages/whois/data/public_suffix_list.dat', 'whois/data'),  # Whois data
    ],
    hiddenimports=[
        'tools.nix.management',
        'tools.nix.ui',
        'tools.nix.flake_ui',
        'tools.nix.models',
        'tools.domains.management',
        'tools.domains.ui',
        'tools.domains.domain_ui',
        'tools.domains.models',
        'tools.domains.templates',
        'tools.databases.management',
        'tools.databases.ui',
        'tools.github.management',
        'tools.github.ui',
        'tools.github.models',
        'tools.caddy.management',
        'tools.caddy.ui',
        'tools.caddy.models',
        'ai',
        'utils',
        'colorama',
        'requests',
        'questionary',
        'psycopg2',
        'cryptography',
        'whois',
        'whois.parser',
        'json',
        'subprocess',
        'pathlib',
    ],
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
