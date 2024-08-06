import json

from PySide6.QtCore import QTimer, Qt, QSize, QPoint, QPropertyAnimation
from PySide6.QtGui import QIcon, QMovie
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QSystemTrayIcon, \
    QMenu, QApplication, QDialog

from app.common.cfg import Config
from app.components.label import ClickableLabel

from app.views.settings_window import SettingsWidget
import app.resources.resouce
class WaterReminderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.reminder_times = None
        self.initConfig()
        # 创建一个 QTimer 对象
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_reminder)
        # 从文件加载提醒时间
        self.load_reminder_times()
        self.timer_running = False
        self.current_dialog = None  # 追踪当前显示的提醒对话框

        self.initUI()

    def show_reminder(self):
        print("show_reminder")
        # 如果已经存在提醒框，则不弹出新的
        if self.current_dialog and self.current_dialog.isVisible():
            print("已经有提醒了")
            return


        dialog = QDialog(self)
        dialog.setWindowTitle("喝水啦")
        dialog.setModal(False)
        dialog.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        dialog.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()

        # 创建 QLabel 来显示 GIF
        gif_label = ClickableLabel()
        movie = QMovie(":images/tips1.gif")
        movie.setScaledSize(QSize(200, 200))  # 设置 GIF 尺寸
        gif_label.setMovie(movie)
        movie.start()
        gif_label.clicked.connect(dialog.close)
        layout.addWidget(gif_label)


        dialog.setLayout(layout)

        # 调整对话框的大小
        dialog.setFixedSize(200, 240)

        # 获取屏幕大小
        screen_geometry = self.screen().geometry()
        dialog_width, dialog_height = dialog.width(), dialog.height()

        # 计算对话框的起始位置，确保它在屏幕范围内
        start_x = screen_geometry.width() - dialog_width
        start_y = screen_geometry.height() - dialog_height

        print(start_x, start_y)

        end_x = screen_geometry.width()- dialog_width
        end_y = screen_geometry.height() - dialog_height-500

        print(end_x, end_y)
        # 确保对话框的起始位置和结束位置在屏幕范围内
        start_pos = QPoint(max(start_x, 0), max(start_y, 0))
        end_pos = QPoint(max(end_x, 0), max(end_y, 0))
        dialog.move(start_pos)
        dialog.show()
        # 创建动画
        animation = QPropertyAnimation(dialog, b"pos")
        animation.setDuration(3000)
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.start()

        # 设置当前对话框为正在显示的对话框
        self.current_dialog = dialog
        # 在对话框关闭时，重置当前对话框
        dialog.finished.connect(self.close_dialog)

        # 调整消息框的大小
        pass

    def close_dialog(self):
        self.current_dialog = None
        pass

    def initUI(self):
        # 系统托盘图标
        self.tray_icon = QSystemTrayIcon(QIcon(":/images/icon.png"), self)
        self.tray_icon.setToolTip("喝水提醒软件")
        tray_menu = QMenu()

        open_server_action = tray_menu.addAction("开始提醒")
        open_server_action.setIcon(QIcon(":/images/check.png"))
        open_server_action.triggered.connect(self.toggle_reminder)
        tray_menu.addSeparator()

        setting_action = tray_menu.addAction("设置间隔时间")
        setting_action.setIcon(QIcon(":/images/setting.png"))
        setting_action.triggered.connect(self.settings_f)
        tray_menu.addSeparator()
        quit_action = tray_menu.addAction("退出")
        quit_action.triggered.connect(self.quit_app)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.settings_widget = SettingsWidget(parent_app=self)
        self.settings_widget.hide()
        open_server_action.trigger()

    def quit_app(self):
        self.tray_icon.hide()
        QApplication.instance().quit()

    def settings_f(self):
        self.settings_widget.line_edit.setText(self.reminder_times)
        self.settings_widget.show()
        pass

    def load_reminder_times(self):
        try:
            with open("cfg.json", "r") as file:
                data = json.load(file)
                self.reminder_times = data.get("date", "")
                if self.reminder_times != "":
                    self.timer.setInterval(int(self.reminder_times) * 60 * 1000)
                else:
                    self.timer_running = False
                    self.timer.stop()
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def toggle_reminder(self):
        actions = self.tray_icon.contextMenu().actions()
        if self.timer_running:
            self.timer.stop()
            print("停止提醒")
            if actions:
                frist_action = actions[0]
                frist_action.setText("开始提醒")
        else:
            self.timer.start()
            print("开启提醒")
            if actions:
                frist_action = actions[0]
                frist_action.setText("暂停提醒")
        self.timer_running = not self.timer_running

    def initConfig(self):
        cfg = Config()
        cfg.init()
        pass

    def update_reminder_times(self, reminder_times):
        self.reminder_times = reminder_times
        self.timer.stop()
        self.timer.setInterval(int(self.reminder_times) * 60 * 1000)
        self.timer.start()
