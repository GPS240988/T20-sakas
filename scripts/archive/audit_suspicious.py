# -*- coding: utf-8 -*-
import json

with open('data/categories/equipamentos.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total equipment items: {len(items)}")

suspicious = []
for item in items:
    desc = item.get('description', '')
    name = item.get('name', '')
    # Check if description contains page headers or page numbers like "146", "147", "148" or intro text
    if any(header in desc for header in ["Armas 142", "Espadas bastardas", "Machados de batalha", "Livrar uma mão", "Características das Armas"]):
        suspicious.append((name, desc[:100]))

print(f"Suspicious items found: {len(suspicious)}")
for name, snippet in suspicious:
    print(f" - {name}: {snippet}")
