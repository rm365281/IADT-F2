from unittest.mock import Mock

import pytest

from graph import Node
from itinerary import Itinerary
from solution import Solution
from vehicle import Vehicle
from vrp.mutation import mutate_vehicle_itinerary, mutate_itinerary_between_vehicles, _swap_customers_between_vehicles, \
    split_routes


@pytest.mark.parametrize("customers, expected", [
    ([1, 2, 3], 3),
    ([4, 5, 6], 3),
    ([7, 8, 9], 3),
    ([0, 0, 0], 1)
])
def test_mutate_vehicle_itinerary(customers, expected):
    vehicle = Vehicle(depot_id=0, capacity=10, itinerary=Itinerary(customers), autonomy=1)

    mutate_vehicle_itinerary(vehicle=vehicle, mutation_probability=1)

    assert customers != vehicle.customers()
    assert expected == len(vehicle.customers())


def test_mutate_itinerary_between_vehicles():
    depot = Node(identifier=0, x=0, y=0)

    vehicles = [Vehicle(depot_id=depot.identifier, capacity=10, itinerary=Itinerary([0, 0, 0]), autonomy=1),
                Vehicle(depot_id=depot.identifier, capacity=10, itinerary=Itinerary([0, 0, 0]), autonomy=1)]
    solution = Solution(vehicles=vehicles)

    mutate_itinerary_between_vehicles(depot, solution)

    assert solution.vehicles[0].customers() == []
    assert solution.vehicles[1].customers() == [0]


@pytest.mark.parametrize("depot, vehicles, expected", [
    (Node(identifier=0, x=0, y=0), [
        Vehicle(depot_id=0, capacity=10, itinerary=Itinerary([0, 0, 0]), autonomy=1),
        Vehicle(depot_id=0, capacity=10, itinerary=Itinerary([0, 0, 0]), autonomy=1),
        Vehicle(depot_id=0, capacity=10, itinerary=Itinerary([0, 0, 0]), autonomy=1)
    ], [[], [0]])
])
def test_swap_customers_between_vehicles(depot, vehicles, expected):
    vehicle1 = vehicles[0]
    vehicle2 = vehicles[1]
    vehicle3 = vehicles[2]
    vehicles = [vehicle1, vehicle2, vehicle3]
    solution = Solution(vehicles=vehicles)

    _swap_customers_between_vehicles(depot, solution, vehicle1, vehicle2)

    assert solution.vehicles[0] == vehicle3
    assert solution.vehicles[1].customers() == expected[0]
    assert solution.vehicles[2].customers() == expected[1]


def test_split_routes():
    depot = Node(identifier=0, x=0, y=0)
    solution = Mock()
    solution.vehicles = [Vehicle(0, Itinerary([0,1,2,3,0]))]

    split_routes(depot, solution)

    assert len(solution.vehicles[0].full_itinerary.customers) == 7
    assert len(solution.vehicles[0].itinerary.customers) == 7
