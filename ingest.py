from src.chefe.rag import create_embeddings
from src.chefe.documents import process_pdf_file

PDF_PATH = "documento_teste.pdf"


def process_pdf() -> None:
    """Build the local index from the sample PDF."""
    total_chunks = process_pdf_file(PDF_PATH, create_embeddings())
    print(f"Processamento concluído: {total_chunks} blocos indexados.")

if __name__ == "__main__":
    process_pdf()