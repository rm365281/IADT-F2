# Restrições
#
# 1 - Prioridade diferente para entregas (medicamentos criticos vs entrega regulares) | 1 ou 0
# 2 - Capacidade do veiculo
# 3 - Autonomia (distancia máxima percorrida)
# 4 - Multiplos veiculos

# Restrições extras (opcionais)
# 13 - Carga horaria do motorista (ex: limites de horas de condução)
# 8 - Restrições de rota (ex: evitar certas ruas, zonas de baixa emissão)
# 9 - Condições de trânsito em tempo real (MUITO COMPLEXO)
# 5 - Organizar as caixas dentro do veiculo de forma a aproveitar o espaço (MUITO COMPLEXO)
# 6 - Separação dos tipos de carga (refrigerados, inflamaveis, etc)
# 7 - Janelas de tempo para entrega (ex: entregar entre 14:00 e 16:00)
# 10 - Custos operacionais (ex: minimizar custos de combustível, pedágios)
# 11 - Restrições legais (ex: limites de peso, regulamentações de transporte)
# 12 - Preferências do cliente (ex: horários preferenciais de entrega)
# 14 - Pontos de combustivel (ex: incluir paradas para reabastecimento)

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
from customer import Customer
from genetic_algorithm import sort_population, default_problems
from vrp import VRP

STOP_GENERATION = False
NUMBER_VEHICLES = 2
POPULATION_SIZE = 100
MUTATION_PROBABILITY = 0.5

cities_locations = default_problems[15]
customers: list[Customer] = [Customer(id=i, city=city) for i, city in enumerate(cities_locations)]

generation_counter = itertools.count(start=1)

vrp = VRP(customers=customers)

population = vrp.generate_initial_population(POPULATION_SIZE, NUMBER_VEHICLES)

generate = True
while generate:
    generation = next(generation_counter)

    population_fitness = [vrp.fitness(individual) for individual in population]

    population, population_fitness = sort_population(population,  population_fitness)

    best_solution = population[0]
    best_fitness = best_solution.total_distance();

    print(f"Generation {generation}: Best fitness = {round(best_fitness, 2)} | Solution: {best_solution}")

    new_population = [population[0]]

    while len(new_population) < POPULATION_SIZE:
        child = vrp.crossover(population, population_fitness)
        child = vrp.mutate(child, MUTATION_PROBABILITY)
        new_population.append(child)

    population = new_population

    generate = not STOP_GENERATION