from unittest import TestCase
from unittest.mock import Mock

from vrp import VRP
from genetic_algorithm import Mutation
from vrp.adjustment.adjustment import Adjustment
from genetic_algorithm.crossover import Crossover
from genetic_algorithm.fitness import Fitness
from genetic_algorithm.initial_population import InitialPopulationGenerator
from vrp.route_spliter import RouteSplitter


class TestVRP(TestCase):
    adjustment: Adjustment = Mock()
    route_splitter: RouteSplitter = Mock()
    crossover: Crossover = Mock()
    mutation: Mutation = Mock()
    initial_population_generator: InitialPopulationGenerator = Mock()
    fitness: Fitness = Mock()

    vrp = VRP(adjustment, route_splitter, crossover, mutation, initial_population_generator, fitness)

    def test_generate_initial_population(self):
        self.initial_population_generator.generate.return_value = [Mock(), Mock()]

        population = self.vrp.generate_initial_population()

        self.assertEqual(len(population), 2)

    def test_fitness(self):
        solution = Mock()
        solution.vehicles = [Mock()]
        solution.total_distance.return_value = 10
        self.fitness.calculate_tolls_penality.return_value = 1
        self.fitness.calculate_priority_violation_penality.return_value = 2
        self.fitness.calculate_capacity_violation_penality.return_value = 3
        self.fitness.calculate_vehicle_unbalanced_distance_penality.return_value = 4

        self.vrp.fitness(solution)

        self.fitness.calculate_tolls_penality.assert_called_once_with(solution.vehicles)
        self.fitness.calculate_priority_violation_penality.assert_called_once_with(solution.vehicles)
        self.fitness.calculate_capacity_violation_penality.assert_called_once_with(solution.vehicles)
        self.fitness.calculate_vehicle_unbalanced_distance_penality.assert_called_once_with(solution.vehicles)
        solution.total_distance.assert_called_once()
        self.assertEqual(solution.fitness, 10 + 1 + 2 + 3 + 4)

    def test_sort_population(self):
        s1 = Mock()
        s2 = Mock()
        s3 = Mock()
        s1.fitness = 30
        s2.fitness = 10
        s3.fitness = 20
        population = [s1, s2, s3]
        sorted_population = self.vrp.sort_population(population)
        self.assertEqual([s.fitness for s in sorted_population], [10, 20, 30])

    def test_crossover(self):
        p1 = Mock()
        p2 = Mock()
        solution1 = Mock()
        solution2 = Mock()
        adjusted_solution1 = Mock()
        adjusted_solution2 = Mock()
        self.crossover.apply.return_value = (solution1, solution2)
        self.adjustment.apply.side_effect = [adjusted_solution1, adjusted_solution2]

        result1, result2 = self.vrp.crossover(p1, p2)

        self.crossover.apply.assert_called_once_with(p1, p2)
        self.adjustment.apply.assert_any_call(solution1)
        self.adjustment.apply.assert_any_call(solution2)
        self.assertEqual(result1, adjusted_solution1)
        self.assertEqual(result2, adjusted_solution2)
