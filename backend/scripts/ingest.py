from pathlib import Path

from app.knowledge.loader import load_transcript
from app.knowledge.cleaner import clean_document
from app.knowledge.chunker import chunk_document
from app.knowledge.embeddings import EmbeddingModel
from app.knowledge.vector_store import VectorStore


PROJECT_ROOT = Path(__file__).resolve().parents[2]

EPISODES_DIR = (
    PROJECT_ROOT
    / "data"
    / "lenny-transcripts"
    / "episodes"
)


def main():

    transcript_files = list(
        EPISODES_DIR.glob("*/transcript.md")
    )

    print(
        f"Found {len(transcript_files)} transcripts"
    )

    embedding_model = EmbeddingModel()
    vector_store = VectorStore()

    total_chunks = 0

    for index, filepath in enumerate(
        transcript_files,
        start=1,
    ):

        print(
            f"[{index}/{len(transcript_files)}] "
            f"{filepath.parent.name}"
        )

        document = load_transcript(filepath)

        document = clean_document(document)

        chunks = chunk_document(document)

        texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = (
            embedding_model.embed_texts(texts)
        )

        vector_store.add_chunks(
            chunks,
            embeddings,
        )

        total_chunks += len(chunks)

    print("\n========================")
    print("Ingestion complete")
    print(f"Transcripts: {len(transcript_files)}")
    print(f"Chunks:      {total_chunks}")
    print("========================")


if __name__ == "__main__":
    main()