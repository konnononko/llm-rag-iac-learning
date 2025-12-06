from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_rag_query_returns_answer():
    # Arrange
    payload = {"query": "テストクエリ"}

    # Act
    response = client.post("/rag/query", json=payload)

    # Assert
    assert response.status_code == 200

    data = response.json()
    # RAGResponse(answer: str) の形になっていること
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert data["answer"] != ""


def test_rag_query_requires_query_field():
    # query フィールドがない場合は 422 (Unprocessable Entity) になることの確認
    response = client.post("/rag/query", json={})
    assert response.status_code == 422
