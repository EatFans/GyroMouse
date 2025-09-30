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
        # 打包静态文件
        ('static', 'static'),
        # 打包文档文件（可选）
        ('doc', 'doc'),
        # 打包README文件
        ('README.md', '.'),
    ],
    hiddenimports=[
        # FastAPI相关
        'fastapi',
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        # pyautogui相关
        'pyautogui',
        'pyautogui._pyautogui_osx',  # macOS
        'pyautogui._pyautogui_win',  # Windows
        'pyautogui._pyautogui_x11',  # Linux
        # 其他依赖
        'qrcode',
        'PIL',
        'socket',
        'json',
        'math',
        'asyncio',
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GyroMouse',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 显示控制台以便查看二维码
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
)