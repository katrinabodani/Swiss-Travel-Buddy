# scripts/chunk_images.py
import os, json
from pathlib import Path

# ——— CONFIG ———
IMG_META   = Path("data/images/image_metadata.json")   # your image metadata
CHUNK_DIR  = Path("data/chunks")                 # where embed.py already looks
# ————————

CHUNK_DIR.mkdir(exist_ok=True, parents=True)

with open(IMG_META, encoding="utf-8") as f:
    images = json.load(f)

for idx, entry in enumerate(images):
    caption = entry.get("caption", "").strip()
    if not caption:
        continue

    # Build chunk record
    chunk = {
      "id":       f"imgcap_{idx}",
      "source":   "image_captions",
      "position": idx,
      "text":     caption
    }

    # Write JSON
    out = CHUNK_DIR / f"{chunk['id']}.json"
    with open(out, "w", encoding="utf-8") as wf:
        json.dump(chunk, wf, ensure_ascii=False, indent=2)
    print(f"Wrote chunk {chunk['id']}")
