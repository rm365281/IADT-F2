# Restrições
#
# 1 - Prioridade diferente para entregas (medicamentos criticos vs entrega regulares)
# 2 - Capacidade do veiculo
# 3 - Autonomia (distancia máxima percorrida)
# 4 - Multiplos veiculos
# Etc...

import itertools
from customer import Customer
from genetic_algorithm import sort_population, default_problems
from vrp import VRP

POPULATION_SIZE = 100
MUTATION_PROBABILITY = 0.5

cities_locations = default_problems[15]
customers: list[Customer] = [Customer(id=i, city=city) for i, city in enumerate(cities_locations)]

generation_counter = itertools.count(start=1)

best_fitness_values = []
best_solutions = []

vrp = VRP(customers=customers)

population = vrp.generate_initial_population(POPULATION_SIZE, 2)

while True:
    generation = next(generation_counter)

    population_fitness = [vrp.fitness(individual) for individual in population]

    population, population_fitness = sort_population(population,  population_fitness)

    best_fitness = vrp.fitness(population[0])
    best_solution = population[0]

    best_fitness_values.append(best_fitness)
    best_solutions.append(best_solution)

    print(f"Generation {generation}: Best fitness = {round(best_fitness, 2)} | Solution: {best_solution}")

    new_population = [population[0]]

    while len(new_population) < POPULATION_SIZE:
        child = vrp.crossover(population, population_fitness)
        child = vrp.mutate(child, MUTATION_PROBABILITY)
        new_population.append(child)

    population = new_population