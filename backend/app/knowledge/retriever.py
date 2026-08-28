from app.knowledge.embeddings import EmbeddingModel
from app.knowledge.vector_store import VectorStore


class Retriever:

    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):

        query_embedding = (
            self.embedding_model.embed_text(query)
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        formatted_results = []

        for i, document in enumerate(documents):

            metadata = metadatas[i]

            formatted_results.append(
                {
                    "id": ids[i],
                    "text": document,
                    "distance": distances[i],
                    "source": {
                        "title": metadata.get("title"),
                        "guest": metadata.get("guest"),
                        "youtube_url": metadata.get(
                            "youtube_url"
                        ),
                        "video_id": metadata.get(
                            "video_id"
                        ),
                        "publish_date": metadata.get(
                            "publish_date"
                        ),
                        "start_timestamp": metadata.get(
                            "start_timestamp"
                        ),
                        "end_timestamp": metadata.get(
                            "end_timestamp"
                        ),
                    },
                }
            )

        return formatted_results