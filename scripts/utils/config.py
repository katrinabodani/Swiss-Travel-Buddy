import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
CHUNKS_DIR = os.path.join(BASE_DIR, "data", "chunks")
EMBED_DIR = os.path.join(BASE_DIR, "data", "embeddings")

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-70b-8192"  # or "llama3-8b-8192"
