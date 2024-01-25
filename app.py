import sys

from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QAction
from PySide6.QtGui import QColor, QPen, QBrush, QTransform
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsEllipseItem,
    QToolBar, QPushButton,
)


class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(-100, -100, 200, 200)
        self.selected = None
        self.selected_offset_x = 0
        self.selected_offset_y = 0

        self.active_mode = None

        self.node_pen = QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine)
        self.node_brush = QBrush(QColor(255, 255, 255, 255))

        self.RADIUS = 20

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.active_mode == "Cursor":
                """Start moving node."""
                x = event.scenePos().x()
                y = event.scenePos().y()

                if not self.selected:
                    item = self.itemAt(event.scenePos(), QTransform())
                    if item:
                        self.selected = item
                        self.selected_offset_x = x - item.pos().x()
                        self.selected_offset_y = y - item.pos().y()

            elif self.active_mode == "Add Node":
                """Create new node."""
                x = event.scenePos().x()
                y = event.scenePos().y()

                node = QGraphicsEllipseItem(0, 0, self.RADIUS * 2, self.RADIUS * 2)
                node.setPos(x - self.RADIUS, y - self.RADIUS)
                node.setPen(self.node_pen)
                node.setBrush(self.node_brush)

                self.addItem(node)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.active_mode == "Cursor":
            """Moving node."""
            if self.selected:
                x = event.scenePos().x()
                y = event.scenePos().y()
                self.selected.setPos(x - self.selected_offset_x, y - self.selected_offset_y)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.active_mode == "Cursor":
            "Stop moving node."
            if self.selected:
                self.selected = None


class GraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = GraphicsScene()
        self.setScene(self.scene)


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
                        QPushButton(text="Delete")]

        for button in self.buttons:
            button.setFixedSize(QSize(100, 50))
            button.setCheckable(True)
            button.clicked.connect(self.change_mode)
            self.toolbar.addWidget(button)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
