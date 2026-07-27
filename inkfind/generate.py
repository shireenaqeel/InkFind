"""AI design generator.

Real generation runs through ``imagegen`` (Replicate/FLUX) when a token is set;
otherwise it falls back to deterministic placeholder images so the full generate ->
vary -> regenerate -> save loop works with zero configuration. Either way the
``GeneratedDesign`` contract is identical, so the UI never changes.

The mock path ports ``lib/generate.ts`` (FNV-1a hash) so placeholder image URLs are
byte-for-byte identical to the original scaffold for the same inputs.
"""

from __future__ import annotations

import logging
import random
import time

from . import imagegen
from .models import GeneratedDesign

log = logging.getLogger("inkfind.generate")

DEFAULT_COUNT = 4
MAX_COUNT = 8


def _hash(s: str) -> int:
    """Tiny stable FNV-1a 32-bit hash → used to seed placeholder image URLs and ids."""
    h = 2166136261
    for ch in s:
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def _slug(prompt: str, style: str, seed: int, index: int) -> str:
    base = f"{style}-{prompt}-{seed}-{index}".lower()
    return str(_hash(base))


def _mock_url(slug: str) -> str:
    # Deterministic placeholder render; stable per seed so ids dedupe in favorites.
    return f"https://picsum.photos/seed/{slug}/600/800"


def generate(
    prompt: str,
    style: str,
    count: int | None = None,
    seed: int | None = None,
) -> list[GeneratedDesign]:
    prompt = (prompt or "").strip()
    # A fresh random seed per call (unless pinned) makes each Generate/Regenerate a
    # new set, while keeping ids stable within the returned batch for dedupe.
    seed = seed if seed is not None else random.randint(1, 2_000_000_000)
    count = min(max(count if count is not None else DEFAULT_COUNT, 1), MAX_COUNT)
    created_at = int(time.time() * 1000)

    image_urls: list[str] | None = None
    if imagegen.is_enabled():
        try:
            image_urls = imagegen.generate_images(prompt, style, count, seed)
        except Exception as exc:  # noqa: BLE001 — degrade gracefully to the mock
            log.warning("Real generation failed, falling back to mock: %s", exc)
            image_urls = None

    designs: list[GeneratedDesign] = []
    n = len(image_urls) if image_urls else count
    for index in range(n):
        slug = _slug(prompt, style, seed, index)
        url = image_urls[index] if image_urls else _mock_url(slug)
        designs.append(
            GeneratedDesign(
                id=slug,
                prompt=prompt,
                style=style,
                image_url=url,
                created_at=created_at,
            )
        )
    return designs
