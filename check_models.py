import os
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

# Carrega a API Key
load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Erro: Chave não encontrada no .env")
else:
    genai.configure(api_key=api_key)
    print("🔍 Consultando modelos disponíveis para sua chave...\n")
    
    try:
        # Lista todos os modelos disponíveis
        for m in genai.list_models():
            # Filtra apenas os que geram texto (generateContent)
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Disponível: {m.name}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")