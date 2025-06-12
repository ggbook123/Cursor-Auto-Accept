# Cursor Auto Accept - Automatic Click Program

A small software that enables CURSOR to automatically execute like AUGMENT.

An intelligent button automatic recognition and click tool based on image template matching technology, specifically designed for Cursor AI programming assistant. It can automatically recognize and click Accept buttons to improve development efficiency.

-------
Quick Start Guide: 1. Let cursor deploy this project environment 2. Click the bat file to run 3. Press F2 to start execution or stop
Additional Notes: If the cursor version update causes interface changes, capture the area that cursor needs to automatically click in template management, then load the image and save.

Note: CURSOR must stay in the foreground, otherwise it cannot be recognized! Future versions may optimize this!
Extra Info: Better when used with shrimp-task-manager's MCP, automatic project planning, automatic project execution, enable continuous mode.

The following is an AI-generated introduction:
-------

## 📋 Project Overview

Cursor Auto Accept is a professional automation tool that uses computer vision technology to automatically recognize Accept buttons on the screen and perform click operations. The program uses a full-screen template matching algorithm without complex window detection, providing higher stability and reliability.

### 🌟 Core Features

- **🎯 Full-Screen Template Matching**: Search for target buttons across the entire screen without window dependency limitations
- **🔄 Sequential Template Traversal**: Support multiple templates for detection and clicking in preset order
- **🔥 Global Hotkey Control**: F2 shortcut key for one-click start/stop monitoring
- **🧪 Test Mode**: Preview detection results without executing actual click operations
- **📊 Real-time Status Monitoring**: Detailed logging and runtime status display
- **⚙️ Configuration Persistence**: Automatic saving of user settings and template configurations
- **🖼️ Template Capture Tool**: Built-in screenshot tool for quick button template creation

## 💻 System Requirements

### System Requirements
- **Operating System**: Windows 11 (development environment) / Windows 10 (compatible)
- **Python Version**: Python 3.7 or higher
- **Screen Resolution**: Supports any resolution (1920x1080 and above recommended)

### Dependencies
- `opencv-python>=4.5.0` - Image processing and computer vision
- `pyautogui>=0.9.50` - GUI automation
- `pywin32>=227` - Windows system API
- `Pillow>=8.0.0` - Image processing library
- `numpy>=1.20.0` - Numerical computing library

## 🚀 Quick Start

### 1. Environment Setup

#### Method 1: One-Click Auto Installation (Recommended)
```bash
# Run dependency installation script
.\安装依赖.bat
```

#### Method 2: Manual Installation
```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Launch Program

#### Method 1: Using Launcher (Recommended)
```bash
# Run complete launcher
.\完整启动器.bat
```

#### Method 2: Direct Launch
```bash
# Launch image template matching version
.\快速启动器.bat

