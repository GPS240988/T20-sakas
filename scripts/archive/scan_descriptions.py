import re

with open("scripts/jda_equip_dump.txt", encoding="utf-8") as f:
    jda = f.read()

# Let's find all headers like "Nome. Descrição..."
print("=== Scanning JDA descriptions ===")
# Pattern: Word(s) at start of paragraph followed by a dot, capital letter
items_found = re.findall(r'\n([A-ZÀ-Ú][a-zà-úA-ZÀ-Ú0-9 \(\)\/\-\'\’]+?)\.\s+([A-ZÀ-Ú][^\n]+(?:\n(?![A-ZÀ-Ú][a-zà-úA-ZÀ-Ú0-9 \(\)\/\-\'\’]+\.)[^\n]+)*)', jda)
print(f"Found {len(items_found)} potential description items in JDA")
for name, desc in items_found[:20]:
    first_few = desc.replace('\n', ' ')[:80]
    print(f"- {name}: {first_few}...")
