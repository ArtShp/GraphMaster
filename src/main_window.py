from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QToolBar, QPushButton, QMessageBox

from src.view import GraphicsView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Set up the application's GUI."""
        self.setup_main_window()
        self.create_actions()
        self.create_menu()
        self.create_toolbar()
        self.show()

    def setup_main_window(self):
        """Create and arrange widgets in the main window."""
        window_size = QSize(800, 600)
        screen_size = self.screen().size()

        window_geometry = QRect((screen_size.width() - window_size.width()) / 2,
                                (screen_size.height() - window_size.height()) / 2,
                                window_size.width(), window_size.height())

        self.setMinimumSize(550, 400)
        self.setGeometry(window_geometry)
        self.setWindowTitle("Graph Master")

        self.setWindowIcon(QIcon("img/icon.png"))

        self.view = GraphicsView()
        self.setCentralWidget(self.view)

    def create_actions(self):
        """Create the application's menu actions."""
        # Create actions for File menu
        self.quit_act = QAction("&Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.close)

    def create_menu(self):
        """Create the application's menu bar."""
        self.menuBar().setNativeMenuBar(False)
        # Create file menu and add actions
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.quit_act)

    def create_toolbar(self):
        """Create the application's toolbar."""
        self.toolbar = QToolBar("Modes", self)

        self.buttons = [QPushButton(text="Cursor"),
                        QPushButton(text="Hand"),
                        QPushButton(text="Add Node"),
                        QPushButton(text="Add Edge"),
                        QPushButton(text="Delete"),
                        QPushButton(text="Clear Graph")]

        for button in self.buttons:
            button.setFixedSize(QSize(100, 50))
            self.toolbar.addWidget(button)

        for i in range(len(self.buttons) - 1):
            self.buttons[i].setCheckable(True)
            self.buttons[i].clicked.connect(self.change_mode)

        self.buttons[-1].clicked.connect(self.clear_graph)

        self.last_button = self.buttons[0]
        self.active_mode = self.buttons[0].text()
        self.view.scene.active_mode = self.active_mode
        self.buttons[0].setChecked(True)

        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

    def change_mode(self):
        """Event handler for changing the mode of working."""
        self.last_button = self.sender()
        self.active_mode = self.last_button.text()
        self.view.scene.active_mode = self.active_mode
        self.last_button.setChecked(True)

        for button in self.buttons:
            if self.last_button != button:
                button.setChecked(False)

    def clear_graph(self):
        """Event handler for clearing the graph."""
        button = QMessageBox.warning(self, self.windowTitle(), "Are you sure you want to clear the graph?",
                                     buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     defaultButton=QMessageBox.StandardButton.No)

        if button == QMessageBox.StandardButton.Yes:
            self.view.scene.clear_graph()
