from dataclasses import dataclass

import numpy as np
from vehicle import Vehicle

class Solution:
    vehicles: list[Vehicle]
    fitness: float = 0.0

    def __init__(self, vehicles: list[Vehicle]) -> None:
        self.vehicles = vehicles

    def __str__(self) -> str:
        lines = [f"Number of vehicles: {len(self.vehicles)}"]
        for v_idx, vehicle in enumerate(self.vehicles, start=1):
            vehicle_str = str(vehicle).replace("Vehicle", f"Vehicle {v_idx}")
            lines.append(f"  {vehicle_str}")
        return "\n".join(lines)
    
    def total_distance(self) -> float:
        return sum(vehicle.distance for vehicle in self.vehicles)
    
    def calculate_total_cost(self) -> None:
        penalty: float = 0
        total_distance = self.total_distance()

        distance_median = total_distance / len(self.vehicles)
        for vehicle in self.vehicles:
            if vehicle.distance > distance_median:
                penalty += (vehicle.distance - distance_median) * 10
        self.fitness = total_distance + penalty

    def flatten_routes(self) -> list[int]:
        route: list[int] = []
        for vehicle in self.vehicles:
            for itinerary in vehicle.itineraries:
                route += itinerary
        return route