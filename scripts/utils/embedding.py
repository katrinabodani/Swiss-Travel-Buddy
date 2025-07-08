# scripts/utils/embedding.py

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Debug print to verify which model and path are being used
# print("✅ Loaded shared embed model")
# print("📁 Model name or path:", model._model_card if hasattr(model, "_model_card") else "N/A")
# print("📂 Model loaded from:", model._model_config.get('model_name_or_path', 'Unknown'))

def embed(text: str):
    # print("📣 Using shared embed() function")
    return model.encode(text)
