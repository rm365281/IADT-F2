import math
import random

from customer import Customer
import numpy as np
from solution import Solution
from vehicle import Vehicle
from itinerary import Itinerary
from sklearn.neighbors import NearestNeighbors

class VRP:
    customers: list[Customer]
    customer_distance_matrix: list[list[float]]

    def __init__(self, customers: list[Customer]) -> None:
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

        coords = np.array([[c.x, c.y] for c in self.customers])
        nn = NearestNeighbors(n_neighbors=n, algorithm="ball_tree").fit(coords)

        for _ in range(population_size):
            unvisited = set(customers)
            vehicles: list[Vehicle] = []

            for _ in range(number_vehicles):
                if not unvisited:
                    break

                start = random.choice(list(unvisited))
                unvisited.remove(start)
                route = [start]

                current = start
                while unvisited and len(route) < n // number_vehicles + 1:
                    distances, indices = nn.kneighbors([[current.x, current.y]])
                    next_customer = None
                    for idx in indices[0]:
                        candidate = self.customers[idx]
                        if candidate in unvisited:
                            next_customer = candidate
                            break
                    if next_customer is None:
                        break
                    unvisited.remove(next_customer)
                    route.append(next_customer)
                    current = next_customer

                vehicles.append(Vehicle(depot=depot, itineraries=[Itinerary(customers=route)]))

            if unvisited:
                for customer in unvisited:
                    random.choice(vehicles).itineraries[0].customers.append(customer)

            solution = Solution(vehicles=vehicles)
            population.append(solution)

        return population

    def fitness(self, solution: Solution) -> float:
        solution.calculate_distances(self.customer_distance_matrix)
        return solution.calculate_total_cost()

    def crossover(self, population: list[Solution], population_fitness: list[float]) -> Solution:
        """
        Performs genetic algorithm crossover to create a child solution from two parents.
        Uses fitness-based selection and route combination strategy.
        """
        # Select parents using inverse fitness weighting (lower fitness = higher probability)
        probability = 1 / np.array(population_fitness)
        parent1, parent2 = random.choices(population, weights=probability, k=2)

        # Extract all routes from parent1
        child_routes = [list(itinerary.customers) for vehicle in parent1.vehicles for itinerary in vehicle.itineraries]

        if not child_routes:
            return Solution(vehicles=[])
    
        # Select random routes from parent2 to integrate
        num_routes = len(child_routes)
        cut_size = random.randint(1, min(num_routes, len(parent2.vehicles)))
        routes_from_parent2 = random.sample(parent2.vehicles, cut_size)

        # Integrate routes from parent2
        for vehicle in routes_from_parent2:
            vehicle_customers = [customer for itinerary in vehicle.itineraries for customer in itinerary.customers]
        
            # Remove customers that will be replaced
            child_routes = [
                [customer for customer in route if customer not in vehicle_customers]
                for route in child_routes
            ]
        
            # Insert new route
            if child_routes:
                idx = random.randrange(len(child_routes))
                child_routes[idx] = vehicle_customers
            else:
                child_routes.append(vehicle_customers)

        # Add missing customers to smallest routes
        customers_in_child = {customer for route in child_routes for customer in route}
        all_customers = set(self.customers[1:])
        missing_customers = all_customers - customers_in_child

        for customer in missing_customers:
            if child_routes:
                min(child_routes, key=len).append(customer)
            else:
                child_routes.append([customer])

        # Create child solution with non-empty routes only
        child_vehicles = [
            Vehicle(depot=self.customers[0], itineraries=[Itinerary(customers=route)], capacity=100)
            for route in child_routes if route
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
        mutated_itineraries = []
        for itinerary in vehicle.itineraries:
            customers = itinerary.customers[:]
            for i in range(len(customers) - 1):
                if random.random() < mutation_probability:
                    customers[i], customers[i + 1] = customers[i + 1], customers[i]
            mutated_itineraries.append(Itinerary(customers=customers))
        return Vehicle(depot=vehicle.depot, itineraries=mutated_itineraries, capacity=vehicle.capacity)


    def _mutate_interroute(self, vehicles: list[Vehicle]) -> list[Vehicle]:
        """
        Move um cliente de uma rota para outra.
        """
        v1, v2 = random.sample(vehicles, 2)
        
        # Collect all customers from all itineraries of v1
        all_customers_v1 = []
        for itinerary in v1.itineraries:
            all_customers_v1.extend(itinerary.customers)
        
        if not all_customers_v1:
            return vehicles

        customer = random.choice(all_customers_v1)

        # Remove customer from v1's itineraries
        v1_new_itineraries = []
        for itinerary in v1.itineraries:
            new_customers = [c for c in itinerary.customers if c != customer]
            v1_new_itineraries.append(Itinerary(customers=new_customers))

        v1_new = Vehicle(
            depot=v1.depot,
            itineraries=v1_new_itineraries,
            capacity=v1.capacity
        )

        # Add customer to a random itinerary of v2 (or create new one if none exist)
        v2_new_itineraries = []
        for itinerary in v2.itineraries:
            v2_new_itineraries.append(Itinerary(customers=itinerary.customers[:]))
        
        if v2_new_itineraries:
            # Add to a random existing itinerary
            random_itinerary = random.choice(v2_new_itineraries)
            random_itinerary.customers.append(customer)
        else:
            # Create new itinerary with the customer
            v2_new_itineraries.append(Itinerary(customers=[customer]))

        v2_new = Vehicle(
            depot=v2.depot,
            itineraries=v2_new_itineraries,
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
