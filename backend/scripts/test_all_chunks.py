from pathlib import Path

from app.knowledge.loader import load_transcript
from app.knowledge.cleaner import clean_document
from app.knowledge.chunker import chunk_document


PROJECT_ROOT = Path(__file__).resolve().parents[2]

EPISODES_DIR = (
    PROJECT_ROOT
    / "data"
    / "lenny-transcripts"
    / "episodes"
)


def main():

    files = list(
        EPISODES_DIR.glob("*/transcript.md")
    )

    print(
        f"Found {len(files)} transcripts"
    )

    successful = 0
    failed = 0
    total_chunks = 0

    for index, filepath in enumerate(
        files,
        start=1,
    ):

        try:

            document = load_transcript(
                filepath
            )

            document = clean_document(
                document
            )

            chunks = chunk_document(
                document
            )

            if not chunks:
                raise ValueError(
                    "No chunks generated"
                )

            total_chunks += len(chunks)

            successful += 1

        except Exception as e:

            failed += 1

            print(
                f"\nFAILED: {filepath}"
            )

            print(
                f"Reason: {e}"
            )

    print("\n============================")
    print("Chunking complete")
    print(
        f"Transcripts: {len(files)}"
    )
    print(
        f"Successful:  {successful}"
    )
    print(
        f"Failed:      {failed}"
    )
    print(
        f"Total chunks: {total_chunks}"
    )
    print("============================")


if __name__ == "__main__":
    main()