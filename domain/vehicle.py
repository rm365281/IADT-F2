from .route import Route

class Vehicle:

    def __init__(self, route: Route, capacity: int = 100, autonomy: float = 500.0) -> None:
        if not isinstance(route, Route):
            raise TypeError('route deve ser uma instância de Route')
        self.route = route
        self.capacity = capacity
        self.autonomy = autonomy

    def customers(self) -> list[int]:
        return self.route.customers

    def distance(self) -> float:
        return self.route.distance

    def to_dict(self, customer_id_to_node=None):
        return {
            "capacity": self.capacity,
            "autonomy": self.autonomy,
            "route": self.route.to_dict(customer_id_to_node=customer_id_to_node)
        }

    def __str__(self):
        lines = [
            f"Vehicle(capacity={self.capacity}, total distance={self.distance()}, autonomy={self.autonomy}",
            f"     {str(self.route)}"]
        return "\n".join(lines)
