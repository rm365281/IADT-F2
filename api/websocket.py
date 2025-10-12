import random

from fastapi import FastAPI, WebSocket

from domain.graph import Graph, Node
from genetic_algorithm import GeneticAlgorithmRunner, default_problems
from vrp.vrp_builder import VrpFactory

cities_locations = default_problems[15]
nodes: list[Node] = [Node(identifier=i, x=city[0], y=city[1], priority=random.randint(0, 1), demand=random.randint(1,11)) for i, city in enumerate(cities_locations)]

app = FastAPI()

async def handle_start_command(data, send_event, websocket):
    population_size = data.get("population_size", 100)
    number_vehicles = data.get("number_vehicles", 2)
    mutation_probability = data.get("mutation_probability", 0.5)
    vehicle_autonomy = data.get("vehicle_autonomy", 600)
    vehicle_capacity = data.get("vehicle_capacity", 20)
    crossover_probability = data.get("crossover_probability", 1.0)

    cities = data.get("cities")
    if cities:
        try:
            nodes_from_client = [
                Node(
                    identifier=city["identifier"],
                    x=city["x"],
                    y=city["y"],
                    priority=city.get("priority", 0),
                    demand=city.get("demand", 1),
                    name=city.get("name")
                )
                for city in cities
            ]
            g = Graph(nodes_from_client)
        except Exception as e:
            await websocket.send_json({"event": "error", "message": f"Erro ao processar cidades: {str(e)}"})
            return None
    else:
        nodes_from_client = None
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
        return runner, nodes_from_client if nodes_from_client else nodes
    except ValueError as e:
        await websocket.send_json({"event": "error", "message": str(e)})
        return None, None

@app.websocket("/ws/genetic")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for managing the genetic algorithm for solving the Vehicle Routing Problem (VRP).
    Args:
        websocket: The WebSocket connection.

    Returns:
        None
    Raises:
        ValueError: If the provided parameters are invalid.

    """
    await websocket.accept()

    runner = None
    node_list = None

    async def send_event_with_nodes(event: dict):
        if event.get("event") == "new_best_solution" and runner and node_list:
            customer_id_to_node = {n.identifier: n for n in node_list}
            solution_obj = runner.best_solution
            event["solution"] = solution_obj.to_dict(customer_id_to_node=customer_id_to_node) if solution_obj else None
        await websocket.send_json(event)

    try:
        while True:
            data = await websocket.receive_json()
            command = data.get("command")

            if command == "start":
                runner, node_list = await handle_start_command(data, send_event_with_nodes, websocket)
            elif command == "pause" and runner:
                await runner.pause()
                await websocket.send_json({"event": "paused"})
            elif command == "resume" and runner:
                await runner.resume()
                await websocket.send_json({"event": "resumed"})
            elif command == "stop" and runner:
                customer_id_to_node = {n.identifier: n for n in node_list} if node_list else {}
                solution_obj = runner.best_solution
                solution = solution_obj.to_dict(customer_id_to_node=customer_id_to_node) if solution_obj else None
                await runner.stop()
                await websocket.send_json({
                    "event": "stopped",
                    "solution": solution
                })
            elif command == "status" and runner:
                customer_id_to_node = {n.identifier: n for n in node_list} if node_list else {}
                status = runner.status()
                solution_obj = runner.best_solution
                status["best_solution"] = solution_obj.to_dict(customer_id_to_node=customer_id_to_node) if solution_obj else None
                await websocket.send_json({"event": "status", **status})
            elif command == "get_best_solution" and runner:
                customer_id_to_node = {n.identifier: n for n in node_list} if node_list else {}
                solution_obj = runner.best_solution
                solution = solution_obj.to_dict(customer_id_to_node=customer_id_to_node) if solution_obj else None
                await websocket.send_json({
                    "event": "best_solution",
                    "solution": solution
                })
    except Exception:
        if runner:
            await runner.stop()
