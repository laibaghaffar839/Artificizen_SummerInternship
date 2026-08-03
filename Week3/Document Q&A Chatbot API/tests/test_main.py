from fastapi.testclient import TestClient
from unittest.mock import patch
import main

client = TestClient(main.app)


# 1. Test document ingestion
def test_ingest_sample_file():

    sample_text = """
    Our company was founded in 2020.
    The company provides e-commerce solutions.
    """

    with patch(
        "main.load_document",
        return_value=sample_text
    ), patch(
        "main.generate_embeddings",
        return_value=[
            [0.1] * 384
        ]
    ), patch(
        "main.store_chunks"
    ) as mock_store:

        response = client.post(
            "/ingest",
            files={
                "file": (
                    "sample.txt",
                    sample_text,
                    "text/plain"
                )
            }
        )

    assert response.status_code == 200
    assert response.json()["filename"] == "sample.txt"
    assert response.json()["chunks"] > 0
    mock_store.assert_called_once()


# 2. Test known question
def test_known_question():

    main.query_cache.clear()
    main.conversation_history.clear()

    with patch(
        "main.generate_query_embedding",
        return_value=[0.1] * 384
    ), patch(
        "main.search_similar_chunks"
    ) as mock_search, patch(
        "main.generate_answer",
        return_value="The company was founded in 2020."
    ):

        mock_result = type(
            "Result",
            (),
            {
                "payload": {
                    "text": "Our company was founded in 2020.",
                    "source": "sample.txt",
                    "chunk_index": 0
                }
            }
        )()

        mock_search.return_value = [mock_result]

        response = client.post(
            "/chat",
            json={
                "session_id": "test-session-1",
                "query": "When was the company founded?"
            }
        )

    assert response.status_code == 200
    assert "2020" in response.json()["answer"]


# 3. Test unknown question
def test_unknown_question():

    main.query_cache.clear()
    main.conversation_history.clear()

    with patch(
        "main.generate_query_embedding",
        return_value=[0.1] * 384
    ), patch(
        "main.search_similar_chunks"
    ) as mock_search, patch(
        "main.generate_answer",
        return_value="I don't know."
    ):

        mock_result = type(
            "Result",
            (),
            {
                "payload": {
                    "text": "Our company was founded in 2020.",
                    "source": "sample.txt",
                    "chunk_index": 0
                }
            }
        )()

        mock_search.return_value = [mock_result]

        response = client.post(
            "/chat",
            json={
                "session_id": "test-session-2",
                "query": "What is the company's CEO's favorite color?"
            }
        )

    assert response.status_code == 200
    assert response.json()["answer"] == "I don't know."


# 4. Test sources are returned
def test_sources_returned():

    main.query_cache.clear()
    main.conversation_history.clear()

    with patch(
        "main.generate_query_embedding",
        return_value=[0.1] * 384
    ), patch(
        "main.search_similar_chunks"
    ) as mock_search, patch(
        "main.generate_answer",
        return_value="The company was founded in 2020."
    ):

        mock_result = type(
            "Result",
            (),
            {
                "payload": {
                    "text": "Our company was founded in 2020.",
                    "source": "sample.txt",
                    "chunk_index": 0
                }
            }
        )()

        mock_search.return_value = [mock_result]

        response = client.post(
            "/chat",
            json={
                "session_id": "test-session-3",
                "query": "When was the company founded?"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert "sources" in data
    assert len(data["sources"]) > 0
    assert data["sources"][0]["source"] == "sample.txt"
    assert data["sources"][0]["chunk_index"] == 0


# 5. Test query cache
def test_cache_hit():

    main.query_cache.clear()
    main.conversation_history.clear()

    with patch(
        "main.generate_query_embedding",
        return_value=[0.1] * 384
    ), patch(
        "main.search_similar_chunks"
    ) as mock_search, patch(
        "main.generate_answer",
        return_value="The company was founded in 2020."
    ) as mock_generate:

        mock_result = type(
            "Result",
            (),
            {
                "payload": {
                    "text": "Our company was founded in 2020.",
                    "source": "sample.txt",
                    "chunk_index": 0
                }
            }
        )()

        mock_search.return_value = [mock_result]

        request_data = {
            "session_id": "cache-session",
            "query": "When was the company founded?"
        }

        # First request
        response1 = client.post(
            "/chat",
            json=request_data
        )

        # Second identical request
        response2 = client.post(
            "/chat",
            json=request_data
        )

    assert response1.status_code == 200
    assert response2.status_code == 200

    assert response1.json() == response2.json()

    # Groq should be called only once
    assert mock_generate.call_count == 1