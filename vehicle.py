class Vehicle:
    full_itineraries: list[list[int]]
    distance: float = 0.0

    def __init__(self, depot_id: int, itineraries: list[list[int]], capacity: int = 100, autonomy: float = 500.0) -> None:
        self.depot_id = depot_id
        self.itineraries = itineraries
        self.capacity = capacity
        self.full_itineraries = [[depot_id] + itinerary + [depot_id] for itinerary in self.itineraries]
        self.autonomy = autonomy

    def flatten_itineraries(self) -> list[int]:
        return [node for itinerary in self.itineraries for node in itinerary]

    def __str__(self):
        return f"Vehicle(depot_id={self.depot_id}, itineraries={self.full_itineraries}, capacity={self.capacity}, distance={self.distance}, autonomy={self.autonomy})"