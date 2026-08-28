from app.knowledge.chunker import chunk_document
from app.knowledge.document import (
    TranscriptDocument,
    TranscriptTurn,
)


def create_test_document():

    turns = [
        TranscriptTurn(
            speaker="Lenny",
            timestamp="00:00:00",
            text=" ".join(["hello"] * 100),
        ),
        TranscriptTurn(
            speaker="Guest",
            timestamp="00:01:00",
            text=" ".join(["world"] * 100),
        ),
        TranscriptTurn(
            speaker="Lenny",
            timestamp="00:02:00",
            text=" ".join(["testing"] * 100),
        ),
    ]

    return TranscriptDocument(
        guest="Test Guest",
        title="Test Episode",
        youtube_url=None,
        video_id=None,
        publish_date=None,
        description=None,
        duration_seconds=None,
        duration=None,
        view_count=None,
        channel=None,
        keywords=[],
        turns=turns,
    )


def test_chunk_document():

    document = create_test_document()

    chunks = chunk_document(
        document,
        max_words=250,
    )

    assert len(chunks) == 2

    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1

    assert chunks[0].start_timestamp == "00:00:00"
    assert chunks[0].end_timestamp == "00:01:00"

def create_raw_document():

    long_text = " ".join(
        ["This is a sentence about product growth."] * 500
    )

    return TranscriptDocument(
        guest="Raw Guest",
        title="Raw Transcript",
        youtube_url=None,
        video_id="raw123",
        publish_date=None,
        description=None,
        duration_seconds=None,
        duration=None,
        view_count=None,
        channel=None,
        keywords=[],
        turns=[
            TranscriptTurn(
                speaker="Unknown",
                timestamp=None,
                text=long_text,
            )
        ],
    )


def test_raw_transcript_is_split():

    document = create_raw_document()

    chunks = chunk_document(
        document,
        max_words=100,
    )

    assert len(chunks) > 1

    for chunk in chunks:
        assert len(chunk.text.split()) <= 100

        assert chunk.start_timestamp is None
        assert chunk.end_timestamp is None

        assert chunk.guest == "Raw Guest"
        assert chunk.video_id == "raw123"