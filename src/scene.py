from PySide6.QtCore import Qt, QLineF, QPointF
from PySide6.QtGui import QColor, QPen, QBrush
from PySide6.QtGui import QTransform
from PySide6.QtWidgets import QGraphicsScene

from src.q_edge import QEdge
from src.q_node import QNode


class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(-100, -100, 200, 200)

        self.selected = None

        self.active_mode = None

        self.node_pen = QPen(QColor(0, 0, 0), 1.5, Qt.SolidLine)
        self.node_brush = QBrush(QColor(255, 255, 255))

        self.edge_pen = QPen(QColor(0, 0, 0), 3.0, Qt.SolidLine)

    def get_node_item(self, pos):
        for item in self.items():
            if isinstance(item, QNode):
                center = item.center()
                if (center.x() - pos.x())**2 + (center.y() - pos.y())**2 <= item.radius**2:
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

                node = QNode(x, y)

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
                        edge_item = QEdge()
                        edge = QLineF(self.selected.center(), item.center())

                        edge_already_exists = False
                        for item in self.items():
                            if isinstance(item, QEdge):
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
                    if isinstance(selected, QNode):
                        i = 0
                        while i < len(self.items()):
                            if isinstance(self.items()[i], QEdge):
                                if (selected.center() in
                                   [self.items()[i].line().p1(), self.items()[i].line().p2()]):
                                    self.removeItem(self.items()[i])
                                    i -= 1
                            i += 1
                        self.removeItem(selected)
                    elif isinstance(selected, QEdge):
                        self.removeItem(selected)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.active_mode == "Cursor":
            """Moving node."""
            if self.selected:
                x = event.scenePos().x()
                y = event.scenePos().y()

                for item in self.items():
                    if isinstance(item, QNode):
                        if self.selected.center() == item.center():
                            item.set_center(x, y)
                    elif isinstance(item, QEdge):
                        if item.line().p1() == self.selected.center():
                            item.setLine(QLineF(QPointF(x, y), item.line().p2()))
                        elif item.line().p2() == self.selected.center():
                            item.setLine(QLineF(item.line().p1(), QPointF(x, y)))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.active_mode == "Cursor":
            "Stop moving node."
            if self.selected:
                self.selected = None
