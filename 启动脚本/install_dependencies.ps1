# Cursor Auto Accept 外部监听程序依赖安装脚本
# 版本: 1.0.0
# 适用环境: Windows 11
# 创建时间: 2024

Write-Host "🚀 Cursor Auto Accept 依赖安装器" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

# 检查PowerShell执行策略
Write-Host "🔧 检查PowerShell执行策略..." -ForegroundColor Cyan
$currentPolicy = Get-ExecutionPolicy
if ($currentPolicy -eq "Restricted") {
    Write-Host "⚠️ PowerShell执行策略受限，尝试临时设置..." -ForegroundColor Yellow
    try {
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Write-Host "✅ 执行策略已临时设置为RemoteSigned" -ForegroundColor Green
    } catch {
        Write-Host "❌ 无法设置执行策略，请以管理员身份运行PowerShell" -ForegroundColor Red
        pause
        exit 1
    }
}

# 检查Python - 先尝试py命令（Windows推荐）
Write-Host ""
Write-Host "🐍 检查Python安装..." -ForegroundColor Cyan
$pythonFound = $false
$pythonCommand = ""

# 尝试py命令
try {
    $pythonVersion = py --version 2>&1
    if ($pythonVersion -match "Python (\d+\.\d+\.\d+)") {
        $version = $matches[1]
        Write-Host "✅ 找到Python (py): $pythonVersion" -ForegroundColor Green
        $pythonCommand = "py"
        $pythonFound = $true
        
        # 检查版本是否满足要求（3.7+）
        if ([version]$version -ge [version]"3.7.0") {
            Write-Host "✅ Python版本满足要求（3.7+）" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Python版本较低，建议升级到3.7+以获得最佳体验" -ForegroundColor Yellow
        }
    }
} catch {
    # py命令失败，尝试python命令
}

# 如果py命令失败，尝试python命令
if (-not $pythonFound) {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+\.\d+\.\d+)") {
            Write-Host "✅ 找到Python (python): $pythonVersion" -ForegroundColor Green
            $pythonCommand = "python"
            $pythonFound = $true
        }
    } catch {
        # python命令也失败
    }
}

if (-not $pythonFound) {
    Write-Host "❌ 未找到Python，请先安装Python 3.7+!" -ForegroundColor Red
    Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "建议安装Python 3.11或更高版本" -ForegroundColor Yellow
    pause
    exit 1
}

# 检查pip
Write-Host ""
Write-Host "📦 检查pip包管理器..." -ForegroundColor Cyan
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip可用: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip不可用，请重新安装Python并确保包含pip" -ForegroundColor Red
    pause
    exit 1
}

# 升级pip到最新版本
Write-Host ""
Write-Host "⬆️ 升级pip到最新版本..." -ForegroundColor Cyan
try {
    & $pythonCommand -m pip install --upgrade pip
    Write-Host "✅ pip升级完成" -ForegroundColor Green
} catch {
    Write-Host "⚠️ pip升级失败，将使用当前版本" -ForegroundColor Yellow
}

# 安装Python包
Write-Host ""
Write-Host "📦 安装Python依赖包..." -ForegroundColor Cyan

$packages = @(
    @{name="opencv-python"; version=">=4.5.0"},
    @{name="pytesseract"; version=">=0.3.8"},
    @{name="pyautogui"; version=">=0.9.50"},
    @{name="pywin32"; version=">=227"},
    @{name="Pillow"; version=">=8.0.0"},
    @{name="numpy"; version=">=1.20.0"}
)

$installErrors = @()

foreach ($package in $packages) {
    $packageName = $package.name
    $packageVersion = $package.version
    
    Write-Host "安装 $packageName $packageVersion..." -ForegroundColor Yellow
    try {
        & $pythonCommand -m pip install "$packageName$packageVersion"
        Write-Host "✅ $packageName 安装成功" -ForegroundColor Green
    } catch {
        Write-Host "❌ $packageName 安装失败: $($_.Exception.Message)" -ForegroundColor Red
        $installErrors += $packageName
    }
}

# 检查安装结果
if ($installErrors.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️ 以下包安装失败，请手动安装:" -ForegroundColor Yellow
    foreach ($errorPkg in $installErrors) {
        Write-Host "  - $errorPkg" -ForegroundColor Red
    }
}

# 安装Tesseract OCR检查
Write-Host ""
Write-Host "👁️ 检查Tesseract OCR..." -ForegroundColor Cyan

$tesseractPaths = @(
    "C:\Program Files\Tesseract-OCR\tesseract.exe",
    "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    "$env:USERPROFILE\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

$tesseractFound = $false
foreach ($path in $tesseractPaths) {
    if (Test-Path $path) {
        Write-Host "✅ 找到Tesseract: $path" -ForegroundColor Green
        $tesseractFound = $true
        
        # 测试Tesseract版本
        try {
            $tesseractVersion = & $path --version 2>&1
            Write-Host "📌 Tesseract版本: $($tesseractVersion.Split([Environment]::NewLine)[0])" -ForegroundColor Cyan
        } catch {
            Write-Host "⚠️ 无法获取Tesseract版本信息" -ForegroundColor Yellow
        }
        break
    }
}

if (-not $tesseractFound) {
    Write-Host "⚠️ 未找到Tesseract OCR，OCR功能需要手动安装" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📥 安装选项:" -ForegroundColor Cyan
    Write-Host "1. 官方下载: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor White
    Write-Host "2. Chocolatey: choco install tesseract" -ForegroundColor White
    Write-Host "3. Scoop: scoop install tesseract" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 注意: 安装时请选择 '添加到PATH环境变量' 选项" -ForegroundColor Yellow
}

# 验证安装
Write-Host ""
Write-Host "🔍 验证安装..." -ForegroundColor Cyan
try {
    # 测试导入主要模块
    & $pythonCommand -c "import cv2, pytesseract, pyautogui, win32gui, PIL, numpy; print('所有模块导入成功')"
    Write-Host "✅ 所有Python包验证成功" -ForegroundColor Green
} catch {
    Write-Host "❌ 模块导入测试失败，可能存在兼容性问题" -ForegroundColor Red
    Write-Host "错误信息: $($_.Exception.Message)" -ForegroundColor Red
}

# 完成提示
Write-Host ""
Write-Host "🎉 依赖安装检查完成!" -ForegroundColor Green
Write-Host ""
Write-Host "现在可以运行以下程序:" -ForegroundColor Cyan
Write-Host "1. py cursor-auto-clicker-ocr.py     (OCR文字识别版本)" -ForegroundColor White
Write-Host "2. py cursor-auto-clicker-template.py (图像模板匹配版本)" -ForegroundColor White
Write-Host ""
Write-Host "或使用启动脚本:" -ForegroundColor Cyan
Write-Host "   .\start_program.ps1" -ForegroundColor White

Write-Host ""
Write-Host "📝 提示:" -ForegroundColor Yellow
Write-Host "- 如果遇到权限问题，请以管理员身份运行PowerShell" -ForegroundColor White
Write-Host "- 首次运行可能需要配置防火墙例外" -ForegroundColor White
Write-Host "- OCR版本需要先安装Tesseract OCR" -ForegroundColor White
Write-Host "- 模板匹配版本需要先加载Accept按钮模板" -ForegroundColor White

Write-Host ""
pause 