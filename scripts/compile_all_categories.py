import json
import os

categories_dir = "data/categories"
os.makedirs(categories_dir, exist_ok=True)

# 1. Carregar as condições, manobras, perícias e regras existentes
with open("data/t20_canonical_database.json", "r", encoding="utf-8") as f:
    existing_db = json.load(f)

condicoes = [e for e in existing_db if e.get("category") == "condicao"]
for c in condicoes:
    if not c.get("subcategory"):
        if c.get("type") in ["Mental", "Medo"]:
            c["subcategory"] = "Condições Mentais"
        elif c.get("type") in ["Movimento", "Sentidos"]:
            c["subcategory"] = "Condições Físicas"
        elif c.get("type") == "Metabólica":
            c["subcategory"] = "Condições Metabólicas"
        elif c["name"] in ["Machucado", "Moribundo", "Morto", "Asfixiado"]:
            c["subcategory"] = "Condições de Saúde"
        else:
            c["subcategory"] = "Condições Físicas"

with open(f"{categories_dir}/condicoes.json", "w", encoding="utf-8") as f:
    json.dump(condicoes, f, ensure_ascii=False, indent=2)

manobras = [e for e in existing_db if e.get("category") == "manobra"]
for m in manobras:
    m["subcategory"] = "Manobras de Combate"

with open(f"{categories_dir}/manobras.json", "w", encoding="utf-8") as f:
    json.dump(manobras, f, ensure_ascii=False, indent=2)

pericias = [e for e in existing_db if e.get("category") == "pericia"]
for p in pericias:
    p["subcategory"] = "Perícias Gerais"

with open(f"{categories_dir}/pericias.json", "w", encoding="utf-8") as f:
    json.dump(pericias, f, ensure_ascii=False, indent=2)

regras = [e for e in existing_db if e.get("category") == "regra"]
for r in regras:
    if not r.get("subcategory"):
        r["subcategory"] = "Combate"

with open(f"{categories_dir}/regras.json", "w", encoding="utf-8") as f:
    json.dump(regras, f, ensure_ascii=False, indent=2)

# 2. Carregar todos os arquivos de categorias
category_files = [
    "equipamentos.json",
    "tesouros.json",
    "magias.json",
    "poderes.json",
    "ameacas.json",
    "origens_distincoes.json",
    "condicoes.json",
    "manobras.json",
    "pericias.json",
    "regras.json"
]

canonical_database = []
stats = {
    "total": 0,
    "categories": {},
    "subcategories": {},
    "books_consolidated": {
        "Tormenta20 - Jogo do Ano": 0,
        "Ameaças de Arton": 0,
        "Atlas de Arton": 0,
        "Heróis de Arton": 0
    }
}

seen_ids = set()

for c_file in category_files:
    file_path = os.path.join(categories_dir, c_file)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            items = json.load(f)
            for item in items:
                # Evitar IDs duplicados
                if item["id"] in seen_ids:
                    # Encontrar e mesclar fontes
                    existing_item = next(x for x in canonical_database if x["id"] == item["id"])
                    for src in item.get("sources", []):
                        if not any(s["book"] == src["book"] for s in existing_item["sources"]):
                            existing_item["sources"].append(src)
                    continue
                    
                seen_ids.add(item["id"])
                canonical_database.append(item)
                
                cat = item.get("category", "outros")
                subcat = item.get("subcategory", "Geral")
                
                stats["categories"][cat] = stats["categories"].get(cat, 0) + 1
                stats["subcategories"][f"{cat} > {subcat}"] = stats["subcategories"].get(f"{cat} > {subcat}", 0) + 1
                
                for s in item.get("sources", []):
                    b = s.get("book", "")
                    for book_key in stats["books_consolidated"]:
                        if book_key in b or b in book_key:
                            stats["books_consolidated"][book_key] += 1

stats["total"] = len(canonical_database)

# Salvar o banco canônico unificado
with open("data/t20_canonical_database.json", "w", encoding="utf-8") as f:
    json.dump(canonical_database, f, ensure_ascii=False, indent=2)

# Salvar resumo de auditoria dos 4 livros
with open("data/consolidation_audit.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print("\n=======================================================")
print("COMPILACAO CANONICA CONCLUIDA COM SUCESSO!")
print(f"Total de Entidades Consolidadas: {stats['total']}")
print("\n--- Entidades por Categoria ---")
for cat, count in sorted(stats["categories"].items(), key=lambda x: -x[1]):
    print(f"  * {cat.upper()}: {count}")

print("\n--- Validacao de Consolidacao dos 4 Livros Oficiais ---")
for book, count in stats["books_consolidated"].items():
    print(f"  [OK] {book}: {count} referencias catalogadas")
print("=======================================================\n")
