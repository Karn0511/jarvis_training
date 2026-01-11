from fastapi.testclient import TestClient
from web_server import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    # It might return 200 (FileResponse) or 503 (JSON) depending on frontend build
    assert response.status_code in [200, 503]


def test_api_state_endpoint():
    response = client.get("/api/state")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
