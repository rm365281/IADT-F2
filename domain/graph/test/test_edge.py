from unittest import TestCase

from domain.graph import Node, Edge


class TestEdge(TestCase):
    def test_calculate_toll_quantity(self):
        node_a = Node(identifier=1, x=0, y=0)
        node_b = Node(identifier=2, x=1, y=1)

        edge_with_distance = Edge(from_node=node_a, to_node=node_b, distance=450)
        self.assertEqual(edge_with_distance.toll_quantity, 2)

        edge_without_distance = Edge(from_node=node_a, to_node=node_b)
        self.assertEqual(edge_without_distance.toll_quantity, 0)

    def test_negative_distance(self):
        node_a = Node(identifier=1, x=0, y=0)
        node_b = Node(identifier=2, x=1, y=1)

        edge = Edge(from_node=node_a, to_node=node_b, distance=-100)
        self.assertEqual(edge.toll_quantity, 0)

    def test_invalid_nodes(self):
        with self.assertRaises(TypeError):
            Edge(from_node='not_a_node', to_node=None, distance=10)

    def test_large_distance(self):
        node_a = Node(identifier=1, x=0, y=0)
        node_b = Node(identifier=2, x=1, y=1)

        edge = Edge(from_node=node_a, to_node=node_b, distance=10000)
        self.assertEqual(edge.toll_quantity, 66)
