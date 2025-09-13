from domain.graph import Node

class Edge:

    def __init__(self, from_node: Node, to_node: Node, distance: float = 0) -> None:
        self.from_node: Node = from_node
        self.to_node: Node = to_node
        self.distance: float = distance

        tolls = []
        km = 150
        while km < distance:
            km += 150
            tolls.append(km)
        self.toll_quantity: int = len(tolls)

    def __str__(self) -> str:
        return f"Edge(from={self.from_node.identifier}, to={self.to_node.identifier}, distance={self.distance})"
    
    __repr__ = __str__