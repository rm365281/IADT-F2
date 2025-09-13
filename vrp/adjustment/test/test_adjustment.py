from unittest import TestCase
from unittest.mock import Mock

from domain import Route
from domain import Solution
from vrp.adjustment.adjustment import Adjustment


def create_vehicle(autonomy=100, capacity=50, route=None):
    vehicle = Mock()
    vehicle.autonomy = autonomy
    vehicle.capacity = capacity
    vehicle.route = route if route is not None else Mock()
    return vehicle


def create_solution(vehicles):
    return Solution(vehicles=vehicles)


class TestAdjustment(TestCase):

    def setUp(self):
        self.helper = Mock()
        self.adjustment = Adjustment(helper=self.helper)

    def mock_helper(self, split_return, remove_return, return_value):
        self.helper.split_route_by_capacity = Mock(return_value=split_return)
        self.helper.remove_duplicated_sequencial_depots = Mock(return_value=remove_return)
        self.helper.calculate_distance = Mock(return_value=return_value)

    def test_applies_adjustment_to_solution_with_single_vehicle(self):
        vehicle = create_vehicle()
        solution = create_solution([vehicle])
        self.mock_helper(Route([0, 1, 2, 0]), Route([0, 1, 2, 0]), 10.0)
        result = self.adjustment.apply(solution)
        self.assertEqual(len(result.vehicles), 1)
        self.assertEqual(result.vehicles[0].customers(), [0, 1, 2, 0])
        self.assertEqual(result.total_distance(), 10)

    def test_handles_solution_with_no_vehicles(self):
        solution = create_solution([])
        result = self.adjustment.apply(solution)
        self.assertEqual(len(result.vehicles), 0)
        self.assertEqual(result.total_distance(), 0)

    def test_applies_adjustment_to_solution_with_multiple_vehicles(self):
        vehicle1 = create_vehicle()
        vehicle2 = create_vehicle(autonomy=80, capacity=30)
        solution = create_solution([vehicle1, vehicle2])
        self.helper.split_route_by_capacity = Mock(side_effect=[Route([0, 1, 0]), Route([0, 2, 0])])
        self.helper.remove_duplicated_sequencial_depots = Mock(side_effect=[Route([0, 1, 0]), Route([0, 2, 0])])
        self.helper.calculate_distance = Mock(return_value=10.0)
        result = self.adjustment.apply(solution)
        self.assertEqual(len(result.vehicles), 2)
        self.assertEqual(result.vehicles[0].customers(), [0, 1, 0])
        self.assertEqual(result.vehicles[1].customers(), [0, 2, 0])
        self.assertEqual(result.total_distance(), 20)

    def test_handles_empty_itinerary_correctly(self):
        vehicle = create_vehicle()
        solution = create_solution([vehicle])
        self.mock_helper(Route([]), Route([]), 0.0)
        result = self.adjustment.apply(solution)
        self.assertEqual(len(result.vehicles), 1)
        self.assertEqual(result.vehicles[0].customers(), [])
        self.assertEqual(result.total_distance(), 0)
