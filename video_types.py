from typing import TypedDict


class Segment(TypedDict):
    start: float
    end: float
    text: str


class TranscriptionResult(TypedDict):
    success: bool
    segments: list[Segment]
    error_message: str | None
