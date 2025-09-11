class Itinerary:
    customers: list[int]

    def __init__(self, customers: list[int]) -> None:
        self.customers = customers
        self.distance = 0.0

    def __str__(self):
        return f"Itinerary: {self.customers}, Distance: {self.distance}, Customers: {len(self.customers)-2}"

    __repr__ = __str__