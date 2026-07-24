"""FastAPI app wiring the two MVP slices to server-rendered HTMX templates.

Routes:
  GET  /                  Smart Search page (full catalog on load)
  GET  /search            Search results fragment (HTMX; prompt + filters)
  GET  /generate          AI Design Generator page
  POST /generate          Generated-designs fragment (HTMX)
  GET  /favorites         Saved collection page
  POST /favorites/toggle  Toggle a design's saved state (HTMX; returns fragment)

The JSON contracts from the original Next.js API routes are preserved as thin
wrappers under /api/* so the same logic can back a real frontend later.
"""

from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import favorites as favs
from . import guide as guide_mod
from .generate import generate
from .models import BODY_PARTS, SIZES, STYLES, GeneratedDesign
from .search import search

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="InkFind")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
templates.env.globals.update(STYLES=STYLES, BODY_PARTS=BODY_PARTS, SIZES=SIZES)

SID_COOKIE = "inkfind_sid"


def _sid(request: Request) -> str:
    return request.cookies.get(SID_COOKIE) or uuid.uuid4().hex


def _with_sid(response: Response, sid: str) -> Response:
    # Idempotent: (re)set the cookie so subsequent requests reuse the session.
    response.set_cookie(SID_COOKIE, sid, httponly=True, samesite="lax", max_age=60 * 60 * 24 * 365)
    return response


def _clean(value: str | None, allowed: tuple[str, ...]) -> str | None:
    return value if value in allowed else None


# --- Pages ---------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> Response:
    sid = _sid(request)
    results = search()  # full catalog on first load
    resp = templates.TemplateResponse(
        request, "index.html",
        {"results": results, "prompt": "", "filters": {}},
    )
    return _with_sid(resp, sid)


@app.get("/search", response_class=HTMLResponse)
def search_fragment(
    request: Request,
    prompt: str = "",
    style: str | None = None,
    bodyPart: str | None = None,
    size: str | None = None,
) -> Response:
    sid = _sid(request)
    results = search(
        prompt=prompt,
        style=_clean(style, STYLES),
        body_part=_clean(bodyPart, BODY_PARTS),
        size=_clean(size, SIZES),
    )
    resp = templates.TemplateResponse(
        request, "_results.html",
        {"results": results, "prompt": prompt.strip()},
    )
    return _with_sid(resp, sid)


@app.get("/try-on", response_class=HTMLResponse)
def try_on_page(
    request: Request,
    design: str | None = None,
    prompt: str = "",
    style: str = "",
) -> Response:
    # `design`/`prompt`/`style` may be passed from a search or generated card so
    # the design is preloaded onto the canvas — this is the Generate/Search -> Try
    # It On loop. Compositing itself is client-side (see static/tryon.js): the body
    # photo never leaves the browser.
    sid = _sid(request)
    resp = templates.TemplateResponse(
        request, "tryon.html",
        {"design": design or "", "prompt": prompt.strip(), "style": _clean(style, STYLES) or ""},
    )
    return _with_sid(resp, sid)


@app.get("/generate", response_class=HTMLResponse)
def generate_page(request: Request) -> Response:
    sid = _sid(request)
    resp = templates.TemplateResponse(request, "generate.html", {"style": "fine-line"})
    return _with_sid(resp, sid)


@app.post("/generate", response_class=HTMLResponse)
def generate_fragment(
    request: Request,
    prompt: str = Form(""),
    style: str = Form("fine-line"),
    seed: int | None = Form(None),
) -> Response:
    sid = _sid(request)
    prompt = prompt.strip()
    if not prompt:
        resp = templates.TemplateResponse(
            request, "_designs.html",
            {"designs": [], "style": style, "error": "Describe the tattoo you want to generate."},
        )
        return _with_sid(resp, sid)

    clean_style = _clean(style, STYLES) or "fine-line"
    designs = generate(prompt=prompt, style=clean_style, count=4, seed=seed)
    resp = templates.TemplateResponse(
        request, "_designs.html",
        {
            "designs": designs,
            "style": clean_style,
            "error": None,
            "is_favorite": lambda d: favs.is_favorite(sid, d.id),
        },
    )
    return _with_sid(resp, sid)