# Or run Python script directly
python cursor-auto-clicker-template.py
```

#### Method 3: PowerShell Launch
```bash
# Launch using PowerShell script
.\start_program.ps1
```

### 3. Create Desktop Shortcut
```bash
# Create convenient desktop shortcut
.\创建桌面快捷方式.bat
```

## 📖 Usage Instructions

### Basic Operation Workflow

1. **Load Templates**
   - Click the "Template Management" tab
   - Use "Load Template" button to add: Accept buttons, VPN prompts, "Used more than 25 times" messages, or other images that cause cursor execution interruptions (defaults are pre-configured)
   - Supports PNG, JPG and other formats

2. **Configure Parameters**
   - **Click Interval**: Set the click interval time after button detection (seconds)
   - **Match Threshold**: Adjust template matching similarity requirement (0.5-1.0)
   - **Test Mode**: When enabled, only detects without clicking, used for debugging

3. **Start Monitoring**
   - Click "Start Monitoring" button or press F2 hotkey
   - Program will begin full-screen scanning for matching buttons
   - Automatically executes click operation when target is detected

4. **Stop Monitoring**
   - Click "Stop Monitoring" button or press F2 hotkey again
   - Program stops monitoring and click operations

### Advanced Features

#### 🔥 Global Hotkey
- **F2 Key**: Quickly start/stop monitoring regardless of whether program window is in foreground

#### 🧪 Test Mode
- When test mode is enabled, program displays detection results but doesn't execute actual clicks

#### 🖼️ Template Capture Feature - When cursor updates cause button position changes, etc., capture screenshots here to enable software recognition
- Use built-in screenshot tool to quickly create button templates
- Supports precise area selection and automatic saving

#### 📊 Real-time Monitoring
- View detailed detection logs and runtime status

## 📁 Project Directory Structure

```
cursor-auto-accept/
├── cursor-auto-clicker-template.py    # Main program file
├── requirements.txt                   # Python dependency configuration
├── template_config.json              # Program configuration file
├── README.md                         # Project documentation
├── 
├── 启动脚本/
│   ├── 完整启动器.bat                # Program launcher
│   ├── 快速启动器.bat                # Direct launch script
│   ├── start_program.ps1             # PowerShell launch script
│   ├── 安装依赖.bat                  # Dependency installation script
│   └── 创建桌面快捷方式.bat          # Shortcut creation script
├── 
├── templates/                        # Template image folder
│   ├── cursor.png                   # Cursor button template
│   └── *.png                        # Other template files
├── 
├── window_templates/                 # Window template folder
│   └── *.png                        # Window-related templates
├── 
├── 日志文件/
│   ├── cursor_template_clicker.log   # Main program log
│   └── cursor_auto_clicker.log       # Runtime log
└── 
└── __pycache__/                      # Python cache files
```

## ⚙️ Configuration Guide

### Template Configuration (template_config.json)
```json
{
  "interval": "3.0",           // Click interval time (seconds)
  "threshold": 0.8,            // Match threshold (0.5-1.0)
  "test_mode": false,          // Test mode switch
  "auto_start": false,         // Auto start monitoring on launch
  "template_paths": [          // Template file path list
    "templates/cursor.png"
  ]
}
```

### Match Threshold Explanation
- **0.9-1.0**: Extremely high precision, requires very precise matching
- **0.8-0.9**: High precision, recommended setting range
- **0.7-0.8**: Medium precision, suitable for cases with significant button variations
- **0.5-0.7**: Low precision, may cause false matches

## 🔧 Troubleshooting

### Common Issues

#### 1. Program Cannot Detect Buttons
- **Check Template Quality**: Ensure template images are clear and complete
- **Adjust Match Threshold**: Lower threshold to 0.7-0.8
- **Use Test Mode**: Verify detection logic is working normally
- **Update Templates**: Re-capture button templates in current state

#### 2. Inaccurate Click Position
- **Check DPI Settings**: Ensure system DPI scaling settings are correct
- **Re-capture Templates**: Use built-in screenshot tool to update templates
- **Adjust Click Delay**: Increase click interval time

#### 3. Program Startup Failure
- **Check Python Environment**: Ensure Python 3.7+ is correctly installed
- **Install Dependencies**: Run `安装依赖.bat` to reinstall dependency packages
- **Permission Issues**: Run program as administrator

#### 4. Hotkey Not Working
- **Check Keyboard Conflicts**: Ensure F2 key is not occupied by other programs
- **Restart Program**: Close program and restart
- **System Permissions**: Run program with administrator privileges

## 📝 Version History

### v2.0.0 (Current Version)
- ✅ Full-screen template matching algorithm
- ✅ Sequential template traversal functionality
- ✅ F2 global hotkey support
- ✅ Test mode and debugging features
- ✅ Configuration persistence
- ✅ Graphical template management interface

### v1.0.0 (Legacy Version)
- ✅ Basic OCR text recognition functionality
- ✅ Window detection and click functionality

## 🤝 Technical Support

### System Requirements
- Windows 11 (development environment)
- Windows 10 (compatible support)
- Python 3.7+ environment

### Technology Stack
- **Image Processing**: OpenCV, Pillow
- **GUI Interface**: tkinter
- **System Integration**: pywin32, pyautogui
- **Numerical Computing**: numpy

## 📄 License

This project is for learning and personal use only. Please do not use for commercial purposes.

## 🆘 Getting Help

If you encounter problems or need technical support, please:

1. **Check Log Files**: Review error information in `cursor_template_clicker.log`
2. **Use Test Mode**: Enable test mode for problem diagnosis
3. **Check Configuration File**: Confirm `template_config.json` is configured correctly
4. **Reinstall Dependencies**: Run `安装依赖.bat` script

---

**🎯 Make AI programming assistant experience smoother and improve development efficiency!** 