import json

from PySide6.QtCore import QPointF

from src.q_edge import QEdge
from src.q_node import QNode


class Graph:
    """Graph class."""
    def __init__(self, nodes: list[QNode] | None = None, edges: list[QEdge] | None = None):
        self.nodes = nodes if nodes else []
        self.edges = edges if edges else []

    def add_node(self, node: QNode):
        self.nodes.append(node)

    def add_edge(self, edge: QEdge):
        self.edges.append(edge)

    def delete_node(self, node: QNode):
        if node in self.nodes:
            i = 0
            while i < len(self.edges):
                if node in self.edges[i].nodes:
                    self.edges.pop(i)
                    i -= 1
                i += 1
            self.nodes.remove(node)

    def delete_edge(self, edge: QEdge):
        self.edges.remove(edge)

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
            "content_type": "Graph",
            "type_version": "1.0",
            "nodes": [],
            "edges": []
        }
        for node in self.nodes:
            res["nodes"].append(
                {
                    "id": node.id,
                    "x": node.center().x(),
                    "y": node.center().y(),
                    "r": node.radius,
                    "name": node.name
                }
            )

        for edge in self.edges:
            res["edges"].append(
                {
                    "id": edge.id,
                    "id_node_1": edge.nodes[0].id,
                    "id_node_2": edge.nodes[1].id,
                    "w": edge.weight,
                    "d": edge.direction
                }
            )

        return json.dumps(res)

    def from_json(self, data: str) -> bool:
        try:
            res = json.loads(data)
            if res["content_type"] != "Graph":
                return False
            if res["type_version"] != "1.0":
                return False

            self.clear()
            for node in res["nodes"]:
                self.add_node(QNode(node["x"], node["y"], node["r"], node["name"], node["id"]))
            for edge in res["edges"]:
                self.add_edge(QEdge(self.get_node_id(edge["id_node_1"]),
                                    self.get_node_id(edge["id_node_2"]),
                                    edge["w"], edge["d"], edge["id"]))
            return True
        except:
            return False
