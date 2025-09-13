from unittest import TestCase
from unittest.mock import MagicMock

from route import Route
from vrp.adjustment.helper import Helper


class TestHelper(TestCase):

    graph = MagicMock()
    depot_identifier = 0
    helper = Helper(graph, depot_identifier=depot_identifier)

    def setUp(self):
        self.graph.get_node_demand.side_effect = [15, 10, 5]

    def test_splits_route_correctly_when_capacity_is_not_exceeded(self):
        route = Route([0, 1, 2, 3])

        result = self.helper.split_route_by_capacity(route, 50)

        self.assertEqual(result.customers, [0, 1, 2, 3])

    def test_splits_route_correctly_when_capacity_is_exceeded(self):
        route = Route([0, 1, 2, 3])

        result = self.helper.split_route_by_capacity(route, 15)

        self.assertEqual(result.customers, [0, 1, 0, 2, 3])

    def test_removes_duplicated_sequential_depots_correctly(self):
        route = Route([0, 1, 0, 0, 2, 0])

        result = self.helper.remove_duplicated_sequencial_depots(route)

        self.assertEqual(result.customers, [0, 1, 0, 2, 0])

    def test_handles_empty_itinerary_correctly(self):
        route = Route([])

        result = self.helper.remove_duplicated_sequencial_depots(route)

        self.assertEqual(result.customers, [])

    def test_handles_itinerary_with_no_duplicates(self):
        route = Route([0, 1, 2, 3])

        result = self.helper.remove_duplicated_sequencial_depots(route)

        self.assertEqual(result.customers, [0, 1, 2, 3])

    def test_calculates_distance_correctly(self):
        route = Route([0, 1, 2])
        self.graph.get_edge.side_effect = [
            MagicMock(distance=10.0),
            MagicMock(distance=20.0)
        ]

        result = self.helper.calculate_distance(route)

        self.assertEqual(result, 30.0)