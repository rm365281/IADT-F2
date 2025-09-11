from unittest import TestCase
from unittest.mock import Mock

from solution import Solution
from vrp.adjustment.adjustment import Adjustment


def create_vehicle(autonomy=100, capacity=50, itinerary=None):
    vehicle = Mock()
    vehicle.autonomy = autonomy
    vehicle.capacity = capacity
    vehicle.itinerary = itinerary if itinerary is not None else Mock()
    return vehicle


def create_solution(vehicles):
    return Solution(vehicles=vehicles)


class TestAdjustment(TestCase):

    def setUp(self):
        self.graph = Mock()
        self.graph.get_node(0).return_value = Mock(identifier=0, demand=0)
        self.adjustment = Adjustment(graph=self.graph, depot_identifier=0)
        self.helper = self.adjustment.__helper

    def mock_helper(self, split_return, remove_return):
        self.helper.split_route_by_capacity = Mock(return_value=split_return)
        self.helper.remove_duplicated_sequencial_depots = Mock(return_value=remove_return)

    def test_applies_adjustment_to_solution_with_single_vehicle(self):
        vehicle = create_vehicle()
        solution = create_solution([vehicle])
        self.mock_helper([0, 1, 2, 0], [0, 1, 2, 0])
        result = self.adjustment.apply(solution)
        self.assertEqual(len(result.vehicles), 1)
        self.assertEqual(result.vehicles[0].itinerary.customers, [0, 1, 2, 0])

    def test_handles_solution_with_no_vehicles(self):
        solution = create_solution([])
        result = self.adjustment.apply(solution)
        self.assertEqual(len(result.vehicles), 0)

    def test_applies_adjustment_to_solution_with_multiple_vehicles(self):
        vehicle1 = create_vehicle()
        vehicle2 = create_vehicle(autonomy=80, capacity=30)
        solution = create_solution([vehicle1, vehicle2])
        self.helper.split_route_by_capacity = Mock(side_effect=[[0, 1, 0], [0, 2, 0]])
        self.helper.remove_duplicated_sequencial_depots = Mock(side_effect=[[0, 1, 0], [0, 2, 0]])
        result = self.adjustment.apply(solution)
        self.assertEqual(len(result.vehicles), 2)
        self.assertEqual(result.vehicles[0].itinerary.customers, [0, 1, 0])
        self.assertEqual(result.vehicles[1].itinerary.customers, [0, 2, 0])

    def test_handles_empty_itinerary_correctly(self):
        vehicle = create_vehicle()
        solution = create_solution([vehicle])
        self.mock_helper([], [])
        result = self.adjustment.apply(solution)
        self.assertEqual(len(result.vehicles), 1)
        self.assertEqual(result.vehicles[0].itinerary.customers, [])
