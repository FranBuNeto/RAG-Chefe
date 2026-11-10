"""Retrieval-augmented generation chain."""

from collections.abc import Callable

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

from .config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL, GROQ_MODEL

PROMPT_TEMPLATE = """Você é um assistente técnico especializado.
Responda à pergunta do usuário utilizando APENAS o contexto fornecido abaixo.
Se a informação não estiver presente no contexto, responda claramente:
"Não encontrei essa informação no documento fornecido."

Contexto:
{context}

Pergunta:
{question}

Resposta:"""


def format_documents(documents: list[Document]) -> str:
    """Combine retrieved document chunks into the prompt context."""
    return "\n\n".join(document.page_content for document in documents)


def create_embeddings() -> HuggingFaceEmbeddings:
    """Create the local embedding model used by the index."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def query_rag(
    question: str,
    embeddings: HuggingFaceEmbeddings | None = None,
    llm_factory: Callable[..., ChatGroq] = ChatGroq,
) -> str:
    """Retrieve relevant chunks and answer a question with Groq."""
    if not question.strip():
        raise ValueError("A pergunta não pode estar vazia.")

    embeddings = embeddings or create_embeddings()
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings,
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    llm = llm_factory(model=GROQ_MODEL, temperature=0)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    rag_chain = (
        {"context": retriever | format_documents, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke(question)
