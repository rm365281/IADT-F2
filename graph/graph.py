from graph import Node
from graph import Edge


class Graph:

    def __init__(self) -> None:
        self._nodes: list[Node] = list()
        self._edges: list[Edge] = list()

    def is_empty(self) -> bool:
        return len(self._nodes) == 0
    
    def add_node(self, node: Node) -> None:
        if node in self._nodes:
            raise ValueError(f"Vertex {node} already exists.")
        
        self._nodes.append(node)

    def add_edge(self, edge: Edge) -> None:
        if edge.from_node not in self:
            self.add_node(edge.from_node)

        if edge.to_node not in self:
            self.add_node(edge.to_node)

        self._edges.append(edge)

    def get_node(self, node_id: int) -> Node:
        for node in self._nodes:
            if node.identifier == node_id:
                return node
        raise ValueError(f"Node {node_id} does not exist.")

    def get_edge(self, from_node: Node, to_node: Node) -> Edge:
        for edge in self._edges:
            if edge.from_node == from_node and edge.to_node == to_node:
                return edge
        raise ValueError(f"Edge from {from_node} to {to_node} does not exist.")
    
    def get_edges(self) -> list[Edge]:
        return self._edges

    def get_nodes(self) -> list[Node]:
        return self._nodes

    def __contains__(self, node: Node) -> bool:
        return node in self._nodes
    
    def __str__(self):
        return f"Graph with {len(self._nodes)} nodes and {len(self._edges)} edges."