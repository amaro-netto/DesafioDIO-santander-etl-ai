import json
import os
import re  # Importante para formatar o texto

# Dados fixos
users = [
  {
    "id": 1,
    "name": "Dev Hiago",
    "account": { "number": "00001-1", "agency": "2030" },
    "card": { "number": "**** **** **** 1111", "limit": 1000 },
    "features": [],
    "news": []
  },
  {
    "id": 2,
    "name": "Dev Julia",
    "account": { "number": "00002-2", "agency": "2030" },
    "card": { "number": "**** **** **** 2222", "limit": 2000 },
    "features": [],
    "news": []
  },
  {
    "id": 3,
    "name": "Dev Python",
    "account": { "number": "00003-3", "agency": "2030" },
    "card": { "number": "**** **** **** 3333", "limit": 5000 },
    "features": [],
    "news": []
  },
  {
    "id": 4,
    "name": "Dev Java",
    "account": { "number": "00004-4", "agency": "2030" },
    "card": { "number": "**** **** **** 4444", "limit": 12000 },
    "features": ["PIX", "Boleto"],
    "news": []
  },
  {
    "id": 5,
    "name": "Dev Frontend",
    "account": { "number": "00005-5", "agency": "2030" },
    "card": { "number": "**** **** **** 5555", "limit": 1500 },
    "features": [],
    "news": [{"icon": "https://img.io/new", "description": "Novo app disponível"}]
  },
  {
    "id": 6,
    "name": "Tester QA",
    "account": { "number": "00006-6", "agency": "2030" },
    "card": { "number": "**** **** **** 6666", "limit": 3000 },
    "features": [],
    "news": []
  },
  {
    "id": 7,
    "name": "Scrum Master",
    "account": { "number": "00007-7", "agency": "2030" },
    "card": { "number": "**** **** **** 7777", "limit": 8000 },
    "features": [],
    "news": []
  },
  {
    "id": 8,
    "name": "Product Owner",
    "account": { "number": "00008-8", "agency": "2030" },
    "card": { "number": "**** **** **** 8888", "limit": 20000 },
    "features": ["Premium"],
    "news": []
  },
  {
    "id": 9,
    "name": "Dev DevOps",
    "account": { "number": "00009-9", "agency": "2030" },
    "card": { "number": "**** **** **** 9999", "limit": 4500 },
    "features": [],
    "news": []
  },
  {
    "id": 10,
    "name": "UX Designer",
    "account": { "number": "00010-0", "agency": "2030" },
    "card": { "number": "**** **** **** 1010", "limit": 2500 },
    "features": [],
    "news": []
  },
  {
    "id": 11,
    "name": "Ana Silva",
    "account": { "number": "00011-1", "agency": "4050" },
    "card": { "number": "**** **** **** 1212", "limit": 1100 },
    "features": [],
    "news": []
  },
  {
    "id": 12,
    "name": "Carlos Oliveira",
    "account": { "number": "00012-2", "agency": "4050" },
    "card": { "number": "**** **** **** 1313", "limit": 5500 },
    "features": [],
    "news": []
  },
  {
    "id": 13,
    "name": "Mariana Souza",
    "account": { "number": "00013-3", "agency": "4050" },
    "card": { "number": "**** **** **** 1414", "limit": 900 },
    "features": [],
    "news": [{"icon": "promo", "description": "Cashback de 10%"}]
  },
  {
    "id": 14,
    "name": "Roberto Santos",
    "account": { "number": "00014-4", "agency": "4050" },
    "card": { "number": "**** **** **** 1515", "limit": 15000 },
    "features": [],
    "news": []
  },
  {
    "id": 15,
    "name": "Fernanda Lima",
    "account": { "number": "00015-5", "agency": "4050" },
    "card": { "number": "**** **** **** 1616", "limit": 3200 },
    "features": [],
    "news": []
  },
  {
    "id": 16,
    "name": "Ricardo Gomes",
    "account": { "number": "00016-6", "agency": "4050" },
    "card": { "number": "**** **** **** 1717", "limit": 600 },
    "features": [],
    "news": []
  },
  {
    "id": 17,
    "name": "Patrícia Alves",
    "account": { "number": "00017-7", "agency": "4050" },
    "card": { "number": "**** **** **** 1818", "limit": 4000 },
    "features": [],
    "news": []
  },
  {
    "id": 18,
    "name": "Lucas Pereira",
    "account": { "number": "00018-8", "agency": "4050" },
    "card": { "number": "**** **** **** 1919", "limit": 2200 },
    "features": [],
    "news": []
  },
  {
    "id": 19,
    "name": "Juliana Costa",
    "account": { "number": "00019-9", "agency": "4050" },
    "card": { "number": "**** **** **** 2020", "limit": 7500 },
    "features": [],
    "news": []
  },
  {
    "id": 20,
    "name": "Bruno Rocha",
    "account": { "number": "00020-0", "agency": "4050" },
    "card": { "number": "**** **** **** 2121", "limit": 1000 },
    "features": [],
    "news": []
  }
]

# 1. Gera o JSON padrão (que ficaria "quebrado" em várias linhas)
json_str = json.dumps(users, indent=2, ensure_ascii=False)

# 2. TRUQUE: Usa Regex para "encolher" o objeto Account para uma linha
# Procura: "account": { ...vários espaços... } e transforma em linha única
json_str = re.sub(
    r'"account": \{\s+"number": "([^"]+)",\s+"agency": "([^"]+)"\s+\}', 
    r'"account": { "number": "\1", "agency": "\2" }', 
    json_str
)

# 3. TRUQUE: Usa Regex para "encolher" o objeto Card para uma linha
json_str = re.sub(
    r'"card": \{\s+"number": "([^"]+)",\s+"limit": ([0-9\.]+)\s+\}', 
    r'"card": { "number": "\1", "limit": \2 }', 
    json_str
)

# 4. Salva o arquivo
output_dir = os.path.join("api", "src")
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, "database.json")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(json_str) # Escrevemos a string formatada diretamente

print(f"Sucesso! Database formatada salva em: {file_path}")