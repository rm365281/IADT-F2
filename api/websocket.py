import random

from fastapi import FastAPI, WebSocket

from domain.graph import Graph, Node
from genetic_algorithm import GeneticAlgorithmRunner, default_problems
from vrp.vrp_builder import VrpFactory

cities_locations = default_problems[15]
nodes: list[Node] = [Node(identifier=i, x=city[0], y=city[1], priority=random.randint(0, 1), demand=random.randint(1,11)) for i, city in enumerate(cities_locations)]

app = FastAPI()

@app.websocket("/ws/genetic")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    async def send_event(event: dict):
        await websocket.send_json(event)

    runner = None

    try:
        while True:
            data = await websocket.receive_json()
            command = data.get("command")

            if command == "start":
                population_size = data.get("population_size", 100)
                number_vehicles = data.get("number_vehicles", 2)
                mutation_probability = data.get("mutation_probability", 0.5)
                vehicle_autonomy = data.get("vehicle_autonomy", 600)
                vehicle_capacity = data.get("vehicle_capacity", 20)
                crossover_probability = data.get("crossover_probability", 1.0)

                g = Graph(nodes)
                try:
                    vrp_factory = VrpFactory(
                        g,
                        population_size,
                        number_vehicles,
                        mutation_probability,
                        vehicle_autonomy,
                        vehicle_capacity,
                        crossover_probability
                    )
                    runner = GeneticAlgorithmRunner(
                        vrp_factory,
                        population_size,
                        on_new_best_solution=send_event
                    )
                    await runner.start()
                    await websocket.send_json({"event": "started"})
                except ValueError as e:
                    await websocket.send_json({"event": "error", "message": str(e)})
            elif command == "pause" and runner:
                await runner.pause()
                await websocket.send_json({"event": "paused"})
            elif command == "resume" and runner:
                await runner.resume()
                await websocket.send_json({"event": "resumed"})
            elif command == "stop" and runner:
                solution = runner.status()["best_solution"]
                await runner.stop()
                await websocket.send_json({
                    "event": "stopped",
                    "solution": solution
                })
            elif command == "status" and runner:
                await websocket.send_json({"event": "status", **runner.status()})
            elif command == "get_best_solution" and runner:
                await websocket.send_json({
                    "event": "best_solution",
                    "solution": runner.status()["best_solution"]
                })
    except Exception:
        if runner:
            await runner.stop()
