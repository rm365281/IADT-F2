class Route:
    customers: list[int]

    def __init__(self, customers: list[int]) -> None:
        if not isinstance(customers, list) or not all(isinstance(c, int) for c in customers):
            raise TypeError('customers deve ser uma lista de int')
        self.customers = customers
        self.distance = 0.0

    def to_dict(self, customer_id_to_node=None):
        route_info = {
            "customers": self.customers,
            "distance": self.distance
        }
        if customer_id_to_node:
            route_info["coordinates"] = [
                {
                    "id": cid,
                    "x": customer_id_to_node[cid].x,
                    "y": customer_id_to_node[cid].y,
                    "name": getattr(customer_id_to_node[cid], "name", None)
                } for cid in self.customers if cid in customer_id_to_node
            ]
        return route_info

    def __str__(self):
        return f"Itinerary: {self.customers}, Distance: {self.distance}, Customers: {len(self.customers)-2}"

    __repr__ = __str__