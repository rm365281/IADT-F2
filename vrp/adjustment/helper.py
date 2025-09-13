from domain.route import Route


class Helper:

    def __init__(self, graph, depot_identifier):
        self.__graph = graph
        self.__depot_identifier = depot_identifier

    def split_route_by_capacity(self, route: Route, vehicle_capacity: int) -> Route:
        """
        Split the route by vehicle capacity, inserting depots as needed.
        Args:
            route: The route to be split.
            vehicle_capacity: The capacity of the vehicle.

        Returns:
            The route split by vehicle capacity.

        Raises:
            ValueError: If any customer's demand is greater than the vehicle capacity.

        """
        new_route: list[int] = []
        current_load = 0
        for customer_identifier in route.customers:
            if customer_identifier == self.__depot_identifier:
                new_route.append(customer_identifier)
                continue
            demand = self.__graph.get_node_demand(customer_identifier)
            if demand > vehicle_capacity:
                raise ValueError(f"Customer {customer_identifier} demand ({demand}) exceeds vehicle capacity ({vehicle_capacity})")
            if current_load + demand > vehicle_capacity:
                new_route.append(self.__depot_identifier)
                current_load = 0
            new_route.append(customer_identifier)
            current_load += demand
        return Route(new_route)

    def remove_duplicated_sequencial_depots(self, route: Route) -> Route:
        """
        Remove duplicated sequential depots from the route.
        Args:
            route: The route to be processed.

        Returns:
            The route without duplicated sequential depots.

        """
        final_route: list[int] = []
        previous_customer_id = None
        for customer_identifier in route.customers:
            if not (previous_customer_id == self.__depot_identifier and customer_identifier == self.__depot_identifier):
                final_route.append(customer_identifier)
            previous_customer_id = customer_identifier
        return Route(final_route)

    def calculate_distance(self, route: Route) -> float:
        """
        Calculate the total distance of a given route.
        Args:
            route: The route for which to calculate the distance.

        Returns:
            The total distance of the route.

        """
        itinerary_distance = 0.0
        customers = route.customers
        for i in range(len(customers) - 1):
            itinerary_distance += self.__graph.get_edge_by_node_ids(customers[i], customers[i + 1]).distance
        return itinerary_distance
