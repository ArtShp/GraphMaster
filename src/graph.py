import json

from PySide6.QtCore import QPointF

from src.q_edge import QEdge
from src.q_node import QNode


class Graph:
    def __init__(self, nodes: list[QNode] | None = None, edges: list[QEdge] | None = None):
        self.nodes = nodes if nodes else []
        self.edges = edges if edges else []
        # self.graph = {}

        self.generate_graph()

    def generate_graph(self):
        # for node in self.nodes:
        #     self.graph[node] = []
        # for edge in self.edges:
        #     self.graph[edge.nodes[0]].append(edge.nodes[1])
        #     self.graph[edge.nodes[1]].append(edge.nodes[0])
        pass

    def add_node(self, node: QNode):
        self.nodes.append(node)
        # self.graph[node] = []

    def add_edge(self, edge: QEdge):
        self.edges.append(edge)
        # self.graph[edge.nodes[0]].append(edge.nodes[1])
        # self.graph[edge.nodes[1]].append(edge.nodes[0])

    def delete_node(self, node: QNode):
        if node in self.nodes:
            i = 0
            while i < len(self.edges):
                if node in self.edges[i].nodes:
                    self.edges.pop(i)
                    i -= 1
                i += 1
            self.nodes.remove(node)
            # del self.graph[node]

    def delete_edge(self, edge: QEdge):
        self.edges.remove(edge)
        # self.graph[edge.nodes[0]].remove(edge.nodes[1])
        # self.graph[edge.nodes[1]].remove(edge.nodes[0])

    def get_node(self, cords: QPointF) -> QNode | None:
        for node in self.nodes:
            if node.center() == cords:
                return node
        return None

    def get_node_id(self, id: int) -> QNode | None:
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    def get_edges(self, node: QNode) -> list[QEdge]:
        res = []
        for edge in self.edges:
            if node in edge.nodes:
                res.append(edge)
        return res

    def clear(self):
        self.nodes = []
        self.edges = []

    def to_json(self) -> str:
        res = {
            "nodes": [],
            "edges": []
        }
        for node in self.nodes:
            res["nodes"].append([node.id, node.center().x(), node.center().y(), node.radius, node.name])

        for edge in self.edges:
            res["edges"].append([edge.id, edge.nodes[0].id, edge.nodes[1].id, edge.weight, edge.direction])

        return json.dumps(res)

    def from_json(self, data: str):
        self.clear()
        res = json.loads(data)
        for node in res["nodes"]:
            self.add_node(QNode(node[1], node[2], node[3], node[4], node[0]))
        for edge in res["edges"]:
            self.add_edge(QEdge(self.get_node_id(edge[1]), self.get_node_id(edge[2]),
                                edge[3], edge[4], edge[0]))
