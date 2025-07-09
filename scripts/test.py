from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
import os
import numpy as np
from scripts.utils.embedding import embed
from scripts.utils.config import EMBED_DIR

# Load DB and model
# EMBED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/embeddings"))
client = PersistentClient(path=EMBED_DIR)
collection = client.get_or_create_collection("hunza_chunks")
# model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Your test query
query = "How many langauges does Switzerland have?"
query_emb = embed(query)
# print("Debug script embedding sample:", query_emb[:5])


# Get all stored embeddings
data = collection.get(include=["documents", "embeddings"])
stored_embs = data["embeddings"]
documents = data["documents"]

# Compare distances manually
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

for i, emb in enumerate(stored_embs):
    score = cosine_similarity(query_emb, emb)
    print(f"Chunk {i} similarity: {score:.4f}")
    if score > 0.7:
        print("Match found:")
        print(documents[i][:300])
        print("---")
