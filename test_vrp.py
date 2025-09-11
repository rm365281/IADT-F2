from unittest import TestCase

from graph import Graph, Node
from itinerary import Itinerary
from solution import Solution
from vehicle import Vehicle
from vrp import VRP


class TestVRP(TestCase):
    graph = Graph()
    graph.add_node(Node(identifier=0, x=0, y=0))  # Depot

    vrp = VRP(graph=graph, population_size=1, mutation_probability=1, number_vehicles=2, vehicle_autonomy=100)

    def test_mutate(self):
        vehicles = [Vehicle(depot_id=0, capacity=10, itinerary=Itinerary([0,0,0]), autonomy=1),
                    Vehicle(depot_id=0, capacity=10, itinerary=Itinerary([0,0,0]), autonomy=1)]
        solution = Solution(vehicles=vehicles)

        mutated_solution = self.vrp.mutate(solution)
        self.assertEqual([0], mutated_solution.vehicles[0].customers())
