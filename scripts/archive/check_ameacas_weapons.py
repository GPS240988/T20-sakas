# -*- coding: utf-8 -*-
import json

with open('data/categories/equipamentos.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print("--- AMEAÇAS DE ARTON WEAPONS ---")
for item in items:
    if item.get('subcategory') == 'Armas' and any('Ameaças' in s['book'] for s in item.get('sources', [])):
        print(f"[{item['name']}]: {item['description'][:110]}...\n")
