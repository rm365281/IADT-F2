import random

from domain.route import Route
from domain.solution import Solution
from vrp.route_spliter import RouteSplitter
from domain.vehicle import Vehicle


def choose_two_different_indices(length: int) -> tuple[int, int]:
    """
        Selects two different indices within the range [0, length).
        The second index is guaranteed to be greater than the first.

        Args:
            length (int): The length of the list to generate indices for.

        Returns:
            tuple[int, int]: A tuple containing two different indices.
        """
    idx1 = random.randint(0, length - 1)
    idx2 = random.randint(idx1 + 1, length)
    return idx1, idx2


def build_child_route(main_parent_flat_routes: list[int], secondary_parent_flat_routes: list[int], end_index: int,
                      start_index: int) -> Route:
    """
        Builds a child route by combining a segment from the main parent and the remaining genes
        from the secondary parent, preserving the order and avoiding duplicates.

        Args:
            main_parent_flat_routes (list[int]): Flattened routes of the main parent.
            secondary_parent_flat_routes (list[int]): Flattened routes of the secondary parent.
            end_index (int): The end index of the segment to copy from the main parent.
            start_index (int): The start index of the segment to copy from the main parent.

        Returns:
            Route: The resulting child route.
        """
    child: list[int] = main_parent_flat_routes[start_index:end_index]
    remaining_positions = [i for i in range(len(main_parent_flat_routes)) if i < start_index or i >= end_index]
    remaining_genes = [gene for gene in secondary_parent_flat_routes if gene not in child]
    for position, gene in zip(remaining_positions, remaining_genes):
        child.insert(position, gene)
    return Route(child)


class Crossover:
    """
        Implements the genetic crossover operation for vehicle routing problem (VRP) solutions.
        Combines two parent solutions to generate two child solutions while respecting constraints
        such as vehicle capacity and autonomy.
        """

    def __init__(self, depot_identifier: int, number_vehicles: int, vehicle_autonomy: float, vehicle_capacity: int,
                 crossover_probability: float = 1.0) -> None:
        """
                Initializes the Crossover class with the necessary parameters.

                Args:
                    depot_identifier (int): Identifier for the depot.
                    number_vehicles (int): Number of vehicles available.
                    vehicle_autonomy (float): Maximum autonomy of the vehicles.
                    vehicle_capacity (int): Maximum capacity of the vehicles.
                    crossover_probability (float, optional): Probability of performing crossover. Defaults to 1.0.

                Raises:
                    ValueError: If the number of vehicles is less than or equal to zero.
                """
        if number_vehicles <= 0:
            raise ValueError("Number of vehicles must be greater than zero.")
        self.__number_vehicles = number_vehicles
        self.__depot_identifier = depot_identifier
        self.__vehicle_autonomy = vehicle_autonomy
        self.__vehicle_capacity = vehicle_capacity
        self.__route_splitter = RouteSplitter(depot_identifier, number_vehicles)
        self.__crossover_probability = crossover_probability

    def apply(self, p1: Solution, p2: Solution) -> tuple[Solution, Solution]:
        """
                Applies the crossover operation to two parent solutions to generate two child solutions.

                Args:
                    p1 (Solution): The first parent solution.
                    p2 (Solution): The second parent solution.

                Returns:
                    tuple[Solution, Solution]: A tuple containing the two child solutions.

                Raises:
                    ValueError: If the parents do not have the same number of customers.
                """
        if random.random() > self.__crossover_probability:
            return p1, p2
        p1_flat_routes: list[int] = [x for x in p1.flatten_routes() if x != self.__depot_identifier]
        p2_flat_routes: list[int] = [x for x in p2.flatten_routes() if x != self.__depot_identifier]
        length = len(p1_flat_routes)
        if length != len(p2_flat_routes):
            raise ValueError("Parents must have the same number of customers for crossover.")

        max_attempts = 10
        for attempt in range(max_attempts):
            start_index, end_index = choose_two_different_indices(length)
            child1 = build_child_route(p1_flat_routes, p2_flat_routes, end_index, start_index)
            child2 = build_child_route(p2_flat_routes, p1_flat_routes, end_index, start_index)

            # Check if children are different from parents
            if child1.customers != p1_flat_routes or child2.customers != p2_flat_routes:
                break
        else:
            # If all attempts fail, force a swap of at least one gene
            if length > 1:
                child1_genes = p1_flat_routes.copy()
                child1_genes[0], child1_genes[1] = child1_genes[1], child1_genes[0]
                child1 = Route(child1_genes)
                child2_genes = p2_flat_routes.copy()
                child2_genes[0], child2_genes[1] = child2_genes[1], child2_genes[0]
                child2 = Route(child2_genes)
            else:
                child1 = Route(p1_flat_routes)
                child2 = Route(p2_flat_routes)

        if len(child1.customers) != length:
            raise ValueError("Children route must have parent length.")
        if len(child2.customers) != length:
            raise ValueError("Children route must have parent length.")
        if len(child1.customers) != len(child2.customers):
            raise ValueError("Children routes must have the same length.")

        vehicles_solution_1 = [Vehicle(route, autonomy=self.__vehicle_autonomy, capacity=self.__vehicle_capacity) for
                               route in self.__route_splitter.split(child1)]
        vehicles_solution_2 = [Vehicle(route, autonomy=self.__vehicle_autonomy, capacity=self.__vehicle_capacity) for
                               route in self.__route_splitter.split(child2)]

        return Solution(vehicles=vehicles_solution_1), Solution(vehicles=vehicles_solution_2)
