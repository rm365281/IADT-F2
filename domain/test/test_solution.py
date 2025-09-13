from unittest import TestCase
from unittest.mock import Mock
from domain.solution import Solution


class TestSolution(TestCase):

    def setUp(self):
        vehicle1 = Mock()
        vehicle1.customers = Mock(return_value=[1, 2, 3])
        vehicle1.distance.return_value = 200
        vehicle2 = Mock()
        vehicle2.customers = Mock(return_value=[4])
        vehicle2.distance.return_value = 50
        self.solution = Solution(vehicles=[vehicle1, vehicle2])

    def test_total_distance(self):
        self.assertEqual(self.solution.total_distance(), 250.0)

    def test_flatten_routes(self):
        self.assertEqual(self.solution.flatten_routes(), [1, 2, 3, 4])