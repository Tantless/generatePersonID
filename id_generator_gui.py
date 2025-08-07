import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QGroupBox, QRadioButton, QPushButton, QLabel, QLineEdit,
                            QTextEdit, QComboBox, QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QGuiApplication, QClipboard
import function
import os
from datetime import datetime

class IDGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("身份证号与姓名生成器")
        # 居中显示窗口
        screen = QGuiApplication.primaryScreen().geometry()
        width, height = 850, 550
        self.move(
            (screen.width() - width) // 2,
            (screen.height() - height) // 2
        )
        self.resize(width, height)
        
        # 主窗口布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # 左侧面板 - 生成器
        left_panel = QGroupBox("生成器")
        left_layout = QVBoxLayout()
        
        # 性别选择
        self.gender_group = QGroupBox("性别选择")
        gender_layout = QVBoxLayout()
        self.random_radio = QRadioButton("随机", checked=True)
        self.male_radio = QRadioButton("男")
        self.female_radio = QRadioButton("女")
        gender_layout.addWidget(self.random_radio)
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        self.gender_group.setLayout(gender_layout)
        left_layout.addWidget(self.gender_group)
        
        # 生成按钮
        self.generate_btn = QPushButton("生成")
        self.generate_btn.clicked.connect(self.generate_data)
        left_layout.addWidget(self.generate_btn)
        
        # 结果显示
        self.id_label = QLabel("身份证号:")
        self.id_display = QLineEdit()
        self.id_display.setReadOnly(True)
        self.name_label = QLabel("姓名:")
        self.name_display = QLineEdit()
        self.name_display.setReadOnly(True)
        
        # 复制按钮
        copy_layout = QHBoxLayout()
        self.copy_id_btn = QPushButton("复制身份证号")
        self.copy_id_btn.clicked.connect(self.copy_id)
        self.copy_name_btn = QPushButton("复制姓名")
        self.copy_name_btn.clicked.connect(self.copy_name)
        copy_layout.addWidget(self.copy_id_btn)
        copy_layout.addWidget(self.copy_name_btn)
        
        left_layout.addWidget(self.id_label)
        left_layout.addWidget(self.id_display)
        left_layout.addWidget(self.name_label)
        left_layout.addWidget(self.name_display)
        left_layout.addLayout(copy_layout)
        
        left_panel.setLayout(left_layout)
        
        # 右侧面板 - 日志查看器
        right_panel = QGroupBox("日志查看器")
        right_layout = QVBoxLayout()
        
        # 日志文件选择
        self.log_selector = QComboBox()
        self.refresh_log_list()
        self.log_selector.currentTextChanged.connect(self.load_log)
        right_layout.addWidget(self.log_selector)
        
        # 日志显示与编辑
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(False)
        right_layout.addWidget(self.log_display)
        
        # 保存按钮
        self.save_btn = QPushButton("保存修改")
        self.save_btn.clicked.connect(self.save_log)
        right_layout.addWidget(self.save_btn)
        
        right_panel.setLayout(right_layout)
        
        # 添加到主布局并设置比例
        main_layout.addWidget(left_panel, 2)  # 左侧占2份
        main_layout.addWidget(right_panel, 3)  # 右侧占3份
        
        # 初始化加载日志列表
        self.refresh_log_list()
        if self.log_selector.count() > 0:
            self.load_log()
            # 延迟100ms确保内容加载完成后再滚动
            QTimer.singleShot(100, lambda: self.log_display.verticalScrollBar().setValue(
                self.log_display.verticalScrollBar().maximum()
            ))
    
    def get_selected_gender(self):
        if self.male_radio.isChecked():
            return 1
        elif self.female_radio.isChecked():
            return 2
        else:
            return 0
    
    def generate_data(self):
        # 获取当前日期对应的日志文件名
        today = datetime.now().strftime("%Y%m%d") + ".txt"
        
        gender = self.get_selected_gender()
        person_id, person_name = function.summon_newPerson(gender)
        self.id_display.setText(person_id)
        self.name_display.setText(person_name)
        
        # 直接追加新内容到日志显示
        new_entry = f"{person_id} {person_name}\n"
        self.log_display.append(new_entry)
        
        # 刷新日志列表
        self.refresh_log_list()
        
        # 自动选择当前日期的日志文件
        index = self.log_selector.findText(today)
        if index >= 0:
            self.log_selector.setCurrentIndex(index)
        
        # 立即滚动到底部
        self.log_display.verticalScrollBar().setValue(
            self.log_display.verticalScrollBar().maximum()
        )
    
    def copy_id(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.id_display.text())
    
    def copy_name(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.name_display.text())
    
    def refresh_log_list(self):
        """刷新日志文件列表"""
        self.log_selector.clear()
        log_dir = os.path.join(os.path.dirname(__file__), "log")
        if os.path.exists(log_dir):
            # 获取所有txt文件及其修改时间
            files = []
            for f in os.listdir(log_dir):
                if f.endswith('.txt'):
                    path = os.path.join(log_dir, f)
                    mtime = os.path.getmtime(path)
                    files.append((f, mtime))
            
            # 按修改时间降序排序
            files.sort(key=lambda x: x[1], reverse=True)
            sorted_files = [f[0] for f in files]
            self.log_selector.addItems(sorted_files)
            
            # 尝试选择当前日期的文件
            today_file = datetime.now().strftime("%Y%m%d") + ".txt"
            if today_file in sorted_files:
                index = sorted_files.index(today_file)
                self.log_selector.setCurrentIndex(index)
            elif sorted_files:  # 如果没有当天文件，选择最新的文件
                self.log_selector.setCurrentIndex(0)
    
    def get_log_path(self):
        selected_file = self.log_selector.currentText()
        if not selected_file:
            return None
        log_dir = os.path.join(os.path.dirname(__file__), "log")
        return os.path.join(log_dir, selected_file)
    
    def load_log(self):
        log_path = self.get_log_path()
        if log_path and os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                self.log_display.setText(f.read())
        else:
            self.log_display.clear()
    
    def save_log(self):
        log_path = self.get_log_path()
        if log_path:
            # 直接保存文件而不刷新列表
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(self.log_display.toPlainText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IDGeneratorApp()
    window.show()
    sys.exit(app.exec_())