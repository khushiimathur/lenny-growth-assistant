from pathlib import Path
import re

import yaml

from app.knowledge.document import (
    TranscriptDocument,
    TranscriptTurn,
)


SPEAKER_PATTERN = re.compile(
    r"^(.+?) \((\d{2}:\d{2}:\d{2})\):$"
)


def load_transcript(filepath: str | Path) -> TranscriptDocument:

    filepath = Path(filepath)

    content = filepath.read_text(
        encoding="utf-8"
    )

    # ---------------------------------------------
    # 1. Parse frontmatter
    # ---------------------------------------------

    parts = content.split("---", 2)

    if len(parts) != 3:
        raise ValueError(
            f"Invalid transcript format: {filepath}"
        )

    frontmatter = yaml.safe_load(parts[1]) or {}

    transcript = parts[2]

    # ---------------------------------------------
    # 2. Try structured transcript format
    # ---------------------------------------------

    turns = _parse_structured_transcript(
        transcript
    )

    # ---------------------------------------------
    # 3. Fallback to raw transcript
    # ---------------------------------------------

    if not turns:

        turns = _parse_raw_transcript(
            transcript
        )

    # ---------------------------------------------
    # 4. Create document
    # ---------------------------------------------

    return TranscriptDocument(
        guest=str(frontmatter.get("guest", "")),
        title=str(frontmatter.get("title", "")),
        youtube_url=frontmatter.get("youtube_url"),
        video_id=frontmatter.get("video_id"),
        publish_date=frontmatter.get("publish_date"),
        description=frontmatter.get("description"),
        duration_seconds=frontmatter.get(
            "duration_seconds"
        ),
        duration=frontmatter.get("duration"),
        view_count=frontmatter.get("view_count"),
        channel=frontmatter.get("channel"),
        keywords=frontmatter.get("keywords", []),
        turns=turns,
    )


def _parse_structured_transcript(
    transcript: str,
) -> list[TranscriptTurn]:

    turns = []

    current_speaker = None
    current_timestamp = None
    current_lines = []

    for line in transcript.splitlines():

        line = line.strip()

        if not line:
            continue

        match = SPEAKER_PATTERN.match(line)

        if match:

            if current_speaker is not None:

                turns.append(
                    TranscriptTurn(
                        speaker=current_speaker,
                        timestamp=current_timestamp,
                        text=" ".join(
                            current_lines
                        ),
                    )
                )

            current_speaker = match.group(1)
            current_timestamp = match.group(2)
            current_lines = []

        else:

            if current_speaker is not None:
                current_lines.append(line)

    # Save final turn
    if current_speaker is not None:

        turns.append(
            TranscriptTurn(
                speaker=current_speaker,
                timestamp=current_timestamp,
                text=" ".join(current_lines),
            )
        )

    return turns


def _parse_raw_transcript(
    transcript: str,
) -> list[TranscriptTurn]:

    text = transcript.strip()

    if not text:
        return []

    return [
        TranscriptTurn(
            speaker="Unknown",
            timestamp=None,
            text=" ".join(
                line.strip()
                for line in text.splitlines()
                if line.strip()
            ),
        )
    ]