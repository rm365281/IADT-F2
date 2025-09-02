import math
import random

from customer import Customer
import numpy as np
from solution import Solution
from vehicle import Vehicle


class VRP:
    customers: list[Customer]
    customer_distance_matrix: list[list[float]]

    def __init__(self, customers: list[Customer]):
        self.customers = customers
        self.customer_distance_matrix = self._build_distance_matrix(customers)

    def _build_distance_matrix(self, customers: list[Customer]) -> list[list[float]]:
        n = len(customers)
        matrix = [[0.0] * n for _ in range(n)]
        for i, a in enumerate(customers):
            for j, b in enumerate(customers):
                if i != j:
                    matrix[i][j] = self._euclidean_distance(a, b)
        return matrix

    def _euclidean_distance(self, a: Customer, b: Customer) -> float:
        return math.hypot(a.x - b.x, a.y - b.y)

    def generate_initial_population(self, population_size: int, number_vehicles: int) -> list[Solution]:
        population = []
        depot = self.customers[0]
        customers = self.customers[1:]
        n = len(customers)

        for _ in range(population_size):
            shuflled = random.sample(customers, n)
            chunks = np.array_split(shuflled, number_vehicles)

            vehicles = [Vehicle(depot, itinerary=list(chunk))
                        for chunk in chunks]
            solution = Solution(vehicles=vehicles)
            population.append(solution)
        return population

    def fitness(self, solution: Solution) -> float:
        solution.calculate_distances(self.customer_distance_matrix)
        return solution.calculate_total_cost()

    def crossover(self, population: list[Solution], population_fitness: list[float]) -> Solution:
        probability = 1 / np.array(population_fitness)
        parent1, parent2 = random.choices(population, weights=probability, k=2)

        child_routes = [list(vehicle.itinerary) for vehicle in parent1.vehicles]

        num_routes = len(child_routes)
        cut_size = random.randint(1, num_routes)
        routes_from_parent2 = random.sample(parent2.vehicles, cut_size)

        customers_in_child = {customer for route in child_routes for customer in route}

        for route in routes_from_parent2:
            child_routes = [[customer for customer in r if customer not in route.itinerary] for r in child_routes]
            idx = random.randrange(num_routes)
            child_routes[idx] = list(route.itinerary)
            customers_in_child = {c for route in child_routes for c in route}

        all_customers = set(self.customers[1:])
        missing = list(all_customers - customers_in_child)

        for customer in missing:
            smallest_route = min(child_routes, key=len)
            smallest_route.append(customer)

        child_vehicles = [
            Vehicle(depot=self.customers[0], itinerary=route, capacity=100)
            for route in child_routes
        ]

        return Solution(vehicles=child_vehicles)

    def mutate(self, solution: Solution, mutation_probability: float) -> Solution:
        """
        Aplica mutações em uma solução do VRP.
        - Intra-rota: troca clientes adjacentes dentro de um veículo.
        - Inter-rota: move um cliente de um veículo para outro.
        """
        vehicles = [self._mutate_intraroute(v, mutation_probability) for v in solution.vehicles]

        if random.random() < mutation_probability:
            vehicles = self._mutate_interroute(vehicles)

        return Solution(vehicles=vehicles)


    def _mutate_intraroute(self, vehicle: Vehicle, mutation_probability: float) -> Vehicle:
        """
        Troca posições de clientes adjacentes dentro de uma rota.
        """
        itinerary = vehicle.itinerary[:]
        for i in range(len(itinerary) - 1):
            if random.random() < mutation_probability:
                itinerary[i], itinerary[i + 1] = itinerary[i + 1], itinerary[i]
        return Vehicle(depot=vehicle.depot, itinerary=itinerary, capacity=vehicle.capacity)


    def _mutate_interroute(self, vehicles: list[Vehicle]) -> list[Vehicle]:
        """
        Move um cliente de uma rota para outra.
        """
        v1, v2 = random.sample(vehicles, 2)
        if not v1.itinerary:
            return vehicles

        customer = random.choice(v1.itinerary)

        v1_new = Vehicle(
            depot=v1.depot,
            itinerary=[c for c in v1.itinerary if c != customer],
            capacity=v1.capacity
        )

        v2_new = Vehicle(
            depot=v2.depot,
            itinerary=v2.itinerary + [customer],
            capacity=v2.capacity
        )

        updated = []
        for v in vehicles:
            if v == v1:
                updated.append(v1_new)
            elif v == v2:
                updated.append(v2_new)
            else:
                updated.append(v)

        return updated
