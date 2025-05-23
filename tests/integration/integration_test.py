import pytest
from app.services.query_service import latest_relevant_chunks

@pytest.fixture(autouse=True)
def clear_hits():
    latest_relevant_chunks.clear()
    yield
    latest_relevant_chunks.clear()

def test_query_endpoint(client, monkeypatch):
    # Arrange: stub process_query
    fake_response = {
        "answer": "OK",
        "sources": [{"source": "f.txt", "page": 2}],
        "relevant_chunks": [{"text":"t","source":"f.txt","page":2,"chunk_id":0,"score":0.1}]
    }
    monkeypatch.setattr(
        "app.routes.queries.QueryService.process_query",
        lambda self, q: fake_response
    )

    # Act
    resp = client.post("/api/v1/query/query", json={"query": "test"})

    # Assert
    assert resp.status_code == 200
    body = resp.json()
    assert body["answer"] == "OK"
    assert body["sources"] == fake_response["sources"]
    assert body["relevant_chunks"] == fake_response["relevant_chunks"]

def test_metadata_endpoint(client):
    # Arrange: populate latest_relevant_chunks
    latest_relevant_chunks.extend([
        {"text":"c1","source":"s1","page":1,"chunk_id":0,"score":0.2},
        {"text":"c2","source":"s2","page":3,"chunk_id":1,"score":0.5}
    ])

    # Act
    resp = client.post("/api/v1/query/metadata")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "metadata" in data
    assert len(data["metadata"]) == 2
    first = data["metadata"][0]
    assert first == {
        "source": "s1",
        "page": 1,
        "chunk_id": 0,
        "score": 0.2,
        "text": "c1"
    }