@app.get("/guide", response_class=HTMLResponse)
def guide_page(
    request: Request,
    style: str | None = None,
    bodyPart: str | None = None,
) -> Response:
    # Optional style/bodyPart preselect the suitability matcher (deep-linkable).
    sid = _sid(request)
    sel_style = _clean(style, STYLES) or "fine-line"
    sel_body = _clean(bodyPart, BODY_PARTS) or "forearm"
    resp = templates.TemplateResponse(
        request, "guide.html",
        {
            "styles": guide_mod.STYLE_GUIDE,
            "body_parts": guide_mod.BODY_PART_GUIDE,
            "pain_label": guide_mod.pain_label,
            "aftercare": guide_mod.AFTERCARE,
            "hygiene": guide_mod.HYGIENE_CHECKLIST,
            "sel_style": sel_style,
            "sel_body": sel_body,
            "assessment": guide_mod.assess(sel_style, sel_body),
        },
    )
    return _with_sid(resp, sid)


@app.get("/guide/assess", response_class=HTMLResponse)
def guide_assess(
    request: Request,
    style: str | None = None,
    bodyPart: str | None = None,
) -> Response:
    sid = _sid(request)
    sel_style = _clean(style, STYLES) or "fine-line"
    sel_body = _clean(bodyPart, BODY_PARTS) or "forearm"
    resp = templates.TemplateResponse(
        request, "_assessment.html",
        {"assessment": guide_mod.assess(sel_style, sel_body)},
    )
    return _with_sid(resp, sid)


@app.get("/favorites", response_class=HTMLResponse)
def favorites_page(request: Request) -> Response:
    sid = _sid(request)
    resp = templates.TemplateResponse(
        request, "favorites.html", {"favorites": favs.list_favorites(sid)},
    )
    return _with_sid(resp, sid)


@app.post("/favorites/toggle", response_class=HTMLResponse)
def favorites_toggle(
    request: Request,
    id: str = Form(...),
    prompt: str = Form(""),
    style: str = Form("fine-line"),
    image_url: str = Form(""),
    created_at: int = Form(0),
    context: str = Form("generate"),
) -> Response:
    sid = _sid(request)
    design = GeneratedDesign(id=id, prompt=prompt, style=style, image_url=image_url, created_at=created_at)
    saved = favs.toggle(sid, design)

    if context == "favorites":
        # On the collection page, an unsaved card is removed from the DOM.
        resp = HTMLResponse("" if not saved else _render_card(request, sid, design))
    else:
        resp = templates.TemplateResponse(
            request, "_heart.html",
            {"design": design, "saved": saved, "context": context},
        )
    return _with_sid(resp, sid)


def _render_card(request: Request, sid: str, design: GeneratedDesign) -> str:
    macros = templates.get_template("_macros.html").module
    return str(macros.design_card(design, True, "favorites"))  # type: ignore[attr-defined]


# --- JSON API (contract-compatible with the original Next.js routes) -----

@app.get("/api/search")
def api_search(
    prompt: str = "",
    style: str | None = None,
    bodyPart: str | None = None,
    size: str | None = None,
) -> JSONResponse:
    results = search(
        prompt=prompt,
        style=_clean(style, STYLES),
        body_part=_clean(bodyPart, BODY_PARTS),
        size=_clean(size, SIZES),
    )
    payload = [
        {
            "id": r.tattoo.id, "title": r.tattoo.title, "style": r.tattoo.style,
            "bodyPart": r.tattoo.body_part, "size": r.tattoo.size,
            "tags": r.tattoo.tags, "imageUrl": r.tattoo.image_url, "score": r.score,
        }
        for r in results
    ]
    return JSONResponse({"count": len(payload), "results": payload})


@app.get("/api/guide")
def api_guide(style: str | None = None, bodyPart: str | None = None) -> JSONResponse:
    # With both params, return the suitability verdict; otherwise the full guide.
    if style is not None or bodyPart is not None:
        result = guide_mod.assess(
            _clean(style, STYLES) or "", _clean(bodyPart, BODY_PARTS) or "",
        )
        if result is None:
            return JSONResponse({"error": "unknown style or bodyPart"}, status_code=400)
        return JSONResponse(result)
    return JSONResponse(guide_mod.guide_data())


@app.post("/api/generate")
async def api_generate(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    prompt = body.get("prompt") if isinstance(body.get("prompt"), str) else ""
    style = body.get("style")

    if not (prompt or "").strip():
        return JSONResponse({"error": "prompt is required"}, status_code=400)
    if style not in STYLES:
        return JSONResponse({"error": f"style must be one of: {', '.join(STYLES)}"}, status_code=400)

    designs = generate(
        prompt=prompt, style=style,
        count=body.get("count") if isinstance(body.get("count"), int) else None,
        seed=body.get("seed") if isinstance(body.get("seed"), int) else None,
    )
    payload = [
        {"id": d.id, "prompt": d.prompt, "style": d.style, "imageUrl": d.image_url, "createdAt": d.created_at}
        for d in designs
    ]
    return JSONResponse({"count": len(payload), "designs": payload})
