from dataclasses import field

from customer import Customer

class Vehicle:
    depot: Customer
    itinerary: list[Customer]
    capacity: int = 100
    distance: float = field(default=0.0, compare=False)
    full_itinerary: list[Customer]

    def __init__(self, depot: Customer, itinerary: list[Customer], capacity: int = 100) -> None:
        self.depot = depot
        self.itinerary = itinerary
        self.capacity = capacity
        self.distance = 0.0
        self.full_itinerary = [self.depot] + self.itinerary + [self.depot]
    
    def calculate_distance(self, customer_distance_matrix: list[list[float]]):
        distance = 0
        full_itinerary_length = len(self.full_itinerary)
        for customer_index in range(full_itinerary_length):
            customer_a = self.full_itinerary[customer_index]
            customer_b = self.full_itinerary[(customer_index + 1) % full_itinerary_length]
            distance += customer_distance_matrix[customer_a.id][customer_b.id]
        self.distance = distance

    def hasAtLeastOneCustomers(self) -> bool:
        return len(self.itinerary) > 1
    
    def __str__(self):
        lines = []
        lines.append(f"Vehicle (capacity={self.capacity}, customers={len(self.itinerary)}, distance={round(self.distance, 2)}):")
        if not self.full_itinerary:
            lines.append("  [empty]")
        else:
            for customer in self.full_itinerary:
                lines.append(f"{customer}")
        return "\n".join(lines)