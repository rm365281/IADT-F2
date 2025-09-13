import itertools
import random

from fastapi import FastAPI, WebSocket

from domain.graph import Graph, Node
from genetic_algorithm import default_problems, GeneticAlgorithmRunner
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
