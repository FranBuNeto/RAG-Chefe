"""Application configuration shared by the UI and command-line scripts."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

CHROMA_PATH = Path(os.getenv("CHROMA_PATH", str(PROJECT_ROOT / "chroma_db")))
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "rag_chefe")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
