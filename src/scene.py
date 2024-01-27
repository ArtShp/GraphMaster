from PySide6.QtCore import Qt, QLineF, QPointF
from PySide6.QtGui import QColor, QPen, QBrush
from PySide6.QtGui import QTransform
from PySide6.QtWidgets import QGraphicsScene

from src.graph import Graph
from src.graphics_mode import GraphicsMode
from src.q_edge import QEdge
from src.q_node import QNode


class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(-100, -100, 200, 200)

        self.selected = None

        self.active_mode = GraphicsMode.NONE

        self.node_pen = QPen(QColor(0, 0, 0), 1.5, Qt.SolidLine)
        self.node_brush = QBrush(QColor(255, 255, 255))

        self.edge_pen = QPen(QColor(0, 0, 0), 3.0, Qt.SolidLine)

        self.graph = Graph()

    def change_mode(self, mode: GraphicsMode):
        self.active_mode = mode

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            match self.active_mode:
                case GraphicsMode.CURSOR:
                    self.select_node(event.scenePos())
                case GraphicsMode.ADD_NODE:
                    self.add_node(event.scenePos())
                case GraphicsMode.ADD_EDGE:
                    self.add_edge(event.scenePos())
                case GraphicsMode.DELETE_ITEM:
                    self.delete_item(event.scenePos())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.active_mode == GraphicsMode.CURSOR:
            self.move_node(event.scenePos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.active_mode == GraphicsMode.CURSOR:
            self.finish_moving_node()

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

    def select_node(self, pos: QPointF):
        """Start moving node."""
        self.selected = None
        item = self.get_node_item(pos)
        if item:
            self.selected = item

    def add_node(self, pos: QPointF):
        """Create new node."""
        node = QNode(pos.x(), pos.y())
        self.draw_node(node)
        self.graph.add_node(node)

    def add_edge(self, pos: QPointF):
        """Create new edge."""
        if not self.selected:
            item = self.get_node_item(pos)
            if item:
                self.selected = item
        else:
            node = self.get_node_item(pos)
            if node and node != self.selected:
                edge = QLineF(self.selected.center(), node.center())

                edge_already_exists = False
                for item in self.items():
                    if isinstance(item, QEdge):
                        if item.line() == edge or \
                                (item.line().p1() == edge.p2() and item.line().p2() == edge.p1()):
                            edge_already_exists = True
                            break

                if not edge_already_exists:
                    edge_item = QEdge(self.selected, node)
                    self.draw_edge(edge_item, edge)
                    self.graph.add_edge(edge_item)

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
                self.graph.delete_node(selected)
            elif isinstance(selected, QEdge):
                self.removeItem(selected)
                self.graph.delete_edge(selected)

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

    def clear_graph(self):
        """Clear graph."""
        self.clear()
        self.graph.clear()

    def draw_node(self, node: QNode):
        node.setPen(self.node_pen)
        node.setBrush(self.node_brush)
        node.setZValue(1000)
        self.addItem(node)

    def draw_edge(self, edge: QEdge, line: QLineF):
        edge.setPen(self.edge_pen)
        edge.setLine(line)
        edge.setZValue(0)
        self.addItem(edge)

    def draw_graph(self):
        """Draw graph that was imported."""
        self.clear()
        for node in self.graph.nodes:
            self.draw_node(node)
        if self.graph.nodes:
            QNode._id = self.graph.nodes[-1].id + 1

        for edge in self.graph.edges:
            self.draw_edge(edge, QLineF(edge.nodes[0].center(), edge.nodes[1].center()))
        if self.graph.edges:
            QEdge._id = self.graph.edges[-1].id + 1
