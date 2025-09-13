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

import uvicorn
from fastapi import FastAPI, WebSocket

from genetic_algorithm import default_problems
from genetic_algorithm.genetic_runner import GeneticAlgorithmRunner
from domain.graph import Graph
from domain.graph import Node
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

app = FastAPI()

@app.websocket("/ws/genetic")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    async def send_event(event: dict):
        await websocket.send_json(event)

    runner = GeneticAlgorithmRunner(vrp_factory, POPULATION_SIZE, on_new_best_solution=send_event)

    try:
        while True:
            data = await websocket.receive_json()
            command = data.get("command")

            if command == "start":
                await runner.start()
                await websocket.send_json({"event": "started"})
            elif command == "pause":
                await runner.pause()
                await websocket.send_json({"event": "paused"})
            elif command == "resume":
                await runner.resume()
                await websocket.send_json({"event": "resumed"})
            elif command == "stop":
                await runner.stop()
                await websocket.send_json({"event": "stopped"})
            elif command == "status":
                await websocket.send_json({"event": "status", **runner.status()})
            elif command == "get_best_solution":
                await websocket.send_json({
                    "event": "best_solution",
                    "solution": runner.status()["best_solution"]
                })
    except Exception:
        await runner.stop()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
