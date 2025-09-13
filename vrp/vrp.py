from solution import Solution
from vrp import Mutation
from vrp.adjustment.adjustment import Adjustment
from vrp.crossover import Crossover
from vrp.fitness import Fitness
from vrp.initial_population import InitialPopulationGenerator
from vrp.route_spliter import RouteSplitter


class VRP:
    def __init__(self, adjustment: Adjustment, route_splitter: RouteSplitter, crossover: Crossover = None,
                 mutation: Mutation = None,
                 initial_population_generator: InitialPopulationGenerator = None, fitness: Fitness = None) -> None:
        self.__adjustment = adjustment
        self.__route_splitter = route_splitter
        self.__crossover = crossover
        self.__mutation = mutation
        self.__initial_population_generator = initial_population_generator
        self.__fitness = fitness

    def generate_initial_population(self) -> list[Solution]:
        return self.__initial_population_generator.generate()

    def fitness(self, solution: Solution) -> None:
        penalty = self.__fitness.calculate_tolls_penality(solution.vehicles)
        penalty += self.__fitness.calculate_priority_violation_penality(solution.vehicles)
        penalty += self.__fitness.calculate_capacity_violation_penality(solution.vehicles)
        penalty += self.__fitness.calculate_vehicle_unbalanced_distance_penality(solution.vehicles)

        solution.fitness = solution.total_distance() + penalty

    def sort_population(self, population: list[Solution]) -> list[Solution]:
        return sorted(population, key=lambda solution: solution.fitness)

    def crossover(self, p1: Solution, p2: Solution) -> tuple[Solution, Solution]:
        solution1, solution2 = self.__crossover.apply(p1, p2)
        adjusted_solution1 = self.__adjustment.apply(solution1)
        adjusted_solution2 = self.__adjustment.apply(solution2)
        return adjusted_solution1, adjusted_solution2

    def mutate(self, solution: Solution) -> Solution:
        mutated_solution = self.__mutation.apply(solution)
        return self.__adjustment.apply(mutated_solution)