from itinerary import Itinerary

class Vehicle:

    def __init__(self, itinerary: Itinerary, capacity: int = 100, autonomy: float = 500.0) -> None:
        self.itinerary = itinerary
        self.capacity = capacity
        self.autonomy = autonomy

    def customers(self) -> list[int]:
        return self.itinerary.customers

    def distance(self) -> float:
        return self.itinerary.distance

    def update_distance(self, distance: float) -> None:
        self.itinerary.distance = distance

    def __str__(self):
        lines = [
            f"Vehicle(capacity={self.capacity}, total distance={self.distance()}, autonomy={self.autonomy}",
            f"     {str(self.itinerary)}"]
        return "\n".join(lines)

