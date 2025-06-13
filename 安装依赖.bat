@echo off
chcp 65001 >nul
title Cursor Auto Accept - 依赖安装器

echo.
echo 🔧 Cursor Auto Accept - 依赖安装器
echo ================================================
echo.
echo 🚀 正在安装Python依赖包...
echo 这可能需要几分钟时间，请耐心等待...
echo.

cd /d "%~dp0"

echo 📋 检查Python环境...
py --version
if %errorlevel% neq 0 (
    echo ❌ Python环境未找到！
    echo 请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo 📦 安装依赖包...
py -m pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✅ 依赖包安装成功！
    echo.
    echo 📚 接下来您可以：
    echo 1. 双击"快速启动器.bat"启动模板匹配程序
echo 2. 双击"完整启动器.bat"使用图形选择界面
    echo.
) else (
    echo.
    echo ❌ 依赖包安装失败！
    echo 请检查网络连接或重试
    echo.
)

pause 