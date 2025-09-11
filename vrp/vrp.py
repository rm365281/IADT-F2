import random
from typing import Any

from graph.node import Node
import numpy as np
from graph.graph import Graph
from itinerary import Itinerary
from solution import Solution
from vehicle import Vehicle
from vrp.adjustment.adjustment import Adjustment
from vrp.crossover import parents_choice, choose_two_different_indices
from vrp.fitness import calculate_vehicle_unbalanced_distance_penality, calculate_priority_violation_penality
from vrp.mutation import mutate_vehicle_itinerary, mutate_itinerary_between_vehicles


class VRP:
    def __init__(self, graph: Graph, population_size: int, number_vehicles: int, mutation_probability: float = 0.5, vehicle_autonomy: float = 500.0, vehicle_capacity: int = 100) -> None:
        self.number_vehicles = number_vehicles
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.graph = graph
        self.depot = graph.get_node(0)
        self.vehicle_autonomy = vehicle_autonomy
        self.vehicle_capacity = vehicle_capacity
        self.__adjustment = Adjustment(graph, self.depot.identifier)

    def generate_initial_population(self) -> list[Solution]:
        customers: list[Node] = self.graph.get_nodes()[1:]
        solutions: list[Solution] = list()
        for _ in range(self.population_size):
            shuffled_customers: list[Node] = random.sample(customers, len(customers))
            customer_ids: list[int] = [customer.identifier for customer in shuffled_customers]
            vehicles = self.build_vehicles(customer_ids)
            solution = Solution(vehicles=vehicles)
            solution = self.__adjustment.apply(solution)
            solutions.append(solution)
        return solutions

    def build_vehicles(self, customer_ids: list[int]) -> list[Any]:
        vehicles = []
        chunks = np.array_split(customer_ids, self.number_vehicles)
        for chunk in chunks:
            itinerary = Itinerary([self.depot.identifier] + chunk.tolist() + [self.depot.identifier])
            vehicles.append(Vehicle(itinerary=itinerary, autonomy=self.vehicle_autonomy, capacity=self.vehicle_capacity))
        return vehicles

    def fitness(self, solution: Solution) -> None:
        penalty: float = 0
        total_distance = 0.0

        for vehicle in solution.vehicles:
            full_itinerary_customers = vehicle.customers()

            itinerary_distance = 0.0
            for i in range(len(full_itinerary_customers) - 1):
                from_node: Node = self.graph.get_node(full_itinerary_customers[i])
                to_node: Node = self.graph.get_node(full_itinerary_customers[i + 1])
                itinerary_distance += self.graph.get_edge(from_node, to_node).distance
            vehicle.update_distance(itinerary_distance)
            total_distance += itinerary_distance

            for i in range(len(full_itinerary_customers) - 1):
                from_node: Node = self.graph.get_node(full_itinerary_customers[i])
                to_node: Node = self.graph.get_node(full_itinerary_customers[i + 1])
                distance = self.graph.get_edge(from_node, to_node).distance
                locais_pedagios = []
                km = 150
                while km < distance:
                    locais_pedagios.append(km)
                    km += 150

                penalty += 5 * len(locais_pedagios)

            has_non_priority_customer_violation = False
            for i in full_itinerary_customers:
                from_node: Node = self.graph.get_node(i)
                has_non_priority_customer_violation, priority_customer_violation_penalty = calculate_priority_violation_penality(self.depot, from_node, has_non_priority_customer_violation)
                penalty += priority_customer_violation_penalty

            current_load = 0
            for customer_id in full_itinerary_customers:
                demand = self.graph.get_node(customer_id).demand
                if customer_id != self.depot.identifier:
                    current_load += demand
                if customer_id == self.depot.identifier:
                    if current_load > vehicle.capacity:
                        penalty += int('inf') #1000 * (current_load - vehicle.capacity)
                    current_load = 0

        penalty += calculate_vehicle_unbalanced_distance_penality(solution.vehicles)

        solution.fitness = total_distance + penalty

    def sort_population(self, population: list[Solution]) -> list[Solution]:
        return sorted(population, key=lambda solution: solution.fitness)

    def crossover(self, population: list[Solution]) -> Solution:
        p1, p2 = parents_choice(population)

        p1_flat_routes: list[int] = [x for x in p1.flatten_routes() if x != self.depot.identifier]
        flatten_routes_length = len(p1_flat_routes)

        start_index, end_index = choose_two_different_indices(flatten_routes_length)

        # Initialize the child with a copy of the substring from parent1
        child: list[int] = p1_flat_routes[start_index:end_index]

        # Fill in the remaining positions with genes from parent2
        routes = [x for x in p2.flatten_routes() if x != self.depot.identifier]
        remaining_positions = [i for i in range(flatten_routes_length) if i < start_index or i >= end_index]
        remaining_genes = [gene for gene in routes if gene not in child]

        for position, gene in zip(remaining_positions, remaining_genes):
            child.insert(position, gene)

        vehicles = self.build_vehicles(child)

        return Solution(vehicles=vehicles)

    def mutate(self, solution: Solution) -> Solution:
        if random.random() <= self.mutation_probability:
            mutation_type = random.randint(0,1)
            if mutation_type == 0:
                for vehicle in solution.vehicles:
                    mutate_vehicle_itinerary(vehicle, self.mutation_probability)
            if mutation_type == 1:
                mutate_itinerary_between_vehicles(solution)
        return solution

    def adjustment(self, solution: Solution) -> Solution:
        return self.__adjustment.apply(solution)