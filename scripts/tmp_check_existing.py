import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/categories/poderes.json', 'r', encoding='utf-8') as f:
    powers = json.load(f)

existing_ids = {p['id'] for p in powers}
existing_names = {p['name'] for p in powers}

print(f"Total existing powers: {len(powers)}")
print(f"Sample existing IDs: {list(existing_ids)[:5]}")
