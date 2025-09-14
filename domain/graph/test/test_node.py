from unittest import TestCase


class TestNode(TestCase):

    def test_init(self):
        from domain.graph.node import Node

        node = Node(identifier=1, x=10.0, y=20.0, priority=5, demand=15)
        self.assertEqual(node.identifier, 1)
        self.assertEqual(node.x, 10.0)
        self.assertEqual(node.y, 20.0)
        self.assertEqual(node.priority, 5)
        self.assertEqual(node.demand, 15)

    def test_eq(self):
        from domain.graph.node import Node

        node1 = Node(identifier=1)
        node2 = Node(identifier=1)
        node3 = Node(identifier=2)

        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, "not a node")

    def test_extreme_values(self):
        """Deve aceitar valores extremos para atributos."""
        from domain.graph.node import Node

        node = Node(identifier=999999, x=1e9, y=-1e9, priority=1000, demand=-100)
        self.assertEqual(node.identifier, 999999)
        self.assertEqual(node.x, 1e9)
        self.assertEqual(node.y, -1e9)
        self.assertEqual(node.priority, 1000)
        self.assertEqual(node.demand, -100)

    def test_invalid_identifier_type(self):
        """Deve lançar erro se identifier não for int."""
        from domain.graph.node import Node

        with self.assertRaises(Exception):
            Node(identifier='not_an_int')
