from unittest import TestCase
from unittest.mock import MagicMock

import pytest

from vrp.adjustment.helper import Helper


class TestHelper(TestCase):

    graph = MagicMock()
    depot_identifier = 0
    helper = Helper(graph, depot_identifier=depot_identifier)

    def setUp(self):
        self.graph.get_node_demand.side_effect = [15, 10, 5]

    def test_splits_route_correctly_when_capacity_is_not_exceeded(self):
        vehicle = MagicMock()
        vehicle.customers.return_value = [self.depot_identifier, 1, 2, 3]
        vehicle.capacity = 50

        result = self.helper.split_route_by_capacity(vehicle)

        self.assertEqual(result, [self.depot_identifier, 1, 2, 3])

    def test_splits_route_correctly_when_capacity_is_exceeded(self):
        vehicle = MagicMock()
        vehicle.customers.return_value = [self.depot_identifier, 1, 2, 3]
        vehicle.capacity = 15

        result = self.helper.split_route_by_capacity(vehicle)

        self.assertEqual(result, [self.depot_identifier, 1, self.depot_identifier, 2, 3])

    def test_removes_duplicated_sequential_depots_correctly(self):
        itinerary = [self.depot_identifier, 1, self.depot_identifier, self.depot_identifier, 2, self.depot_identifier]

        result = self.helper.remove_duplicated_sequencial_depots(itinerary)

        self.assertEqual(result, [self.depot_identifier, 1, self.depot_identifier, 2, self.depot_identifier])

    def test_handles_empty_itinerary_correctly(self):
        itinerary = []

        result = self.helper.remove_duplicated_sequencial_depots(itinerary)

        self.assertEqual(result, [])

    def test_handles_itinerary_with_no_duplicates(self):
        itinerary = [self.depot_identifier, 1, 2, 3]

        result = self.helper.remove_duplicated_sequencial_depots(itinerary)

        self.assertEqual(result, [self.depot_identifier, 1, 2, 3])