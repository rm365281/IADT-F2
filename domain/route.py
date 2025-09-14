class Route:
    customers: list[int]

    def __init__(self, customers: list[int]) -> None:
        if not isinstance(customers, list) or not all(isinstance(c, int) for c in customers):
            raise TypeError('customers deve ser uma lista de int')
        self.customers = customers
        self.distance = 0.0

    def __str__(self):
        return f"Itinerary: {self.customers}, Distance: {self.distance}, Customers: {len(self.customers)-2}"

    __repr__ = __str__