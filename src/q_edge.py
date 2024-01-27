from PySide6.QtWidgets import QGraphicsLineItem

from src.q_node import QNode


class QEdge(QGraphicsLineItem):
    """Graph edge class."""
    _id = 0

    def __init__(self, node1: QNode = None, node2: QNode = None,
                 weight: float | None = None,
                 direction: int = 0, id: int | None = None):
        super().__init__()
        if id is None:
            self.id = QEdge._id
            QEdge._id += 1
        else:
            self.id = id
        self.nodes = [node1, node2]
        self.weight = weight
        self.direction = direction

    def add_nodes(self, node1: QNode, node2: QNode):
        self.nodes = [node1, node2]

    def add_weight(self, weight: float | None):
        self.weight = weight

    def add_direction(self, direction: int):
        self.direction = direction

    def get_nodes(self):
        return self.nodes
