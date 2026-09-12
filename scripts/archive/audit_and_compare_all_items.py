import json
import re

with open('data/categories/equipamentos.json', 'r', encoding='utf-8') as f:
    current_equips = json.load(f)

current_map = {e['name'].strip().lower(): e for e in current_equips}
print(f"Total current equipments loaded in db: {len(current_equips)}")

with open('scripts/all_tables_exact.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect sections
sections = text.split("=========================")
print(f"Total sections extracted: {len(sections)}")

for sec in sections:
    if not sec.strip(): continue
    lines = [l.strip() for l in sec.strip().split('\n') if l.strip()]
    title = lines[0] if lines else "Unknown"
    print(f"\n--- Section: {title} ---")
    print(f"Lines count: {len(lines)}")
