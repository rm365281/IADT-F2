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
        print(matrix)
        return matrix

    def _euclidean_distance(self, a: Customer, b: Customer) -> float:
        return math.hypot(a.x - b.x, a.y - b.y)
    
    def generate_initial_population(self, population_size: int, number_vehicles: int) -> list[Solution]:
        population = []
        n = len(self.customers)

        for _ in range(population_size):
            shuflled = random.sample(self.customers, n)
            chunks = np.array_split(shuflled, number_vehicles)

            vehicles = [Vehicle(itinerary=list(chunk)) for chunk in chunks]
            solution = Solution(vehicles=vehicles)
            population.append(solution)
        return population
    
    def fitness(self, solution: Solution) -> float:
        total_distance = 0
        for vehicle in solution.vehicles:
            total_distance += self.calculate_distance(vehicle=vehicle)
            vehicle.distance = total_distance
        return total_distance

    def calculate_distance(self, vehicle: Vehicle) -> float:
        distance = 0
        itinerary_length = len(vehicle.itinerary)
        for customer in range(itinerary_length):
            customer_a = vehicle.itinerary[customer]
            customer_b = vehicle.itinerary[(customer + 1) % itinerary_length]
            distance += self.customer_distance_matrix[customer_a.id][customer_b.id]
        return distance
    
    def crossover(self, population: list[Solution], population_fitness: list[float]) -> Solution:
        probability = 1 / np.array(population_fitness)
        parent1, parent2 = random.choices(population, weights=probability, k=2)

        p1_flat = [c for v in parent1.vehicles for c in v.itinerary]
        p2_flat = [c for v in parent2.vehicles for c in v.itinerary]
        n = len(p1_flat)

        start, end = sorted(random.sample(range(n), 2))

        child_flat = [None] * n
        child_flat[start:end] = p1_flat[start:end]

        pointer = 0
        for c in p2_flat:
            if c not in child_flat:
                while child_flat[pointer] is not None:
                    pointer += 1
                child_flat[pointer] = c

        vehicle_sizes = [len(v.itinerary) for v in parent1.vehicles]
        vehicles = []
        idx = 0
        for size in vehicle_sizes:
            vehicles.append(Vehicle(itinerary=child_flat[idx:idx+size], capacity=100))
            idx += size

        return Solution(vehicles=vehicles)
    
    def mutate(self, solution: Solution, mutation_probability: float) -> Solution:
        new_vehicles = []

        for vehicle in solution.vehicles:
            itinerary = vehicle.itinerary[:]
            for i in range(len(itinerary) - 1):
                if random.random() < mutation_probability:
                    itinerary[i], itinerary[i + 1] = itinerary[i + 1], itinerary[i]
            new_vehicles.append(Vehicle(itinerary=itinerary, capacity=vehicle.capacity))

        if random.random() < mutation_probability:
            v1, v2 = random.sample(new_vehicles, 2)
            if v1.itinerary:
                c = random.choice(v1.itinerary)
                v1_itinerary = [x for x in v1.itinerary if x != c]
                v2_itinerary = v2.itinerary + [c]
                new_vehicles[new_vehicles.index(v1)] = Vehicle(itinerary=v1_itinerary, capacity=v1.capacity)
                new_vehicles[new_vehicles.index(v2)] = Vehicle(itinerary=v2_itinerary, capacity=v2.capacity)

        return Solution(vehicles=new_vehicles)