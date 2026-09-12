import json
import re
import os

categories_dir = "data/categories"

# 1. Ajustar páginas em condicoes.json (JDA offset de -6 páginas em relação ao índice PDF)
with open(f"{categories_dir}/condicoes.json", "r", encoding="utf-8") as f:
    condicoes = json.load(f)
for c in condicoes:
    for s in c.get("sources", []):
        if "Jogo do Ano" in s.get("book", ""):
            # Página 400 do PDF corresponde à página 394 do livro impresso
            s["page"] = 394
with open(f"{categories_dir}/condicoes.json", "w", encoding="utf-8") as f:
    json.dump(condicoes, f, ensure_ascii=False, indent=2)

# 2. Ajustar páginas em manobras.json (JDA página 232 do livro)
with open(f"{categories_dir}/manobras.json", "r", encoding="utf-8") as f:
    manobras = json.load(f)
for m in manobras:
    for s in m.get("sources", []):
        if "Jogo do Ano" in s.get("book", ""):
            s["page"] = 232
with open(f"{categories_dir}/manobras.json", "w", encoding="utf-8") as f:
    json.dump(manobras, f, ensure_ascii=False, indent=2)

# 3. Ajustar páginas em pericias.json (JDA página 114 a 124 do livro)
with open(f"{categories_dir}/pericias.json", "r", encoding="utf-8") as f:
    pericias = json.load(f)
for p in pericias:
    for s in p.get("sources", []):
        if "Jogo do Ano" in s.get("book", ""):
            # Subtrai 6 do índice original
            old_p = s.get("page", 120)
            s["page"] = max(114, old_p - 6)
with open(f"{categories_dir}/pericias.json", "w", encoding="utf-8") as f:
    json.dump(pericias, f, ensure_ascii=False, indent=2)

# 4. Ajustar páginas em magias.json
with open(f"{categories_dir}/magias.json", "r", encoding="utf-8") as f:
    magias = json.load(f)
for sp in magias:
    for s in sp.get("sources", []):
        if "Jogo do Ano" in s.get("book", ""):
            old_p = s.get("page", 184)
            s["page"] = max(178, old_p - 6)
        elif "Heróis" in s.get("book", ""):
            old_p = s.get("page", 254)
            s["page"] = max(252, old_p - 2)
        elif "Ameaças" in s.get("book", ""):
            old_p = s.get("page", 406)
            s["page"] = max(404, old_p - 2)
with open(f"{categories_dir}/magias.json", "w", encoding="utf-8") as f:
    json.dump(magias, f, ensure_ascii=False, indent=2)

# 5. Ajustar páginas em tesouros.json (JDA pág 328 a 333)
with open(f"{categories_dir}/tesouros.json", "r", encoding="utf-8") as f:
    tesouros = json.load(f)
for tr in tesouros:
    for s in tr.get("sources", []):
        if "Jogo do Ano" in s.get("book", ""):
            old_p = s.get("page", 334)
            s["page"] = max(328, old_p - 6)
with open(f"{categories_dir}/tesouros.json", "w", encoding="utf-8") as f:
    json.dump(tesouros, f, ensure_ascii=False, indent=2)

# 6. Ajustar páginas em regras.json (JDA pág 230 a 236)
with open(f"{categories_dir}/regras.json", "r", encoding="utf-8") as f:
    regras = json.load(f)
for r in regras:
    for s in r.get("sources", []):
        if "Jogo do Ano" in s.get("book", ""):
            old_p = s.get("page", 236)
            s["page"] = max(230, old_p - 6)
with open(f"{categories_dir}/regras.json", "w", encoding="utf-8") as f:
    json.dump(regras, f, ensure_ascii=False, indent=2)

# Recompilar a base de dados consolidada
os.system("python scripts/compile_all_categories.py")

print("Ajuste de numeração de páginas impresso concluído em todo o sistema!")
