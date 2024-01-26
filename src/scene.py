from PySide6.QtCore import Qt, QLineF, QPointF
from PySide6.QtGui import QColor, QPen, QBrush
from PySide6.QtGui import QTransform
from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
)


class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(-100, -100, 200, 200)

        self.selected = None

        self.active_mode = None

        self.node_pen = QPen(QColor(0, 0, 0), 1.5, Qt.SolidLine)
        self.node_brush = QBrush(QColor(255, 255, 255))

        self.edge_pen = QPen(QColor(0, 0, 0), 3.0, Qt.SolidLine)

        self.RADIUS = 25
        self.RADIUS_OFFSET = QPointF(self.RADIUS, self.RADIUS)

    def get_node_item(self, pos):
        for item in self.items():
            if isinstance(item, QGraphicsEllipseItem):
                center = item.pos() + self.RADIUS_OFFSET
                if (center.x() - pos.x())**2 + (center.y() - pos.y())**2 <= self.RADIUS**2:
                    return item
        return None

    def get_any_item(self, pos):
        item = self.get_node_item(pos)
        if item:
            return item
        else:
            return self.itemAt(pos, QTransform())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.active_mode == "Cursor":
                """Start moving node."""
                self.selected = None
                item = self.get_node_item(event.scenePos())
                if item:
                    self.selected = item

            elif self.active_mode == "Add Node":
                """Create new node."""
                x = event.scenePos().x()
                y = event.scenePos().y()

                node = QGraphicsEllipseItem(0, 0, self.RADIUS * 2, self.RADIUS * 2)
                node.setPos(x - self.RADIUS, y - self.RADIUS)
                node.setPen(self.node_pen)
                node.setBrush(self.node_brush)

                self.addItem(node)

            elif self.active_mode == "Add Edge":
                """Create new edge."""
                if not self.selected:
                    item = self.get_node_item(event.scenePos())
                    if item:
                        self.selected = item
                else:
                    item = self.get_node_item(event.scenePos())
                    if item and item != self.selected:
                        edge_item = QGraphicsLineItem()

                        edge = QLineF(self.selected.pos() + self.RADIUS_OFFSET,
                                      item.pos() + self.RADIUS_OFFSET)

                        edge_already_exists = False
                        for item in self.items():
                            if isinstance(item, QGraphicsLineItem):
                                if item.line() == edge or \
                                   (item.line().p1() == edge.p2() and item.line().p2() == edge.p1()):
                                    edge_already_exists = True
                                    break

                        if not edge_already_exists:
                            edge_item.setPen(self.edge_pen)
                            edge_item.setLine(edge)

                            self.addItem(edge_item)

                    self.selected = None

            elif self.active_mode == "Delete":
                "Delete node/edge."
                selected = self.get_any_item(event.scenePos())
                if selected:
                    if isinstance(selected, QGraphicsEllipseItem):
                        i = 0
                        while i < len(self.items()):
                            if isinstance(self.items()[i], QGraphicsLineItem):
                                if ((selected.pos() + self.RADIUS_OFFSET) in
                                   [self.items()[i].line().p1(), self.items()[i].line().p2()]):
                                    self.removeItem(self.items()[i])
                                    i -= 1
                            i += 1
                        self.removeItem(selected)
                    elif isinstance(selected, QGraphicsLineItem):
                        self.removeItem(selected)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.active_mode == "Cursor":
            """Moving node."""
            if self.selected:
                x = event.scenePos().x()
                y = event.scenePos().y()

                for item in self.items():
                    if isinstance(item, QGraphicsEllipseItem):
                        if self.selected.pos() == item.pos():
                            item.setPos(x - self.RADIUS, y - self.RADIUS)
                    elif isinstance(item, QGraphicsLineItem):
                        if item.line().p1() == self.selected.pos() + self.RADIUS_OFFSET:
                            item.setLine(QLineF(QPointF(x, y), item.line().p2()))
                        elif item.line().p2() == self.selected.pos() + self.RADIUS_OFFSET:
                            item.setLine(QLineF(item.line().p1(), QPointF(x, y)))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.active_mode == "Cursor":
            "Stop moving node."
            if self.selected:
                self.selected = None
