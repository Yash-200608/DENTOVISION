from fastapi.testclient import TestClient
from dentovision.api.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_predict_endpoint_no_file():
    response = client.post("/predict")
    assert response.status_code == 422 # Unprocessable Entity

def test_predict_endpoint_invalid_file():
    response = client.post(
        "/predict", 
        files={"file": ("test.txt", b"not an image", "text/plain")}
    )
    assert response.status_code == 400
    assert "error" in response.json()
