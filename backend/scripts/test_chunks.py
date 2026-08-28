from pathlib import Path

from app.knowledge.loader import load_transcript
from app.knowledge.cleaner import clean_document
from app.knowledge.chunker import chunk_document


PROJECT_ROOT = Path(__file__).resolve().parents[2]

FILE = (
    PROJECT_ROOT
    / "data"
    / "lenny-transcripts"
    / "episodes"
    / "ada-chen-rekhi"
    / "transcript.md"
)


def main():

    document = load_transcript(FILE)

    document = clean_document(document)

    chunks = chunk_document(document)

    print(f"Episode: {document.title}")
    print(f"Guest: {document.guest}")
    print(f"Turns: {len(document.turns)}")
    print(f"Chunks: {len(chunks)}")

    print("\n=== FIRST CHUNK ===")

    chunk = chunks[0]

    print(f"Chunk index: {chunk.chunk_index}")
    print(f"Start: {chunk.start_timestamp}")
    print(f"End: {chunk.end_timestamp}")
    print(f"Guest: {chunk.guest}")

    print("\nText:")
    print(chunk.text)


if __name__ == "__main__":
    main()