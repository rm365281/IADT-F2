from dataclasses import field

from customer import Customer

class Vehicle:
    itinerary: list[Customer]
    capacity: int = 100
    distance: float = field(default=0.0, compare=False)

    def __init__(self, itinerary: list[Customer], capacity: int = 100) -> None:
        self.itinerary = itinerary
        self.capacity = capacity
        self.distance = 0.0
    
    def calculate_distance(self, customer_distance_matrix: list[list[float]]):
        distance = 0
        itinerary_length = len(self.itinerary)
        for customer_index in range(itinerary_length):
            customer_a = self.itinerary[customer_index]
            customer_b = self.itinerary[(customer_index + 1) % itinerary_length]
            distance += customer_distance_matrix[customer_a.id][customer_b.id]
        self.distance = distance

    def __str__(self):
        lines = []
        lines.append(f"Vehicle (capacity={self.capacity}, customers={len(self.itinerary)}, distance={round(self.distance, 2)}):")
        if not self.itinerary:
            lines.append("  [empty]")
        else:
            for customer in self.itinerary:
                lines.append(f"{customer}")
        return "\n".join(lines)