import json

with open('data/categories/equipamentos.json', encoding='utf-8') as f:
    equips = json.load(f)

hda_armors = [e for e in equips if 'Heróis' in e['sources'][0]['book'] and e['subcategory'] == 'Armaduras & Escudos']
print(f'Total de Armaduras & Escudos em HDA: {len(hda_armors)}')
for a in hda_armors:
    def_b = a['tableData'].get('defenseBonus', 0)
    pen = a['tableData'].get('armorPenalty', 0)
    pr = a['tableData'].get('price')
    pg = a['sources'][0]['page']
    print(f"- [{a['proficiency']}] {a['name']}: Defesa +{def_b}, Pen {pen}, Preço {pr}, Pág {pg}")

print("\n--- Armaduras Leves Totais ---")
leves = [e for e in equips if e['proficiency'] == 'Armaduras Leves']
for l in leves:
    print(f"- {l['name']} ({l['sources'][0]['book']}, Pág {l['sources'][0]['page']}): Defesa +{l['tableData'].get('defenseBonus')}, Preço {l['tableData'].get('price')}")

print("\n--- Armaduras Pesadas Totais ---")
pesadas = [e for e in equips if e['proficiency'] == 'Armaduras Pesadas']
for p in pesadas:
    print(f"- {p['name']} ({p['sources'][0]['book']}, Pág {p['sources'][0]['page']}): Defesa +{p['tableData'].get('defenseBonus')}, Preço {p['tableData'].get('price')}")
