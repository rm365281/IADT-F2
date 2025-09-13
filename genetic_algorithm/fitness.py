from domain.graph import Node, Graph
from domain.vehicle import Vehicle


class Fitness:
    def __init__(self, graph: Graph=None):
        self.__graph = graph

    @staticmethod
    def total_distance(vehicles: list[Vehicle]) -> float:
        """
        Calculate the total distance of all vehicles in the solution.
        Args:
            vehicles: List of vehicles in the solution.

        Returns:
            Total distance of all vehicles.
        """
        return sum(vehicle.distance() for vehicle in vehicles)

    def calculate_tolls_penality(self, vehicles: list[Vehicle]) -> int:
        """
        Calculate the penality by passing by tolls;
        Args:
            vehicles: List of vehicles in the solution.

        Returns:
            Penality value.
        """
        if self.__graph is None:
            raise ValueError("Graph is not set for Fitness calculation.")

        total_tolls = 0
        for vehicle in vehicles:
            route = vehicle.customers()
            for i in range(len(route) - 1):
                total_tolls += self.__graph.get_edge_toll_by_node_id(route[i], route[i + 1])
        return total_tolls * 5

    def calculate_priority_violation_penality(self, vehicles: list[Vehicle]) -> int:
        """
        Calculate the penality for priority violations in the route.
        Args:
            vehicles: List of vehicles in the solution.

        Returns:
            Penality value.
        """
        penalty = 0
        for vehicle in vehicles:
            has_non_priority_customer_before_priority_customer_in_itinerary = False
            customer_ids = vehicle.customers()
            for customer_id in customer_ids:
                node: Node = self.__graph.get_node(customer_id)
                has_non_priority_customer_before_priority_customer_in_itinerary, priority_customer_violation_penalty = self._calculate_priority_violation_penality(self.__graph.get_node(0), node, has_non_priority_customer_before_priority_customer_in_itinerary)
                penalty += priority_customer_violation_penalty
        return penalty

    def _calculate_priority_violation_penality(self, depot: Node, node: Node,
                                              has_non_priority_customer_before_priority_customer_in_itinerary: bool) -> \
            tuple[bool, int]:
        """
        Calculate the penality for priority violations in the route.
        Args:
            depot: Node: The depot node.
            node: Node: The current node being evaluated.
            has_non_priority_customer_before_priority_customer_in_itinerary: Boolean indicating if a non-priority customer has been visited before a priority customer in the itinerary.

        Returns:
            Tuple containing updated has_non_priority_customer_before_priority_customer_in_itinerary and the penalty value.

        """
        penalty = 0
        if node.priority == 1 and has_non_priority_customer_before_priority_customer_in_itinerary:
            penalty = 50

        if node.priority == 0 and depot != node:
            has_non_priority_customer_before_priority_customer_in_itinerary = True

        return has_non_priority_customer_before_priority_customer_in_itinerary, penalty

    def calculate_vehicle_unbalanced_distance_penality(self, vehicles: list[Vehicle]) -> float:
        """
        Calculate the penality for unbalanced distances among vehicles.
        Args:
            vehicles: List of vehicles in the solution.

        Returns:
            Penality value.

        """
        penalty = 0
        total_distance = self.total_distance(vehicles)
        average_distance = total_distance / len(vehicles) if vehicles else 0

        for vehicle in vehicles:
            penalty += abs(vehicle.distance() - average_distance)

        return penalty

    def calculate_capacity_violation_penality(self, vehicles: list[Vehicle]) -> float:
        """
        Calculate the penality for capacity violations among vehicles.
        Args:
            vehicles: List of vehicles in the solution.

        Returns:
            Penality value.

        """
        penalty = 0

        for vehicle in vehicles:
            current_load = 0
            for customer_id in vehicle.customers():
                demand = self.__graph.get_node(customer_id).demand
                if customer_id != 0:
                    current_load += demand
                if customer_id == 0:
                    if current_load > vehicle.capacity:
                        penalty += float('inf')
                    current_load = 0

        return penalty