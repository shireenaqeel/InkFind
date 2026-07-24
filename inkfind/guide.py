"""Tattoo Guide — the educational layer of the MVP (feature #4).

Content-driven, deterministic reference data plus a small suitability matcher that
answers "does this style suit this body part?". No AI/network — this is a curated
knowledge base. The hygiene checklist is India-specific on purpose: it reflects the
March 2025 Karnataka FDA heavy-metal-in-ink flags cited in the product plan.

Nothing here is medical advice; it's general, widely-cited tattoo guidance meant to
help someone walk into a studio informed.
"""

from __future__ import annotations

from .models import BODY_PARTS, STYLES

# --- Style → placement suitability -------------------------------------------
# `detail`: "fine" styles rely on thin lines/soft gradients that blur faster on
# high-movement, thin-skin areas; "bold" styles age well almost anywhere.

STYLE_GUIDE: dict[str, dict] = {
    "fine-line": {
        "detail": "fine",
        "blurb": "Delicate single-weight lines. Elegant and subtle, but the thinnest lines soften over the years.",
        "best_placements": ["forearm", "arm", "wrist", "ankle"],
    },
    "traditional": {
        "detail": "bold",
        "blurb": "Bold outlines and a limited, saturated palette — the style that ages best of all.",
        "best_placements": ["arm", "forearm", "chest", "back", "leg"],
    },
    "blackwork": {
        "detail": "bold",
        "blurb": "Heavy solid black. High-impact and durable; wants a bit of canvas to breathe.",
        "best_placements": ["back", "arm", "chest", "leg", "forearm"],
    },
    "watercolor": {
        "detail": "fine",
        "blurb": "Soft, paint-like washes with no hard outlines. Beautiful, but fades fastest — keep it out of the sun.",
        "best_placements": ["forearm", "arm", "back", "leg"],
    },
    "geometric": {
        "detail": "medium",
        "blurb": "Precise lines and symmetry. Reads best on flatter, less-curved areas so the geometry stays true.",
        "best_placements": ["forearm", "arm", "back", "chest", "leg"],
    },
    "minimalist": {
        "detail": "fine",
        "blurb": "Small, clean, and understated. Great for a first tattoo; give tiny details a little room.",
        "best_placements": ["wrist", "ankle", "forearm", "neck"],
    },
    "tribal": {
        "detail": "bold",
        "blurb": "Bold flowing black shapes that follow the body. Durable and striking at size.",
        "best_placements": ["arm", "chest", "back", "leg", "forearm"],
    },
    "realism": {
        "detail": "medium",
        "blurb": "Photographic detail and shading. Needs space and smooth skin to hold fine gradients.",
        "best_placements": ["arm", "forearm", "back", "chest", "leg"],
    },
}

# --- Body part → pain + healing reference ------------------------------------
# `pain` is a 1–5 scale (general guidance, varies by person). `healing` is surface
# healing; full healing under the skin takes ~2–3 months for any tattoo.

BODY_PART_GUIDE: dict[str, dict] = {
    "arm": {"pain": 2, "healing": "2–3 weeks", "note": "Upper/outer arm is one of the most forgiving spots — muscle padding, low pain."},
    "forearm": {"pain": 2, "healing": "2–3 weeks", "note": "Easy to reach, heals cleanly, low pain. A great first-tattoo location."},
    "back": {"pain": 3, "healing": "2–3 weeks", "note": "Large flat canvas; moderate pain, more over the spine and shoulder blades."},
    "chest": {"pain": 4, "healing": "2–4 weeks", "note": "High pain near the sternum and collarbone (thin skin over bone)."},
    "leg": {"pain": 2, "healing": "2–4 weeks", "note": "Thigh and calf are low-pain with lots of room; shin is bonier and sharper."},
    "ankle": {"pain": 4, "healing": "3–4 weeks", "note": "Thin skin over bone — sharper pain, and movement/footwear slows healing."},
    "wrist": {"pain": 3, "healing": "2–3 weeks", "note": "Thin skin and tendons; high-friction, so fine detail can blur over time."},
    "neck": {"pain": 4, "healing": "2–3 weeks", "note": "Sensitive and highly visible — worth being sure before committing."},
}

PAIN_LABELS = {1: "Very low", 2: "Low", 3: "Moderate", 4: "High", 5: "Very high"}

# High-friction / high-movement areas where fine detail fades soonest.
_HIGH_FRICTION = {"wrist", "ankle", "neck"}

