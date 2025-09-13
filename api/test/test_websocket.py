import pytest
from fastapi.testclient import TestClient
from api.websocket import app

client = TestClient(app)

def test_websocket_connection_accepts_and_closes():
    with client.websocket_connect("/ws/genetic") as websocket:
        websocket.send_json({"command": "start"})
        data = websocket.receive_json()
        assert data["event"] == "started"
        websocket.send_json({"command": "stop"})
        # Consome eventos até encontrar 'stopped'
        for _ in range(5):
            data = websocket.receive_json()
            if data["event"] == "stopped":
                break
        assert data["event"] == "stopped"

def test_websocket_returns_status_and_best_solution():
    with client.websocket_connect("/ws/genetic") as websocket:
        websocket.send_json({"command": "status"})
        data = websocket.receive_json()
        assert data["event"] == "status"
        websocket.send_json({"command": "get_best_solution"})
        data = websocket.receive_json()
        assert data["event"] == "best_solution"
        assert "solution" in data

def test_websocket_handles_pause_and_resume():
    with client.websocket_connect("/ws/genetic") as websocket:
        websocket.send_json({"command": "pause"})
        data = websocket.receive_json()
        assert data["event"] == "paused"
        websocket.send_json({"command": "resume"})
        data = websocket.receive_json()
        assert data["event"] == "resumed"

def test_websocket_ignores_unknown_command():
    with client.websocket_connect("/ws/genetic") as websocket:
        websocket.send_json({"command": "unknown_command"})
        # Should not raise, may not respond
        # Optionally, check for no response or error handling
