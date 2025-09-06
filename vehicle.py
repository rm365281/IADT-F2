from customer import Customer
from itinerary import Itinerary
from graph.node import Node

class Vehicle:
    depot_id: int
    itineraries: list[list[int]]
    capacity: int = 100
    full_itineraries: list[list[int]]
    distance: float = 0.0

    def __init__(self, depot_id: int, node_ids: list[list[int]], capacity: int = 100) -> None:
        self.depot_id = depot_id
        self.itineraries = node_ids
        self.capacity = capacity
        self.full_itineraries = [[depot_id] + itinerary + [depot_id] for itinerary in self.itineraries]

    def __str__(self):
        return f"Vehicle(depot_id={self.depot_id}, itineraries={self.itineraries}, capacity={self.capacity}, distance={self.distance})"