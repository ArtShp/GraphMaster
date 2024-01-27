from PySide6.QtWidgets import QGraphicsView

from src.scene import GraphicsScene


class GraphicsView(QGraphicsView):
    """Graphics view class."""
    def __init__(self):
        super().__init__()
        self.scene = GraphicsScene()
        self.setScene(self.scene)
