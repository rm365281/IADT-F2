from unittest import TestCase
from domain.vehicle import Vehicle
from domain.route import Route


class TestVehicle(TestCase):
    def test_customers(self):
        route = Route([1, 2, 3])
        vehicle = Vehicle(route=route, capacity=50, autonomy=300.0)

        self.assertEqual(vehicle.customers(), [1, 2, 3])

    def test_distance(self):
        route = Route([1, 2, 3])
        route.distance = 150.0
        vehicle = Vehicle(route=route, capacity=50, autonomy=300.0)

        self.assertEqual(vehicle.distance(), 150.0)

    def test_zero_capacity(self):
        route = Route([])
        vehicle = Vehicle(route=route, capacity=0, autonomy=100.0)

        self.assertEqual(vehicle.capacity, 0)

    def test_negative_autonomy(self):
        route = Route([1, 2])
        vehicle = Vehicle(route=route, capacity=10, autonomy=-50.0)

        self.assertEqual(vehicle.autonomy, -50.0)

    def test_invalid_route_type(self):
        with self.assertRaises(TypeError):
            Vehicle(route='not_a_route', capacity=10, autonomy=100.0)
