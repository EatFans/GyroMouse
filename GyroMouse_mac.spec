# -*- mode: python ; coding: utf-8 -*-

import sys
import os

# 获取项目根目录
project_root = os.getcwd()

block_cipher = None

# 分析主要脚本
a = Analysis(
    ['main.py'],
    pathex=[project_root],
    binaries=[],
    datas=[
        ('static', 'static'),
        ('doc', 'doc'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'fastapi', 'uvicorn', 'uvicorn.logging', 'uvicorn.loops',
        'uvicorn.loops.auto', 'uvicorn.protocols', 'uvicorn.protocols.http',
        'uvicorn.protocols.websockets', 'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan', 'uvicorn.lifespan.on',
        'pyautogui', 'pyautogui._pyautogui_osx',
        'qrcode', 'PIL', 'socket', 'json', 'math', 'asyncio',
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

# 创建可执行文件
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GyroMouse',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GyroMouse',
)
