from pathlib import Path

from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QToolBar, QPushButton, QMessageBox, QFileDialog

from src.graphics_mode import GraphicsMode
from src.q_button import QButton
from src.view import GraphicsView


class MainWindow(QMainWindow):
    """Main window class."""
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

        self.view = GraphicsView()  # where graph is shown
        self.setCentralWidget(self.view)

    def create_actions(self):
        """Create the application's menu actions."""
        self.quit_act = QAction("&Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.close)

        self.import_act = QAction("&Import")
        self.import_act.setShortcut("Ctrl+I")
        self.import_act.triggered.connect(self.import_graph)

        self.export_act = QAction("&Export")
        self.export_act.setShortcut("Ctrl+E")
        self.export_act.triggered.connect(self.export_graph)

    def create_menu(self):
        """Create the application's menu bar."""
        self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.quit_act)
        file_menu.addAction(self.import_act)
        file_menu.addAction(self.export_act)

    def create_toolbar(self):
        """Create the application's toolbar."""
        toolbar = QToolBar("Modes", self)

        self.buttons = [cursor_button := QButton("Cursor", GraphicsMode.CURSOR),
                        QButton("Add Node", GraphicsMode.ADD_NODE),
                        QButton("Add Edge", GraphicsMode.ADD_EDGE),
                        QButton("Delete", GraphicsMode.DELETE_ITEM),
                        clear_button := QPushButton("Clear Graph")]

        for button in self.buttons:
            button.setFixedSize(QSize(100, 50))
            toolbar.addWidget(button)

        for i in range(len(self.buttons) - 1):
            self.buttons[i].setCheckable(True)
            self.buttons[i].clicked.connect(self.change_mode)

        clear_button.clicked.connect(self.clear_graph)

        self.view.scene.change_mode(cursor_button.mode)
        cursor_button.setChecked(True)

        self.addToolBar(Qt.TopToolBarArea, toolbar)

    def change_mode(self):
        """Event handler for changing the mode of working."""
        self.view.scene.change_mode(self.sender().mode)
        self.sender().setChecked(True)

        for button in self.buttons:
            if self.sender() != button:
                button.setChecked(False)

    def clear_graph(self):
        """Event handler for clearing the graph."""
        button = QMessageBox.warning(self, self.windowTitle(), "Are you sure you want to clear the graph?",
                                     buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     defaultButton=QMessageBox.StandardButton.No)

        if button == QMessageBox.StandardButton.Yes:
            self.view.scene.clear_graph()

    def export_graph(self):
        """Event handler for exporting the graph to json file."""
        data = self.view.scene.graph.to_json()
        filename, ok = QFileDialog.getSaveFileName(
            self,
            "Save as",
            "data.txt",
            "Graph JSON (*.txt)"
        )
        if filename:
            path = Path(filename)
            with open(path, "w") as file:
                file.write(data)

    def import_graph(self):
        """Event handler for importing the graph from json file."""
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a file",
            filter="Graph JSON (*.txt)"
        )
        if filename:
            path = Path(filename)
            with open(path, "r") as file:
                data = file.read()

            ok = self.view.scene.graph.from_json(data)
            if ok:
                self.view.scene.draw_graph()
