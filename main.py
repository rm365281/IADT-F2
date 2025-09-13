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

import asyncio
import copy
import itertools
import random
import time

import uvicorn
from fastapi import FastAPI, WebSocket

from genetic_algorithm import default_problems
from graph import Graph
from graph import Node
from solution import Solution
from vrp.selection import parents_selection
from vrp.vrp_builder import VrpFactory

STOP_GENERATION = False
NUMBER_VEHICLES = 2
POPULATION_SIZE = 100
MUTATION_PROBABILITY = 1
VEHICLE_AUTONOMY = 600
VEHICLE_CAPACITY = 20

cities_locations = default_problems[15]
nodes: list[Node] = [Node(identifier=i, x=city[0], y=city[1], priority=random.randint(0, 1), demand=random.randint(1,11)) for i, city in enumerate(cities_locations)]

g = Graph(nodes)

generation_counter = itertools.count(start=1)

vrp_factory = VrpFactory(g, POPULATION_SIZE, NUMBER_VEHICLES, MUTATION_PROBABILITY, VEHICLE_AUTONOMY, VEHICLE_CAPACITY)

vrp = vrp_factory.create_vrp()

population: list[Solution] = vrp.generate_initial_population()

app = FastAPI()

# Variáveis globais para controle do algoritmo
algorithm_running = False
algorithm_paused = False
websocket_client = None

best_solution: Solution = None

async def genetic_algorithm_loop():
    global algorithm_running, algorithm_paused, best_solution, population, vrp, generation_counter
    start_time = time.time()
    while algorithm_running:
        if algorithm_paused:
            await asyncio.sleep(0.1)
            continue
        generation_start = time.time()
        generation = next(generation_counter)

        for individual in population:
            vrp.fitness(individual)

        population = vrp.sort_population(population=population)

        generation_time = time.time() - generation_start
        total_time = time.time() - start_time

        if best_solution is None or best_solution.fitness > population[0].fitness:
            best_solution = population[0]
            if websocket_client:
                await websocket_client.send_json({
                    "event": "new_best_solution",
                    "generation": generation,
                    "best_distance": round(best_solution.total_distance(), 2),
                    "best_fitness": round(best_solution.fitness, 2),
                    "generation_time": round(generation_time, 2),
                    "total_time": round(total_time, 2),
                    "solution": str(best_solution)
                })

        new_population = [copy.deepcopy(population[0])]

        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = parents_selection(population)
            child1, child2 = vrp.crossover(parent1, parent2)
            mutated_child1 = vrp.mutate(child1)
            mutated_child2 = vrp.mutate(child2)
            new_population.extend([mutated_child1, mutated_child2])

        population = new_population
        await asyncio.sleep(0)  # Yield para o event loop

@app.websocket("/ws/genetic")
async def websocket_endpoint(websocket: WebSocket):
    global algorithm_running, algorithm_paused, websocket_client
    await websocket.accept()
    websocket_client = websocket
    try:
        while True:
            data = await websocket.receive_json()
            command = data.get("command")
            if command == "start":
                if not algorithm_running:
                    algorithm_running = True
                    algorithm_paused = False
                    asyncio.create_task(genetic_algorithm_loop())
                    await websocket.send_json({"event": "started"})
            elif command == "pause":
                algorithm_paused = True
                await websocket.send_json({"event": "paused"})
            elif command == "resume":
                algorithm_paused = False
                await websocket.send_json({"event": "resumed"})
            elif command == "stop":
                algorithm_running = False
                await websocket.send_json({"event": "stopped"})
            elif command == "status":
                await websocket.send_json({
                    "event": "status",
                    "running": algorithm_running,
                    "paused": algorithm_paused,
                    "best_solution": str(best_solution) if best_solution else None
                })
            elif command == "get_best_solution":
                await websocket.send_json({
                    "event": "best_solution",
                    "solution": str(best_solution) if best_solution else None
                })
    except Exception:
        algorithm_running = False
        websocket_client = None

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
