import pandas as pd
import requests
import json
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

# --- 1. CONFIGURAÇÃO INICIAL E SEGURANÇA ---
# Localiza e carrega o arquivo .env automaticamente
env_path = find_dotenv()
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")
sdw2023_api_url = os.getenv("SDW2023_API_URL", "http://127.0.0.1:8000")

# Debug para garantir que a chave foi lida
print("-" * 50)
if not api_key:
    print("❌ ERRO GRAVE: A variável GEMINI_API_KEY não foi encontrada!")
    print(f"   Arquivo .env procurado em: {env_path}")
else:
    print(f"🔑 Chave carregada com sucesso! (Início: {api_key[:6]}...)")
    # Configura a biblioteca do Google (type: ignore evita erro falso do Pylance no VS Code)
    genai.configure(api_key=api_key) # type: ignore
print("-" * 50)

# --- 2. FUNÇÕES DO PIPELINE (ETL) ---

def get_user(id):
    """
    EXTRACT: Busca os dados do usuário na API (Backend).
    """
    try:
        response = requests.get(f"{sdw2023_api_url}/users/{id}")
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.ConnectionError:
        print(f"❌ Erro: A API local parece estar desligada em {sdw2023_api_url}")
        return None

def generate_ai_news(user):
    """
    TRANSFORM: Gera uma mensagem de marketing usando o Google Gemini.
    """
    # Fallback se a chave não existir
    if not api_key:
        return "Invista com segurança e planeje seu futuro!"

    try:
        # Usando o modelo gemini-2.0-flash (type: ignore evita erro falso do Pylance)
        model = genai.GenerativeModel("gemini-2.0-flash") # type: ignore
        
        prompt = (
            f"Você é um especialista em investimentos do banco Santander. "
            f"Escreva uma mensagem muito curta (máximo 100 caracteres), persuasiva e personalizada "
            f"para o cliente {user['name']} sobre a importância de investir dinheiro."
        )
        
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"⚠️ Erro ao chamar o Gemini: {e}")
        return "Invista hoje para colher amanhã!"

def update_user(user):
    """
    LOAD: Envia os dados atualizados de volta para a API.
    """
    try:
        response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro no Load: {e}")
        return False

# --- 3. ORQUESTRAÇÃO (MAIN) ---

def run_pipeline():
    # Caminho seguro para o arquivo CSV (funciona em qualquer pasta)
    csv_path = os.path.join('etl', 'data', 'SDW2023.csv')
    
    try:
        df = pd.read_csv(csv_path)
        user_ids = df['UserID'].tolist()
        print(f"📋 IDs encontrados na planilha: {user_ids}")
        print(f"ℹ️  Modo Free Tier: Aguardando 60 segundos entre requisições...")
    except FileNotFoundError:
        print(f"❌ Arquivo CSV não encontrado em: {csv_path}")
        print("   Verifique se a pasta 'data' e o arquivo 'SDW2023.csv' existem.")
        return

    # Loop principal com índice (enumerate) para controlar a pausa
    for i, user_id in enumerate(user_ids):
        print(f"\n🔄 [{i+1}/{len(user_ids)}] Processando UserID {user_id}...")

        # A. Extract
        user = get_user(user_id)
        if not user:
            print(f"   ⏭️ Usuário {user_id} não encontrado na API. Pulando.")
            continue
        
        print(f"   👤 Cliente: {user['name']}")

        # B. Transform
        news_content = generate_ai_news(user)
        print(f"   🤖 Gemini Sugere: '{news_content}'")
        
        # Adiciona a nova mensagem à lista de news do usuário
        user['news'].append({
            "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
            "description": news_content
        })

        # C. Load
        success = update_user(user)
        if success:
            print(f"   💾 Sucesso! Dados atualizados na API.")
        else:
            print(f"   ❌ Falha ao salvar dados.")
        
        # --- THROTTLING (FREIO) ---
        # Se NÃO for o último item da lista, espera 60 segundos
        if i < len(user_ids) - 1:
            print("   ⏳ Aguardando 60s para respeitar a cota do Google...")
            time.sleep(60)

if __name__ == '__main__':
    run_pipeline()