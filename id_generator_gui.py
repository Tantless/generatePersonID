# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QGroupBox, QRadioButton, QPushButton, QLabel, QLineEdit,
                            QTextEdit, QComboBox, QFileDialog, QStatusBar, QMessageBox,
                            QSplitter)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QGuiApplication, QClipboard, QFont, QFontDatabase
import function
import os
from datetime import datetime

class IDGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("身份证号与姓名生成器")
        
        # 设置应用程序字体
        self.setup_fonts()
        
        # 居中显示窗口
        screen = QGuiApplication.primaryScreen().geometry()
        width, height = 1000, 650
        self.move(
            (screen.width() - width) // 2,
            (screen.height() - height) // 2
        )
        self.resize(width, height)
        self.setMinimumSize(800, 500)
        
        # 主窗口布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # 创建一个水平分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧面板 - 生成器
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(12)
        
        # 标题
        title_label = QLabel("身份证号与姓名生成器")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                margin: 10px 0 20px 0;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 8px;
            }
        """)
        left_layout.addWidget(title_label)
        
        # 性别选择
        self.gender_group = QGroupBox("性别选择")
        gender_layout = QHBoxLayout()
        gender_layout.setSpacing(20)
        self.random_radio = QRadioButton("随机", checked=True)
        self.male_radio = QRadioButton("男")
        self.female_radio = QRadioButton("女")
        gender_layout.addWidget(self.random_radio)
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        gender_layout.addStretch()
        self.gender_group.setLayout(gender_layout)
        left_layout.addWidget(self.gender_group)
        
        # 生成按钮
        self.generate_btn = QPushButton("生成")
        self.generate_btn.setMinimumHeight(40)
        self.generate_btn.clicked.connect(self.generate_data)
        left_layout.addWidget(self.generate_btn)
        
        # 结果显示组
        result_group = QGroupBox("生成结果")
        result_layout = QVBoxLayout()
        result_layout.setSpacing(10)
        
        # 身份证号
        id_layout = QHBoxLayout()
        self.id_label = QLabel("身份证号:")
        self.id_label.setMinimumWidth(80)
        self.id_display = QLineEdit()
        self.id_display.setReadOnly(True)
        self.id_display.setStyleSheet("QLineEdit { font-family: 'Consolas', 'Courier New', monospace; }")
        id_layout.addWidget(self.id_label)
        id_layout.addWidget(self.id_display, 1)
        result_layout.addLayout(id_layout)
        
        # 姓名
        name_layout = QHBoxLayout()
        self.name_label = QLabel("姓名:")
        self.name_label.setMinimumWidth(80)
        self.name_display = QLineEdit()
        self.name_display.setReadOnly(True)
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_display, 1)
        result_layout.addLayout(name_layout)
        
        # 复制按钮
        copy_layout = QHBoxLayout()
        copy_layout.setSpacing(10)
        self.copy_id_btn = QPushButton("复制身份证号")
        self.copy_id_btn.clicked.connect(self.copy_id)
        self.copy_name_btn = QPushButton("复制姓名")
        self.copy_name_btn.clicked.connect(self.copy_name)
        self.copy_all_btn = QPushButton("复制全部")
        self.copy_all_btn.clicked.connect(self.copy_all)
        copy_layout.addWidget(self.copy_id_btn)
        copy_layout.addWidget(self.copy_name_btn)
        copy_layout.addWidget(self.copy_all_btn)
        result_layout.addLayout(copy_layout)
        
        result_group.setLayout(result_layout)
        left_layout.addWidget(result_group)
        
        # 添加伸缩项使控件靠上对齐
        left_layout.addStretch(1)
        
        # 右侧面板 - 日志查看器
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        # 日志标题
        log_title = QLabel("日志查看器")
        log_title.setFont(font)
        log_title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(log_title)
        
        # 日志控制面板
        log_control_layout = QHBoxLayout()
        
        # 日志文件选择
        log_control_layout.addWidget(QLabel("选择日志:"))
        self.log_selector = QComboBox()
        log_control_layout.addWidget(self.log_selector, 1)
        
        # 刷新按钮
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.refresh_log_list)
        log_control_layout.addWidget(self.refresh_btn)
        
        right_layout.addLayout(log_control_layout)
        
        # 日志显示（只读）
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMinimumHeight(300)
        right_layout.addWidget(self.log_display)
        
        # 添加到分割器
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([int(width*0.35), int(width*0.65)])  # 设置初始比例

        # 添加到主布局
        main_layout.addWidget(splitter)
        
        # 添加状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("准备就绪")
        
        # 初始化剪贴板
        self.clipboard = QApplication.clipboard()
        
        # 初始化加载日志列表
        self.refresh_log_list()
        self.log_selector.currentTextChanged.connect(self.load_log)
        if self.log_selector.count() > 0:
            self.load_log()
    
    def setup_fonts(self):
        """设置应用程序字体"""
        # 检查系统是否有合适的中文字体
        font_db = QFontDatabase()
        available_families = font_db.families()
        font_families = ["Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "SimSun", "Arial Unicode MS"]
        available_font = None
        
        for font_family in font_families:
            if font_family in available_families:
                available_font = font_family
                break
        
        if available_font:
            # 设置应用程序默认字体
            app_font = QFont(available_font, 10)
            QApplication.instance().setFont(app_font)
        else:
            # 如果没有找到合适的中文字体，使用默认字体
            app_font = QFont("Arial", 10)
            QApplication.instance().setFont(app_font)
        
        # 设置样式表来确保字体一致性和更好的视觉效果
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                font-family: "Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "SimSun", sans-serif;
                font-size: 10pt;
                color: #333;
            }
            QLabel {
                font-size: 10pt;
                color: #333;
            }
            QPushButton {
                font-size: 10pt;
                padding: 8px 16px;
                min-height: 25px;
                background-color: #e1e1e1;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d4edda;
                border-color: #c3e6cb;
            }
            QPushButton:pressed {
                background-color: #c3e6cb;
            }
            QLineEdit {
                font-size: 10pt;
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QTextEdit {
                font-size: 9pt;
                font-family: "Consolas", "Courier New", "Microsoft YaHei UI", monospace;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                line-height: 1.4;
            }
            QComboBox {
                font-size: 10pt;
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                min-width: 100px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-style: solid;
                border-width: 3px;
                border-color: #666 transparent transparent transparent;
            }
            QGroupBox {
                font-size: 10pt;
                font-weight: bold;
                padding-top: 15px;
                margin-top: 10px;
                border: 2px solid #ccc;
                border-radius: 6px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                background-color: white;
                color: #2c3e50;
            }
            QRadioButton {
                font-size: 10pt;
                spacing: 5px;
                color: #333;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #ccc;
                border-radius: 9px;
                background-color: white;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #007bff;
                border-radius: 9px;
                background-color: #007bff;
            }
            QStatusBar {
                font-size: 9pt;
                color: #666;
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
            }
            QSplitter::handle {
                background-color: #ccc;
                width: 3px;
            }
            QSplitter::handle:hover {
                background-color: #999;
            }
        """)
    
    def get_selected_gender(self):
        if self.male_radio.isChecked():
            return 1
        elif self.female_radio.isChecked():
            return 2
        else:
            return 0
    
    def generate_data(self):
        self.statusBar.showMessage("正在生成...")
        
        # 获取当前日期对应的日志文件名
        today = datetime.now().strftime("%Y%m%d") + ".txt"
        
        gender = self.get_selected_gender()
        try:
            person_id, person_name = function.summon_newPerson(gender)
            self.id_display.setText(person_id)
            self.name_display.setText(person_name)
            
            # 如果当前选择的是今天的日志，直接追加到显示区
            if self.log_selector.currentText() == today:
                self.log_display.append(f"{person_id} {person_name}")
                # 立即滚动到底部
                self.log_display.verticalScrollBar().setValue(
                    self.log_display.verticalScrollBar().maximum()
                )
            
            # 刷新日志列表确保今天的日志文件在列表中
            current_file = self.log_selector.currentText()
            self.refresh_log_list()
            
            # 如果当前未选择日志文件或不是今天的日志，自动切换到今天
            if not current_file or current_file != today:
                index = self.log_selector.findText(today)
                if index >= 0:
                    self.log_selector.setCurrentIndex(index)
            
            self.statusBar.showMessage(f"已生成: {person_name} {person_id}", 3000)
        except Exception as e:
            self.statusBar.showMessage(f"生成失败: {str(e)}", 5000)
            QMessageBox.critical(self, "错误", f"生成数据时发生错误：{str(e)}")
    
    def copy_id(self):
        text = self.id_display.text()
        if text:
            self.clipboard.setText(text)
            self.statusBar.showMessage("已复制身份证号到剪贴板", 3000)
    
    def copy_name(self):
        text = self.name_display.text()
        if text:
            self.clipboard.setText(text)
            self.statusBar.showMessage("已复制姓名到剪贴板", 3000)
    
    def copy_all(self):
        id_text = self.id_display.text()
        name_text = self.name_display.text()
        if id_text and name_text:
            self.clipboard.setText(f"{name_text} {id_text}")
            self.statusBar.showMessage("已复制姓名和身份证号到剪贴板", 3000)
    
    def refresh_log_list(self):
        """刷新日志文件列表"""
        current_text = self.log_selector.currentText()
        self.log_selector.clear()
        self.statusBar.showMessage("正在刷新日志列表...", 1000)
        
        log_dir = os.path.join(os.path.dirname(__file__), "log")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            self.statusBar.showMessage("已创建日志目录", 2000)
            return
            
        # 获取所有txt文件及其修改时间
        files = []
        for f in os.listdir(log_dir):
            if f.endswith('.txt'):
                path = os.path.join(log_dir, f)
                mtime = os.path.getmtime(path)
                files.append((f, mtime))
        
        if not files:
            self.statusBar.showMessage("未找到日志文件", 2000)
            return
            
        # 按修改时间降序排序
        files.sort(key=lambda x: x[1], reverse=True)
        sorted_files = [f[0] for f in files]
        self.log_selector.addItems(sorted_files)
        
        # 尝试选择之前选择的文件或当前日期的文件
        today_file = datetime.now().strftime("%Y%m%d") + ".txt"
        if current_text and current_text in sorted_files:
            index = sorted_files.index(current_text)
            self.log_selector.setCurrentIndex(index)
        elif today_file in sorted_files:
            index = sorted_files.index(today_file)
            self.log_selector.setCurrentIndex(index)
        elif sorted_files:  # 如果没有当天文件，选择最新的文件
            self.log_selector.setCurrentIndex(0)
            
        self.statusBar.showMessage("日志列表已刷新", 2000)
    
    def get_log_path(self):
        selected_file = self.log_selector.currentText()
        if not selected_file:
            return None
        log_dir = os.path.join(os.path.dirname(__file__), "log")
        return os.path.join(log_dir, selected_file)
    
    def load_log(self):
        self.statusBar.showMessage("正在加载日志...")
        log_path = self.get_log_path()
        if log_path and os.path.exists(log_path):
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    self.log_display.setText(f.read())
                self.statusBar.showMessage(f"已加载日志: {self.log_selector.currentText()}", 2000)
                # 滚动到底部
                self.log_display.verticalScrollBar().setValue(
                    self.log_display.verticalScrollBar().maximum()
                )
            except Exception as e:
                self.statusBar.showMessage(f"加载日志失败: {str(e)}", 3000)
                QMessageBox.warning(self, "警告", f"无法读取日志文件：{str(e)}")
        else:
            self.log_display.clear()
            self.statusBar.showMessage("未找到日志文件", 2000)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IDGeneratorApp()
    window.show()
    sys.exit(app.exec_())