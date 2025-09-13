from unittest import TestCase
from domain.graph import Node, Graph
from genetic_algorithm import default_problems
from genetic_algorithm.initial_population import InitialPopulationGenerator


class TestInitialPopulationGenerator(TestCase):
    POPULATION_SIZE = 100
    NUMBER_VEHICLES = 2
    MUTATION_PROBABILITY = 1
    VEHICLE_AUTONOMY = 600
    VEHICLE_CAPACITY = 20

    cities_locations = default_problems[15]
    nodes: list[Node] = [Node(identifier=i, x=city[0], y=city[1], priority=0, demand=1) for i, city in
                         enumerate(cities_locations)]
    g = Graph(nodes)

    initialPopulationGenerator = InitialPopulationGenerator(g, POPULATION_SIZE, NUMBER_VEHICLES, MUTATION_PROBABILITY, VEHICLE_AUTONOMY, VEHICLE_CAPACITY)

    def test_generate_initial_population(self):
        population = self.initialPopulationGenerator.generate()

        self.assertEqual(len(population), self.POPULATION_SIZE)
        for individual in population:
            self.assertIsNotNone(individual)
            self.assertEqual(len(individual.flatten_routes()), 18)
            self.assertTrue(len(individual.vehicles) <= self.NUMBER_VEHICLES)
            self.assertEqual(0, individual.flatten_routes()[0])
            self.assertEqual(0, individual.flatten_routes()[-1])
