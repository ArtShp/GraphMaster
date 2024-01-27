from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QGraphicsEllipseItem


class QNode(QGraphicsEllipseItem):
    """Graph node class."""
    _id = 0

    def __init__(self, x: int, y: int, r: int = 25, name: str = "", id: int | None = None):
        super().__init__(0, 0, r*2, r*2)
        if id is None:
            self.id = QNode._id
            QNode._id += 1
        else:
            self.id = id
        self.radius = r
        self.name = name
        self.set_center(x, y)

    def center(self) -> QPointF:
        return QPointF(self.pos().x() + self.radius, self.pos().y() + self.radius)

    def set_center(self, x: int, y: int):
        self.setPos(x - self.radius, y - self.radius)
