class Node:

    def __init__(self, identifier: int = None, x: float = None, y: float = None, priority: int = 0) -> None:
        self.identifier: int = identifier
        self.x: float = x
        self.y: float = y
        self.priority: int = priority

    def __eq__(self, value) -> bool:
        if not isinstance(value, Node):
            return False
        return self.identifier == value.identifier
    
    def __str__(self):
        return f"Node(id={self.identifier}, x={self.x}, y={self.y}, priority={self.priority})"
    
    __repr__ = __str__