import { NextResponse } from "next/server";
import { generate } from "@/lib/generate";
import { STYLES, type GenerateRequest, type Style } from "@/lib/types";

// POST /api/generate
// Body: { prompt, style, count?, seed? } → { designs: GeneratedDesign[] }
// Mock generator today; swap for a real image-gen API later (same contract).
export async function POST(request: Request) {
  let body: Partial<GenerateRequest>;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const prompt = typeof body.prompt === "string" ? body.prompt : "";
  const style = body.style;

  if (!prompt.trim()) {
    return NextResponse.json({ error: "prompt is required" }, { status: 400 });
  }
  if (!style || !(STYLES as readonly string[]).includes(style)) {
    return NextResponse.json(
      { error: `style must be one of: ${STYLES.join(", ")}` },
      { status: 400 },
    );
  }

  const designs = generate({
    prompt,
    style: style as Style,
    count: typeof body.count === "number" ? body.count : undefined,
    seed: typeof body.seed === "number" ? body.seed : undefined,
  });

  return NextResponse.json({ count: designs.length, designs });
}
