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