from src.chefe.rag import query_rag

if __name__ == "__main__":
    pergunta_usuario = input("Digite sua pergunta sobre o PDF: ")
    resposta = query_rag(pergunta_usuario)
    print("\n--- RESPOSTA ---")
    print(resposta)