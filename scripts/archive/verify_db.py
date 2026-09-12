import json

with open('data/t20_canonical_database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

print(f"Total de registros na base canônica: {len(db)}")
categories = {}
for e in db:
    c = e.get("category", "outros")
    categories[c] = categories.get(c, 0) + 1

for c, count in categories.items():
    print(f"- {c}: {count}")

print("\n--- Exemplos de Entidades Extraídas ---")
sample_names = ['Bola de Fogo', 'Curar Ferimentos', 'Armadura Arcana', 'Agarrado', 'Agarrar', 'Luta']
for name in sample_names:
    matching = [e for e in db if e.get("name") == name]
    if matching:
        item = matching[0]
        print(f"\n[{item['category'].upper()}] {item['name']} (ID: {item['id']})")
        print(f"Resumo: {item.get('summary', item.get('description', ''))[:100]}...")
        print(f"Fonte: {item['sources'][0]['book']}, Pág. {item['sources'][0]['page']}")
