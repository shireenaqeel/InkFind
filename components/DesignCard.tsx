"use client";

import type { GeneratedDesign } from "@/lib/types";

const cap = (s: string) =>
  s.charAt(0).toUpperCase() + s.slice(1).replace(/-/g, " ");

async function downloadImage(design: GeneratedDesign) {
  try {
    const res = await fetch(design.imageUrl);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `inkfind-${design.style}-${design.id}.jpg`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  } catch {
    // Fallback: just open it.
    window.open(design.imageUrl, "_blank");
  }
}

export default function DesignCard({
  design,
  saved,
  onToggleSave,
}: {
  design: GeneratedDesign;
  saved: boolean;
  onToggleSave: (design: GeneratedDesign) => void;
}) {
  return (
    <article className="card">
      <div className="thumb">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={design.imageUrl} alt={design.prompt || design.style} loading="lazy" />
        <button
          type="button"
          className={saved ? "heart saved" : "heart"}
          aria-label={saved ? "Remove from favorites" : "Save to favorites"}
          title={saved ? "Saved" : "Save"}
          onClick={() => onToggleSave(design)}
        >
          {saved ? "♥" : "♡"}
        </button>
      </div>
      <div className="card-body">
        <h3>{design.prompt || cap(design.style)}</h3>
        <div className="card-actions">
          <span className="tag">{cap(design.style)}</span>
          <button
            type="button"
            className="link-btn"
            onClick={() => downloadImage(design)}
          >
            Download
          </button>
        </div>
      </div>
    </article>
  );
}
