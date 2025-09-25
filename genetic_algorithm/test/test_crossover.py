from unittest import TestCase
from genetic_algorithm import Crossover
from domain.solution import Solution
from domain.vehicle import Vehicle
from domain.route import Route
from genetic_algorithm.crossover import choose_two_different_indices


def test_choose_two_different_indices():
    length = 10
    idx1, idx2 = choose_two_different_indices(length)
    assert 0 <= idx1 < idx2 <= length


class TestCrossover(TestCase):
    depot_identifier = 0
    number_vehicles = 3
    vehicle_autonomy = 100.0
    vehicle_capacity = 50

    crossover = Crossover(depot_identifier, number_vehicles, vehicle_autonomy, vehicle_capacity)

    vehicles_p1 = [
        Vehicle(Route([0, 1, 2, 7, 0]), autonomy=vehicle_autonomy, capacity=vehicle_capacity),
        Vehicle(Route([0, 3, 4, 8, 0]), autonomy=vehicle_autonomy, capacity=vehicle_capacity),
        Vehicle(Route([0, 5, 6, 9, 0]), autonomy=vehicle_autonomy, capacity=vehicle_capacity)
    ]
    parent1 = Solution(vehicles=vehicles_p1)

    vehicles_p2 = [
        Vehicle(Route([0, 4, 5, 7, 0]), autonomy=vehicle_autonomy, capacity=vehicle_capacity),
        Vehicle(Route([0, 6, 1, 8, 0]), autonomy=vehicle_autonomy, capacity=vehicle_capacity),
        Vehicle(Route([0, 2, 3, 9, 0]), autonomy=vehicle_autonomy, capacity=vehicle_capacity)
    ]
    parent2 = Solution(vehicles=vehicles_p2)

    def test_crossover(self):
        child1, child2 = self.crossover.apply(self.parent1, self.parent2)

        self.assertIsInstance(child1, Solution)
        self.assertIsInstance(child2, Solution)

        self.assertEqual(len(child1.vehicles), self.number_vehicles)
        self.assertEqual(len(child2.vehicles), self.number_vehicles)

        self.assertNotEqual(self.parent1.flatten_routes(), child1.flatten_routes())
        self.assertNotEqual(self.parent2.flatten_routes(), child2.flatten_routes())

    def test_crossover_preserves_customers(self):
        """Deve garantir que todos os clientes dos pais estejam nos filhos."""
        child1, child2 = self.crossover.apply(self.parent1, self.parent2)
        all_customers_parent = set(self.parent1.flatten_routes() + self.parent2.flatten_routes())
        self.assertTrue(set(child1.flatten_routes()).issubset(all_customers_parent))
        self.assertTrue(set(child2.flatten_routes()).issubset(all_customers_parent))

    def test_invalid_parents_type(self):
        """Deve lançar erro se os pais não forem Solution."""
        with self.assertRaises(Exception):
            self.crossover.apply('not_a_solution', self.parent2)

    def test_empty_parents(self):
        """Deve lançar erro se os pais não tiverem veículos."""
        empty_parent = Solution(vehicles=[])
        with self.assertRaises(Exception):
            self.crossover.apply(empty_parent, self.parent2)
