from dataclasses import field
from customer import Customer


class Itinerary:
    customers: list[Customer]
    distance: float = field(default=0.0, compare=False)

    def __init__(self, customers: list[Customer]) -> None:
        self.customers = customers
        self.distance = 0.0