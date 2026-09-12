# -*- coding: utf-8 -*-
import json
import glob

files = glob.glob('data/categories/*.json') + ['data/t20_canonical_database.json']

replacements = {
    "Tormenta20 - Jogo do Ano (v1.3)": "Tormenta20 - Jogo do Ano",
    "Heróis de Arton (v1.1)": "Heróis de Arton",
    "Ameaças de Arton (v1.0)": "Ameaças de Arton",
    "Atlas de Arton (v1.0)": "Atlas de Arton",
    "v1.3": "",
    "v1.1": "",
    "v1.0": ""
}

total_updates = 0

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = content
    for old_str, new_str in replacements.items():
        modified = modified.replace(old_str, new_str)
    
    if modified != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified)
        total_updates += 1
        print(f"Updated: {file_path}")

print(f"Cleaned version suffixes from {total_updates} JSON files.")
