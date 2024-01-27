"""
Project: Graph Master
Author: Artemiy Shipovalov
Created on: January 2024
"""

import ctypes
import sys

from PySide6.QtWidgets import QApplication

from src.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)  # create app
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("graphmasterapp")  # to show app icon in taskbar
    window = MainWindow()  # create main window
    sys.exit(app.exec())  # start app
