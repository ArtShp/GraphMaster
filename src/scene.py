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

    def get_node_item(self, pos: QPointF) -> QNode | None:
        for item in self.items():
            if isinstance(item, QNode):
                center = item.center()
                if (center.x() - pos.x())**2 + (center.y() - pos.y())**2 <= item.radius**2:
                    return item
        return None

    def get_any_item(self, pos: QPointF) -> QNode | QEdge | None:
        item = self.get_node_item(pos)
        if item:
            return item
        else:
            return self.itemAt(pos, QTransform())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.active_mode == "Cursor":
                self.select_node(event.scenePos())
            elif self.active_mode == "Add Node":
                self.add_node(event.scenePos())
            elif self.active_mode == "Add Edge":
                self.add_edge(event.scenePos())
            elif self.active_mode == "Delete":
                self.delete_item(event.scenePos())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.active_mode == "Cursor":
            self.move_node(event.scenePos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.active_mode == "Cursor":
            self.finish_moving_node()

    def select_node(self, pos: QPointF):
        """Start moving node."""
        self.selected = None
        item = self.get_node_item(pos)
        if item:
            self.selected = item

    def add_node(self, pos: QPointF):
        """Create new node."""
        node = QNode(pos.x(), pos.y())

        node.setPen(self.node_pen)
        node.setBrush(self.node_brush)

        node.setZValue(1000)

        self.addItem(node)

    def add_edge(self, pos: QPointF):
        """Create new edge."""
        if not self.selected:
            item = self.get_node_item(pos)
            if item:
                self.selected = item
        else:
            node = self.get_node_item(pos)
            if node and node != self.selected:
                edge_item = QEdge()
                edge = QLineF(self.selected.center(), node.center())

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

                    edge_item.add_nodes(self.selected, node)

                    edge_item.setZValue(0)

                    self.addItem(edge_item)

            self.selected = None

    def delete_item(self, pos: QPointF):
        """Delete node/edge."""
        selected = self.get_any_item(pos)
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

    def move_node(self, pos: QPointF):
        """Moving node."""
        if self.selected:
            x, y = pos.x(), pos.y()
            for item in self.items():
                if isinstance(item, QNode):
                    if self.selected.center() == item.center():
                        item.set_center(x, y)
                if isinstance(item, QEdge):
                    if item.get_nodes()[0] == self.selected:
                        item.setLine(QLineF(QPointF(x, y), item.line().p2()))
                    elif item.get_nodes()[1] == self.selected:
                        item.setLine(QLineF(item.line().p1(), QPointF(x, y)))

    def finish_moving_node(self):
        """Stop moving node."""
        if self.selected:
            self.selected = None
