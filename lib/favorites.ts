"use client";

import { useCallback, useEffect, useState } from "react";
import type { GeneratedDesign } from "@/lib/types";

// Personal collection of saved designs.
//
// MVP: persisted to localStorage (no auth yet). When accounts land, swap the
// storage layer for an API-backed collection — the hook's surface stays the same.

const KEY = "inkfind:favorites";

function read(): GeneratedDesign[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = window.localStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as GeneratedDesign[]) : [];
  } catch {
    return [];
  }
}

function write(items: GeneratedDesign[]) {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(items));
  } catch {
    /* ignore quota / serialization errors */
  }
  // Notify other hook instances in this tab.
  window.dispatchEvent(new Event("inkfind:favorites-changed"));
}

export function useFavorites() {
  const [favorites, setFavorites] = useState<GeneratedDesign[]>([]);

  // Hydrate after mount (avoids SSR/client mismatch) and stay in sync.
  useEffect(() => {
    setFavorites(read());
    const sync = () => setFavorites(read());
    window.addEventListener("inkfind:favorites-changed", sync);
    window.addEventListener("storage", sync);
    return () => {
      window.removeEventListener("inkfind:favorites-changed", sync);
      window.removeEventListener("storage", sync);
    };
  }, []);

  const isFavorite = useCallback(
    (id: string) => favorites.some((f) => f.id === id),
    [favorites],
  );

  const toggle = useCallback((design: GeneratedDesign) => {
    const current = read();
    const exists = current.some((f) => f.id === design.id);
    const next = exists
      ? current.filter((f) => f.id !== design.id)
      : [design, ...current];
    write(next);
    setFavorites(next);
  }, []);

  const remove = useCallback((id: string) => {
    const next = read().filter((f) => f.id !== id);
    write(next);
    setFavorites(next);
  }, []);

  return { favorites, isFavorite, toggle, remove };
}
