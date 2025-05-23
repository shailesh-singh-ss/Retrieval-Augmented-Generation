import pytest
from unittest.mock import patch
from app.services.query_service import QueryService, latest_relevant_chunks

@pytest.fixture(autouse=True)
def clear_global_hits():
    # Ensure latest_relevant_chunks is cleared before each test
    latest_relevant_chunks.clear()
    yield
    latest_relevant_chunks.clear()

@patch.object(QueryService, 'generate_response', autospec=True)
@patch.object(QueryService, 'chroma_db', autospec=True)
@patch.object(QueryService, 'embedding_model', autospec=True)
def test_process_query_flow(mock_embed_model, mock_chroma_db, mock_llm, monkeypatch):
    # Arrange
    query = "hello world"
    fake_embedding = [0.1, 0.2]
    mock_embed_model.generate_embeddings.return_value = [fake_embedding]
    
    fake_docs = [
        {
            "text": "chunk1",
            "source": "file1.txt",
            "page": 1,
            "chunk_id": 0,
            "score": 0.42
        }
    ]
    mock_chroma_db.retrieve_documents.return_value = fake_docs

    # patch GeminiLLM.generate_response
    from app.services.query_service import GeminiLLM
    mock_llm.generate_response.return_value = "ANSWER"

    svc = QueryService()
    svc.embedding_model = mock_embed_model
    svc.chroma_db = mock_chroma_db
    svc.llm = mock_llm

    # Act
    result = pytest.run(svc.process_query(query)) if hasattr(pytest, 'run') else svc.process_query(query)
    # In async context
    if hasattr(result, '__await__'):
        import asyncio
        result = asyncio.get_event_loop().run_until_complete(result)

    # Assert structure
    assert result["answer"] == "ANSWER"
    assert isinstance(result["sources"], list)
    assert result["sources"][0] == {"source": "file1.txt", "page": 1}
    assert result["relevant_chunks"] == fake_docs

    # ensure global latest_relevant_chunks was updated
    assert latest_relevant_chunks == fake_docs