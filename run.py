import sys

from PySide6.QtWidgets import (
    QApplication
)
from  qt_material import apply_stylesheet

from app.views.main_window import WaterReminderApp




if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)
    window = WaterReminderApp()
    apply_stylesheet(app,theme="light_pink_500.xml")
    # window.show()
    sys.exit(app.exec())

