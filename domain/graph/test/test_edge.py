from unittest import TestCase
from unittest.mock import Mock

from domain.graph import Node, Edge


class TestEdge(TestCase):

    def test_calculate_toll_quantity(self):

        node_a = Mock(identifier=1)
        node_b = Mock(identifier=2)

        edge_with_distance = Edge(from_node=node_a, to_node=node_b, distance=450)
        self.assertEqual(edge_with_distance.toll_quantity, 2)

        edge_without_distance = Edge(from_node=node_a, to_node=node_b)
        self.assertEqual(edge_without_distance.toll_quantity, 0)