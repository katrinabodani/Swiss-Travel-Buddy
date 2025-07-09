# services/backend/app/main.py
from fastapi import FastAPI
from .api import ask

app = FastAPI()

app.include_router(ask.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def index():
    return {"message": "Swiss Ragbuddy backend is running."}

