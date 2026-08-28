from dataclasses import dataclass, field


@dataclass
class TranscriptTurn:
    speaker: str
    timestamp: str|None
    text: str


@dataclass
class TranscriptDocument:
    guest: str
    title: str
    youtube_url: str | None
    video_id: str | None
    publish_date: str | None
    description: str | None
    duration_seconds: float | None
    duration: str | None
    view_count: int | None
    channel: str | None
    keywords: list[str] = field(default_factory=list)
    turns: list[TranscriptTurn] = field(default_factory=list)

@dataclass
class TranscriptChunk:
    text: str
    chunk_index: int

    title: str
    guest: str

    youtube_url: str | None
    video_id: str | None
    publish_date: str | None

    start_timestamp: str | None
    end_timestamp: str | None

    keywords: list[str] = field(default_factory=list)