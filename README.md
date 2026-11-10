# RAG Chefe 😎

Assistente de perguntas e respostas sobre documentos PDF usando **RAG
(Retrieval-Augmented Generation)**. O projeto transforma o conteúdo enviado
em vetores no ChromaDB e combina a busca semântica com um modelo da Groq para
gerar respostas fundamentadas no documento.

> Projeto desenvolvido para demonstrar uma aplicação de IA generativa com
> processamento de documentos, busca vetorial e interface interativa em
> Streamlit.

## Demonstração 💻

Disponível em: https://rag-chefe.streamlit.app

1. Envie um PDF pela barra lateral.
2. Clique em **Processar Documento**.
3. Faça perguntas no chat.

O assistente instrui o modelo a responder apenas com os trechos recuperados e
informa quando não encontra a resposta no documento.

## Tecnologias 🔨

- Python
- Streamlit
- LangChain (LCEL)
- ChromaDB
- Hugging Face Sentence Transformers
- Groq
- PyMuPDF

## Arquitetura ⚙️

```text
app.py                  Interface Streamlit e estado da sessão
src/chefe/
  config.py             Configurações e variáveis de ambiente
  documents.py          Leitura, chunking e indexação dos PDFs
  rag.py                Recuperação de contexto e geração da resposta
ingest.py               Entrada de linha de comando para indexação local
rag_chain.py            Entrada de linha de comando para consultas
check_models.py         Verificação dos modelos disponíveis na Groq
```

O arquivo `app.py` permanece na raiz para ser reconhecido diretamente pelo
Streamlit Community Cloud. O diretório `chroma_db/` é gerado localmente em
tempo de execução e não deve ser versionado.

## Como executar localmente

### 1. Pré-requisitos

- Python 3.10 ou superior
- Uma chave da [Groq](https://console.groq.com/keys)

### 2. Instalação

```bash
git clone https://github.com/FranBuNeto/RAG-Chefe.git
cd RAG-Chefe
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configuração

Copie `.env.example` para `.env` e preencha:

```env
GROQ_API_KEY=sua_chave_aqui
```

Opcionalmente, personalize `GROQ_MODEL`, `EMBEDDING_MODEL` ou
`CHROMA_PATH`.

### 4. Iniciar a aplicação

```bash
streamlit run app.py
```

O navegador abrirá a aplicação em `http://localhost:8501`.

## Scripts auxiliares

Para indexar o PDF de teste local:

```bash
python ingest.py
```

Para consultar o índice pelo terminal:

```bash
python rag_chain.py
```

Para listar os modelos disponíveis na conta Groq:

```bash
python check_models.py
```
  um público amplo.

## Licença

Este projeto ainda não possui uma licença definida. Escolha uma licença antes
de aceitar contribuições ou reutilização pública.
