"""Sample catalog for the search slice.

Stands in for the real vector-searchable tattoo dataset — replace with a
DB/embeddings backend later. Images use picsum.photos seeds so each card renders
a stable placeholder. This is a 1:1 port of the original `lib/data/tattoos.ts`.
"""

from __future__ import annotations

from .models import Tattoo


def _img(seed: str) -> str:
    return f"https://picsum.photos/seed/{seed}/600/800"


TATTOOS: list[Tattoo] = [
    Tattoo("t1", "Minimalist Line Wolf", "fine-line", "forearm", "small",
           ["wolf", "animal", "line", "minimal", "single-needle"], _img("wolf-line")),
    Tattoo("t2", "Traditional Dragon Sleeve", "traditional", "arm", "large",
           ["dragon", "sleeve", "japanese", "bold", "color"], _img("dragon-sleeve")),
    Tattoo("t3", "Blackwork Mandala", "blackwork", "back", "large",
           ["mandala", "geometric", "ornamental", "symmetry", "dotwork"], _img("blackwork-mandala")),
    Tattoo("t4", "Watercolor Hummingbird", "watercolor", "leg", "medium",
           ["hummingbird", "bird", "color", "splash", "floral"], _img("watercolor-bird")),
    Tattoo("t5", "Geometric Mountain Range", "geometric", "forearm", "medium",
           ["mountain", "landscape", "lines", "nature", "triangle"], _img("geo-mountain")),
    Tattoo("t6", "Fine-Line Rose", "fine-line", "wrist", "small",
           ["rose", "flower", "floral", "delicate", "botanical"], _img("fineline-rose")),
    Tattoo("t7", "Tribal Shoulder Band", "tribal", "arm", "medium",
           ["tribal", "band", "bold", "pattern", "maori"], _img("tribal-band")),
    Tattoo("t8", "Realism Lion Portrait", "realism", "chest", "large",
           ["lion", "animal", "portrait", "shading", "realistic"], _img("realism-lion")),
    Tattoo("t9", "Minimalist Wave", "minimalist", "ankle", "small",
           ["wave", "ocean", "simple", "line", "nature"], _img("minimal-wave")),
    Tattoo("t10", "Geometric Wolf Head", "geometric", "forearm", "medium",
           ["wolf", "animal", "geometric", "lines", "lowpoly"], _img("geo-wolf")),
    Tattoo("t11", "Blackwork Snake", "blackwork", "leg", "medium",
           ["snake", "animal", "bold", "ornamental", "serpent"], _img("blackwork-snake")),
    Tattoo("t12", "Watercolor Lotus", "watercolor", "back", "medium",
           ["lotus", "flower", "floral", "color", "spiritual"], _img("watercolor-lotus")),
    Tattoo("t13", "Fine-Line Constellation", "fine-line", "neck", "small",
           ["stars", "constellation", "celestial", "dots", "minimal"], _img("fineline-stars")),
    Tattoo("t14", "Traditional Anchor", "traditional", "forearm", "small",
           ["anchor", "nautical", "bold", "old-school", "classic"], _img("traditional-anchor")),
    Tattoo("t15", "Realism Tiger", "realism", "arm", "large",
           ["tiger", "animal", "portrait", "shading", "realistic"], _img("realism-tiger")),
    Tattoo("t16", "Geometric Elephant", "geometric", "chest", "medium",
           ["elephant", "animal", "geometric", "mandala", "india"], _img("geo-elephant")),
]