# --- Aftercare basics --------------------------------------------------------

AFTERCARE: list[dict] = [
    {"phase": "First few hours", "tip": "Leave the artist's wrap on for as long as they advised — it protects the fresh wound."},
    {"phase": "Wash (2–3× a day)", "tip": "Clean gently with lukewarm water and fragrance-free soap, then pat dry. Never scrub."},
    {"phase": "Moisturise", "tip": "A thin layer of fragrance-free lotion or aftercare balm. Over-applying suffocates it — less is more."},
    {"phase": "Protect (~2 weeks)", "tip": "No pools, sea, or long soaks, and keep it out of direct sun while it heals."},
    {"phase": "Don't pick", "tip": "Scabbing and flaking are normal — let them fall off on their own. Picking pulls out ink and scars."},
    {"phase": "Long term", "tip": "Once healed, sunscreen is the single best thing for keeping it crisp for years."},
]

# --- Hygiene & safety checklist (India context) ------------------------------

HYGIENE_CHECKLIST: list[dict] = [
    {"check": "Licensed, visibly clean studio", "why": "You should be able to see the workspace. A clean, professional setup is the baseline — walk if it isn't."},
    {"check": "New, sealed single-use needles", "why": "Needles should be opened from a sealed pack in front of you, and never reused."},
    {"check": "Fresh gloves + wrapped surfaces", "why": "The artist wears new gloves and wraps/sanitises equipment and surfaces between clients."},
    {"check": "Autoclave-sterilised reusable tools", "why": "Any reusable metal tools must be autoclave-sterilised — it's fine to ask how they sterilise."},
    {"check": "Reputable, safe ink", "why": "After the March 2025 Karnataka FDA heavy-metal contamination flags, ask which ink brand they use and that caps are single-use."},
    {"check": "Portfolio of healed work", "why": "Fresh photos look good on anyone — healed work shows how the artist's tattoos actually settle."},
    {"check": "Clear written aftercare", "why": "A good studio sends you home knowing exactly how to care for it."},
    {"check": "It feels right", "why": "Budget shouldn't override safety. If anything feels off about hygiene, trust your gut and leave."},
]


def _label(style: str) -> str:
    return style[:1].upper() + style[1:].replace("-", " ")


def pain_label(level: int) -> str:
    return PAIN_LABELS.get(level, "Moderate")


def assess(style: str, body_part: str) -> dict | None:
    """Suitability verdict for a (style, body_part) pairing, or None if unknown."""
    sg = STYLE_GUIDE.get(style)
    bp = BODY_PART_GUIDE.get(body_part)
    if not sg or not bp:
        return None

    fits = body_part in sg["best_placements"]
    caution = sg["detail"] == "fine" and body_part in _HIGH_FRICTION

    if fits and not caution:
        rating, level = "Great fit", "good"
    elif fits and caution:
        rating, level = "Good — size it up", "ok"
    elif caution:
        rating, level = "Tricky placement", "warn"
    else:
        rating, level = "Workable", "ok"

    notes: list[str] = []
    if fits:
        notes.append(f"{_label(style)} is commonly placed on the {body_part}.")
    else:
        notes.append(f"The {body_part} isn't a classic spot for {_label(style).lower()}, but it can still work with the right sizing.")
    if caution:
        notes.append(
            f"Fine detail on the {body_part} (thin skin, high movement) blurs faster over time — "
            "scale it up a little and keep lines from crowding."
        )
    notes.append(f"Pain here is {pain_label(bp['pain']).lower()}, and surface healing takes {bp['healing']}.")

    return {
        "style": style,
        "body_part": body_part,
        "rating": rating,
        "level": level,
        "notes": notes,
        "pain": bp["pain"],
        "pain_label": pain_label(bp["pain"]),
        "healing": bp["healing"],
    }


# Convenience for the JSON API — the whole knowledge base in one payload.
def guide_data() -> dict:
    return {
        "styles": {
            s: {**STYLE_GUIDE[s], "label": _label(s)} for s in STYLES if s in STYLE_GUIDE
        },
        "bodyParts": {
            b: {**BODY_PART_GUIDE[b], "painLabel": pain_label(BODY_PART_GUIDE[b]["pain"])}
            for b in BODY_PARTS if b in BODY_PART_GUIDE
        },
        "aftercare": AFTERCARE,
        "hygieneChecklist": HYGIENE_CHECKLIST,
    }
