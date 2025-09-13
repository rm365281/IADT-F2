import random

from route import Route
from solution import Solution
from vehicle import Vehicle
from vrp.route_spliter import RouteSplitter


def choose_two_different_indices(length: int) -> tuple[int, int]:
    idx1 = random.randint(0, length - 1)
    idx2 = random.randint(idx1 + 1, length)
    return idx1, idx2


def build_child_route(main_parent_flat_routes: list[int], secondary_parent_flat_routes: list[int], end_index: int, start_index: int) -> Route:
    child: list[int] = main_parent_flat_routes[start_index:end_index]
    remaining_positions = [i for i in range(len(main_parent_flat_routes)) if i < start_index or i >= end_index]
    remaining_genes = [gene for gene in secondary_parent_flat_routes if gene not in child]
    for position, gene in zip(remaining_positions, remaining_genes):
        child.insert(position, gene)
    return Route(child)

class Crossover:
    def __init__(self, depot_identifier: int, number_vehicles: int, vehicle_autonomy: float, vehicle_capacity: int) -> None:
        if number_vehicles <= 0:
            raise ValueError("Number of vehicles must be greater than zero.")
        self.__number_vehicles = number_vehicles
        self.__depot_identifier = depot_identifier
        self.__vehicle_autonomy = vehicle_autonomy
        self.__vehicle_capacity = vehicle_capacity
        self.__route_splitter = RouteSplitter(depot_identifier, number_vehicles)

    def apply(self, p1: Solution, p2: Solution) -> tuple[Solution, Solution]:
        # Remover o identificador do depósito corretamente
        p1_flat_routes: list[int] = [x for x in p1.flatten_routes() if x != self.__depot_identifier]
        p1_flatten_routes_length = len(p1_flat_routes)
        p2_flat_routes = [x for x in p2.flatten_routes() if x != self.__depot_identifier]
        p2_flatten_routes_length = len(p2_flat_routes)

        if p1_flatten_routes_length != p2_flatten_routes_length:
            raise ValueError("Parents must have the same number of customers for crossover.")

        start_index, end_index = choose_two_different_indices(p1_flatten_routes_length)

        # Child 1: segmento de p1, completa com genes de p2
        child1 = build_child_route(p1_flat_routes, p2_flat_routes, end_index, start_index)

        # Child 2: segmento de p2, completa com genes de p1
        child2 = build_child_route(p2_flat_routes, p1_flat_routes, end_index, start_index)

        if len(child1.customers) != p1_flatten_routes_length:
            raise ValueError("Children route must have parent length.")
        if len(child2.customers) != p2_flatten_routes_length:
            raise ValueError("Children route must have parent length.")
        if len(child1.customers) != len(child2.customers):
            raise ValueError("Children routes must have the same length.")

        vehicles_solution_1 = [Vehicle(route, autonomy=self.__vehicle_autonomy, capacity=self.__vehicle_capacity) for route in self.__route_splitter.split(child1)]
        vehicles_solution_2 = [Vehicle(route, autonomy=self.__vehicle_autonomy, capacity=self.__vehicle_capacity) for route in self.__route_splitter.split(child2)]

        return Solution(vehicles=vehicles_solution_1), Solution(vehicles=vehicles_solution_2)

