from app.knowledge.document import TranscriptTurn
from app.knowledge.cleaner import clean_text


def test_clean_text_removes_inaudible():
    text = "This is a [inaudible 00:01:23] sentence."

    result = clean_text(text)

    assert result == "This is a sentence."


def test_clean_text_normalizes_whitespace():
    text = "This    has   too   much     whitespace."

    result = clean_text(text)

    assert result == "This has too much whitespace."