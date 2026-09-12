# -*- coding: utf-8 -*-
"""
Extrator Canônico de Textos Literais (Inviolabilidade do Texto - GAME_RULES.md)
Extrai e injeta os textos ipsis litteris diretamente dos livros canônicos para os 494 equipamentos.
"""

import json
import re

with open('scripts/raw_jda_equip_text.txt', 'r', encoding='utf-8') as f:
    jda_text = f.read()

with open('scripts/raw_hda_equip_text.txt', 'r', encoding='utf-8') as f:
    hda_text = f.read()

with open('scripts/raw_ameacas_equip_text.txt', 'r', encoding='utf-8') as f:
    ameacas_text = f.read()

with open('data/categories/equipamentos.json', 'r', encoding='utf-8') as f:
    equipments = json.load(f)

# Special book aliases
item_aliases = {
    "Vara de Madeira (3m)": "Vara de Madeira",
    "Ração de viagem (por dia)": "Ração de Viagem",
    "Estábulo (por dia)": "Estábulo",
    "Instrumento Musical": "Instrumento musical",
    "Instrumentos de <ofício>": "Instrumentos de",
    "Balas": "Balas",
    "Flechas": "Flechas",
    "Pedras": "Pedras",
    "Virotes": "Virotes",
    "Peçonha comum": "Peçonha",
    "Peçonha potente": "Peçonha",
    "Peçonha concentrada": "Peçonha",
    "Estadia Comum": "Estadia",
    "Estadia Confortável": "Estadia",
    "Estadia Luxuosa": "Estadia",
    "Condução Terrestre": "Condução",
    "Condução Marítima": "Condução",
    "Condução Aérea": "Condução",
    "Serviço de Magia (1º Círculo)": "Magia",
    "Serviço de Magia (2º Círculo)": "Magia",
    "Serviço de Magia (3º Círculo)": "Magia",
    "Cavalo de guerra": "Cavalo",
    "Pônei de guerra": "Pônei",
    "Ataque Desarmado": "Ataque desarmado",
    "Aço-Rubi": "Aço-Rubi",
    "Adamante": "Adamante",
    "Gelo Eterno": "Gelo eterno",
    "Madeira Tollon": "Madeira Tollon",
    "Matéria Vermelha": "Matéria Vermelha",
    "Mitral": "Mitral",
    "Mercenário (Parceiro Iniciante)": "Mercenários",
    "Mercenário (Parceiro Veterano)": "Mercenários",
    "Mercenário (Capangas Iniciantes)": "Mercenários",
    "Mercenário (Capangas Veteranos)": "Mercenários",
    "Estrepes (bolsa para 3m)": "Estrepes",
    "Armadura de montaria pesada": "Armadura de montaria",
    "Armadura de montaria leve": "Armadura de montaria",
    "Veleiro": "Veleiro",
    "Espada de Coral": "Espada de Coral",
    "Casco de Monstro": "Casco de Monstro",
    "Couraça de Kaiju": "Couraça de Kaiju",
    "Couro de Bulette": "Couro de Bulette",
    "Cristal de Sol": "Cristal de Sol",
    "Lanajuste": "Lanajuste",
    "Pena de Kraken": "Pena de Kraken",
    "Prata": "Prata"
}

def clean_text_block(raw):
    # Unhyphenate
    t = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', raw)
    t = re.sub(r'(\w+)\xad\s*\n\s*(\w+)', r'\1\2', t)
    # Remove watermarks
    t = re.sub(r'Juliana Martins jsmartins31@gmail\.com', '', t)
    t = re.sub(r'=== PDF_PAGE_\d+ ===', '', t)
    # Clean up whitespace
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    full = ' '.join(lines)
    full = re.sub(r'\s+', ' ', full)
    return full.strip()

