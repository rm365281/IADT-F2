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

        customer_ids = [c.id for c in customers]
        id2c = {c.id: c for c in self.customers}

        for _ in range(population_size):
            unvisited = set(customer_ids)
            vehicles: list[Vehicle] = []

            for _ in range(number_vehicles):
                if not unvisited:
                    break

                start_id  = random.choice(tuple(unvisited))
                unvisited.remove(start_id)
                route = [start_id]

                current = id2c[start_id]
                while unvisited and len(route) < n // number_vehicles + 1:
                    distances, indices = nn.kneighbors([[current.x, current.y]])
                    next_customer_id = None
                    for idx in indices[0]:
                        candidate_id = self.customers[idx].id
                        if candidate_id in unvisited:
                            next_customer_id = candidate_id
                            break
                    if next_customer_id is None:
                        break
                    unvisited.remove(next_customer_id)
                    route.append(next_customer_id)
                    current = id2c[next_customer_id]

                vehicles.append(Vehicle(depot=depot, itineraries=[Itinerary(customers=[id2c[cid] for cid in route])]))

            if unvisited:
                for cid in unvisited:
                    random.choice(vehicles).itineraries[0].customers.append(id2c[cid])

            solution = Solution(vehicles=vehicles)
            population.append(solution)

        return population

    def fitness(self, solution: Solution) -> float:
        solution.calculate_distances(self.customer_distance_matrix)
        return solution.calculate_total_cost()

    def crossover(self, population: list[Solution], population_fitness: list[float]) -> Solution:
        """
        Seleciona 2 pais por roleta invertida, aplica CEX em arrays de IDs e reconstrói o filho.
        Cada filho é reconstruído com a estrutura do respectivo pai (mantém nº de veículos/itinerários).
        Aqui retornamos apenas um child (padrão do seu loop).
        """
        # seleção por probabilidade inversa (menor fitness = maior peso)
        weights = 1 / (np.asarray(population_fitness, dtype=float) + 1e-9)
        p1, p2 = random.choices(population, weights=weights, k=2)

        depot = self.customers[0]

        # flatten
        p1_ids = self._flatten_ids(p1)
        p2_ids = self._flatten_ids(p2)

        # CEX
        c1_ids, c2_ids = self._cycle_crossover_numpy(p1_ids, p2_ids)

        # reconstrói o filho 1 com a estrutura do p1
        struct_p1 = self._structure_of(p1)
        child1 = self._rebuild_from(c1_ids, struct_p1, depot)

        # reconstrói o filho 2 com a estrutura do p2
        struct_p2 = self._structure_of(p2)
        child2 = self._rebuild_from(c2_ids, struct_p2, depot)

        # escolhe o melhor fitness
        f1 = self.fitness(child1)
        f2 = self.fitness(child2)
        return child1 if f1 <= f2 else child2
    
    def _cycle_crossover_numpy(self, p1: np.ndarray, p2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        CEX em O(n) usando mapa de posições. Supõe que p1/p2 são permutações do mesmo conjunto de IDs.
        """
        n = len(p1)
        c1 = np.empty(n, dtype=int); c1.fill(-1)
        c2 = np.empty(n, dtype=int); c2.fill(-1)

        # pos1[val] = posição de 'val' em p1
        pos1 = np.empty(p1.max() + 1, dtype=int)
        pos1[p1] = np.arange(n, dtype=int)

        visited = np.zeros(n, dtype=bool)
        take_from_p1 = True

        for start in range(n):
            if visited[start]:
                continue
            # percorre o ciclo começando em 'start'
            idx = start
            cycle_idxs = []
            while not visited[idx]:
                visited[idx] = True
                cycle_idxs.append(idx)
                # próximo índice: onde em p1 está o valor p2[idx]
                idx = pos1[p2[idx]]

            cycle_idxs = np.asarray(cycle_idxs, dtype=int)
            if take_from_p1:
                c1[cycle_idxs] = p1[cycle_idxs]
                c2[cycle_idxs] = p2[cycle_idxs]
            else:
                c1[cycle_idxs] = p2[cycle_idxs]
                c2[cycle_idxs] = p1[cycle_idxs]
            take_from_p1 = not take_from_p1

        return c1, c2

    def mutate(self, solution: Solution, mutation_probability: float) -> Solution:
        """
        Mutação em array de IDs + reconstrução com a MESMA estrutura da solução original.
        """
        if mutation_probability <= 0:
            return solution

        depot = self.customers[0]
        struct = self._structure_of(solution)
        ids = self._flatten_ids(solution)

        ids = self._swap_mutation_numpy(ids, mutation_probability)

        return self._rebuild_from(ids, struct, depot)


    def _swap_mutation_numpy(self, arr: np.ndarray, mutation_rate: float) -> np.ndarray:
        """
        Troca valores em posições sorteadas. Mantém a permutação.
        """
        if mutation_rate <= 0:
            return arr
        n = len(arr)
        mask = np.random.rand(n) < mutation_rate
        idx = np.nonzero(mask)[0]
        if idx.size >= 2:
            shuffled = idx.copy()
            np.random.shuffle(shuffled)
            arr[idx] = arr[shuffled]
        return arr
    
    def _id_to_customer(self) -> dict[int, Customer]:
        return {c.id: c for c in self.customers}

    def _structure_of(self, solution: Solution) -> list[list[int]]:
        """
        Estrutura = lista de veículos; para cada veículo, lista com o tamanho de cada itinerary.
        Ex: [[5], [3, 2]] significa: veic0 com 1 itinerary de 5 clientes; veic1 com 2 itinerários (3 e 2 clientes).
        """
        return [[len(it.customers) for it in v.itineraries] for v in solution.vehicles]

    def _flatten_ids(self, solution: Solution) -> np.ndarray:
        """
        Converte Solution -> array (np.ndarray) de IDs de clientes (sem depósitos).
        A ordem segue veículos/itinerários/clients.
        """
        ids = []
        for v in solution.vehicles:
            for it in v.itineraries:
                ids.extend([c.id for c in it.customers])
        return np.asarray(ids, dtype=int)

    def _rebuild_from(self, ids: np.ndarray, structure: list[list[int]], depot: Customer) -> Solution:
        """
        Reconstrói Solution a partir do array de IDs e da estrutura (quantos itinerários e seus tamanhos por veículo).
        Reusa instâncias originais de Customer (id->Customer).
        """
        id2c = self._id_to_customer()
        cursor = 0
        vehicles: list[Vehicle] = []
        for veh_it_sizes in structure:
            itineraries: list[Itinerary] = []
            for size in veh_it_sizes:
                customers = [id2c[int(i)] for i in ids[cursor: cursor + size]]
                cursor += size
                itineraries.append(Itinerary(customers=customers))
            vehicles.append(Vehicle(depot=depot, itineraries=itineraries))
        return Solution(vehicles=vehicles)
