"""Real image generation via Replicate (FLUX), with a hard requirement of nothing.

This is the seam that turns InkFind's mock generator into a real one. It's fully
optional: if no ``REPLICATE_API_TOKEN`` is set, ``is_enabled()`` returns False and
the caller (``generate.py``) falls back to deterministic placeholder images, so the
app runs with zero configuration.

Provider: Replicate. Default model FLUX.1 [schnell] — fast and cheap, supports up to
4 outputs per call and a ``seed`` for reproducible "regenerate". Swap the model with
``REPLICATE_MODEL`` (e.g. a tattoo-specific fine-tune) without touching the UI.
"""

from __future__ import annotations

import os
import time

import httpx

# Descriptive modifiers so each preset prompts the model toward the right look.
STYLE_PROMPTS: dict[str, str] = {
    "fine-line": "delicate fine-line single-needle",
    "traditional": "bold American traditional, thick black outlines, limited solid colour palette",
    "blackwork": "solid blackwork, heavy black ink, high contrast",
    "watercolor": "watercolour, soft colour washes, no hard outlines",
    "geometric": "precise geometric linework, clean symmetry",
    "minimalist": "minimalist, simple clean single-weight lines",
    "tribal": "bold tribal blackwork, flowing solid black shapes",
    "realism": "black-and-grey realism, detailed fine shading",
}

_API_ROOT = "https://api.replicate.com/v1"
_MAX_OUTPUTS = 4  # FLUX schnell caps num_outputs at 4


def _token() -> str | None:
    return os.getenv("REPLICATE_API_TOKEN") or None


def _model() -> str:
    return os.getenv("REPLICATE_MODEL", "black-forest-labs/flux-schnell")


def is_enabled() -> bool:
    """True when a Replicate token is configured; otherwise the caller mocks."""
    return _token() is not None


def build_prompt(prompt: str, style: str) -> str:
    style_desc = STYLE_PROMPTS.get(style, style.replace("-", " "))
    return (
        f"A {style_desc} tattoo design of {prompt}, isolated on a plain white "
        "background, crisp clean linework, high contrast, professional tattoo flash "
        "art, centered composition, no background scenery, no photographic frame"
    )


def generate_images(prompt: str, style: str, count: int, seed: int) -> list[str]:
    """Return a list of generated image URLs. Raises on any failure.

    Uses Replicate's ``Prefer: wait`` to return synchronously for fast models, and
    falls back to short polling if the prediction is still running.
    """
    token = _token()
    if not token:
        raise RuntimeError("REPLICATE_API_TOKEN is not set")

    count = max(1, min(count, _MAX_OUTPUTS))
    payload = {
        "input": {
            "prompt": build_prompt(prompt, style),
            "num_outputs": count,
            "aspect_ratio": "3:4",  # matches the card thumbnail ratio
            "output_format": "png",
            "seed": seed,
            "go_fast": True,
        }
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "wait",  # block up to ~60s so fast models return in one request
    }

    with httpx.Client(timeout=90) as client:
        resp = client.post(
            f"{_API_ROOT}/models/{_model()}/predictions", json=payload, headers=headers
        )
        resp.raise_for_status()
        data = resp.json()

        # If Prefer:wait didn't fully resolve it, poll the prediction briefly.
        get_url = data.get("urls", {}).get("get")
        tries = 0
        while data.get("status") in ("starting", "processing") and get_url and tries < 40:
            time.sleep(1.5)
            data = client.get(get_url, headers=headers).json()
            tries += 1

    if data.get("status") != "succeeded":
        raise RuntimeError(f"Replicate prediction did not succeed: {data.get('status')}")

    output = data.get("output") or []
    if isinstance(output, str):
        output = [output]
    urls = [u for u in output if isinstance(u, str)]
    if not urls:
        raise RuntimeError("Replicate returned no images")
    return urls
