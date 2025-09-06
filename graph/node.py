class Node:

    def __init__(self, id: int = None, x: float = None, y: float = None) -> None:
        self.id: int = id
        self.x: float = x
        self.y: float = y

    def __eq__(self, value) -> bool:
        if not isinstance(value, Node):
            return False
        return self.id == value.id
    
    def __str__(self):
        return f"Node(id={self.id}, x={self.x}, y={self.y})"
    
    __repr__ = __str__