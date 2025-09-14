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

    def test_empty_route(self):
        """Deve permitir rota vazia e distância zero."""
        route = Route([])
        self.assertEqual(route.customers, [])
        self.assertEqual(route.distance, 0.0)

    def test_invalid_customers_type(self):
        """Deve lançar erro se clientes não forem lista."""
        with self.assertRaises(TypeError):
            Route('not_a_list')

    def test_negative_distance(self):
        """Deve aceitar distância negativa (caso de borda)."""
        route = Route([0, 1])
        route.distance = -5.0
        self.assertEqual(route.distance, -5.0)
