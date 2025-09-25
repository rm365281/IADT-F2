import random

import numpy as np

from domain.graph import Graph, Node
from domain.route import Route
from domain.solution import Solution
from domain.vehicle import Vehicle
from vrp.adjustment.adjustment import Adjustment


class InitialPopulationGenerator:
    def __init__(self, graph: Graph, population_size: int, adjustment: Adjustment, vehicle_capacity: int,
                 vehicle_autonomy: float, number_vehicles: int, depot_identifier: int = 0) -> None:
        self.__adjustment = adjustment
        self.__vehicle_capacity = vehicle_capacity
        self.__vehicle_autonomy = vehicle_autonomy
        self.__number_vehicles = number_vehicles
        self.__graph = graph
        self.__population_size = population_size
        self.__depot_identifier = depot_identifier

    def generate(self):
        """
        Generate the initial population of solutions using a random shuffle of customers.
        Returns:
            Initial population of solutions.
        """
        customers: list[Node] = self.__graph.get_nodes()[1:]
        solutions: list[Solution] = list()
        for _ in range(self.__population_size):
            shuffled_customers: list[Node] = random.sample(customers, len(customers))
            customer_ids: list[int] = [customer.identifier for customer in shuffled_customers]
            vehicles = self.__build_vehicles(customer_ids)
            solution = Solution(vehicles=vehicles)
            solution = self.__adjustment.apply(solution)
            solutions.append(solution)
        return solutions

    def __build_vehicles(self, customer_ids: list[int]) -> list[Vehicle]:
        """
        Split route into vehicles and create vehicles with the given capacity and autonomy.
        Args:
            customer_ids: List of customer IDs to be served by the vehicles.

        Returns:
            List of vehicles with assigned routes.

        """
        vehicles = []
        chunks = np.array_split(customer_ids, self.__number_vehicles)
        for chunk in chunks:
            route = Route([self.__depot_identifier] + chunk.tolist() + [self.__depot_identifier])
            vehicles.append(Vehicle(route=route, autonomy=self.__vehicle_autonomy, capacity=self.__vehicle_capacity))
        return vehicles
