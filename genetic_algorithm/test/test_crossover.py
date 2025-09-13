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
        def get_all_customers(solution: Solution) -> set:
            customers = set()
            for vehicle in solution.vehicles:
                customers.update([c for c in vehicle.customers() if c != self.depot_identifier])
            return customers

        child1, child2 = self.crossover.apply(self.parent1, self.parent2)

        all_customers_parent1 = get_all_customers(self.parent1)
        all_customers_parent2 = get_all_customers(self.parent2)
        all_customers_children = get_all_customers(child1).union(get_all_customers(child2))

        self.assertEqual(all_customers_parent1, all_customers_children)
        self.assertEqual(all_customers_parent2, all_customers_children)

        self.assertEqual(len(self.parent1.flatten_routes()), len(child1.flatten_routes()))
        self.assertEqual(len(self.parent2.flatten_routes()), len(child2.flatten_routes()))
        self.assertEqual(len(self.parent1.flatten_routes()), len(child2.flatten_routes()))
        self.assertEqual(len(self.parent2.flatten_routes()), len(child1.flatten_routes()))
