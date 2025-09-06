import random

from graph.node import Node
import numpy as np
from graph.graph import Graph
from solution import Solution
from vehicle import Vehicle

class VRP:

    def generate_initial_population(self, nodes: list[Node], population_size: int, number_vehicles: int) -> list[Solution]:
        depot: Node = nodes[0]
        customers: list[Node] = nodes[1:]
        solutions: list[Solution] = list()
        for _ in range(population_size):
            customers: list[Node] = random.sample(customers, len(customers))
            node_ids: list[int] = []
            for node in customers:
                node_ids.append(node.id)
            vehicle = Vehicle(depot_id=depot.id, node_ids=[node_ids])
            solution = Solution(vehicles=[vehicle])
            solutions.append(solution)
        return solutions
    
    def fitness(self, solution: Solution, graph: Graph) -> None:
        for vehicle in solution.vehicles:
            full_itinerary = vehicle.full_itineraries[0]
            for i in range(len(full_itinerary)):
                from_node: Node = graph.get_node(full_itinerary[i])
                if i + 1 < len(full_itinerary):
                    to_node: Node = graph.get_node(full_itinerary[i + 1])
                    vehicle.distance += graph.get_edge(from_node, to_node).distance
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

        sorted_solutions: list[Solution] = sorted(population, key=lambda solution: solution.fitness)

        return sorted_solutions

    def crossover(self, population: list[Solution], graph: Graph) -> Solution:
        """
        Seleciona 2 pais por roleta invertida, aplica CEX em arrays de IDs e reconstrói o filho.
        Cada filho é reconstruído com a estrutura do respectivo pai (mantém nº de veículos/itinerários).
        Aqui retornamos apenas um child (padrão do seu loop).
        """
        # seleção por probabilidade inversa (menor fitness = maior peso)
        population_fitness = [ind.fitness for ind in population]
        weights = 1 / (np.asarray(population_fitness, dtype=float) + 1e-9)
        p1, p2 = random.choices(population, weights=weights, k=2)

        depot: Node = graph.get_node(0)

        length = len(p1.flatten_routes())

        # Choose two random indices for the crossover
        start_index = random.randint(0, length - 1)
        end_index = random.randint(start_index + 1, length)

        # Initialize the child with a copy of the substring from parent1
        child = p1.flatten_routes()[start_index:end_index]

        # Fill in the remaining positions with genes from parent2
        remaining_positions = [i for i in range(length) if i < start_index or i >= end_index]
        remaining_genes = [gene for gene in p2.flatten_routes() if gene not in child]

        for position, gene in zip(remaining_positions, remaining_genes):
            child.insert(position, gene)

        vehicle = Vehicle(depot_id=depot.id, node_ids=[child])
        return Solution(vehicles=[vehicle])
    
    def _cycle_crossover_numpy(self, p1: list[int], p2: list[int]) -> tuple[list[int], list[int]]:
        """
        CEX em O(n) usando mapa de posições. Supõe que p1/p2 são permutações do mesmo conjunto de IDs.
        """
        n = len(p1)
        c1: list[int] = []
        c2: list[int] = []

        # pos1[val] = posição de 'val' em p1
        pos1 = np.empty(p1.max() + 1, dtype=int)
        pos1[p1] = np.arange(n, dtype=int)

        visited: list[bool] = [False] * n
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

    def mutate(self, solution: Solution, mutation_probability: float, g: Graph) -> Solution:
        """
        Mutação em array de IDs + reconstrução com a MESMA estrutura da solução original.
        """
        if mutation_probability <= 0:
            return solution

        depot = g.get_node(0)
        struct = self._structure_of(solution)
        ids = solution.flatten_routes()

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
    
    def _structure_of(self, solution: Solution) -> list[list[int]]:
        """
        Estrutura = lista de veículos; para cada veículo, lista com o tamanho de cada itinerary.
        Ex: [[5], [3, 2]] significa: veic0 com 1 itinerary de 5 clientes; veic1 com 2 itinerários (3 e 2 clientes).
        """
        return [[len(it) for it in v.itineraries] for v in solution.vehicles]

    def _rebuild_from(self, ids: np.ndarray, structure: list[list[int]], depot: Node) -> Solution:
        """
        Reconstrói Solution a partir do array de IDs e da estrutura (quantos itinerários e seus tamanhos por veículo).
        Reusa instâncias originais de Customer (id->Customer).
        """
        cursor = 0
        vehicles: list[Vehicle] = []
        for veh_it_sizes in structure:
            itineraries: list[list[int]] = []
            for size in veh_it_sizes:
                node_ids = [i for i in ids[cursor: cursor + size]]
                cursor += size
                itineraries.append(node_ids)
            vehicles.append(Vehicle(depot_id=depot, node_ids=itineraries))
        return Solution(vehicles=vehicles)
