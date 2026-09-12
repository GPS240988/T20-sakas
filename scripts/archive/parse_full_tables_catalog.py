import re
import json

with open('scripts/all_tables_exact.txt', 'r', encoding='utf-8') as f:
    full_text = f.read()

# Let's inspect JDA Tabela 3-6 (Itens Gerais) specifically
print("=== JDA TABELA 3-6 RAW TEXT ===")
jda_part = full_text[full_text.find("Tabela 3-6 Itens Gerais"):full_text.find("Tabela 3-8 Melhorias")]
for line in jda_part.split('\n'):
    if 'T$' in line or 'Item' in line or 'Vestuário' in line or 'Esotéricos' in line or 'Alquímicos' in line or 'Animais' in line or 'Veículos' in line:
        print(line)

print("\n=== HDA TABELA 3-4 RAW TEXT ===")
hda_part = full_text[full_text.find("HDA Tabela 3-4 Itens Gerais"):full_text.find("HDA Tabela 3-5 Novas Melhorias")]
for line in hda_part.split('\n'):
    if 'T$' in line or 'Item' in line or 'Vestuário' in line or 'Esotéricos' in line or 'Alquímicos' in line or 'Animais' in line or 'Veículos' in line:
        print(line)

print("\n=== AMEACAS TABELA 3-3 RAW TEXT ===")
ameacas_part = full_text[full_text.find("Ameacas Tabela 3-3 Itens Gerais"):full_text.find("Ameacas Tabela 3-4 Materiais")]
for line in ameacas_part.split('\n'):
    if 'T$' in line or 'Item' in line or 'Vestuário' in line or 'Esotéricos' in line or 'Alquímicos' in line or 'Animais' in line or 'Veículos' in line:
        print(line)
