from PySide6.QtCore import QPointF

from src.q_edge import QEdge
from src.q_node import QNode


class Graph:
    def __init__(self, nodes: list[QNode] | None = None, edges: list[QEdge] | None = None):
        self.nodes = nodes if nodes else []
        self.edges = edges if edges else []
        self.graph = {}

        self.generate_graph()

    def generate_graph(self):
        for node in self.nodes:
            self.graph[node] = []
        for edge in self.edges:
            self.graph[edge.nodes[0]].append(edge.nodes[1])
            self.graph[edge.nodes[1]].append(edge.nodes[0])

    def add_node(self, node: QNode):
        self.nodes.append(node)
        self.graph[node] = []

    def add_edge(self, edge: QEdge):
        self.edges.append(edge)
        self.graph[edge.nodes[0]].append(edge.nodes[1])
        self.graph[edge.nodes[1]].append(edge.nodes[0])

    def delete_node(self, node: QNode):
        if node in self.nodes:
            i = 0
            while i < len(self.edges):
                if node in self.edges[i]:
                    self.edges.pop(i)
                    i -= 1
                i += 1
            self.nodes.remove(node)
            del self.graph[node]

    def delete_edge(self, edge: QEdge):
        if edge in self.edges:
            self.edges.remove(edge)
            self.graph[edge.nodes[0]].remove(edge.nodes[1])
            self.graph[edge.nodes[1]].remove(edge.nodes[0])

    def get_node(self, cords: QPointF) -> QNode | None:
        for node in self.nodes:
            if node.center() == cords:
                return node
        return None

    def get_edges(self, node: QNode) -> list[QEdge]:
        res = []
        for edge in self.edges:
            if node in edge.nodes:
                res.append(edge)
        return res
