# Cursor Auto Accept 外部监听程序启动脚本
# 版本: 1.0.0
# 适用环境: Windows 11
# 创建时间: 2024

# 清屏并显示欢迎信息
Clear-Host
Write-Host "🎯 Cursor Auto Accept 外部监听程序" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host "版本: 1.0.0 | 适用环境: Windows 11" -ForegroundColor Gray
Write-Host ""

# 检查Python环境
Write-Host "🔍 检查运行环境..." -ForegroundColor Cyan
$pythonCommand = ""
$pythonFound = $false

# 尝试检测Python命令
try {
    $pyVersion = py --version 2>&1
    if ($pyVersion -match "Python") {
        $pythonCommand = "py"
        $pythonFound = $true
        Write-Host "✅ Python环境: $pyVersion" -ForegroundColor Green
    }
} catch {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python") {
            $pythonCommand = "python"
            $pythonFound = $true
            Write-Host "✅ Python环境: $pythonVersion" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ 未找到Python环境！" -ForegroundColor Red
        Write-Host "请先运行 install_dependencies.ps1 安装依赖" -ForegroundColor Yellow
        pause
        exit 1
    }
}

if (-not $pythonFound) {
    Write-Host "❌ Python环境检测失败！" -ForegroundColor Red
    Write-Host "请先运行 install_dependencies.ps1 安装依赖" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host ""

# 检查程序文件
$templateFile = "cursor-auto-clicker-template.py"
$templateExists = Test-Path $templateFile

Write-Host "📁 检查程序文件..." -ForegroundColor Cyan
if ($templateExists) {
    Write-Host "✅ 模板匹配程序文件: $templateFile" -ForegroundColor Green
} else {
    Write-Host "❌ 缺失模板匹配程序文件: $templateFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "💥 错误：找不到程序文件！" -ForegroundColor Red
    Write-Host "请确保以下文件存在:" -ForegroundColor Yellow
    Write-Host "  - $templateFile" -ForegroundColor White
    Write-Host ""
    Write-Host "如果文件缺失，请重新运行项目安装程序。" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host ""

# 显示主菜单
do {
    Write-Host "📋 请选择操作:" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "1. 🖼️  启动图像模板匹配程序" -ForegroundColor White
    Write-Host "   └─ 使用图像模板匹配识别Accept按钮" -ForegroundColor Gray
    
    Write-Host "2. 🔧 安装依赖" -ForegroundColor White
    Write-Host "3. ❓ 帮助信息" -ForegroundColor White
    Write-Host "4. 🚪 退出程序" -ForegroundColor White
    Write-Host ""

    $choice = Read-Host "请输入选择 (1-4)"

    switch ($choice) {
        "1" {
            if ($templateExists) {
                Write-Host ""
                Write-Host "🚀 启动图像模板匹配程序..." -ForegroundColor Green
                Write-Host "💡 提示: 需要先加载Accept按钮模板图片" -ForegroundColor Yellow
                Write-Host ""
                try {
                    & $pythonCommand $templateFile
                } catch {
                    Write-Host "❌ 程序启动失败: $($_.Exception.Message)" -ForegroundColor Red
                    Write-Host "请检查Python环境和依赖包是否正确安装" -ForegroundColor Yellow
                }
            }
            Write-Host ""
            Write-Host "按任意键返回主菜单..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            Clear-Host
            Write-Host "🎯 Cursor Auto Accept 外部监听程序" -ForegroundColor Green
            Write-Host "=================================" -ForegroundColor Green
            Write-Host ""
        }
        "2" {
            Write-Host ""
            Write-Host "🔧 启动依赖安装程序..." -ForegroundColor Green
            if (Test-Path "install_dependencies.ps1") {
                try {
                    & ".\install_dependencies.ps1"
                } catch {
                    Write-Host "❌ 依赖安装程序启动失败: $($_.Exception.Message)" -ForegroundColor Red
                }
            } else {
                Write-Host "❌ 找不到依赖安装脚本 install_dependencies.ps1" -ForegroundColor Red
            }
            Write-Host ""
            Write-Host "按任意键返回主菜单..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            Clear-Host
            Write-Host "🎯 Cursor Auto Accept 外部监听程序" -ForegroundColor Green
            Write-Host "=================================" -ForegroundColor Green
            Write-Host ""
        }
        "3" {
            Clear-Host
            Write-Host "❓ Cursor Auto Accept 使用帮助" -ForegroundColor Green
            Write-Host "=================================" -ForegroundColor Green
            Write-Host ""
            Write-Host "📖 程序说明:" -ForegroundColor Cyan
            Write-Host "  这是一个自动点击Cursor IDE中Accept按钮的外部工具程序。" -ForegroundColor White
            Write-Host "  类似游戏外挂的工作原理，通过屏幕监听检测按钮并自动点击。" -ForegroundColor White
            Write-Host ""
            Write-Host "🖼️ 图像模板匹配程序:" -ForegroundColor Cyan
            Write-Host "  • 使用OpenCV图像匹配算法识别按钮" -ForegroundColor White
            Write-Host "  • 需要先加载Accept按钮的模板图片" -ForegroundColor White
            Write-Host "  • 匹配精度可调节，适用于固定样式按钮" -ForegroundColor White
            Write-Host "  • 响应速度快，资源占用低" -ForegroundColor White
            Write-Host ""
            Write-Host "⚙️ 使用步骤:" -ForegroundColor Cyan
            Write-Host "  1. 首次使用请先运行安装依赖确保环境配置正确" -ForegroundColor White
            Write-Host "  2. 启动图像模板匹配程序" -ForegroundColor White
            Write-Host "  3. 在模板管理中加载Accept按钮模板" -ForegroundColor White
            Write-Host "  4. 点击开始监听" -ForegroundColor White
            Write-Host "  5. 打开Cursor IDE，程序将自动检测和点击Accept按钮" -ForegroundColor White
            Write-Host ""
            Write-Host "⚠️ 注意事项:" -ForegroundColor Yellow
            Write-Host "  • 程序需要屏幕访问权限" -ForegroundColor White
            Write-Host "  • 首次运行可能需要配置防火墙例外" -ForegroundColor White
            Write-Host "  • 建议在Cursor IDE打开时运行程序" -ForegroundColor White
            Write-Host "  • 可以随时在程序界面中停止监听" -ForegroundColor White
            Write-Host ""
            Write-Host "按任意键返回主菜单..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            Clear-Host
            Write-Host "🎯 Cursor Auto Accept 外部监听程序" -ForegroundColor Green
            Write-Host "=================================" -ForegroundColor Green
            Write-Host ""
        }
        "4" {
            Write-Host ""
            Write-Host "👋 感谢使用 Cursor Auto Accept！" -ForegroundColor Green
            Write-Host "程序已退出。" -ForegroundColor Gray
            exit 0
        }
        default {
            Write-Host ""
            Write-Host "❌ 无效选择，请输入 1-4 之间的数字" -ForegroundColor Red
            Write-Host ""
            Start-Sleep -Seconds 1
        }
    }
} while ($true) 