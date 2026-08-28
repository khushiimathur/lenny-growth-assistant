from pathlib import Path

import chromadb

from app.knowledge.document import TranscriptChunk


PROJECT_ROOT = Path(__file__).resolve().parents[3]

VECTOR_STORE_PATH = (
    PROJECT_ROOT / "data" / "vector_store"
)


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=str(VECTOR_STORE_PATH)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="lenny_transcripts"
            )
        )

    def add_chunks(
        self,
        chunks: list[TranscriptChunk],
        embeddings: list[list[float]],
    ):

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:

            chunk_id = (
                f"{chunk.video_id}_{chunk.chunk_index}"
            )

            ids.append(chunk_id)

            documents.append(chunk.text)

            metadatas.append(
                {
                    "title": chunk.title,
                    "guest": chunk.guest,
                    "youtube_url": chunk.youtube_url or "",
                    "video_id": chunk.video_id or "",
                    "publish_date": str(chunk.publish_date or ""),
                    "start_timestamp": chunk.start_timestamp,
                    "end_timestamp": chunk.end_timestamp,
                    "chunk_index": chunk.chunk_index,
                }
            )

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ):

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )