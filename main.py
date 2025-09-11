# Restrições
#
# 1 - Prioridade diferente para entregas (medicamentos criticos vs entrega regulares) | 1 ou 0 - ok
# 2 - Capacidade do veiculo - ok
# 3 - Autonomia (distancia máxima percorrida) - nok
# 4 - Multiplos veiculos - ok

# Restrições extras implementadas
# Equilibrar a distancia percorrida por cada veiculo - ok

# Restrições extras (opcionais)
# Custos operacionais (pedágios) - Maybe - Definir 1 pedagio a cada 50km, pune a cada pedagio presente no trajeto entre dois pontos - ok
# Restrições de rota (ex: evitar certas ruas, zonas de baixa emissão) - Maybe

# Ideias
# Visualização do mapa com rotas reais
# Diferentes tipos de veiculos (motos, carros, caminhões)
# Diferentes capacidades e custos dos veiculos
# Usar cidadades reais
# Analisar o melhor veiculo para entregar a carga (ex: motos para entregas pequenas e rápidas, caminhões para cargas maiores)
# Centro de distribuição, a carga vai até o centro e depois é distribuida pelos veiculos menores
# Informar o tempo estimado de entrega
# Usuário parametrizar o problema (número de veiculos, capacidade, etc)
# Interface web
# Separar o código em frontend e backend

import itertools
import random
import time
import math
import copy
from graph import Node
from graph import Edge
from graph import Graph
from genetic_algorithm import default_problems
from solution import Solution
from vrp import VRP
from vrp.selection import parents_selection

STOP_GENERATION = False
NUMBER_VEHICLES = 2
POPULATION_SIZE = 100
MUTATION_PROBABILITY = 1
VEHICLE_AUTONOMY = 600
VEHICLE_CAPACITY = 30

cities_locations = default_problems[15]
nodes: list[Node] = [Node(identifier=i, x=city[0], y=city[1], priority=random.randint(0, 1), demand=random.randint(1,11)) for i, city in enumerate(cities_locations)]

g = Graph(nodes)

generation_counter = itertools.count(start=1)

vrp = VRP(g, POPULATION_SIZE, NUMBER_VEHICLES, MUTATION_PROBABILITY, VEHICLE_AUTONOMY, VEHICLE_CAPACITY)

population: list[Solution] = vrp.generate_initial_population()

generate = True
start_time = time.time()

best_solution: Solution = None

while generate:
    generation_start = time.time()
    generation = next(generation_counter)

    for individual in population:
        vrp.fitness(individual)

    population = vrp.sort_population(population=population)

    generation_time = time.time() - generation_start
    total_time = time.time() - start_time

    if best_solution is None or best_solution.fitness > population[0].fitness:
        best_solution = population[0]
        print(f"Generation {generation}: Best distance = {round(best_solution.total_distance(), 2)} - Best fitness: {round(best_solution.fitness, 2)} | Time: {generation_time:.2f}s | Total: {total_time:.2f}s | Solution: {best_solution}")
    
    new_population = [copy.deepcopy(population[0])]

    while len(new_population) < POPULATION_SIZE:
        parent1, parent2 = parents_selection(population)
        child = vrp.crossover(parent1, parent2)
        child = vrp.mutate(child)
        child = vrp.adjustment(child)
        new_population.append(child)

    population = new_population

    generate = not STOP_GENERATION