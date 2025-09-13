from unittest import TestCase
from unittest.mock import Mock

from domain.route import Route
from genetic_algorithm.mutation import Mutation


class TestMutation(TestCase):

    splitter = Mock()
    splitter.split.return_value = [Route([0, 3, 2, 1, 0])]

    def test_apply_no_mutation_due_to_probability(self):
        mutation = Mutation(0.0, self.splitter)

        solution = Mock()

        mutated_solution = mutation.apply(solution)

        self.assertEqual(solution, mutated_solution)

    def test_apply_with_mutation_due_to_probability(self):
        mutation = Mutation(1.0, self.splitter)

        vehicle_mock = Mock()
        vehicle_mock.route.customers = [0, 1, 2, 3, 0]
        vehicle_mock.autonomy = 100
        vehicle_mock.capacity = 50

        solution = Mock()
        solution.vehicles = [vehicle_mock]
        solution.flatten_routes.return_value = [0, 1, 2, 3, 0]

        mutated_solution = mutation.apply(solution)

        self.assertNotEqual(solution, mutated_solution)
        self.assertEqual(len(mutated_solution.vehicles), 1)
        self.assertEqual(mutated_solution.vehicles[0].route.customers[0], 0)
        self.assertEqual(mutated_solution.vehicles[0].route.customers[-1], 0)
        self.assertCountEqual(mutated_solution.vehicles[0].route.customers[1:-1], [1, 2, 3])
        self.assertNotEqual(mutated_solution.vehicles[0].route.customers[1:-1], [1, 2, 3])

    def test_apply_with_mutation_with_insufficient_customers(self):
        mutation = Mutation(1.0, self.splitter)

        vehicle_mock = Mock()
        vehicle_mock.route.customers = [0, 1, 0]
        vehicle_mock.autonomy = 100
        vehicle_mock.capacity = 50

        solution = Mock()
        solution.vehicles = [vehicle_mock]
        solution.flatten_routes.return_value = [0, 1, 0]

        mutated_solution = mutation.apply(solution)

        self.assertEqual(solution, mutated_solution)

    def test_apply_no_mutation_with_no_vehicles(self):
        mutation = Mutation(1.0, self.splitter)

        solution = Mock()
        solution.vehicles = []

        mutated_solution = mutation.apply(solution)

        self.assertEqual(solution, mutated_solution)