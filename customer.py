from dataclasses import dataclass
from math import fabs

class Customer:
    id: int
    x: int
    y: int
    priority: int

    def __init__(self, id: int, city: tuple[int, int], priority: int = 1):
        self.id = id
        self.x = city[0]
        self.y = city[1]
        self.priority = priority

    def __str__(self):
        return f"Customer {self.id} at ({self.x}, {self.y})"