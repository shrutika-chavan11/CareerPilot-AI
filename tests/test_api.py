import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_health(client):
    r=client.get("/health")
    assert r.status_code==200 and r.json()["status"]=="ok"

def test_jobs(client):
    r=client.get("/jobs")
    assert r.status_code==200 and isinstance(r.json(),list) and len(r.json())>0

def test_search(client):
    r=client.post("/search",json={"query":"Python backend internship","top_k":3})
    assert r.status_code==200 and isinstance(r.json(),list)
