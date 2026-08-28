import re

from app.knowledge.document import TranscriptDocument, TranscriptTurn


INAUDIBLE_PATTERN = re.compile(
    r"\[inaudible(?:\s+[^\]]*)?\]",
    re.IGNORECASE,
)


def clean_text(text: str) -> str:
    """
    Clean the text of a single transcript turn.
    """

    # Remove [inaudible ...] markers
    text = INAUDIBLE_PATTERN.sub("", text)

    # Normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_document(
    document: TranscriptDocument,
) -> TranscriptDocument:

    cleaned_turns = []

    for turn in document.turns:

        cleaned_text = clean_text(turn.text)

        # Don't keep empty turns
        if not cleaned_text:
            continue

        cleaned_turns.append(
            TranscriptTurn(
                speaker=turn.speaker,
                timestamp=turn.timestamp,
                text=cleaned_text,
            )
        )

    document.turns = cleaned_turns

    return document