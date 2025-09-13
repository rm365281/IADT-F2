from unittest import TestCase
from unittest.mock import Mock

from domain.graph import Node
from genetic_algorithm.fitness import Fitness


class TestFitness(TestCase):

    fitness = Fitness()

    def test_calculates_priority_violation_penalty(self):
        vehicle = Mock()
        vehicle.customers.return_value = [0, 1, 2]
        vehicles = [vehicle]

        graph = Mock()
        graph.get_node.side_effect = [
            Node(identifier=0, x=0, y=0, priority=0),
            Node(identifier=0, x=0, y=0, priority=0),
            Node(identifier=1, x=1, y=1, priority=0),
            Node(identifier=0, x=0, y=0, priority=0),
            Node(identifier=2, x=2, y=2, priority=1),
            Node(identifier=0, x=0, y=0, priority=0),
        ]
        fitness = Fitness(graph)

        result = fitness.calculate_priority_violation_penality(vehicles)
        assert result == 50

    def test_calculate_tolls_penality(self):
        graph = Mock()
        graph.get_edge_toll_by_node_id = Mock(side_effect=lambda from_id, to_id: {
            (0, 1): 2,
            (1, 2): 3,
            (2, 0): 4
        }.get((from_id, to_id), 0))

        fitness = Fitness(graph)

        vehicle1 = Mock()
        vehicle1.customers = Mock(return_value=[0, 1, 2, 0])

        vehicle2 = Mock()
        vehicle2.customers = Mock(return_value=[0, 2, 0])

        vehicles = [vehicle1, vehicle2]

        total_tolls_penalty = fitness.calculate_tolls_penality(vehicles)

        expected_penalty = (2 + 3 + 4 + 4) * 5

        assert total_tolls_penalty == expected_penalty

    def test_vehicle_unbalanced_distance_penality(self):
        vehicles = [Mock(distance=Mock(return_value=100)), Mock(distance=Mock(return_value=300)), Mock(distance=Mock(return_value=500))]
        penalty = self.fitness.calculate_vehicle_unbalanced_distance_penality(vehicles)
        expected_penalty = 300 - 100 + 500 - 300
        assert penalty == expected_penalty