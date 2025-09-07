import random
from typing import Any

from graph.node import Node
import numpy as np
from graph.graph import Graph
from solution import Solution
from vehicle import Vehicle

class VRP:
    def __init__(self, graph: Graph, population_size: int, number_vehicles: int, mutation_probability: float = 0.5, vehicle_autonomy: float = 500.0) -> None:
        self.number_vehicles = number_vehicles
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.graph = graph
        self.depot = graph.get_node(0)
        self.vehicle_autonomy = vehicle_autonomy

    def generate_initial_population(self) -> list[Solution]:
        customers: list[Node] = self.graph.get_nodes()[1:]
        solutions: list[Solution] = list()
        for _ in range(self.population_size):
            shuffled_customers: list[Node] = random.sample(customers, len(customers))
            customer_ids: list[int] = [customer.identifier for customer in shuffled_customers]
            vehicles = self.build_vehicles(customer_ids)
            solution = Solution(vehicles=vehicles)
            solutions.append(solution)
        return solutions

    def build_vehicles(self, customer_ids: list[int]) -> list[Any]:
        vehicles = []
        chunks = np.array_split(customer_ids, self.number_vehicles)
        for chunk in chunks:
            customer_ids = chunk.tolist()
            itineraries = self.build_itineraries(customer_ids)

            vehicles.append(Vehicle(depot_id=self.depot.identifier, itineraries=itineraries, autonomy=self.vehicle_autonomy))
        return vehicles

    def build_itineraries(self, customer_ids) -> list[list[int]]:
        node_ids: list[int] = []
        from_node = self.depot  # inicia o from_node com o depot
        distance = 0.0
        itineraries: list[list[int]] = []
        for i in range(len(customer_ids)):
            to_node = self.graph.get_node(customer_ids[i])

            if to_node == self.depot:
                raise ValueError("Crossover resulted in a route containing the depot as a customer.")

            step_distance = self.graph.get_edge(from_node, to_node).distance

            from_node = self.graph.get_node(customer_ids[
                                                i])  # atualiza o from_node com o valor do to_node pois será a origem na proxima iteração dentro do loop

            depot_step_distance = 0.0
            if from_node != self.depot:
                depot_step_distance = self.graph.get_edge(from_node, self.depot).distance

            if distance + step_distance + depot_step_distance > self.vehicle_autonomy:  # se a distancia acumulada for maior que a autonomia do veiculo
                itineraries.append(node_ids)  # adiciona o itinerario atual na lista de itinerarios
                from_node = self.depot  # reseta o from_node para o depot
                distance = 0.0  # reseta a distancia acumulada
                node_ids = []  # reseta a lista de node_ids para iniciar um novo itinerario
            distance += step_distance
            node_ids.append(customer_ids[i])
        itineraries.append(node_ids)
        return itineraries

    def fitness(self, solution: Solution) -> None:
        penalty: float = 0
        total_distance = 0.0

        for vehicle in solution.vehicles:
            vehicle.distance = 0.0
            has_non_priority_customer_earlier_in_itinerary = False
            for full_itinerary in vehicle.full_itineraries:
                itinerary_distance = 0.0
                for i in range(len(full_itinerary) - 1):
                    from_node: Node = self.graph.get_node(full_itinerary[i])
                    to_node: Node = self.graph.get_node(full_itinerary[i + 1])

                    if from_node.priority == 1 and has_non_priority_customer_earlier_in_itinerary:
                        penalty += 50
                    if from_node.priority == 0 and self.depot != from_node:
                        has_non_priority_customer_earlier_in_itinerary = True

                    if from_node == to_node:
                        penalty += 1000000
                        continue
                    itinerary_distance += self.graph.get_edge(from_node, to_node).distance
                if itinerary_distance > self.vehicle_autonomy:
                    penalty += 1000000
                vehicle.distance += itinerary_distance
            total_distance += vehicle.distance

        distance_median = total_distance / len(solution.vehicles)
        for vehicle in solution.vehicles:
            penalty += abs(vehicle.distance - distance_median)

        solution.fitness = total_distance + penalty

    def sort_population(self, population: list[Solution]) -> list[Solution]:
        return sorted(population, key=lambda solution: solution.fitness)

    def crossover(self, population: list[Solution]) -> Solution:
        population_fitness = [ind.fitness for ind in population]
        weights = 1 / (np.asarray(population_fitness, dtype=float) + 1e-9)
        p1, p2 = random.choices(population, weights=weights, k=2)

        p1_flat_routes: list[int] = p1.flatten_routes()
        flatten_routes_length = len(p1_flat_routes)

        # Choose two random indices for the crossover
        start_index = random.randint(0, flatten_routes_length - 1)
        end_index = random.randint(start_index + 1, flatten_routes_length)

        # Initialize the child with a copy of the substring from parent1
        child: list[int] = p1_flat_routes[start_index:end_index]

        # Fill in the remaining positions with genes from parent2
        remaining_positions = [i for i in range(flatten_routes_length) if i < start_index or i >= end_index]
        remaining_genes = [gene for gene in p2.flatten_routes() if gene not in child]

        for position, gene in zip(remaining_positions, remaining_genes):
            child.insert(position, gene)

        vehicles = self.build_vehicles(child)

        return Solution(vehicles=vehicles)
    
    def mutate(self, solution: Solution) -> Solution:
        if self.mutation_probability <= 0:
            return solution

        for vehicle in solution.vehicles:
            itinerary = vehicle.flatten_itineraries()[:]
            for i in range(len(itinerary) - 1):
                if random.random() < self.mutation_probability:
                    itinerary[i], itinerary[i + 1] = itinerary[i + 1], itinerary[i]
            vehicle.itineraries = [itinerary]

        if random.random() < self.mutation_probability:
            v1, v2 = random.sample(solution.vehicles, 2)
            if v1.flatten_itineraries():
                c = random.choice(v1.flatten_itineraries())
                v1_itinerary = [x for x in v1.flatten_itineraries() if x != c]
                v2_itinerary = v2.flatten_itineraries() + [c]
                v1.itineraries = self.build_itineraries(v1_itinerary)
                v2.itineraries = self.build_itineraries(v2_itinerary)

        return solution
