from dataclasses import dataclass
from customer import Customer
from vehicle import Vehicle

@dataclass(frozen=True)
class Solution:
    vehicles: list[Vehicle]

    def __str__(self):
        lines = []
        lines.append(f"Number of vehicles: {len(self.vehicles)}")
        for v_idx, vehicle in enumerate(self.vehicles, start=1):
            vehicle_str = str(vehicle).replace("Vehicle", f"Vehicle {v_idx}")
            lines.append(f"  {vehicle_str}")
        return "\n".join(lines)
    
    def total_distance(self) -> float:
        return sum(vehicle.distance for vehicle in self.vehicles)
    
    def calculate_distances(self, customer_distance_matrix: list[list[float]]):
        for vehicle in self.vehicles:
            vehicle.calculate_distance(customer_distance_matrix)

    def calculate_total_cost(self) -> float:
        distance_median: float = 0.0
        penalty = 0
        total_distance = 0
        for vehicle in self.vehicles:
            if not vehicle.hasAtLeastOneCustomers():
                penalty += 1000
            total_distance += vehicle.distance

        distance_median = total_distance / len(self.vehicles)
        for vehicle in self.vehicles:
            if vehicle.distance > distance_median:
                penalty += (vehicle.distance - distance_median) * 200
        return total_distance + penalty