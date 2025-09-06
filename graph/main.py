import math
import random
from turtle import distance
from node import Node
from edge import Edge
from graph import Graph

cities_locations = [(512, 317), (741, 72), (552, 50), (772, 346), (637, 12), (589, 131), (732, 165), (605, 15), (730, 38), (576, 216), (589, 381), (711, 387), (563, 228), (494, 22), (787, 288)]
nodes: list[Node] = [Node(id=i, x=city[0], y=city[1]) for i, city in enumerate(cities_locations)]

g = Graph()
for node in nodes:
    g.add_node(node)

for from_node in nodes:
    for to_node in nodes:
        if from_node != to_node:
            distance: float = math.hypot(from_node.x - to_node.x, from_node.y - to_node.y)
            edge = Edge(from_node=from_node, to_node=to_node, distance=distance)
            g.add_edge(edge)

depot = g.get_node(0)
print(depot)

print(g.get_edges())

population: list[list[Node]] = list()

# Gera a população inicial de forma aleatória
population = [random.sample(nodes, len(nodes)) for _ in range(100)]
print(population)

# Calcula o fitness de cada indivíduo na população
population_fitness = []
for individual in population:
    distance = 0
    for i in range(len(individual)):
        distance += g.get_edge(individual[i], individual[(i + 1) % len(individual)]).distance
    population_fitness.append(distance)

print(population_fitness)