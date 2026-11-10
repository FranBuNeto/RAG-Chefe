"""PDF ingestion and ChromaDB persistence."""

import gc
import tempfile
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import CHROMA_PATH, COLLECTION_NAME


def reset_vector_store(embeddings: HuggingFaceEmbeddings) -> None:
    """Remove the current collection while keeping the Chroma directory."""
    if not CHROMA_PATH.exists():
        return

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings,
    )
    vector_store.delete_collection()
    del vector_store
    gc.collect()


def process_pdf_bytes(
    pdf_bytes: bytes,
    embeddings: HuggingFaceEmbeddings,
) -> int:
    """Split PDF content, replace the index, and return the chunk count."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temporary_file:
        temporary_file.write(pdf_bytes)
        temporary_path = Path(temporary_file.name)

    try:
        documents = PyMuPDFLoader(str(temporary_path)).load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = splitter.split_documents(documents)
        if not chunks:
            raise ValueError("O PDF não contém texto extraível.")

        reset_vector_store(embeddings)
        CHROMA_PATH.mkdir(parents=True, exist_ok=True)
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(CHROMA_PATH),
            collection_name=COLLECTION_NAME,
        )
        del vector_store
        gc.collect()
        return len(chunks)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def process_pdf_file(
    pdf_path: str | Path,
    embeddings: HuggingFaceEmbeddings,
) -> int:
    """Process a PDF from disk using the same pipeline as the web app."""
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    return process_pdf_bytes(path.read_bytes(), embeddings)
