import re

from app.knowledge.document import (
    TranscriptChunk,
    TranscriptDocument,
    TranscriptTurn,
)


MAX_WORDS = 600
MIN_WORDS = 300


def word_count(text: str) -> int:
    return len(text.split())


def chunk_document(
    document: TranscriptDocument,
    max_words: int = MAX_WORDS,
) -> list[TranscriptChunk]:
    """
    Convert a TranscriptDocument into retrieval-friendly chunks.

    Handles:
    - speaker-aware transcripts
    - raw transcripts without speaker information
    - very long individual turns
    """

    if not document.turns:
        return []

    # Raw transcript fallback:
    # loader represents it as one "Unknown" turn.
    if _is_raw_transcript(document):
        return _chunk_raw_transcript(
            document,
            max_words,
        )

    # Normal speaker/timestamp transcript.
    return _chunk_structured_transcript(
        document,
        max_words,
    )


def _is_raw_transcript(
    document: TranscriptDocument,
) -> bool:
    """
    Determine whether the document came from the
    raw transcript format.
    """

    return all(
        turn.speaker == "Unknown"
        and turn.timestamp is None
        for turn in document.turns
    )


def _chunk_structured_transcript(
    document: TranscriptDocument,
    max_words: int,
) -> list[TranscriptChunk]:

    chunks = []

    current_turns: list[TranscriptTurn] = []
    current_words = 0

    chunk_index = 0

    for turn in document.turns:

        turn_words = word_count(turn.text)

        # ------------------------------------------------
        # Handle an individual turn that is too large.
        # ------------------------------------------------

        if turn_words > max_words:

            # First finish the existing chunk.
            if current_turns:

                chunks.append(
                    _create_chunk(
                        document=document,
                        turns=current_turns,
                        chunk_index=chunk_index,
                    )
                )

                chunk_index += 1

                current_turns = []
                current_words = 0

            # Split the large turn into smaller pieces.
            pieces = _split_text(
                turn.text,
                max_words,
            )

            for piece in pieces:

                chunks.append(
                    _create_chunk_from_single_text(
                        document=document,
                        text=f"{turn.speaker}: {piece}",
                        chunk_index=chunk_index,
                        start_timestamp=turn.timestamp,
                        end_timestamp=turn.timestamp,
                    )
                )

                chunk_index += 1

            continue

        # ------------------------------------------------
        # Normal turn.
        # ------------------------------------------------

        if (
            current_turns
            and current_words + turn_words > max_words
        ):
            chunks.append(
                _create_chunk(
                    document=document,
                    turns=current_turns,
                    chunk_index=chunk_index,
                )
            )

            chunk_index += 1

            current_turns = []
            current_words = 0

        current_turns.append(turn)
        current_words += turn_words

    # ----------------------------------------------------
    # Final chunk.
    # ----------------------------------------------------

    if current_turns:

        chunks.append(
            _create_chunk(
                document=document,
                turns=current_turns,
                chunk_index=chunk_index,
            )
        )

    return chunks


def _chunk_raw_transcript(
    document: TranscriptDocument,
    max_words: int,
) -> list[TranscriptChunk]:
    """
    Chunk a transcript where speaker/timestamp information
    is unavailable.

    We split primarily on paragraph boundaries and only
    split individual paragraphs if they are too large.
    """

    full_text = document.turns[0].text.strip()

    if not full_text:
        return []

    # Try to preserve paragraph boundaries.
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(
            r"\n\s*\n",
            full_text,
        )
        if paragraph.strip()
    ]

    # If the transcript was flattened into one line,
    # fall back to sentence-based splitting.
    if len(paragraphs) <= 1:

        paragraphs = _split_into_sentences(
            full_text
        )

    chunks = []

    current_parts: list[str] = []
    current_words = 0
    chunk_index = 0

    for paragraph in paragraphs:

        paragraph_words = word_count(paragraph)

        # ------------------------------------------------
        # Very large paragraph.
        # ------------------------------------------------

        if paragraph_words > max_words:

            if current_parts:

                chunks.append(
                    _create_chunk_from_single_text(
                        document=document,
                        text="\n\n".join(
                            current_parts
                        ),
                        chunk_index=chunk_index,
                        start_timestamp=None,
                        end_timestamp=None,
                    )
                )

                chunk_index += 1

                current_parts = []
                current_words = 0

            pieces = _split_text(
                paragraph,
                max_words,
            )

            for piece in pieces:

                chunks.append(
                    _create_chunk_from_single_text(
                        document=document,
                        text=piece,
                        chunk_index=chunk_index,
                        start_timestamp=None,
                        end_timestamp=None,
                    )
                )

                chunk_index += 1

            continue

        # ------------------------------------------------
        # Add paragraph to current chunk.
        # ------------------------------------------------

        if (
            current_parts
            and current_words + paragraph_words > max_words
        ):
            chunks.append(
                _create_chunk_from_single_text(
                    document=document,
                    text="\n\n".join(
                        current_parts
                    ),
                    chunk_index=chunk_index,
                    start_timestamp=None,
                    end_timestamp=None,
                )
            )

            chunk_index += 1

            current_parts = []
            current_words = 0

        current_parts.append(paragraph)
        current_words += paragraph_words

    # ----------------------------------------------------
    # Final chunk.
    # ----------------------------------------------------

    if current_parts:

        chunks.append(
            _create_chunk_from_single_text(
                document=document,
                text="\n\n".join(
                    current_parts
                ),
                chunk_index=chunk_index,
                start_timestamp=None,
                end_timestamp=None,
            )
        )

    return chunks


def _split_text(
    text: str,
    max_words: int,
) -> list[str]:
    """
    Split long text into pieces of at most max_words.
    """

    words = text.split()

    pieces = []

    for start in range(
        0,
        len(words),
        max_words,
    ):
        piece = " ".join(
            words[start:start + max_words]
        )

        if piece:
            pieces.append(piece)

    return pieces


def _split_into_sentences(
    text: str,
) -> list[str]:
    """
    Basic sentence splitter used when raw transcript
    text has been flattened into one line.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text,
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def _create_chunk(
    document: TranscriptDocument,
    turns: list[TranscriptTurn],
    chunk_index: int,
) -> TranscriptChunk:

    text_parts = []

    for turn in turns:

        text_parts.append(
            f"{turn.speaker}: {turn.text}"
        )

    return _create_chunk_from_single_text(
        document=document,
        text="\n\n".join(text_parts),
        chunk_index=chunk_index,
        start_timestamp=turns[0].timestamp,
        end_timestamp=turns[-1].timestamp,
    )


def _create_chunk_from_single_text(
    document: TranscriptDocument,
    text: str,
    chunk_index: int,
    start_timestamp: str | None,
    end_timestamp: str | None,
) -> TranscriptChunk:

    return TranscriptChunk(
        text=text,
        chunk_index=chunk_index,

        title=document.title,
        guest=document.guest,

        youtube_url=document.youtube_url,
        video_id=document.video_id,
        publish_date=document.publish_date,

        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,

        keywords=document.keywords,
    )