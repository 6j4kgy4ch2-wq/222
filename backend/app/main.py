from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import analyze, upload

app = FastAPI(title="财务慧眼-Ollama版", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(analyze.router)


@app.get("/")
async def root():
    return {
        "name": "财务慧眼",
        "mode": "local-ollama",
        "docs": "/docs",
        "ollama": "http://127.0.0.1:11434",
    }
