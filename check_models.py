import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Erro: GROQ_API_KEY não foi encontrada no arquivo .env!")
else:
    try:
        client = Groq(api_key=api_key)
        models = client.models.list()
        print("--- MODELOS DISPONÍVEIS NA SUA CONTA GROQ ---")
        for m in models.data:
            print(f"- {m.id}")
    except Exception as e:
        print(f"Erro ao consultar a API da Groq: {e}")