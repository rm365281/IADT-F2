from dataclasses import field

from customer import Customer
from itinerary import Itinerary

class Vehicle:
    depot: Customer
    itinerary: Itinerary
    capacity: int = 100
    full_itinerary: Itinerary

    def __init__(self, depot: Customer, itinerary: Itinerary, capacity: int = 100) -> None:
        self.depot = depot
        self.itinerary = itinerary
        self.capacity = capacity
        self.full_itinerary = Itinerary(customers=([self.depot] + self.itinerary.customers + [self.depot]))
    
    def calculate_distance(self, customer_distance_matrix: list[list[float]]):
        distance = 0
        full_itinerary_length = len(self.full_itinerary.customers)
        for customer_index in range(full_itinerary_length):
            customer_a = self.full_itinerary.customers[customer_index]
            customer_b = self.full_itinerary.customers[(customer_index + 1) % full_itinerary_length]
            distance += customer_distance_matrix[customer_a.id][customer_b.id]
        self.itinerary.distance = distance

    def hasAtLeastOneCustomers(self) -> bool:
        return len(self.itinerary.customers) > 1
    
    def __str__(self):
        lines = []
        lines.append(f"Vehicle (capacity={self.capacity}, customers={len(self.itinerary.customers)}, distance={round(self.itinerary.distance, 2)}):")
        if not self.full_itinerary.customers:
            lines.append("  [empty]")
        else:
            for customer in self.full_itinerary.customers:
                lines.append(f"{customer}")
        return "\n".join(lines)