import ctypes
import sys

from PySide6.QtWidgets import QApplication

from src.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("graphmasterapp")
    window = MainWindow()
    sys.exit(app.exec())
