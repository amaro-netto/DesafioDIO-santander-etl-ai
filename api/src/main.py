import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Santander Dev Week (Mock API)")

# --- 1. Modelagem de Dados (Segurança e Validação) ---
class News(BaseModel):
    icon: str
    description: str

class Account(BaseModel):
    number: str
    agency: str

class User(BaseModel):
    id: int
    name: str
    account: Optional[Account] = None
    news: List[News] = []

# --- 2. Funções Auxiliares (Acesso a Dados) ---
DB_PATH = "api/src/database.json"

def load_db() -> List[dict]:
    """Lê o banco de dados JSON"""
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_db(data: List[dict]):
    """Salva as alterações no JSON"""
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- 3. Endpoints (Rotas da API) ---

@app.get("/users", response_model=List[User])
def get_all_users():
    """Retorna todos os usuários"""
    return load_db()

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """Busca um usuário pelo ID"""
    db = load_db()
    # Filtra usuário (List Comprehension - Pythonico e eficiente)
    user = next((u for u in db if u["id"] == user_id), None)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: User):
    """Atualiza um usuário (Usaremos para salvar a News da IA)"""
    db = load_db()
    
    # Encontra o índice do usuário na lista
    index = next((i for i, u in enumerate(db) if u["id"] == user_id), None)
    
    if index is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Atualiza os dados preservando o ID original
    # O model_dump() converte o objeto Pydantic para dicionário
    updated_data = user_update.model_dump()
    db[index] = updated_data
    
    save_db(db) # Persiste no arquivo
    return updated_data