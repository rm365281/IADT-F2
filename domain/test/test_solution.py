from unittest import TestCase
from domain.solution import Solution
from domain.vehicle import Vehicle
from domain.route import Route


class TestSolution(TestCase):
    def setUp(self):
        vehicle1 = Vehicle(Route([1, 2, 3]), capacity=50, autonomy=200)
        vehicle2 = Vehicle(Route([4]), capacity=50, autonomy=50)
        self.solution = Solution(vehicles=[vehicle1, vehicle2])

    def test_total_distance(self):
        self.solution.vehicles[0].route.distance = 200
        self.solution.vehicles[1].route.distance = 50
        self.assertEqual(self.solution.total_distance(), 250.0)

    def test_flatten_routes(self):
        self.assertEqual(self.solution.flatten_routes(), [1, 2, 3, 4])

    def test_empty_solution(self):
        solution = Solution(vehicles=[])
        self.assertEqual(solution.total_distance(), 0.0)
        self.assertEqual(solution.flatten_routes(), [])

    def test_vehicle_with_no_customers(self):
        vehicle = Vehicle(Route([]), capacity=10, autonomy=10)
        solution = Solution(vehicles=[vehicle])
        self.assertEqual(solution.flatten_routes(), [])

    def test_invalid_vehicles_type(self):
        with self.assertRaises(TypeError):
            Solution(vehicles='not_a_list')
