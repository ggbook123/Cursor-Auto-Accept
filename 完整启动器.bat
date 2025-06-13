@echo off
chcp 65001 >nul
title Cursor Auto Accept - 程序启动器

:main_menu
cls
echo.
echo 🎯 Cursor Auto Accept - 程序启动器
echo ================================================
echo.
echo 请选择操作：
echo.
echo 1. 🖼️ 启动图像模板匹配程序 ⭐ 推荐
echo    └─ 使用图像模板匹配识别Accept按钮
echo    └─ 🔥 支持F2全局热键启停监听
echo    └─ 💾 配置自动保存和加载
echo    └─ 🚀 可选择启动时自动开始监听
echo.
echo 2. 🔧 安装依赖包
echo    └─ 安装运行所需的Python依赖包
echo.
echo 3. ❓ 帮助信息
echo    └─ 查看使用说明和故障排除
echo.
echo 4. 🚪 退出程序
echo.

set /p choice=请输入选择 (1-4): 

if "%choice%"=="1" goto start_template
if "%choice%"=="2" goto install_deps
if "%choice%"=="3" goto show_help
if "%choice%"=="4" goto exit_program

echo.
echo ❌ 无效选择，请输入 1-4 之间的数字
timeout /t 2 >nul
goto main_menu

:start_template
cls
echo.
echo 🚀 启动图像模板匹配程序...
echo 💡 提示: 首次使用请在"模板管理"中加载模板
echo ⚡ 配置会自动保存，下次启动无需重新设置
echo.
cd /d "%~dp0"
py cursor-auto-clicker-template.py
goto main_menu

:install_deps
cls
echo.
echo 🔧 启动依赖安装程序...
echo.
cd /d "%~dp0"
call "安装依赖.bat"
pause
goto main_menu

:show_help
cls
echo.
echo ❓ Cursor Auto Accept 使用帮助
echo ================================================
echo.
echo 📖 程序说明:
echo   这是一个自动点击Cursor IDE中Accept按钮的外部工具程序。
echo   类似游戏外挂的工作原理，通过屏幕监听检测按钮并自动点击。
echo.
echo 🖼️ 图像模板匹配程序: ⭐ 推荐
echo   • 使用OpenCV图像匹配算法识别按钮
echo   • 💾 配置自动保存：无需重复设置模板和参数
echo   • 🚀 自动启动选项：启动程序后可自动开始监听
echo   • 🎯 顺序模板遍历：支持多个模板按顺序检测
echo   • 🔍 智能窗口检测：准确识别Cursor IDE窗口
echo   • 匹配精度可调节，适用于固定样式按钮
echo   • 响应速度快，资源占用低
echo   • 🔥 支持F2全局热键：在任何窗口按F2启停监听
echo.
echo ⚙️ 使用步骤:
echo   1. 首次使用请先运行"安装依赖"确保环境配置正确
echo   2. 启动图像模板匹配程序
echo   3. 在"模板管理"中加载Accept按钮模板
echo   4. 点击"开始监听"或直接按F2键
echo   5. 打开Cursor IDE，程序将自动检测和点击Accept按钮
echo   6. 🔥 快捷操作：在Cursor IDE中按F2快速启停监听
echo.
echo ⚠️ 注意事项:
echo   • 程序需要屏幕访问权限
echo   • 首次运行可能需要配置防火墙例外
echo   • 建议在Cursor IDE打开时运行程序
echo   • 可以随时在程序界面中停止监听
echo.
pause
goto main_menu

:exit_program
cls
echo.
echo 👋 感谢使用 Cursor Auto Accept！
echo 程序已退出。
echo.
timeout /t 2 >nul
exit 