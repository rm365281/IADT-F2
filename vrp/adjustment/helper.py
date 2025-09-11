from vehicle import Vehicle


class Helper:

    def __init__(self, graph, depot_identifier):
        self.graph = graph
        self.depot_identifier = depot_identifier

    def split_route_by_capacity(self, vehicle: Vehicle) -> list[int]:
        new_route: list[int] = []
        current_load = 0
        for customer_identifier in vehicle.customers():
            if customer_identifier == self.depot_identifier:
                new_route.append(customer_identifier)
                continue
            demand = self.graph.get_node_demand(customer_identifier)
            if current_load + demand > vehicle.capacity:
                new_route.append(self.depot_identifier)
                current_load = 0
            new_route.append(customer_identifier)
            current_load += demand
        return new_route

    def remove_duplicated_sequencial_depots(self, itinerary: list[int]) -> list[int]:
        final_itinerary: list[int] = []
        previous_customer_id = None
        for customer_identifier in itinerary:
            if not (previous_customer_id == self.depot_identifier and customer_identifier == self.depot_identifier):
                final_itinerary.append(customer_identifier)
            previous_customer_id = customer_identifier
        return final_itinerary
