"use client";

import {
  BODY_PARTS,
  SIZES,
  STYLES,
  type SearchFilters,
} from "@/lib/types";

interface Props {
  prompt: string;
  filters: SearchFilters;
  onPromptChange: (value: string) => void;
  onFiltersChange: (filters: SearchFilters) => void;
  onSubmit: () => void;
}

const cap = (s: string) =>
  s.charAt(0).toUpperCase() + s.slice(1).replace(/-/g, " ");

export default function SearchControls({
  prompt,
  filters,
  onPromptChange,
  onFiltersChange,
  onSubmit,
}: Props) {
  const hasFilters = Boolean(filters.style || filters.bodyPart || filters.size);

  return (
    <div>
      <form
        className="searchbar"
        onSubmit={(e) => {
          e.preventDefault();
          onSubmit();
        }}
      >
        <input
          type="text"
          value={prompt}
          placeholder='Try "minimalist line wolf" or "traditional dragon sleeve"'
          onChange={(e) => onPromptChange(e.target.value)}
          aria-label="Search tattoos by prompt"
        />
        <button type="submit" className="btn btn-primary">
          Search
        </button>
      </form>

      {/* Image-based search is stubbed for the scaffold — wired to real
          embedding lookup later. */}
      <div className="image-stub">
        <span>or</span>
        <label htmlFor="img-search">upload a reference photo</label>
        <input
          id="img-search"
          type="file"
          accept="image/*"
          onChange={() =>
            alert(
              "Image-based search is coming soon — it'll find visually similar designs.",
            )
          }
        />
        <span>(coming soon)</span>
      </div>

      <div className="filters">
        <label className="filter-group">
          <span>Style</span>
          <select
            value={filters.style ?? ""}
            onChange={(e) =>
              onFiltersChange({
                ...filters,
                style: (e.target.value || undefined) as SearchFilters["style"],
              })
            }
          >
            <option value="">Any</option>
            {STYLES.map((s) => (
              <option key={s} value={s}>
                {cap(s)}
              </option>
            ))}
          </select>
        </label>

        <label className="filter-group">
          <span>Body part</span>
          <select
            value={filters.bodyPart ?? ""}
            onChange={(e) =>
              onFiltersChange({
                ...filters,
                bodyPart: (e.target.value ||
                  undefined) as SearchFilters["bodyPart"],
              })
            }
          >
            <option value="">Any</option>
            {BODY_PARTS.map((b) => (
              <option key={b} value={b}>
                {cap(b)}
              </option>
            ))}
          </select>
        </label>

        <label className="filter-group">
          <span>Size</span>
          <select
            value={filters.size ?? ""}
            onChange={(e) =>
              onFiltersChange({
                ...filters,
                size: (e.target.value || undefined) as SearchFilters["size"],
              })
            }
          >
            <option value="">Any</option>
            {SIZES.map((s) => (
              <option key={s} value={s}>
                {cap(s)}
              </option>
            ))}
          </select>
        </label>

        {hasFilters && (
          <button
            type="button"
            className="filter-clear"
            onClick={() => onFiltersChange({})}
          >
            Clear filters
          </button>
        )}
      </div>
    </div>
  );
}
