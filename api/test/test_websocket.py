from fastapi.testclient import TestClient

from api.websocket import app

client = TestClient(app)

def receive_until(websocket, expected_event, timeout=5, max_events=50):
    import time
    start = time.time()
    for _ in range(max_events):
        if time.time() - start > timeout:
            raise TimeoutError(f"Timeout esperando pelo evento '{expected_event}'")
        data = websocket.receive_json()
        if data["event"] == expected_event:
            return data
    raise TimeoutError(f"Evento '{expected_event}' não recebido após {max_events} eventos")

def test_websocket_connection_accepts_and_closes():
    with client.websocket_connect("/ws/genetic") as websocket:
        websocket.send_json({"command": "start"})
        data = receive_until(websocket, "started")
        assert data["event"] == "started"
        websocket.send_json({"command": "stop"})
        data = receive_until(websocket, "stopped")
        assert data["event"] == "stopped"

def test_websocket_returns_status_and_best_solution():
    with client.websocket_connect("/ws/genetic") as websocket:
        websocket.send_json({"command": "start"})
        data = receive_until(websocket, "started")
        assert data["event"] == "started"
        websocket.send_json({"command": "status"})
        data = receive_until(websocket, "status")
        assert data["event"] == "status"
        websocket.send_json({"command": "get_best_solution"})
        data = receive_until(websocket, "best_solution")
        assert data["event"] == "best_solution"
        assert "solution" in data

def test_websocket_handles_pause_and_resume():
    with client.websocket_connect("/ws/genetic") as websocket:
        websocket.send_json({"command": "start"})
        data = receive_until(websocket, "started")
        assert data["event"] == "started"
        websocket.send_json({"command": "pause"})
        data = receive_until(websocket, "paused")
        assert data["event"] == "paused"
        websocket.send_json({"command": "resume"})
        data = receive_until(websocket, "resumed")
        assert data["event"] == "resumed"

def test_websocket_ignores_unknown_command():
    with client.websocket_connect("/ws/genetic") as websocket:
        websocket.send_json({"command": "start"})
        data = websocket.receive_json()
        assert data["event"] == "started"
        websocket.send_json({"command": "unknown_command"})

def test_websocket_start_with_invalid_capacity():
    with client.websocket_connect("/ws/genetic") as websocket:
        websocket.send_json({"command": "start", "vehicle_capacity": 0})
        data = websocket.receive_json()
        assert data["event"] == "error"
        assert "exceeds vehicle capacity" in data["message"]
