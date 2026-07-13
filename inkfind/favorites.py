"""Personal collection of saved designs.

The original scaffold stored favorites in the browser's localStorage. Since this
port is server-rendered (HTMX), favorites live server-side instead, keyed by a
per-browser session cookie. No auth yet — when accounts land, swap this in-memory
store for a DB-backed collection; the surface (list/toggle/is_favorite) stays the
same so the templates don't change.

NOTE: in-memory means favorites reset when the server restarts. That's fine for
an MVP scaffold and mirrors the "swap the storage layer later" intent.
"""

from __future__ import annotations

from .models import GeneratedDesign

# session id -> {design_id -> GeneratedDesign}, insertion-ordered (newest first).
_STORE: dict[str, dict[str, GeneratedDesign]] = {}


def list_favorites(sid: str) -> list[GeneratedDesign]:
    return list(_STORE.get(sid, {}).values())


def is_favorite(sid: str, design_id: str) -> bool:
    return design_id in _STORE.get(sid, {})


def toggle(sid: str, design: GeneratedDesign) -> bool:
    """Add or remove a design. Returns True if it is now saved."""
    bucket = _STORE.setdefault(sid, {})
    if design.id in bucket:
        del bucket[design.id]
        return False
    # Prepend so newest saved appears first.
    _STORE[sid] = {design.id: design, **bucket}
    return True
