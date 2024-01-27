from PySide6.QtWidgets import QPushButton

from src.graphics_mode import GraphicsMode


class QButton(QPushButton):
    def __init__(self, text: str, mode: GraphicsMode):
        super().__init__(text=text)
        self.mode = mode