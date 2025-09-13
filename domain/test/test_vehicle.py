from unittest import TestCase
from unittest.mock import Mock


class TestVehicle(TestCase):

    def test_customers(self):
        from domain.vehicle import Vehicle

        route = Mock(customers=[1, 2, 3])
        vehicle = Vehicle(route=route, capacity=50, autonomy=300.0)

        self.assertEqual(vehicle.customers(), [1, 2, 3])

    def test_distance(self):
        from domain.vehicle import Vehicle

        route = Mock(distance=150.0)
        vehicle = Vehicle(route=route, capacity=50, autonomy=300.0)

        self.assertEqual(vehicle.distance(), 150.0)