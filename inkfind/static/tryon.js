/* Placement Preview ("Try It On") — client-side canvas compositor.
 *
 * Slice 3 of the MVP. Compositing is inherently browser-side (canvas), so this is
 * the one feature that lives in JS rather than server-rendered Python. Design
 * intent: keep the user's body photo entirely on-device (privacy) — nothing here
 * is uploaded. A design can be preloaded via data-design (the Generate/Search
 * loop) or uploaded directly.
 */
(function () {
  "use strict";

  const root = document.querySelector(".tryon");
  if (!root) return;

  const canvas = document.getElementById("tryon-canvas");
  const ctx = canvas.getContext("2d");
  const placeholder = document.getElementById("tryon-placeholder");
  const controls = document.getElementById("tryon-controls");
  const hint = document.getElementById("tryon-hint");

  const bodyInput = document.getElementById("body-input");
  const bodyInput2 = document.getElementById("body-input-2");
  const designInput = document.getElementById("design-input");

  const scaleEl = document.getElementById("ctrl-scale");
  const rotateEl = document.getElementById("ctrl-rotate");
  const opacityEl = document.getElementById("ctrl-opacity");
  const blendEl = document.getElementById("ctrl-blend");

  const MAX_DIM = 1200; // cap canvas resolution for perf + a reasonable export size

  // Design transform is stored as fractions of the canvas so it survives a photo
  // swap (different pixel dimensions) without jumping around.
  const state = {
    body: null, // HTMLImageElement (background photo)
    design: null, // HTMLImageElement (tattoo overlay)
    x: 0.5, // design centre, 0..1 across canvas width
    y: 0.5, // design centre, 0..1 down canvas height
    scale: scaleEl.value / 100, // design width as a fraction of canvas width
    rotation: Number(rotateEl.value), // degrees
    opacity: opacityEl.value / 100,
    blend: blendEl.value, // canvas globalCompositeOperation
  };

  const clamp01 = (n) => Math.min(Math.max(n, 0), 1);

  function loadImage(src, crossOrigin) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      if (crossOrigin) img.crossOrigin = "anonymous";
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = src;
    });
  }

  function fileToDataURL(file) {
    return new Promise((resolve, reject) => {
      const fr = new FileReader();
      fr.onload = () => resolve(fr.result);
      fr.onerror = reject;
      fr.readAsDataURL(file);
    });
  }

  function fitCanvasToBody() {
    let w = state.body.naturalWidth || 600;
    let h = state.body.naturalHeight || 800;
    const longest = Math.max(w, h);
    if (longest > MAX_DIM) {
      const k = MAX_DIM / longest;
      w = Math.round(w * k);
      h = Math.round(h * k);
    }
    canvas.width = w;
    canvas.height = h;
  }

  function render() {
    if (!state.body) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = "source-over";
    ctx.drawImage(state.body, 0, 0, canvas.width, canvas.height);

    if (state.design) {
      const dw = canvas.width * state.scale;
      const ratio = state.design.naturalHeight / state.design.naturalWidth || 1;
      const dh = dw * ratio;
      ctx.save();
      ctx.translate(state.x * canvas.width, state.y * canvas.height);
      ctx.rotate((state.rotation * Math.PI) / 180);
      ctx.globalAlpha = state.opacity;
      ctx.globalCompositeOperation = state.blend;
      ctx.drawImage(state.design, -dw / 2, -dh / 2, dw, dh);
      ctx.restore();
    }
  }

  async function setBody(file) {
    state.body = await loadImage(await fileToDataURL(file));
    fitCanvasToBody();
    placeholder.hidden = true;
    controls.hidden = false;
    render();
  }

  async function setDesignFromFile(file) {
    state.design = await loadImage(await fileToDataURL(file));
    render();
  }

  async function setDesignFromUrl(url) {
    try {
      // crossOrigin so a picsum/remote design doesn't taint the canvas and block export.
      state.design = await loadImage(url, true);
      render();
    } catch (e) {
      // Non-fatal: the user can still upload their own design image.
    }
  }

  // --- uploads ---
  const onBodyPick = (e) => e.target.files[0] && setBody(e.target.files[0]);
  bodyInput.addEventListener("change", onBodyPick);
  bodyInput2.addEventListener("change", onBodyPick);
  designInput.addEventListener("change", (e) => e.target.files[0] && setDesignFromFile(e.target.files[0]));

  // --- sliders / blend ---
  scaleEl.addEventListener("input", () => { state.scale = scaleEl.value / 100; render(); });
  rotateEl.addEventListener("input", () => { state.rotation = Number(rotateEl.value); render(); });
  opacityEl.addEventListener("input", () => { state.opacity = opacityEl.value / 100; render(); });
  blendEl.addEventListener("change", () => { state.blend = blendEl.value; render(); });

  // --- drag to reposition (pointer events cover mouse + touch) ---
  let drag = null; // { px, py, cx, cy } fractional pointer + centre at grab time

  function pointerFraction(e) {
    const rect = canvas.getBoundingClientRect();
    return {
      x: clamp01((e.clientX - rect.left) / rect.width),
      y: clamp01((e.clientY - rect.top) / rect.height),
    };
  }

  canvas.addEventListener("pointerdown", (e) => {
    if (!state.design) return;
    const p = pointerFraction(e);
    drag = { px: p.x, py: p.y, cx: state.x, cy: state.y };
    canvas.setPointerCapture(e.pointerId);
  });
  canvas.addEventListener("pointermove", (e) => {
    if (!drag) return;
    const p = pointerFraction(e);
    state.x = clamp01(drag.cx + (p.x - drag.px));
    state.y = clamp01(drag.cy + (p.y - drag.py));
    render();
  });
  const endDrag = () => { drag = null; };
  canvas.addEventListener("pointerup", endDrag);
  canvas.addEventListener("pointercancel", endDrag);

  // --- reset ---
  document.getElementById("btn-reset").addEventListener("click", () => {
    scaleEl.value = 40; rotateEl.value = 0; opacityEl.value = 90; blendEl.value = "multiply";
    Object.assign(state, { x: 0.5, y: 0.5, scale: 0.4, rotation: 0, opacity: 0.9, blend: "multiply" });
    render();
  });

  // --- download composite ---
  document.getElementById("btn-download").addEventListener("click", () => {
    try {
      canvas.toBlob((blob) => {
        if (!blob) return;
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "inkfind-preview.png";
        a.click();
        setTimeout(() => URL.revokeObjectURL(a.href), 1000);
      }, "image/png");
    } catch (e) {
      // Tainted canvas (cross-origin design that didn't allow CORS export).
      hint.textContent =
        "Couldn't export — that design blocks cross-origin download. Upload the design image and try again.";
    }
  });

  // --- preload a design passed from a card (Generate/Search -> Try It On) ---
  if (root.dataset.design) setDesignFromUrl(root.dataset.design);
})();
