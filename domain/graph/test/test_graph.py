from unittest import TestCase

import pytest

from domain.graph import Graph, Node, Edge


class TestGraph(TestCase):

    def test_graph_initialization_creates_correct_edges(self):
        node1 = Node(identifier=1, x=0, y=0, priority=0, demand=10)
        node2 = Node(identifier=2, x=3, y=4, priority=0, demand=20)
        graph = Graph(nodes=[node1, node2])
        edge = graph.get_edge(node1, node2)
        self.assertEqual(edge.distance, 5)

    def test_add_node_raises_error_for_duplicate_node(self):
        node = Node(identifier=1, x=0, y=0, priority=0, demand=10)
        graph = Graph(nodes=[])
        graph.add_node(node)
        with pytest.raises(ValueError, match="Vertex Node.*already exists."):
            graph.add_node(node)

    def test_get_node_returns_correct_node(self):
        node = Node(identifier=1, x=0, y=0, priority=0, demand=10)
        graph = Graph(nodes=[node])
        result = graph.get_node(1)
        self.assertEqual(result, node)

    def test_get_node_raises_error_for_nonexistent_node(self):
        graph = Graph(nodes=[])
        with pytest.raises(ValueError, match="Node 1 does not exist."):
            graph.get_node(1)

    def test_get_edge_raises_error_for_nonexistent_edge(self):
        node1 = Node(identifier=1, x=0, y=0, priority=0, demand=10)
        node2 = Node(identifier=2, x=3, y=4, priority=0, demand=20)
        graph = Graph(nodes=[node1])
        with pytest.raises(ValueError, match="Edge from Node.*to Node.*does not exist."):
            graph.get_edge(node1, node2)

    def test_contains_returns_true_for_existing_node(self):
        node = Node(identifier=1, x=0, y=0, priority=0, demand=10)
        graph = Graph(nodes=[node])
        self.assertTrue(node in graph)

    def test_contains_returns_false_for_nonexistent_node(self):
        node = Node(identifier=1, x=0, y=0, priority=0, demand=10)
        graph = Graph(nodes=[])
        self.assertFalse(node in graph)

    def test_get_edge_toll_by_node_id_returns_correct_toll(self):
        node1 = Node(identifier=1, x=0, y=0, priority=0, demand=10)
        node2 = Node(identifier=2, x=3, y=4, priority=0, demand=20)
        edge = Edge(from_node=node1, to_node=node2, distance=2400)
        graph = Graph(nodes=[])
        graph.add_edge(edge)
        toll = graph.get_edge_toll_by_node_id(1, 2)
        self.assertEqual(toll, 15)
