from unittest.mock import Mock

import pytest

from graph import Node
from itinerary import Itinerary
from vehicle import Vehicle
from vrp.fitness import calculate_distance_penality, calculate_priority_violation_penality, \
    calculate_vehicle_unbalanced_distance_penality


def test_calculate_distance_penality():
    full_itinerary: Itinerary = Mock()
    full_itinerary.distance = 100

    vehicle: Vehicle = Mock()
    vehicle.autonomy = 80

    penalty = calculate_distance_penality(full_itinerary, vehicle)

    assert penalty == (100 - 80) * 1000

@pytest.mark.parametrize('depot, from_node, has_non_priority_customer_before_priority_customer_in_itinerary, expected_has_non_priority_customer_before_priority_customer_in_itinerary, expected_penalty', [
    (Node(identifier=0, x=1, y=1, priority=0), Node(identifier=1, x=2, y=2, priority=0), False, True, 0),
    (Node(identifier=0, x=1, y=1, priority=0), Node(identifier=2, x=3, y=3, priority=1), True, True, 50),
])
def test_calculate_priority_violation_penality(depot, from_node, has_non_priority_customer_before_priority_customer_in_itinerary, expected_has_non_priority_customer_before_priority_customer_in_itinerary, expected_penalty):
    has_non_priority_customer_before_priority_customer_in_itinerary, penalty = calculate_priority_violation_penality(depot, from_node, has_non_priority_customer_before_priority_customer_in_itinerary)

    assert expected_has_non_priority_customer_before_priority_customer_in_itinerary == has_non_priority_customer_before_priority_customer_in_itinerary
    assert expected_penalty == penalty

@pytest.mark.parametrize('vehicles, expected_penalty', [
    ([], 0),
    ([Mock(distance=Mock(return_value=100))], 0),
    ([Mock(distance=Mock(return_value=100)), Mock(distance=Mock(return_value=200))], 100),
    ([Mock(distance=Mock(return_value=100)), Mock(distance=Mock(return_value=200)), Mock(distance=Mock(return_value=300))], 200),
])
def test_calculate_vehicle_unbalanced_distance_penality(vehicles, expected_penalty):
    penalty = calculate_vehicle_unbalanced_distance_penality(vehicles)
    assert expected_penalty == penalty
