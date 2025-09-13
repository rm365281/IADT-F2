from unittest import TestCase
from domain.route import Route


class TestRoute(TestCase):

    def test_customers(self):
        route = Route([0, 1, 2, 3, 0])
        self.assertEqual(route.customers, [0, 1, 2, 3, 0])

    def test_distance(self):
        route = Route([0, 1, 2, 3, 0])
        self.assertEqual(route.distance, 0.0)

    def test_distance_assignment(self):
        route = Route([0, 1, 2, 3, 0])
        route.distance = 10.5
        self.assertEqual(route.distance, 10.5)