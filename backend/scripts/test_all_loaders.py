from pathlib import Path

from app.knowledge.loader import load_transcript


EPISODES_DIR = Path(
    "../data/lenny-transcripts/episodes"
)


def main():
    files = list(
        EPISODES_DIR.glob("*/transcript.md")
    )

    print(f"Found {len(files)} transcript files")

    successful = 0
    failed = 0

    for filepath in files:
        try:
            document = load_transcript(filepath)

            if not document.title:
                raise ValueError("Missing title")

            if not document.guest:
                raise ValueError("Missing guest")

            if not document.turns:
                raise ValueError("No transcript turns")

            successful += 1

        except Exception as e:
            failed += 1

            print(f"\nFAILED: {filepath}")
            print(f"Reason: {e}")

    print("\n====================")
    print(f"Successful: {successful}")
    print(f"Failed:     {failed}")
    print(f"Total:      {len(files)}")
    print("====================")


if __name__ == "__main__":
    main()