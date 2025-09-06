import random

from graph.node import Node
import numpy as np
from graph.graph import Graph
from solution import Solution
from vehicle import Vehicle

class VRP:
    def __init__(self, graph: Graph, population_size: int, number_vehicles: int, mutation_probability: float = 0.5) -> None:
        self.number_vehicles = number_vehicles
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.graph = graph

    def generate_initial_population(self) -> list[Solution]:
        depot: Node = self.graph.get_node(0)
        customers: list[Node] = self.graph.get_nodes()[1:]
        solutions: list[Solution] = list()
        for _ in range(self.population_size):
            shuffled_customers: list[Node] = random.sample(customers, len(customers))
            customer_ids: list[int] = [customer.id for customer in shuffled_customers]
            chunks = np.array_split(customer_ids, self.number_vehicles)
            vehicles = [Vehicle(depot_id=depot.id, node_ids=[chunk.tolist()]) for chunk in chunks]
            solution = Solution(vehicles=vehicles)
            solutions.append(solution)
        return solutions

    def fitness(self, solution: Solution) -> None:
        for vehicle in solution.vehicles:
            vehicle.distance = sum(
                self.graph.get_edge(self.graph.get_node(vehicle.full_itineraries[0][i]),
                                    self.graph.get_node(vehicle.full_itineraries[0][i + 1])).distance
                for i in range(len(vehicle.full_itineraries[0]) - 1)
            )
        solution.calculate_total_cost()

    def sort_population(self, population: list[Solution]) -> list[Solution]:
        """
        Sort a population based on fitness values.

        Parameters:
        - population (List[List[Tuple[float, float]]]): The population of solutions, where each solution is represented as a list.
        - fitness (List[float]): The corresponding fitness values for each solution in the population.

        Returns:
        Tuple[List[List[Tuple[float, float]]], List[float]]: A tuple containing the sorted population and corresponding sorted fitness values.
        """
        return sorted(population, key=lambda solution: solution.fitness)

    def crossover(self, population: list[Solution]) -> Solution:
        """
        Seleciona 2 pais por roleta invertida, aplica CEX em arrays de IDs e reconstrói o filho.
        Cada filho é reconstruído com a estrutura do respectivo pai (mantém nº de veículos/itinerários).
        Aqui retornamos apenas um child (padrão do seu loop).
        """
        population_fitness = [ind.fitness for ind in population]
        weights = 1 / (np.asarray(population_fitness, dtype=float) + 1e-9)
        p1, p2 = random.choices(population, weights=weights, k=2)

        depot: Node = self.graph.get_node(0)

        number_vehicles = len(p1.vehicles)
        p1_flat_routes = p1.flatten_routes()
        flatten_routes_length = len(p1_flat_routes)

        # Choose two random indices for the crossover
        start_index = random.randint(0, flatten_routes_length - 1)
        end_index = random.randint(start_index + 1, flatten_routes_length)

        # Initialize the child with a copy of the substring from parent1
        child = p1_flat_routes[start_index:end_index]

        # Fill in the remaining positions with genes from parent2
        remaining_positions = [i for i in range(flatten_routes_length) if i < start_index or i >= end_index]
        remaining_genes = [gene for gene in p2.flatten_routes() if gene not in child]

        for position, gene in zip(remaining_positions, remaining_genes):
            child.insert(position, gene)

        chunks = np.array_split(child, number_vehicles)

        vehicles = []
        for chunk in chunks:
            vehicles.append(Vehicle(depot_id=depot.id, node_ids=[chunk.tolist()]))

        return Solution(vehicles=vehicles)
    
    def mutate(self, solution: Solution) -> Solution:
        if self.mutation_probability <= 0:
            return solution

        for vehicle in solution.vehicles:
            itinerary = vehicle.itineraries[0][:]
            for i in range(len(itinerary) - 1):
                if random.random() < self.mutation_probability:
                    itinerary[i], itinerary[i + 1] = itinerary[i + 1], itinerary[i]
            vehicle.itineraries = [itinerary]

        if random.random() < self.mutation_probability:
            v1, v2 = random.sample(solution.vehicles, 2)
            if v1.itineraries[0]:
                c = random.choice(v1.itineraries[0])
                v1_itinerary = [x for x in v1.itineraries[0] if x != c]
                v2_itinerary = v2.itineraries[0] + [c]
                v1.itineraries = [v1_itinerary]
                v2.itineraries = [v2_itinerary]

        return solution
