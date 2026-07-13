"""Keyword-based stand-in for vector similarity search.

MVP scaffold strategy: filters are exact-match, and the free-text prompt is
scored against each tattoo's title/style/tags by simple token overlap. This
keeps the UI -> API -> data slice honest end-to-end without any AI dependency.
Swap `_score_prompt` for an embeddings + vector-DB lookup later; the shape of
SearchResult stays the same so the UI doesn't change.

1:1 port of the original `lib/search.ts`.
"""

from __future__ import annotations

import re

from .data import TATTOOS
from .models import SearchResult, Tattoo

_TOKEN_SPLIT = re.compile(r"[^a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN_SPLIT.split(text.lower()) if t]


def _searchable_text(t: Tattoo) -> list[str]:
    return _tokenize(" ".join([t.title, t.style, t.body_part, t.size, *t.tags]))


def _score_prompt(prompt: str, t: Tattoo) -> float:
    query_tokens = _tokenize(prompt)
    if not query_tokens:
        return 1.0  # no prompt = everything is equally relevant
    haystack = set(_searchable_text(t))
    hits = sum(1 for tok in query_tokens if tok in haystack)
    return hits / len(query_tokens)


def search(
    prompt: str = "",
    style: str | None = None,
    body_part: str | None = None,
    size: str | None = None,
) -> list[SearchResult]:
    filtered = [
        t
        for t in TATTOOS
        if (style is None or t.style == style)
        and (body_part is None or t.body_part == body_part)
        and (size is None or t.size == size)
    ]

    has_prompt = bool(_tokenize(prompt))

    results = [SearchResult(tattoo=t, score=_score_prompt(prompt, t)) for t in filtered]
    # When a prompt is given, drop zero-relevance results; otherwise keep all.
    results = [r for r in results if not has_prompt or r.score > 0]
    results.sort(key=lambda r: r.score, reverse=True)
    return results
