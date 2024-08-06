import json

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout


class SettingsWidget(QWidget):
    def __init__(self, parent_app):
        super().__init__()

        self.line_edit = None
        self.cancel_button = None
        self.add_button = None
        self.parent_app = parent_app
        self.initUI()


    def initUI(self):
        self.setWindowTitle("请输入间隔时间（分钟）")
        self.setGeometry(100, 100, 300, 100)

        layout = QVBoxLayout()

        # 创建 QLineEdit 对象
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("提醒间隔")
        layout.addWidget(self.line_edit)

        # 设置正则表达式验证器，只允许输入正整数
        regex = QRegularExpression(r"^[1-9]\d*$")
        validator = QRegularExpressionValidator(regex)
        self.line_edit.setValidator(validator)
        btn_layout = QHBoxLayout()
        self.add_button = QPushButton("确定")
        self.add_button.setFixedWidth(80)
        self.add_button.clicked.connect(self.add_tips)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setFixedWidth(80)
        self.cancel_button.clicked.connect(self.close_window)
        btn_layout.addWidget(self.add_button)
        btn_layout.addWidget(self.cancel_button)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def add_tips(self):
        input_text = self.line_edit.text()
        self.parent_app.update_reminder_times(input_text)

        data = {"date": input_text}
        # 清空JSON文件
        open("cfg.json", "w").close()
        with open("cfg.json", "w") as file:
            json.dump(data, file, indent=4)
        self.close()

    def close_window(self):
        self.hide()
        pass