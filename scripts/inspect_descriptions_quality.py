# -*- coding: utf-8 -*-
import json

with open('data/categories/equipamentos.json', 'r', encoding='utf-8') as f:
    equips = json.load(f)

print(f"Total equipamentos: {len(equips)}")

short_items = []
for eq in equips:
    d = eq['description']
    if len(d) < 80:
        short_items.append((eq['name'], eq['sources'][0]['book'], d))

print(f"Itens com descrição curta (< 80 chars): {len(short_items)}")
for name, book, desc in short_items:
    print(f"  - [{name}] ({book}): {desc}")
