#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cursor Auto Accept - 全屏图像模板匹配监听程序
使用全屏模板匹配识别Accept按钮并自动点击
无需复杂的窗口检测，更稳定可靠

特性:
- 全屏模板匹配：在整个屏幕范围内搜索模板
- 无窗口依赖：不需要特定窗口检测，避免窗口识别失败
- 顺序遍历：支持多模板按顺序检测和点击
- 热键控制：F2快捷键启动/停止监听
- 测试模式：可预览检测结果而不执行点击

作者: Cursor Auto Accept
版本: 2.0.0 (全屏模式)
适用环境: Windows 11
创建时间: 2024
"""

import cv2
import numpy as np
import pyautogui
import win32gui
import win32con
import win32api
import time
import threading
import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import json
from datetime import datetime

class CursorTemplateClicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cursor 自动执行-Cursor Auto Accept")
        self.root.geometry("900x600")
        
        # 配置文件路径
        self.config_file = "template_config.json"
        
        # 核心变量
        self.templates = []
        self.running = False
        self.click_count = 0
        self.last_click_time = 0
        self.cursor_window = None
        self.match_threshold = 0.8
        
        # 模板遍历相关
        self.current_template_index = 0
        
        # GUI变量
        self.interval_var = tk.StringVar(value="2.0")
        self.threshold_var = tk.DoubleVar(value=0.8)
        self.test_mode_var = tk.BooleanVar(value=False)
        self.auto_start_var = tk.BooleanVar(value=False)  # 新增：自动启动选项
        self.only_24h_log_var = tk.BooleanVar(value=True)  # 新增：24小时日志过滤选项
        
        # 设置日志
        self.setup_logging()
        
        # 全局热键相关
        self.hotkey_thread = None
        self.hotkey_running = False
        
        # 创建GUI
        self.create_gui()
        
        # 启动热键监听
        self.setup_global_hotkey()
        
        # 加载保存的配置
        self.load_config()
        
        # 如果启用自动启动且有模板，自动开始监听
        if self.auto_start_var.get() and self.templates:
            self.root.after(2000, self.auto_start_monitoring)  # 延迟2秒启动
        
        self.log_message("🖼️ Cursor Auto Accept 全屏图像匹配监听程序启动")
        self.log_message("🌟 新特性: 全屏模板匹配 - 无需复杂的窗口检测，更稳定可靠！")
        if not self.templates:
            self.log_message("💡 提示: 请先加载Accept按钮模板，然后开始监听")
        else:
            self.log_message("💡 已加载 {} 个模板，{}".format(
                len(self.templates), 
                "将自动开始监听" if self.auto_start_var.get() else "可以开始监听"
            ))
        
    def setup_logging(self):
        """配置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('cursor_template_clicker.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def create_gui(self):
        """创建图形界面"""
        # 创建笔记本标签页
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 主控制面板
        main_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text="主控制")
        
        # 模板管理面板
        template_frame = ttk.Frame(notebook)
        notebook.add(template_frame, text="模板管理")
        
        # 日志查看面板
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="日志查看")
        
        # 创建主控制面板内容
        self.create_main_panel(main_frame)
        
        # 创建模板管理面板内容
        self.create_template_panel(template_frame)
        
        # 创建日志面板内容
        self.create_log_panel(log_frame)
        
    def create_main_panel(self, parent):
        """创建主控制面板"""
        # 控制面板
        control_frame = ttk.LabelFrame(parent, text="监听控制", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 第一行：基本控制
        row1 = ttk.Frame(control_frame)
        row1.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = ttk.Button(row1, text="开始监听", command=self.start_monitoring, style="Accent.TButton")
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(row1, text="停止监听", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        

        
        # 第二行：热键提示和自动启动
        row2 = ttk.Frame(control_frame)
        row2.pack(fill=tk.X, pady=(0, 10))
        
        hotkey_label = ttk.Label(row2, text="🔥 全局快捷键: F2 (启动/停止监听)", 
                                font=("Arial", 10, "bold"), foreground="red")
        hotkey_label.pack(side=tk.LEFT)
        
        # 自动启动选项
        auto_start_check = ttk.Checkbutton(row2, text="启动时自动开始监听", 
                                          variable=self.auto_start_var,
                                          command=self.save_config)
        auto_start_check.pack(side=tk.RIGHT)
        
        # 第三行：设置选项
        row3 = ttk.Frame(control_frame)
        row3.pack(fill=tk.X)
        
        # 点击间隔设置
        ttk.Label(row3, text="点击间隔(秒):").pack(side=tk.LEFT)
        interval_entry = ttk.Entry(row3, textvariable=self.interval_var, width=10)
        interval_entry.pack(side=tk.LEFT, padx=(5, 15))
        interval_entry.bind('<KeyRelease>', lambda e: self.save_config())
        
        # 匹配阈值设置
        ttk.Label(row3, text="匹配阈值:").pack(side=tk.LEFT)
        threshold_scale = ttk.Scale(row3, from_=0.5, to=1.0, 
                                   variable=self.threshold_var, 
                                   command=self.update_threshold_label,
                                   length=150)
        threshold_scale.pack(side=tk.LEFT, padx=(5, 10))
        
        self.threshold_label = ttk.Label(row3, text="0.80")
        self.threshold_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # 测试模式
        test_check = ttk.Checkbutton(row3, text="测试模式(仅检测不点击)", variable=self.test_mode_var)
        test_check.pack(side=tk.RIGHT)
        
        # 状态显示面板
        status_frame = ttk.LabelFrame(parent, text="运行状态", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        # 状态信息
        self.status_text = tk.Text(status_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def update_threshold_label(self, value):
        """更新阈值标签"""
        self.threshold_label.config(text="{:.2f}".format(float(value)))
        self.match_threshold = float(value)
        

            
    def view_log(self):
        """查看日志文件"""
        log_file = "cursor_template_clicker.log"
        
        try:
            if os.path.exists(log_file):
                # 创建日志查看窗口
                log_window = tk.Toplevel(self.root)
                log_window.title("运行日志")
                log_window.geometry("800x600")
                
                # 创建文本框和滚动条
                text_frame = ttk.Frame(log_window)
                text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10))
                scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
                text_widget.configure(yscrollcommand=scrollbar.set)
                
                text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                # 使用全局的24小时过滤设置加载日志内容
                log_content = self.get_filtered_log_content(log_file, self.only_24h_log_var.get())
                text_widget.insert(tk.END, log_content)
                text_widget.see(tk.END)  # 滚动到底部
                text_widget.config(state=tk.DISABLED)  # 设为只读
                
                # 添加按钮
                button_frame = ttk.Frame(log_window)
                button_frame.pack(fill=tk.X, padx=10, pady=5)
                
                ttk.Button(button_frame, text="刷新", 
                          command=lambda: self.refresh_log_with_filter(text_widget, log_file, self.only_24h_log_var)).pack(side=tk.LEFT, padx=(0, 10))
                ttk.Button(button_frame, text="清空日志", 
                          command=lambda: self.clear_log(log_file)).pack(side=tk.LEFT)
                
            else:
                messagebox.showinfo("提示", "日志文件不存在")
                
        except Exception as e:
            messagebox.showerror("错误", "无法打开日志文件: {}".format(e))
            
    def get_filtered_log_content(self, log_file, only_24h=False):
        """获取过滤后的日志内容"""
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if not only_24h:
                # 如果不过滤，返回最后1000行
                recent_lines = lines[-1000:]
                return ''.join(recent_lines)
            
            # 过滤24小时内的日志
            from datetime import datetime, timedelta
            now = datetime.now()
            twenty_four_hours_ago = now - timedelta(hours=24)
            
            filtered_lines = []
            for line in lines:
                try:
                    # 尝试解析日志中的时间戳（格式：2024-12-09 15:30:25,123）
                    if len(line) > 19 and line[4] == '-' and line[7] == '-':
                        timestamp_str = line[:19]  # 提取前19个字符作为时间戳
                        log_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        
                        # 如果日志时间在24小时内，保留这行
                        if log_time >= twenty_four_hours_ago:
                            filtered_lines.append(line)
                except (ValueError, IndexError):
                    # 如果无法解析时间戳，保留这行（可能是多行日志的续行）
                    if filtered_lines:  # 只有在已经有过滤行的情况下才添加
                        filtered_lines.append(line)
            
            # 如果过滤后没有内容，显示提示信息
            if not filtered_lines:
                return "📅 24小时内没有日志记录\n\n💡 提示：可以取消勾选上方的'只保留24小时日志'来查看所有日志"
            
            return ''.join(filtered_lines)
            
        except Exception as e:
            return "读取日志失败: {}".format(e)

    def refresh_log_with_filter(self, text_widget, log_file, only_24h_var):
        """使用过滤器刷新日志显示"""
        try:
            log_content = self.get_filtered_log_content(log_file, only_24h_var.get())
                
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, log_content)
            text_widget.see(tk.END)
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("错误", "刷新日志失败: {}".format(e))
    
    def refresh_log(self, text_widget, log_file):
        """刷新日志显示（保留原方法以兼容其他地方的调用）"""
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                recent_lines = lines[-1000:]
                log_content = ''.join(recent_lines)
                
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, log_content)
            text_widget.see(tk.END)
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("错误", "刷新日志失败: {}".format(e))
            
    def clear_log(self, log_file):
        """清空日志文件"""
        result = messagebox.askyesno("确认", "确定要清空日志文件吗？")
        if result:
            try:
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.write("")
                messagebox.showinfo("成功", "日志已清空")
            except Exception as e:
                messagebox.showerror("错误", "清空日志失败: {}".format(e))
        
    def load_config(self):
        """加载保存的配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 加载设置
                self.interval_var.set(config.get('interval', '2.0'))
                self.threshold_var.set(config.get('threshold', 0.8))
                self.test_mode_var.set(config.get('test_mode', False))
                self.auto_start_var.set(config.get('auto_start', False))
                self.only_24h_log_var.set(config.get('only_24h_log', True))
                
                # 更新匹配阈值
                self.match_threshold = self.threshold_var.get()
                self.update_threshold_label(self.match_threshold)
                
                # 加载模板路径列表
                template_paths = config.get('template_paths', [])
                if template_paths:
                    self.log_message("🔄 正在加载保存的模板配置...")
                    loaded_count = 0
                    for template_path in template_paths:
                        if os.path.exists(template_path):
                            self.load_template_file(template_path, quiet=True)
                            loaded_count += 1
                        else:
                            self.log_message("⚠️ 模板文件不存在: {}".format(template_path))
                    
                    if loaded_count > 0:
                        self.log_message("✅ 成功加载 {} 个保存的模板".format(loaded_count))
                        self.display_template_order()
                    else:
                        self.log_message("❌ 没有找到有效的模板文件")
                
        except Exception as e:
            self.log_message("⚠️ 加载配置失败: {}".format(e))

    def save_config(self):
        """保存当前配置"""
        try:
            config = {
                'interval': self.interval_var.get(),
                'threshold': self.threshold_var.get(),
                'test_mode': self.test_mode_var.get(),
                'auto_start': self.auto_start_var.get(),
                'only_24h_log': self.only_24h_log_var.get(),
                'template_paths': [template['path'] for template in self.templates]
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.log_message("⚠️ 保存配置失败: {}".format(e))

    def auto_start_monitoring(self):
        """自动启动监听"""
        if self.templates and not self.running:
            self.log_message("🚀 自动启动监听...")
            self.start_monitoring()

    def display_template_order(self):
        """显示模板加载顺序"""
        if self.templates:
            template_names = [template['name'] for template in self.templates]
            self.log_message("📋 加载的模板顺序: {}".format(" → ".join(template_names)))
            self.log_message("🔄 将按顺序检测每个模板，发现即点击，然后检测下一个模板")

    def load_template_file(self, file_path, quiet=False):
        """加载模板文件"""
        try:
            template = cv2.imread(file_path)
            if template is not None:
                template_name = os.path.basename(file_path)
                
                # 检查是否已经加载过这个模板
                existing_template = next((t for t in self.templates if t['path'] == file_path), None)
                if existing_template:
                    if not quiet:
                        self.log_message("⚠️ 模板已存在: {}".format(template_name))
                    return
                
                self.templates.append({
                    'name': template_name,
                    'path': file_path,
                    'image': template
                })
                
                if hasattr(self, 'template_listbox'):
                    self.template_listbox.insert(tk.END, template_name)
                
                if not quiet:
                    self.log_message("✅ 加载模板: {}".format(template_name))
                
                # 保存配置
                self.save_config()
            else:
                if not quiet:
                    self.log_message("❌ 无法加载模板: {}".format(file_path))
                
        except Exception as e:
            if not quiet:
                self.log_message("加载模板失败: {}".format(e))

    def delete_template(self):
        """删除选中的模板"""
        selection = self.template_listbox.curselection()
        if selection:
            index = selection[0]
            template_name = self.templates[index]['name']
            
            del self.templates[index]
            self.template_listbox.delete(index)
            
            self.log_message("🗑️ 删除模板: {}".format(template_name))
            
            # 保存配置
            self.save_config()
            
    def preview_template(self):
        """预览选中的模板"""
        selection = self.template_listbox.curselection()
        if selection:
            index = selection[0]
            template = self.templates[index]
            
            # 创建预览窗口
            preview_window = tk.Toplevel(self.root)
            preview_window.title("模板预览 - {}".format(template['name']))
            preview_window.geometry("400x300")
            
            # 加载并显示图片
            img = Image.open(template['path'])
            img.thumbnail((350, 250))
            photo = ImageTk.PhotoImage(img)
            
            label = ttk.Label(preview_window, image=photo)
            label.image = photo  # 保持引用
            label.pack(pady=20)
            
    def find_cursor_window(self):
        """查找Cursor窗口 - 改进版本"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                
                # 更严格地排除自己的程序窗口
                exclude_keywords = [
                    'Cursor Auto Accept',
                    '图像匹配',
                    'template',
                    '外部监听程序',
                    'CursorTemplateClicker',
                    'Template Clicker',
                    'Auto Accept'
                ]
                
                # 检查是否包含排除关键词
                should_exclude = any(keyword.lower() in window_title.lower() for keyword in exclude_keywords)
                
                # 检查是否是Cursor相关窗口
                is_cursor_window = (
                    'cursor' in window_title.lower() and 
                    len(window_title) > 5 and 
                    not should_exclude
                )
                
                if is_cursor_window:
                    # 进一步验证窗口类名
                    try:
                        class_name = win32gui.GetClassName(hwnd)
                        # Cursor IDE通常使用Chrome或Electron框架
                        valid_classes = ['Chrome', 'Electron', 'Window']
                        if any(cls in class_name for cls in valid_classes):
                            # 额外检查：排除包含Python关键词的窗口标题
                            python_keywords = ['python', 'tkinter', 'tk', '.py', 'interpreter']
                            if not any(keyword in window_title.lower() for keyword in python_keywords):
                                # 获取窗口位置信息，排除最小化的窗口
                                try:
                                    rect = win32gui.GetWindowRect(hwnd)
                                    if rect[2] - rect[0] > 100 and rect[3] - rect[1] > 100:  # 窗口大小合理
                                        windows.append((hwnd, window_title, class_name))
                                except:
                                    pass
                    except:
                        pass
            return True
            
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        # 添加详细调试信息
        self.log_message("🔍 开始搜索Cursor窗口...")
        
        # 首先列出所有包含cursor的窗口（不管是否符合条件）
        all_cursor_windows = []
        def debug_enum_callback(hwnd, debug_windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if 'cursor' in window_title.lower() and len(window_title) > 3:
                    try:
                        class_name = win32gui.GetClassName(hwnd)
                        rect = win32gui.GetWindowRect(hwnd)
                        size = "{}x{}".format(rect[2] - rect[0], rect[3] - rect[1])
                        debug_windows.append((window_title, class_name, size))
                    except:
                        debug_windows.append((window_title, "未知类名", "未知大小"))
            return True
        
        win32gui.EnumWindows(debug_enum_callback, all_cursor_windows)
        
        if all_cursor_windows:
            self.log_message("🔍 找到包含'cursor'的所有窗口:")
            for i, (title, class_name, size) in enumerate(all_cursor_windows, 1):
                self.log_message("  {}. {} (类名: {}, 大小: {})".format(i, title, class_name, size))
        else:
            self.log_message("🔍 未找到任何包含'cursor'的窗口")
        
        # 记录筛选后的候选窗口
        if windows:
            self.log_message("🔍 通过筛选的候选Cursor窗口:")
            for i, (hwnd, title, class_name) in enumerate(windows, 1):
                try:
                    rect = win32gui.GetWindowRect(hwnd)
                    size = "{}x{}".format(rect[2] - rect[0], rect[3] - rect[1])
                    self.log_message("  {}. {} (类名: {}, 大小: {})".format(i, title, class_name, size))
                except:
                    self.log_message("  {}. {} (类名: {}, 大小: 未知)".format(i, title, class_name))
        else:
            self.log_message("🔍 没有窗口通过筛选条件")
            self.log_message("💡 筛选条件:")
            self.log_message("  - 窗口标题包含'cursor'")
            self.log_message("  - 标题长度 > 5")
            self.log_message("  - 不包含排除关键词: Cursor Auto Accept, 图像匹配, template, 外部监听程序等")
            self.log_message("  - 窗口类名包含: Chrome, Electron, Window")
            self.log_message("  - 不包含Python关键词: python, tkinter, tk, .py, interpreter")
            self.log_message("  - 窗口大小 > 100x100")
        
        # 优先级排序：
        # 1. 包含文件扩展名的窗口
        # 2. 包含项目名的窗口  
        # 3. 标题较长的窗口（通常包含更多信息）
        priority_windows = []
        
        for hwnd, title, class_name in windows:
            priority = 0
            priority_reasons = []
            
            # 检查文件扩展名
            if any(ext in title.lower() for ext in ['.py', '.js', '.ts', '.json', '.md', '.txt', '.cpp', '.java', '.html', '.css']):
                priority += 100
                priority_reasons.append("包含文件扩展名(+100)")
                
            # 检查是否包含项目相关关键词
            if any(keyword in title.lower() for keyword in ['project', 'workspace', 'folder']):
                priority += 50
                priority_reasons.append("包含项目关键词(+50)")
                
            # 较长的标题通常包含更多信息
            length_bonus = len(title)
            priority += length_bonus
            priority_reasons.append("标题长度(+{})".format(length_bonus))
            
            priority_windows.append((priority, hwnd, title, class_name, priority_reasons))
            self.log_message("🔍 窗口优先级计算: {} - 总分: {} ({})".format(title, priority, ", ".join(priority_reasons)))
        
        # 按优先级排序
        priority_windows.sort(reverse=True)
        
        if priority_windows:
            priority, hwnd, title, class_name, reasons = priority_windows[0]
            self.log_message("✅ 选择最佳匹配窗口: {} (类名: {}, 优先级: {})".format(title, class_name, priority))
            return hwnd, title
        
        self.log_message("❌ 未找到符合条件的Cursor窗口")
        
        # 提供故障排除建议
        if all_cursor_windows:
            self.log_message("💡 故障排除建议:")
            self.log_message("  1. 确保Cursor IDE窗口没有最小化")
            self.log_message("  2. 确保Cursor IDE窗口标题包含文件名或项目名")
            self.log_message("  3. 尝试在Cursor中打开一个文件")
            self.log_message("  4. 检查Cursor窗口是否被其他程序遮挡")
        else:
            self.log_message("💡 故障排除建议:")
            self.log_message("  1. 确保Cursor IDE正在运行")
            self.log_message("  2. 确保Cursor IDE窗口可见（未最小化）")
            self.log_message("  3. 尝试重启Cursor IDE")
            self.log_message("  4. 检查Cursor进程是否在任务管理器中")
        
        return None, None
        
    def capture_window_screenshot(self, hwnd):
        """截取窗口截图"""
        try:
            rect = win32gui.GetWindowRect(hwnd)
            x, y, x2, y2 = rect
            width = x2 - x
            height = y2 - y
            
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
        except Exception as e:
            self.log_message("截图失败: {}".format(e))
            return None
            
    def find_accept_button_template(self, image):
        """使用模板匹配查找Accept按钮（旧版本，用于窗口模式测试检测）"""
        best_match = None
        best_confidence = 0
        
        for template_info in self.templates:
            template = template_info['image']
            
            # 模板匹配
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > self.match_threshold and max_val > best_confidence:
                best_confidence = max_val
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                best_match = (center_x, center_y, max_val, template_info['name'])
                
        if best_match:
            x, y, confidence, template_name = best_match
            self.log_message("🎯 找到按钮匹配: {} (置信度: {:.2f})".format(template_name, confidence))
            return x, y, confidence
            
        return None, None, 0
        
    def find_accept_button_template_fullscreen(self, image):
        """全屏模式：使用模板匹配查找Accept按钮（检测所有模板）"""
        best_match = None
        best_confidence = 0
        
        for template_info in self.templates:
            template = template_info['image']
            
            # 模板匹配
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > self.match_threshold and max_val > best_confidence:
                best_confidence = max_val
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                best_match = (center_x, center_y, max_val, template_info['name'])
                
        if best_match:
            x, y, confidence, template_name = best_match
            self.log_message("🎯 全屏找到按钮匹配: {} (置信度: {:.2f}) - 屏幕坐标: ({}, {})".format(template_name, confidence, x, y))
            return x, y, confidence
            
        return None, None, 0
        
    def find_current_template_match(self, image):
        """检测当前模板索引对应的模板是否匹配（窗口模式）"""
        if not self.templates or self.current_template_index >= len(self.templates):
            return None, None, 0, None
            
        template_info = self.templates[self.current_template_index]
        template = template_info['image']
        template_name = template_info['name']
        
        # 模板匹配
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > self.match_threshold:
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            self.log_message("🎯 模板 {} 匹配成功 (置信度: {:.2f})".format(template_name, max_val))
            return center_x, center_y, max_val, template_name
            
        return None, None, 0, None
        
    def find_current_template_match_fullscreen(self, image):
        """全屏模式：检测当前模板索引对应的模板是否匹配"""
        if not self.templates or self.current_template_index >= len(self.templates):
            return None, None, 0, None
            
        template_info = self.templates[self.current_template_index]
        template = template_info['image']
        template_name = template_info['name']
        
        # 模板匹配
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > self.match_threshold:
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            self.log_message("🎯 全屏模板 {} 匹配成功 (置信度: {:.2f}) - 屏幕坐标: ({}, {})".format(template_name, max_val, center_x, center_y))
            return center_x, center_y, max_val, template_name
            
        return None, None, 0, None
        
    def click_button(self, window_rect, button_x, button_y):
        """点击按钮"""
        try:
            # 转换为屏幕坐标
            screen_x = window_rect[0] + button_x
            screen_y = window_rect[1] + button_y
            
            # 检查点击间隔
            current_time = time.time()
            if current_time - self.last_click_time < float(self.interval_var.get()):
                return False
                
            # 执行点击
            pyautogui.click(screen_x, screen_y)
            
            # 更新统计
            self.click_count += 1
            self.last_click_time = current_time
            
            self.log_message("✅ 自动点击 Accept 按钮 (坐标: {}, {})".format(screen_x, screen_y))
            return True
            
        except Exception as e:
            self.log_message("点击失败: {}".format(e))
            return False
            
    def click_button_fullscreen(self, button_x, button_y):
        """全屏模式：直接点击屏幕坐标"""
        try:
            # 检查点击间隔
            current_time = time.time()
            if current_time - self.last_click_time < float(self.interval_var.get()):
                return False
                
            # 直接使用屏幕坐标执行点击
            pyautogui.click(button_x, button_y)
            
            # 更新统计
            self.click_count += 1
            self.last_click_time = current_time
            
            self.log_message("✅ 全屏模式自动点击 Accept 按钮 (屏幕坐标: {}, {})".format(button_x, button_y))
            return True
            
        except Exception as e:
            self.log_message("全屏点击失败: {}".format(e))
            return False
            
    def monitoring_loop(self):
        """监听循环 - 全屏模板匹配模式（不依赖窗口检测）"""
        test_mode = self.test_mode_var.get()
        mode_text = "全屏测试模式" if test_mode else "全屏监听模式"
        self.log_message("🚀 开始{} - 在整个屏幕范围内搜索模板...".format(mode_text))
        self.log_message("💡 优势: 无需复杂窗口检测，直接全屏搜索，更稳定可靠")
        
        # 重置模板索引
        self.current_template_index = 0
        
        while self.running:
            try:
                if self.templates:
                    # 直接截取整个屏幕
                    screenshot = pyautogui.screenshot()
                    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                    
                    if test_mode:
                        # 测试模式：检测所有模板
                        button_x, button_y, confidence = self.find_accept_button_template_fullscreen(image)
                        if button_x is not None and button_y is not None:
                            # 测试模式：移动鼠标到位置但不点击
                            try:
                                pyautogui.moveTo(button_x, button_y, duration=0.3)
                                self.log_message("🧪 测试模式 - 检测到Accept按钮")
                                self.log_message("📍 鼠标已移动到位置: ({}, {}), 置信度: {:.2f}".format(button_x, button_y, confidence))
                                self.log_message("🎯 测试模式下不执行点击操作")
                            except Exception as e:
                                self.log_message("🧪 测试模式 - 检测到Accept按钮")
                                self.log_message("📍 屏幕坐标: ({}, {}), 置信度: {:.2f}".format(button_x, button_y, confidence))
                                self.log_message("⚠️ 鼠标移动失败: {}".format(e))
                        else:
                            # 测试模式下也显示未检测到的信息（降低频率）
                            if self.current_template_index == 0:  # 只在第一个模板时显示，避免日志刷屏
                                self.log_message("❌ 测试未检测到Accept按钮（已检查所有模板）")
                    else:
                        # 正常模式：按顺序检测当前模板
                        current_template_name = self.templates[self.current_template_index]['name'] if self.templates else "未知"
                        
                        # 检测当前模板
                        button_x, button_y, confidence, template_name = self.find_current_template_match_fullscreen(image)
                        
                        if button_x is not None and button_y is not None:
                            # 找到匹配，执行点击
                            if self.click_button_fullscreen(button_x, button_y):
                                self.log_message("✅ 已点击模板: {} (第{}个) - 屏幕坐标: ({}, {})".format(
                                    template_name, self.current_template_index + 1, button_x, button_y))
                                # 更新GUI统计
                                self.root.after(0, self.update_stats)
                                
                                # 移动到下一个模板
                                self.current_template_index = (self.current_template_index + 1) % len(self.templates)
                                next_template_name = self.templates[self.current_template_index]['name']
                                self.log_message("🔄 切换到下一个模板: {} (第{}个)".format(next_template_name, self.current_template_index + 1))
                                
                                # 等待点击间隔
                                interval = float(self.interval_var.get())
                                self.log_message("⏳ 等待 {:.1f} 秒后检测下一个模板...".format(interval))
                                time.sleep(interval)
                                continue
                        else:
                            # 当前模板未匹配，移动到下一个模板
                            self.current_template_index = (self.current_template_index + 1) % len(self.templates)
                            
                            # 如果回到第一个模板，说明完成了一轮遍历
                            if self.current_template_index == 0:
                                # 短暂等待后开始新一轮
                                time.sleep(0.2)
                                
                else:
                    if not hasattr(self, '_no_template_warned') or not self._no_template_warned:
                        self.log_message("⚠️ 没有加载模板，请先加载Accept按钮模板")
                        self._no_template_warned = True
                    time.sleep(1)
                    
            except Exception as e:
                self.log_message("监听循环错误: {}".format(e))
                time.sleep(1)
                
        self.log_message("⏹️ 监听已停止")
        
    def update_stats(self):
        """更新统计信息"""
        stats_text = "点击次数: {}\n".format(self.click_count)
        if hasattr(self, 'status_text'):
            # 只更新最后一行的统计信息，避免重复
            current_content = self.status_text.get(1.0, tk.END)
            lines = current_content.strip().split('\n')
            
            # 如果最后一行是统计信息，则替换，否则添加
            if lines and lines[-1].startswith("点击次数:"):
                lines[-1] = "点击次数: {}".format(self.click_count)
                self.status_text.delete(1.0, tk.END)
                self.status_text.insert(1.0, '\n'.join(lines) + '\n')
            else:
                self.status_text.insert(tk.END, stats_text)
            
            self.status_text.see(tk.END)
        
    def start_monitoring(self):
        """开始监听"""
        if not self.templates:
            self.log_message("❌ 请先加载模板文件")
            messagebox.showwarning("警告", "请先加载模板文件")
            return
            
        if not self.running:
            self.running = True
            self.monitoring_thread = threading.Thread(target=self.monitoring_loop)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            self.log_message("🚀 开始监听 Accept 按钮")
            
            # 更新UI状态
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # 显示监听模式信息
            mode = "全屏测试模式" if self.test_mode_var.get() else "全屏监听模式"
            self.log_message("📊 运行模式: {}".format(mode))
            self.log_message("🌐 检测范围: 整个屏幕 (无需窗口检测)")
            self.log_message("⏱️ 点击间隔: {} 秒".format(self.interval_var.get()))
            self.log_message("🎯 匹配阈值: {:.2f}".format(self.match_threshold))
            self.display_template_order()
            
    def stop_monitoring(self):
        """停止监听"""
        self.running = False
        self.log_message("⏹️ 停止监听")
        
        # 更新UI状态
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        
    def log_message(self, message):
        """记录日志信息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = "[{}] {}".format(timestamp, message)
        
        # 写入日志文件
        logging.info(message)
        
        # 显示在界面状态区域
        if hasattr(self, 'status_text'):
            self.status_text.insert(tk.END, log_entry + "\n")
            self.status_text.see(tk.END)
            # 限制显示行数，保持界面性能
            lines = self.status_text.get(1.0, tk.END).split('\n')
            if len(lines) > 500:  # 超过500行就清理前面的
                self.status_text.delete(1.0, "100.0")  # 删除前100行
        
        # 同时显示在日志面板（如果存在）
        if hasattr(self, 'log_text'):
            self.log_text.insert(tk.END, log_entry + "\n")
            self.log_text.see(tk.END)
            # 限制日志面板行数
            lines = self.log_text.get(1.0, tk.END).split('\n')
            if len(lines) > 1000:  # 超过1000行清理
                self.log_text.delete(1.0, "200.0")  # 删除前200行

    def run(self):
        """运行程序"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def setup_global_hotkey(self):
        """设置全局热键"""
        self.hotkey_running = True
        self.hotkey_thread = threading.Thread(target=self.hotkey_listener, daemon=True)
        self.hotkey_thread.start()
        self.log_message("🔥 全局热键已启用: F2 (启动/停止监听)")
        
    def hotkey_listener(self):
        """全局热键监听器"""
        try:
            # 注册F2为全局热键
            # VK_F2 = 0x71
            win32gui.RegisterHotKey(None, 1, 0, 0x71)
            self.log_message("✅ F2热键注册成功")
            
            # 监听热键消息
            while self.hotkey_running:
                try:
                    msg = win32gui.GetMessage(None, 0, 0)
                    if msg[1][1] == win32con.WM_HOTKEY:
                        # F2被按下，切换监听状态
                        self.root.after(0, self.toggle_monitoring_by_hotkey)
                except:
                    time.sleep(0.1)
                    
        except Exception as e:
            self.log_message("热键注册失败: {}".format(e))
            # 备用方案：使用轮询检测
            self.fallback_hotkey_listener()
            
    def fallback_hotkey_listener(self):
        """备用热键监听器（轮询方式）"""
        self.log_message("🔄 使用备用热键检测方式")
        
        while self.hotkey_running:
            try:
                # 检测F2键状态
                if win32api.GetAsyncKeyState(0x71) & 0x8000:  # F2 = 0x71
                    # 防止重复触发
                    time.sleep(0.2)
                    while win32api.GetAsyncKeyState(0x71) & 0x8000:
                        time.sleep(0.05)
                    
                    # 切换监听状态
                    self.root.after(0, self.toggle_monitoring_by_hotkey)
                    
                time.sleep(0.05)  # 50ms检测间隔
                
            except Exception as e:
                time.sleep(0.1)
                
    def toggle_monitoring_by_hotkey(self):
        """通过热键切换监听状态"""
        if self.running:
            self.stop_monitoring()
            self.log_message("🔥 F2热键: 停止监听")
        else:
            if not self.templates:
                self.log_message("⚠️ F2热键: 请先加载Accept按钮模板")
                return
            self.start_monitoring()
            self.log_message("🔥 F2热键: 开始监听")
            
    def stop_global_hotkey(self):
        """停止全局热键"""
        self.hotkey_running = False
        try:
            win32gui.UnregisterHotKey(None, 1)
        except:
            pass
        
    def on_closing(self):
        """关闭程序"""
        if self.running:
            self.stop_monitoring()
        self.stop_global_hotkey()
        self.root.destroy()

    def create_template_panel(self, parent):
        """创建模板管理面板"""
        # 控制按钮框架
        control_frame = ttk.Frame(parent, padding="10")
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="📸 截取模板", command=self.capture_template).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="📂 加载模板", command=self.load_template).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="🔄 重新加载", command=self.reload_templates).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="💾 保存配置", command=self.save_config).pack(side=tk.LEFT)
        
        # 模板列表框架
        list_frame = ttk.LabelFrame(parent, text="模板列表", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 列表框和滚动条
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        self.template_listbox = tk.Listbox(list_container, height=12)
        template_scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.template_listbox.yview)
        self.template_listbox.configure(yscrollcommand=template_scrollbar.set)
        
        self.template_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        template_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 模板操作按钮
        template_button_frame = ttk.Frame(list_frame)
        template_button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(template_button_frame, text="🗑️ 删除", command=self.delete_template).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(template_button_frame, text="👁️ 预览", command=self.preview_template).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(template_button_frame, text="⬆️ 上移", command=self.move_template_up).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(template_button_frame, text="⬇️ 下移", command=self.move_template_down).pack(side=tk.LEFT)

    def create_log_panel(self, parent):
        """创建日志面板"""
        # 日志控制框架
        control_frame = ttk.Frame(parent, padding="10")
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="🔄 刷新日志", command=self.refresh_current_log).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="🗑️ 清空日志", command=self.clear_current_log).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="📂 查看日志文件", command=self.view_log).pack(side=tk.LEFT, padx=(0, 15))
        
        # 添加24小时日志过滤选项到按钮右边
        only_24h_check = ttk.Checkbutton(control_frame, text="只保留24小时日志", 
                                        variable=self.only_24h_log_var,
                                        command=self.refresh_current_log)
        only_24h_check.pack(side=tk.LEFT)
        
        # 日志显示框架
        log_frame = ttk.LabelFrame(parent, text="程序日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.log_text = tk.Text(log_frame, height=20, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_template(self):
        """加载模板文件"""
        file_path = filedialog.askopenfilename(
            title="选择模板文件",
            filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
        )
        
        if file_path:
            self.load_template_file(file_path)

    def reload_templates(self):
        """重新加载所有模板"""
        self.log_message("🔄 重新加载模板配置...")
        template_paths = [template['path'] for template in self.templates]
        
        # 清空当前模板
        self.templates.clear()
        if hasattr(self, 'template_listbox'):
            self.template_listbox.delete(0, tk.END)
        
        # 重新加载
        loaded_count = 0
        for template_path in template_paths:
            if os.path.exists(template_path):
                self.load_template_file(template_path, quiet=True)
                loaded_count += 1
            else:
                self.log_message("⚠️ 模板文件不存在: {}".format(template_path))
        
        if loaded_count > 0:
            self.log_message("✅ 重新加载了 {} 个模板".format(loaded_count))
            self.display_template_order()
        else:
            self.log_message("❌ 没有找到有效的模板文件")

    def move_template_up(self):
        """向上移动模板"""
        selection = self.template_listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            
            # 交换模板位置
            self.templates[index], self.templates[index-1] = self.templates[index-1], self.templates[index]
            
            # 更新列表框
            self.template_listbox.delete(0, tk.END)
            for template in self.templates:
                self.template_listbox.insert(tk.END, template['name'])
            
            # 保持选中状态
            self.template_listbox.select_set(index-1)
            
            self.log_message("⬆️ 模板上移: {}".format(self.templates[index-1]['name']))
            self.save_config()

    def move_template_down(self):
        """向下移动模板"""
        selection = self.template_listbox.curselection()
        if selection and selection[0] < len(self.templates) - 1:
            index = selection[0]
            
            # 交换模板位置
            self.templates[index], self.templates[index+1] = self.templates[index+1], self.templates[index]
            
            # 更新列表框
            self.template_listbox.delete(0, tk.END)
            for template in self.templates:
                self.template_listbox.insert(tk.END, template['name'])
            
            # 保持选中状态
            self.template_listbox.select_set(index+1)
            
            self.log_message("⬇️ 模板下移: {}".format(self.templates[index+1]['name']))
            self.save_config()

    def refresh_current_log(self):
        """刷新当前日志显示"""
        if hasattr(self, 'log_text'):
            self.log_text.delete(1.0, tk.END)
            
            # 使用24小时过滤设置读取日志文件内容
            try:
                log_file = "cursor_template_clicker.log"
                if os.path.exists(log_file):
                    content = self.get_filtered_log_content(log_file, self.only_24h_log_var.get())
                    self.log_text.insert(1.0, content)
                    self.log_text.see(tk.END)
                else:
                    self.log_text.insert(1.0, "日志文件不存在")
            except Exception as e:
                self.log_text.insert(1.0, "读取日志失败: {}".format(e))

    def clear_current_log(self):
        """清空当前日志"""
        if hasattr(self, 'log_text'):
            self.log_text.delete(1.0, tk.END)
        
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("")
            self.log_message("🗑️ 日志已清空")
        except Exception as e:
            self.log_message("清空日志失败: {}".format(e))

    def capture_template(self):
        """截取模板"""
        self.log_message("📸 准备截取模板...")
        self.root.after(1000, self._do_capture_template)
        
    def _do_capture_template(self):
        """执行模板截取"""
        try:
            # 暂时隐藏主窗口
            self.root.withdraw()
            time.sleep(0.5)
            
            # 显示指导信息
            messagebox.showinfo("截取模板", 
                "即将开始截取模板！\n\n"
                "操作步骤：\n"
                "1. 点击确定后，找到Cursor中的Accept按钮\n"
                "2. 按住鼠标左键拖拽选择Accept按钮区域\n"
                "3. 松开鼠标完成截取\n"
                "4. 在保存对话框中命名并保存模板")
            
            # 获取当前屏幕截图
            screenshot = pyautogui.screenshot()
            
            # 创建截取窗口
            self.create_capture_window(screenshot)
                
        except Exception as e:
            self.log_message("截取模板失败: {}".format(e))
            self.root.deiconify()
            
    def create_capture_window(self, screenshot):
        """创建截取窗口"""
        capture_window = tk.Toplevel()
        capture_window.title("截取Accept按钮模板")
        capture_window.attributes('-fullscreen', True)
        capture_window.attributes('-topmost', True)
        capture_window.configure(bg='black')
        
        # 获取屏幕尺寸
        screen_width = screenshot.width
        screen_height = screenshot.height
        
        # 将PIL图像转换为Tkinter PhotoImage
        screenshot_photo = ImageTk.PhotoImage(screenshot)
        
        # 创建画布显示屏幕截图
        canvas = tk.Canvas(capture_window, 
                          width=screen_width, 
                          height=screen_height,
                          highlightthickness=0)
        canvas.pack()
        
        # 显示屏幕截图作为背景
        canvas.create_image(0, 0, anchor=tk.NW, image=screenshot_photo)
        
        # 添加半透明说明
        info_text = canvas.create_text(screen_width//2, 50, 
                                     text="请拖拽鼠标选择Accept按钮区域 | 按ESC键取消",
                                     font=("Arial", 16, "bold"),
                                     fill="yellow")
        
        # 截取变量
        self.start_x = self.start_y = 0
        self.rect_id = None
        self.capture_screenshot = screenshot
        
        def start_capture(event):
            self.start_x, self.start_y = event.x, event.y
            if self.rect_id:
                canvas.delete(self.rect_id)
            # 隐藏说明文字
            canvas.itemconfig(info_text, state='hidden')
                
        def draw_rectangle(event):
            if self.rect_id:
                canvas.delete(self.rect_id)
            self.rect_id = canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline="red", width=3, fill="", stipple="gray50")
                
        def finish_capture(event):
            end_x, end_y = event.x, event.y
            
            # 计算选择区域
            x1 = min(self.start_x, end_x)
            y1 = min(self.start_y, end_y)
            x2 = max(self.start_x, end_x)
            y2 = max(self.start_y, end_y)
            
            # 验证选择区域大小
            if abs(x2 - x1) > 10 and abs(y2 - y1) > 10:
                # 关闭截取窗口
                capture_window.destroy()
                
                # 截取选定区域（这里坐标就是屏幕坐标）
                region_image = self.capture_screenshot.crop((x1, y1, x2, y2))
                
                # 保存模板
                self.save_captured_template(region_image)
                
                self.log_message("✅ 截取区域: ({},{}) 到 ({},{})，尺寸: {}x{}".format(
                    x1, y1, x2, y2, x2-x1, y2-y1))
            else:
                capture_window.destroy()
                self.root.deiconify()
                messagebox.showwarning("警告", "选择区域太小（至少10x10像素），请重新选择")
                
        def cancel_capture(event):
            capture_window.destroy()
            self.root.deiconify()
            self.log_message("❌ 取消截取模板")
            
        # 绑定鼠标事件
        canvas.bind("<Button-1>", start_capture)
        canvas.bind("<B1-Motion>", draw_rectangle)
        canvas.bind("<ButtonRelease-1>", finish_capture)
        capture_window.bind("<Escape>", cancel_capture)
        
        # 保持图像引用防止被垃圾回收
        capture_window.screenshot_photo = screenshot_photo
        
        capture_window.focus_set()
        
    def save_captured_template(self, image):
        """保存截取的模板"""
        try:
            # 显示主窗口
            self.root.deiconify()
            
            # 选择保存路径
            template_path = filedialog.asksaveasfilename(
                title="保存Accept按钮模板",
                defaultextension=".png",
                initialdir="./templates",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            
            if template_path:
                # 确保templates目录存在
                os.makedirs(os.path.dirname(template_path), exist_ok=True)
                
                # 保存图像
                image.save(template_path)
                
                # 加载到模板列表
                self.load_template_file(template_path)
                self.log_message("✅ 模板已保存并加载: {}".format(os.path.basename(template_path)))
            else:
                self.log_message("❌ 未保存模板")
                
        except Exception as e:
            self.log_message("保存模板失败: {}".format(e))
            self.root.deiconify()



if __name__ == "__main__":
    print("🖼️ Cursor Auto Accept - 图像匹配监听程序")
    print("=" * 50)
    print("正在启动图形界面...")
    
    app = CursorTemplateClicker()
    app.run() 