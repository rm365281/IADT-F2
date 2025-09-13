import random
from vrp.route_spliter import RouteSplitter
from domain import Solution
from domain import Vehicle
from domain import Route


class Mutation:
    def __init__(self, mutation_probability: float, splitter: RouteSplitter) -> None:
        self.__mutation_probability = mutation_probability
        self.__splitter = splitter

    def apply(self, solution: Solution) -> Solution:
        """
        Applies the Inverted Displacement Mutation to the solution.
        Args:
            solution: Solution to be mutated.

        Returns:
            Mutated solution.

        """
        if random.random() > self.__mutation_probability:
            return solution

        vehicles = solution.vehicles
        if not vehicles:
            return solution
        depot_identifier = vehicles[0].route.customers[0]  # Assumes depot is the first node
        autonomy = vehicles[0].autonomy
        capacity = vehicles[0].capacity
        number_vehicles = len(vehicles)

        # Obtains the linear route without the depot
        flat_route = [x for x in solution.flatten_routes() if x != depot_identifier]
        route_length = len(flat_route)
        if route_length < 2:
            return solution

        # Selects two distinct indices
        idx1 = random.randint(0, route_length - 2)
        idx2 = random.randint(idx1 + 1, route_length - 1)

        # Extracts, inverts, and repositions the segment
        segment = flat_route[idx1:idx2 + 1]
        segment.reverse()
        mutated_route = flat_route[:idx1] + segment + flat_route[idx2 + 1:]

        # Divides the mutated route into routes for each vehicle
        split_routes = self.__splitter.split(Route(mutated_route))
        mutated_vehicles = [Vehicle(route, autonomy=autonomy, capacity=capacity) for route in split_routes]

        return Solution(mutated_vehicles)
