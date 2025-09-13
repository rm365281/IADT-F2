from domain.graph import Graph
from vrp import VRP
from genetic_algorithm.mutation import Mutation
from vrp.adjustment.adjustment import Adjustment
from vrp.adjustment.helper import Helper
from genetic_algorithm.crossover import Crossover
from genetic_algorithm.fitness import Fitness
from genetic_algorithm.initial_population import InitialPopulationGenerator
from vrp.route_spliter import RouteSplitter


class VrpFactory:

    def __init__(self, graph: Graph, population_size: int, number_vehicles: int, mutation_probability: float = 0.5,
                 vehicle_autonomy: float = 500.0, vehicle_capacity: int = 100) -> None:
        self.__depot = graph.get_node(0)
        self.__adjustment = Adjustment(self.__depot.identifier, Helper(graph, self.__depot.identifier))
        self.__route_splitter = RouteSplitter(self.__depot.identifier, number_vehicles)
        self.__crossover = Crossover(self.__depot.identifier, number_vehicles, vehicle_autonomy,
                                     vehicle_capacity)
        self.__mutation = Mutation(mutation_probability, self.__route_splitter)
        self.__initial_population_generator = InitialPopulationGenerator(graph, population_size,
                                                                         self.__adjustment, vehicle_capacity,
                                                                         vehicle_autonomy,
                                                                         number_vehicles,
                                                                         self.__depot.identifier)
        self.__fitness = Fitness(graph)

    def create_vrp(self) -> VRP:
        return VRP(self.__adjustment, self.__route_splitter, self.__crossover, self.__mutation, self.__initial_population_generator, self.__fitness)
