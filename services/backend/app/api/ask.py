# services/backend/app/api/ask.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from chromadb import PersistentClient
import os
import numpy as np
from scripts.utils.embedding import embed
from scripts.utils.config import EMBED_DIR
from scripts.utils.llm import format_answer

persist_path = EMBED_DIR
client = PersistentClient(path=persist_path)
collection = client.get_or_create_collection("hunza_chunks")

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    top_k: int = 3

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

@router.post("/ask")
def ask_question(data: AskRequest):
    query = data.question.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # Create query embedding
    query_embedding = embed(query)
    # print("API embedding sample:", query_embedding[:5])

    # Retrieve all stored embeddings and docs
    data_all = collection.get(include=["embeddings", "documents", "metadatas"])
    stored_embeddings = data_all["embeddings"]
    documents = data_all["documents"]
    metadatas = data_all["metadatas"]

    # Compute cosine similarity
    similarities = [
        cosine_similarity(query_embedding, emb) for emb in stored_embeddings
    ]

    # Pair and sort
    top_k = data.top_k
    sorted_indices = np.argsort(similarities)[::-1][:top_k]

    top_chunks = [documents[i] for i in sorted_indices]
    top_sources = [metadatas[i] for i in sorted_indices]
    top_scores = [round(similarities[i], 4) for i in sorted_indices]

    print("Top Cosine Similarities:", top_scores)

    answer = format_answer(query, top_chunks)

    return {
        "question": query,
        "answer":answer,
        "relevant_chunks": top_chunks,
        "similarities": top_scores,
        "sources": top_sources
    }
