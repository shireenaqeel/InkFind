"""Mock AI design generator.

MVP scaffold strategy: instead of calling a diffusion model, we produce
deterministic placeholder images seeded by (prompt, style, seed, index). This
lets the full generate -> vary -> regenerate -> save loop work end-to-end with no
AI dependency. Swap `generate()` internals for a real image-gen API later; the
GeneratedDesign contract stays the same so the UI doesn't change.

Ports `lib/generate.ts`, including the FNV-1a hash, so the placeholder image
URLs are byte-for-byte identical to the original scaffold for the same inputs.
"""

from __future__ import annotations

import time

from .models import GeneratedDesign

DEFAULT_COUNT = 4
MAX_COUNT = 8


def _hash(s: str) -> int:
    """Tiny stable FNV-1a 32-bit hash → used to seed placeholder image URLs."""
    h = 2166136261
    for ch in s:
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def _slug(prompt: str, style: str, seed: int, index: int) -> str:
    base = f"{style}-{prompt}-{seed}-{index}".lower()
    return str(_hash(base))


def generate(
    prompt: str,
    style: str,
    count: int | None = None,
    seed: int | None = None,
) -> list[GeneratedDesign]:
    prompt = (prompt or "").strip()
    seed = seed if seed is not None else 0
    count = min(max(count if count is not None else DEFAULT_COUNT, 1), MAX_COUNT)
    created_at = int(time.time() * 1000)

    designs: list[GeneratedDesign] = []
    for index in range(count):
        s = _slug(prompt, style, seed, index)
        designs.append(
            GeneratedDesign(
                id=s,
                prompt=prompt,
                style=style,
                # Placeholder render; deterministic per seed so "regenerate" yields a new set.
                image_url=f"https://picsum.photos/seed/{s}/600/800",
                created_at=created_at,
            )
        )
    return designs
