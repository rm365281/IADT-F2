import random
from vrp.route_spliter import RouteSplitter
from domain import Solution
from domain import Vehicle
from domain import Route


class Mutation:
    def __init__(self, mutation_probability: float, splitter: RouteSplitter) -> None:
        self.__mutation_probability = mutation_probability
        self.__splitter = splitter

    def apply(self, solution: Solution) -> Solution:
        """
        Aplica a Inverted Displacement Mutation na solução.
        Args:
            solution: solução a ser mutada.

        Returns:
            Solução mutada.

        """
        if random.random() > self.__mutation_probability:
            return solution

        vehicles = solution.vehicles
        if not vehicles:
            return solution
        depot_identifier = vehicles[0].route.customers[0]  # Assume depósito é o primeiro nó
        autonomy = vehicles[0].autonomy
        capacity = vehicles[0].capacity
        number_vehicles = len(vehicles)

        # Obtém a rota linear sem o depósito
        flat_route = [x for x in solution.flatten_routes() if x != depot_identifier]
        route_length = len(flat_route)
        if route_length < 2:
            return solution

        # Seleciona dois índices distintos
        idx1 = random.randint(0, route_length - 2)
        idx2 = random.randint(idx1 + 1, route_length - 1)

        # Extrai, inverte e recoloca o segmento
        segment = flat_route[idx1:idx2 + 1]
        segment.reverse()
        mutated_route = flat_route[:idx1] + segment + flat_route[idx2 + 1:]

        # Divide a rota mutada em rotas para cada veículo
        split_routes = self.__splitter.split(Route(mutated_route))
        mutated_vehicles = [Vehicle(route, autonomy=autonomy, capacity=capacity) for route in split_routes]

        return Solution(mutated_vehicles)
