@echo off
chcp 65001 >nul
title 创建桌面快捷方式

echo.
echo 🔗 Cursor Auto Accept - 桌面快捷方式创建器
echo ================================================
echo.
echo 🚀 正在创建桌面快捷方式...
echo.

cd /d "%~dp0"

:: 获取当前目录
set "CURRENT_DIR=%cd%"

:: 使用用户配置文件路径获取桌面
set "DESKTOP_PATH=%USERPROFILE%\Desktop"

echo 📂 当前目录: %CURRENT_DIR%
echo 🖥️ 桌面路径: %DESKTOP_PATH%
echo.

:: 创建主启动器快捷方式
echo 🔗 创建"Cursor Auto Accept 完整启动器"快捷方式...
powershell -NoProfile -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_PATH%\Cursor Auto Accept 完整启动器.lnk'); $Shortcut.TargetPath = '%CURRENT_DIR%\完整启动器.bat'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'Cursor Auto Accept 完整启动器'; $Shortcut.Save()}"

if %ERRORLEVEL% EQU 0 (
    echo ✅ 完整启动器快捷方式创建成功
) else (
    echo ❌ 完整启动器快捷方式创建失败
)

:: 创建快速启动器快捷方式
echo 🔗 创建"Cursor Auto Accept 快速启动器"快捷方式...
powershell -NoProfile -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_PATH%\Cursor Auto Accept 快速启动器.lnk'); $Shortcut.TargetPath = '%CURRENT_DIR%\快速启动器.bat'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'Cursor Auto Accept 快速启动器'; $Shortcut.Save()}"

if %ERRORLEVEL% EQU 0 (
    echo ✅ 快速启动器快捷方式创建成功
) else (
    echo ❌ 快速启动器快捷方式创建失败
)

echo.
echo 🎉 桌面快捷方式创建过程完成！
echo.
echo 📋 请检查桌面是否有以下快捷方式：
echo • Cursor Auto Accept 完整启动器.lnk
echo • Cursor Auto Accept 快速启动器.lnk
echo.
echo 💡 如果快捷方式创建成功，您现在可以直接从桌面启动程序了！
echo 💡 如果创建失败，请检查是否有权限问题或手动创建快捷方式
echo.

pause 