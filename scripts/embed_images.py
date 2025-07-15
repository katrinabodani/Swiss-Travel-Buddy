# scripts/embed_images.py

import os
import json
from pathlib import Path
from PIL import Image
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

# ——— CONFIG ———
IMG_DIR        = Path("data/images")
META_FILE      = IMG_DIR / "image_metadata.json"
EMBED_DIR      = "data/embeddings"
COLLECTION     = "swiss_image_chunks"

# Use an available CLIP model:
CLIP_MODEL     = "clip-ViT-B-32"
# ————————

def main():
    # 1) Init ChromaDB client & collection
    client = PersistentClient(path=EMBED_DIR)
    try:
        client.delete_collection(COLLECTION)
    except ValueError:
        pass
    collection = client.get_or_create_collection(COLLECTION)

    # 2) Load your image metadata
    with open(META_FILE, encoding="utf-8") as f:
        images_meta = json.load(f)

    # 3) Load the CLIP‐style encoder
    model = SentenceTransformer(CLIP_MODEL)

    # 4) Iterate and embed
    for entry in images_meta:
        fname   = entry["filename"]
        caption = entry.get("caption", "").strip()
        imgpath = IMG_DIR / fname

        if not imgpath.exists():
            print(f"⚠️  Missing image file: {fname}")
            continue

        # Open & encode
        img = Image.open(imgpath).convert("RGB")
        vec = model.encode(img)  # numpy array

        # Unique ID for this image chunk
        chunk_id = f"img_{fname.replace('.', '_')}"

        # Minimal metadata
        meta = {
            "filename":     fname,
            "source_url":   entry.get("url"),
            "page":         entry.get("page"),
            "image_number": entry.get("image_number")
        }

        # Add to ChromaDB
        collection.add(
            ids=[chunk_id],
            embeddings=[vec.tolist()],
            metadatas=[meta],
            documents=[caption]  # caption as “document” text
        )

        print(f"✅ Embedded {fname} → {chunk_id}")

    print("🎉 All images embedded into ChromaDB!")

if __name__ == "__main__":
    main()
