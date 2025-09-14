import pytest
from fastapi.testclient import TestClient

from api.websocket import app

client = TestClient(app)

def receive_until(websocket, expected_event, timeout=5, max_events=50):
    """
    Waits for a specific event from the websocket, with timeout and max events.
    """
    import time
    start = time.time()
    for _ in range(max_events):
        if time.time() - start > timeout:
            raise TimeoutError(f"Timeout waiting for event '{expected_event}'")
        data = websocket.receive_json()
        if data["event"] == expected_event:
            return data
    raise TimeoutError(f"Event '{expected_event}' not received after {max_events} events")

@pytest.mark.timeout(10)
def test_websocket_connection_accepts_and_closes():
    """
    Test that the websocket accepts connection, starts and stops correctly.
    """
    with client.websocket_connect("/ws/genetic") as websocket:
        websocket.send_json({"command": "start"})
        data = receive_until(websocket, "started")
        assert data["event"] == "started"
        websocket.send_json({"command": "stop"})
        data = receive_until(websocket, "stopped")
        assert data["event"] == "stopped"

@pytest.mark.timeout(10)
def test_websocket_returns_status_and_best_solution():
    """
    Test that the websocket returns status and best solution events.
    """
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

@pytest.mark.timeout(10)
def test_websocket_handles_pause_and_resume():
    """
    Test that the websocket handles pause and resume commands.
    """
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

@pytest.mark.timeout(10)
def test_websocket_ignores_unknown_command():
    """
    Test that the websocket ignores unknown commands gracefully.
    """
    with client.websocket_connect("/ws/genetic") as websocket:
        websocket.send_json({"command": "start"})
        data = receive_until(websocket, "started")
        assert data["event"] == "started"
        websocket.send_json({"command": "unknown_command"})
        # Should not raise, may not respond

@pytest.mark.timeout(10)
def test_websocket_start_with_invalid_capacity():
    """
    Test that the websocket returns error when vehicle_capacity is invalid.
    """
    with client.websocket_connect("/ws/genetic") as websocket:
        websocket.send_json({"command": "start", "vehicle_capacity": 0})
        data = websocket.receive_json()
        assert data["event"] == "error"
        assert "exceeds vehicle capacity" in data["message"]

@pytest.mark.timeout(10)
def test_websocket_multiple_connections():
    """
    Test that multiple websocket connections can be handled concurrently.
    """
    with client.websocket_connect("/ws/genetic") as ws1, client.websocket_connect("/ws/genetic") as ws2:
        ws1.send_json({"command": "start"})
        ws2.send_json({"command": "start"})
        data1 = receive_until(ws1, "started")
        data2 = receive_until(ws2, "started")
        assert data1["event"] == "started"
        assert data2["event"] == "started"
        ws1.send_json({"command": "stop"})
        ws2.send_json({"command": "stop"})
        data1 = receive_until(ws1, "stopped")
        data2 = receive_until(ws2, "stopped")
        assert data1["event"] == "stopped"
        assert data2["event"] == "stopped"
