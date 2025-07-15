# services/backend/app/api/ask.py

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from chromadb import PersistentClient
import os
import numpy as np
from scripts.utils.embedding import embed
from scripts.utils.config import EMBED_DIR
from scripts.utils.llm import format_answer
from sentence_transformers import SentenceTransformer
from PIL import Image
from io import BytesIO

persist_path = EMBED_DIR
client = PersistentClient(path=persist_path)
collection = client.get_or_create_collection("swiss_chunks")

# Set up image collection and CLIP model
IMAGE_COLLECTION = "swiss_image_chunks"
image_collection = client.get_or_create_collection(IMAGE_COLLECTION)
clip_model = SentenceTransformer("clip-ViT-B-32")

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

    # Text‐based RAG
    query_embedding = embed(query)
    data_all = collection.get(include=["embeddings", "documents", "metadatas"])
    stored_embeddings = data_all["embeddings"]
    documents = data_all["documents"]
    metadatas = data_all["metadatas"]

    similarities = [cosine_similarity(query_embedding, emb) for emb in stored_embeddings]
    sorted_indices = np.argsort(similarities)[::-1][: data.top_k]

    top_chunks  = [documents[i] for i in sorted_indices]
    top_sources = [metadatas[i] for i in sorted_indices]
    top_scores  = [round(similarities[i], 4) for i in sorted_indices]

    answer = format_answer(query, top_chunks)

    return {
        "question": query,
        "answer": answer,
        "relevant_chunks": top_chunks,
        "similarities": top_scores,
        "sources": top_sources
    }

@router.post("/ask/image")
async def ask_image(file: UploadFile = File(...), top_k: int = 3):
    # 1) Read and open uploaded image
    contents = await file.read()
    try:
        img = Image.open(BytesIO(contents)).convert("RGB")
    except:
        raise HTTPException(400, "Invalid image file")

    # 2) Embed with CLIP and find best image match
    img_vec = clip_model.encode(img).astype(float).tolist()
    img_res = image_collection.query(
        query_embeddings=[img_vec],
        n_results=1,
        include=["metadatas", "documents", "distances"]
    )
    if not img_res["ids"][0]:
        raise HTTPException(404, "No similar image found")

    match_meta    = img_res["metadatas"][0][0]
    match_caption = img_res["documents"][0][0]
    match_score   = 1 - img_res["distances"][0][0]

    # 3) Use that caption to do a text RAG lookup
    text_emb = embed(match_caption)
    text_res = collection.query(
        query_embeddings=[text_emb],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    docs  = text_res["documents"][0]
    metas = text_res["metadatas"][0]
    sims  = [round(1 - d, 4) for d in text_res["distances"][0]]

    natural_answer = format_answer(
        f"This looks like: {match_caption}", 
        docs
    )

    return {
        "matched_image": {
            "filename":     match_meta.get("filename"),
            "source_url":   match_meta.get("source_url"),
            "page":         match_meta.get("page"),
            "image_number": match_meta.get("image_number"),
            "caption":      match_caption,
            "similarity":   round(match_score, 4)
        },
        "answer": natural_answer,
        "relevant_chunks": docs,
        "similarities":    sims,
        "sources":         metas
    }
