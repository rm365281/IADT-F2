from customer import Customer
from itinerary import Itinerary

class Vehicle:
    depot: Customer
    itineraries: list[Itinerary]
    capacity: int = 100
    full_itineraries: list[Itinerary]

    def __init__(self, depot: Customer, itineraries: list[Itinerary], capacity: int = 100) -> None:
        self.depot = depot
        self.itineraries = itineraries
        self.capacity = capacity
        self.full_itineraries = [Itinerary(customers=([self.depot] + itinerary.customers + [self.depot])) for itinerary in self.itineraries]
    
    def calculate_distance(self, customer_distance_matrix: list[list[float]]) -> None:
        distance = 0
        for full_itinerary in self.full_itineraries:
            full_itinerary_length = len(full_itinerary.customers)
            for customer_index in range(full_itinerary_length):
                customer_a = full_itinerary.customers[customer_index]
                customer_b = full_itinerary.customers[(customer_index + 1) % full_itinerary_length]
                distance += customer_distance_matrix[customer_a.id][customer_b.id]
            full_itinerary.distance = distance

    def hasAtLeastOneCustomersInEachItinerary(self) -> bool:
        for itinerary in self.itineraries:
            if not itinerary.hasAtLeastOneCustomers():
                return False
        return True
    
    def total_distance(self) -> float:
        return sum(itinerary.distance for itinerary in self.full_itineraries)

    def __str__(self) -> str:
        lines = []
        
        total_customers = 0
        total_distance = 0.0
        all_customers = []
        
        for itinerary in self.full_itineraries:
            total_customers += len(itinerary.customers)
            all_customers.extend(itinerary.customers)
            total_distance += itinerary.distance
        
        lines.append(f"Vehicle (capacity={self.capacity}, customers={total_customers}, distance={round(total_distance, 2)}):")
        
        if not all_customers:
            lines.append("  [empty]")
        else:
            for customer in all_customers:
                lines.append(f"  {customer}")
        
        return "\n".join(lines)