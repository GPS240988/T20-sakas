# -*- coding: utf-8 -*-
import json

with open('data/categories/equipamentos.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print("--- JDA WEAPONS DESCRIPTIONS ---")
for item in items:
    if item.get('subcategory') == 'Armas' and item['sources'][0]['book'].startswith('Tormenta20'):
        print(f"[{item['name']}]: {item['description'][:100]}...\n")
