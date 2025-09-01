from dataclasses import dataclass, field

from numpy import deg2rad

from customer import Customer

class Vehicle:
    itinerary: list[Customer]
    capacity: int = 100
    distance: float = field(default=0.0, compare=False)

    def __init__(self, itinerary: list[Customer], capacity: int = 100) -> None:
        self.itinerary = itinerary
        self.capacity = capacity
        self.distance = 0.0

    def __str__(self):
        lines = []
        lines.append(f"Vehicle (capacity={self.capacity}, customers={len(self.itinerary)}, distance={round(self.distance, 2)}):")
        if not self.itinerary:
            lines.append("  [empty]")
        else:
            for customer in self.itinerary:
                lines.append(f"{customer}")
        return "\n".join(lines)