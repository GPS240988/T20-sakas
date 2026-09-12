import json
import re

# Let's inspect all items in hda_tables_utf8.txt for Alquimicos, Aparatos, Bebidas, Animais, Veiculos, Capangas, Melhorias
with open('scripts/hda_tables_utf8.txt', 'r', encoding='utf-8') as f:
    hda_txt = f.read()

# Let's inspect all items in ameacas_tables_utf8.txt for Alquimicos, Materiais, Melhorias
with open('scripts/ameacas_tables_utf8.txt', 'r', encoding='utf-8') as f:
    ada_txt = f.read()

print("HDA text length:", len(hda_txt))
print("ADA text length:", len(ada_txt))
