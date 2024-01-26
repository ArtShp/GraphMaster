from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QGraphicsEllipseItem


class QNode(QGraphicsEllipseItem):
    def __init__(self, x: int, y: int, r: int = 25):
        super().__init__(0, 0, r*2, r*2)
        self.radius = r
        self.set_center(x, y)

    def center(self) -> QPointF:
        return QPointF(self.pos().x() + self.radius, self.pos().y() + self.radius)

    def set_center(self, x: int, y: int):
        self.setPos(x - self.radius, y - self.radius)
