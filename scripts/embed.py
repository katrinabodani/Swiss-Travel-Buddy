# scripts/embed.py
# Embed preprocessed chunks into ChromaDB using MiniLM from shared utility

from chromadb import PersistentClient
import os
import json
from scripts.utils.embedding import embed
from scripts.utils.config import EMBED_DIR
import sys

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHUNKS_DIR = os.path.join(BASE_DIR, "data", "chunks")

# Init ChromaDB persistent client
client = PersistentClient(path=EMBED_DIR)
# In scripts/embed.py before embedding chunks:
try:
    client.delete_collection("hunza_chunks")
    print("Old collection deleted.")
except ValueError:
    print("No previous collection found. Skipping delete.")

collection = client.get_or_create_collection("hunza_chunks")

# Loop through all chunked files
for filename in os.listdir(CHUNKS_DIR):
    if not filename.endswith(".json"): continue

    filepath = os.path.join(CHUNKS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        chunk = json.load(f)
        text = chunk["text"]
        metadata = {
            "source": chunk["source"],
            "position": chunk["position"]
        }
        chunk_id = f"{chunk['source']}_chunk_{chunk['position']}"

        embedding = embed(text).tolist()

        collection.add(
            ids=[chunk_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata]
        )

        print(f"Embedded and added chunk: {chunk_id}")

print("All chunks embedded and saved in ChromaDB!")