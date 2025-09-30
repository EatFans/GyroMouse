#!/bin/bash

echo "🍎 MacOS打包脚本启动..."
echo "==================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到Python3，请先安装Python3"
    exit 1
fi

# 检查PyInstaller
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "📦 正在安装PyInstaller..."
    pip3 install pyinstaller
fi

# 清理之前的构建
echo "🧹 清理之前的构建文件..."
rm -rf build dist __pycache__
rm -f GyroMouse_mac.spec

# 创建MacOS特定的spec文件
cat > GyroMouse_mac.spec << 'EOF'
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
EOF

# 执行打包
echo "🔨 开始打包MacOS版本..."
python3 -m PyInstaller GyroMouse_mac.spec --clean

# 检查打包结果
if [ $? -eq 0 ]; then
    echo "✅ MacOS打包成功！"
    echo "📦 输出文件位于: dist/GyroMouse/"
    echo "🚀 运行方式:"
    echo "   cd dist/GyroMouse/"
    echo "   ./GyroMouse"
    echo ""
    echo "📱 使用说明:"
    echo "   1. 运行程序后，终端会显示二维码"
    echo "   2. 用手机扫描二维码连接"
    echo "   3. 开始远程控制您的电脑"
else
    echo "❌ MacOS打包失败，请检查错误信息"
    exit 1
fi

echo "==================================="
echo "🎉 MacOS打包完成！"