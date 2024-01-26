from PySide6.QtWidgets import QGraphicsLineItem

from src.q_node import QNode


class QEdge(QGraphicsLineItem):
    def __init__(self):
        super().__init__()
        self.nodes = []

    def add_nodes(self, node1: QNode, node2: QNode):
        self.nodes = [node1, node2]
