@echo off
echo 🪟 Windows打包脚本启动...
echo ===================================

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查PyInstaller
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 正在安装PyInstaller...
    pip install pyinstaller
)

REM 清理之前的构建
echo 🧹 清理之前的构建文件...
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist __pycache__ rd /s /q __pycache__
if exist GyroMouse_win.spec del /f /q GyroMouse_win.spec

REM 创建Windows特定的spec文件
echo 🔨 创建Windows打包配置...
(
echo # -*- mode: python ; coding: utf-8 -*-
echo.
echo import sys
echo import os
echo.
echo # 获取项目根目录
echo project_root = os.getcwd()
echo.
echo block_cipher = None
echo.
echo # 分析主要脚本
echo a = Analysis^(^
    echo     ['main.py'],^
    echo     pathex=[project_root],^
    echo     binaries=[],^
    echo     datas=[^
    echo         ^('static', 'static'^),^
    echo         ^('doc', 'doc'^),^
    echo         ^('README.md', '.'^),^
    echo     ],^
    echo     hiddenimports=[^
    echo         'fastapi', 'uvicorn', 'uvicorn.logging', 'uvicorn.loops',^
    echo         'uvicorn.loops.auto', 'uvicorn.protocols', 'uvicorn.protocols.http',^
    echo         'uvicorn.protocols.websockets', 'uvicorn.protocols.websockets.auto',^
    echo         'uvicorn.lifespan', 'uvicorn.lifespan.on',^
    echo         'pyautogui', 'pyautogui._pyautogui_win',^
    echo         'qrcode', 'PIL', 'socket', 'json', 'math', 'asyncio',^
    echo     ],^
    echo     hookspath=[],^
    echo     hooksconfig={},^
    echo     runtime_hooks=[],^
    echo     excludes=[],^
    echo     win_no_prefer_redirects=False,^
    echo     win_private_assemblies=False,^
    echo     cipher=block_cipher,^
    echo     noarchive=False,^
    echo ^)
echo.
echo # 创建可执行文件
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
echo.
echo exe = EXE^(^
    echo     pyz,^
    echo     a.scripts,^
    echo     a.binaries,^
    echo     a.zipfiles,^
    echo     a.datas,^
    echo     [],^
    echo     name='GyroMouse',^
    echo     debug=False,^
    echo     bootloader_ignore_signals=False,^
    echo     strip=False,^
    echo     upx=True,^
    echo     upx_exclude=[],^
    echo     runtime_tmpdir=None,^
    echo     console=True,^
    echo     disable_windowed_traceback=False,^
    echo     target_arch=None,^
    echo ^)
) > GyroMouse_win.spec

REM 执行打包
echo 🔨 开始打包Windows版本...
python -m PyInstaller GyroMouse_win.spec --clean

REM 检查打包结果
if %errorlevel% equ 0 (
    echo ✅ Windows打包成功！
    echo 📦 输出文件位于: dist\GyroMouse\
    echo 🚀 运行方式:
    echo    cd dist\GyroMouse\
    echo    GyroMouse.exe
    echo.
    echo 📱 使用说明:
    echo    1. 运行程序后，控制台会显示二维码
    echo    2. 用手机扫描二维码连接
    echo    3. 开始远程控制您的电脑
) else (
    echo ❌ Windows打包失败，请检查错误信息
    pause
    exit /b 1
)

echo ===================================
echo 🎉 Windows打包完成！
pause