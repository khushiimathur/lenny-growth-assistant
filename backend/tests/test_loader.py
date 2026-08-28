from pathlib import Path

from app.knowledge.loader import load_transcript


TRANSCRIPT = Path(
    "../data/lenny-transcripts/"
    "episodes/ada-chen-rekhi/transcript.md"
)


def test_load_transcript():
    document = load_transcript(TRANSCRIPT)

    assert document.guest == "Ada Chen Rekhi"

    assert (
        document.title
        == "Feeling stuck? Here's how to know when it's time to leave your job | Ada Chen Rekhi"
    )

    assert document.video_id == "l-T8sNRcWQk"

    assert document.publish_date is not None

    assert len(document.turns) > 0


def test_first_turn():
    document = load_transcript(TRANSCRIPT)

    first_turn = document.turns[0]

    assert first_turn.speaker == "Ada Chen Rekhi"

    assert first_turn.timestamp == "00:00:00"

    assert len(first_turn.text) > 0