from app.knowledge.embeddings import EmbeddingModel


def test_embedding():

    model = EmbeddingModel()

    vector = model.embed_text(
        "How do I improve product adoption?"
    )

    assert isinstance(vector, list)

    assert len(vector) > 0

    assert all(
        isinstance(value, float)
        for value in vector
    )