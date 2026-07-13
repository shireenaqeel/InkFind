"""Shared domain types for the tattoo catalog, search, and generation.

Mirrors the original `lib/types.ts`. Style presets are kept aligned with the AI
Generator presets so search & generation stay consistent.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Style presets mirror the AI Generator presets.
STYLES: tuple[str, ...] = (
    "fine-line",
    "traditional",
    "blackwork",
    "watercolor",
    "geometric",
    "minimalist",
    "tribal",
    "realism",
)

BODY_PARTS: tuple[str, ...] = (
    "arm",
    "forearm",
    "back",
    "chest",
    "leg",
    "ankle",
    "wrist",
    "neck",
)

SIZES: tuple[str, ...] = ("small", "medium", "large")


@dataclass(frozen=True)
class Tattoo:
    id: str
    title: str
    style: str
    body_part: str
    size: str
    # Free-text tags power prompt matching until real image embeddings land.
    tags: list[str] = field(default_factory=list)
    image_url: str = ""


@dataclass(frozen=True)
class SearchResult:
    tattoo: Tattoo
    # 0..1 relevance from the (currently keyword-based) matcher.
    score: float


@dataclass(frozen=True)
class GeneratedDesign:
    id: str  # stable per (prompt, style, seed, index) so favorites dedupe
    prompt: str
    style: str
    image_url: str
    created_at: int