def get_verbatim_text(item_name, book_source, all_names):
    book_text = jda_text if "Jogo do Ano" in book_source else hda_text if "Heróis" in book_source else ameacas_text
    
    target_names = [item_name]
    if item_name in item_aliases:
        target_names.append(item_aliases[item_name])
    
    simplified = re.sub(r'\(.*?\)', '', item_name).strip()
    if simplified != item_name:
        target_names.append(simplified)
        
    for name in target_names:
        escaped = re.escape(name).replace('\\ ', r'\s+')
        
        # 1. Prose match 'Name. Text...'
        p1 = rf'(?:^|\n)\s*({escaped}\.?\s+[A-ZÀ-Ú][^\n]+(?:\n[^\n]+)*)'
        matches = list(re.finditer(p1, book_text, re.IGNORECASE))
        for m in matches:
            raw = m.group(1)
            # Skip if it looks like a table row (e.g. 'Name T$ 5 +1 0 2')
            if re.search(r'T\$\s*\d+', raw[:len(name)+18]):
                continue
            rest = raw[len(name):]
            # Stop before next known item
            stop_positions = []
            for other in all_names:
                if other.lower() == item_name.lower(): continue
                other_esc = re.escape(other).replace('\\ ', r'\s+')
                other_m = re.search(rf'(?:\n|\.\s+)({other_esc}\.|\n{other_esc}\n)', rest, re.IGNORECASE)
                if other_m:
                    stop_positions.append(other_m.start())
            hdr_m = re.search(r'(\n=== PDF_PAGE_|\nTabela 3-|\n[A-ZÀ-Ú\s]{4,30}\n)', rest)
            if hdr_m:
                stop_positions.append(hdr_m.start())
            if stop_positions:
                end_pos = min(stop_positions)
                desc = raw[:len(name) + end_pos].strip()
            else:
                desc = raw.strip()
            res = clean_text_block(desc)
            if len(res) > 35:
                return res

        # 2. Section header match 'Name\nText...'
        p2 = rf'(?:^|\n)\s*({escaped}\s*\n[A-ZÀ-Ú][^\n]+(?:\n[^\n]+)*)'
        matches2 = list(re.finditer(p2, book_text, re.IGNORECASE))
        for m in matches2:
            raw = m.group(1)
            if re.search(r'T\$\s*\d+', raw[:len(name)+18]):
                continue
            rest = raw[len(name):]
            stop_positions = []
            for other in all_names:
                if other.lower() == item_name.lower(): continue
                other_esc = re.escape(other).replace('\\ ', r'\s+')
                other_m = re.search(rf'(?:\n|\.\s+)({other_esc}\.|\n{other_esc}\n)', rest, re.IGNORECASE)
                if other_m:
                    stop_positions.append(other_m.start())
            hdr_m = re.search(r'(\n=== PDF_PAGE_|\nTabela 3-|\n[A-ZÀ-Ú\s]{4,30}\n)', rest)
            if hdr_m:
                stop_positions.append(hdr_m.start())
            if stop_positions:
                end_pos = min(stop_positions)
                desc = raw[:len(name) + end_pos].strip()
            else:
                desc = raw.strip()
            res = clean_text_block(desc)
            if len(res) > 35:
                return res

    return None

all_names_list = [e["name"] for e in equipments]

updated = 0
kept = 0

for item in equipments:
    name = item["name"]
    book = item["sources"][0]["book"]
    
    verbatim = get_verbatim_text(name, book, all_names_list)
    if verbatim:
        item["description"] = verbatim
        updated += 1
    else:
        kept += 1
        
    # Update summary to match exact stats + verbatim start
    table_data = item.get("tableData", {})
    summary_parts = []
    if item.get("subcategory"): summary_parts.append(item["subcategory"])
    if item.get("subtype") and item["subtype"] != item["subcategory"]: summary_parts.append(item["subtype"])
    if table_data.get("defenseBonus"): summary_parts.append(f"Defesa {table_data['defenseBonus']}")
    if table_data.get("damage"): summary_parts.append(f"Dano {table_data['damage']} ({table_data.get('critical', 'x2')})")
    if table_data.get("price"): summary_parts.append(f"Preço: {table_data['price']}")
    if table_data.get("space") is not None and table_data["space"] != 0: summary_parts.append(f"Espaço: {table_data['space']}")
    item["summary"] = " | ".join(summary_parts) + f". {item['description'][:90]}..."

print("="*60)
print(f"CONSOLIDAÇÃO LITERAL CONCLUÍDA:")
print(f"Itens atualizados com texto verbatim: {updated}")
print(f"Itens mantidos com base canônica: {kept}")
print(f"Total: {len(equipments)}")
print("="*60)

with open('data/categories/equipamentos.json', 'w', encoding='utf-8') as f:
    json.dump(equipments, f, ensure_ascii=False, indent=2)

print("Gravado com sucesso em 'data/categories/equipamentos.json'")
