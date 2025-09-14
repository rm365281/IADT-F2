from .vehicle import Vehicle

class Solution:
    vehicles: list[Vehicle]
    fitness: float = 0.0

    def __init__(self, vehicles: list[Vehicle]) -> None:
        if not isinstance(vehicles, list) or not all(isinstance(v, Vehicle) for v in vehicles):
            raise TypeError('vehicles deve ser uma lista de Vehicle')
        self.vehicles = vehicles

    def __str__(self) -> str:
        lines = [f"Number of vehicles: {len(self.vehicles)}"]
        for v_idx, vehicle in enumerate(self.vehicles, start=1):
            vehicle_str = str(vehicle).replace("Vehicle", f"Vehicle {v_idx}")
            lines.append(f"  {vehicle_str}")
        return "\n".join(lines)
    
    def total_distance(self) -> float:
        return sum(vehicle.distance() for vehicle in self.vehicles)
    
    def flatten_routes(self) -> list[int]:
        route: list[int] = []
        for vehicle in self.vehicles:
            route += vehicle.customers()
        return route