@echo off
chcp 65001 >nul
title Cursor Auto Accept - 模板匹配版本

echo.
echo 🖼️ Cursor Auto Accept - 图像模板匹配版本
echo ================================================
echo.
echo 🚀 正在启动模板匹配版本程序...
echo 💡 提示: 此版本使用OpenCV图像匹配识别Accept按钮
echo 📸 记得先加载或截取Accept按钮模板图片
echo.

cd /d "%~dp0"

py cursor-auto-clicker-template.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ 程序启动失败！
    echo 可能的原因：
    echo 1. Python环境未正确安装
    echo 2. 依赖包未安装，请先运行"安装依赖.bat"
    echo 3. 程序文件损坏
    echo.
    pause
)

exit 