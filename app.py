import streamlit as st

from src.chefe.documents import process_pdf_bytes
from src.chefe.rag import create_embeddings, query_rag

st.set_page_config(page_title="RAG Chefe", page_icon="😎", layout="wide")
st.title("RAG Chefe 😎")
st.markdown(
    "Assistente técnico com **RAG (Retrieval-Augmented Generation)**, "
    "Groq e ChromaDB para responder perguntas com base em PDFs."
)

@st.cache_resource
def load_embeddings():
    return create_embeddings()

embeddings = load_embeddings()

with st.sidebar:
    st.header("📄 Upload do Documento")
    uploaded_file = st.file_uploader("Envie um PDF para consultar", type=["pdf"])

    if st.button("Processar Documento", type="primary"):
        if uploaded_file is not None:
            with st.spinner("Processando e vetorizando o arquivo..."):
                try:
                    total_chunks = process_pdf_bytes(uploaded_file.getvalue(), embeddings)
                except (OSError, ValueError) as error:
                    st.error(f"Não foi possível processar o PDF: {error}")
                else:
                    st.session_state.processed = True
                    st.success(f"Concluído! {total_chunks} blocos indexados.")
        else:
            st.warning("Por favor, selecione um PDF antes de clicar.")

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "Olá! Eu sou o RAG Chefe. 👋\n\n"
            "Para começar:\n"
            "1. Envie um arquivo PDF no menu lateral.\n"
            "2. Clique em **Processar Documento**.\n"
            "3. Faça uma pergunta sobre o conteúdo do documento.\n\n"
            "As respostas serão baseadas apenas no PDF processado."
        )
    }]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Faça uma pergunta sobre o documento..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando trechos e gerando resposta..."):
            try:
                resposta = query_rag(prompt)
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            except (OSError, RuntimeError, ValueError) as error:
                st.error(f"Erro ao consultar a RAG Chain: {error}")