import pypdf
import json
import re
import os

pdf_jda = "Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf"
pdf_ameacas = "Ameacas-de-Arton-v1.0-17-11-2023_compressed.pdf"
pdf_herois = "T20-Herois-de-Arton-v1-1_compressed.pdf"

os.makedirs("data/categories", exist_ok=True)

def clean_text(t):
    if not t:
        return ""
    t = t.replace('\x00', '')
    t = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', t)
    t = re.sub(r'\n+', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def parse_spells_from_text(raw_text, book_name, base_page, default_sub="Magias Arcanas"):
    text_norm = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', raw_text)
    
    spell_header_pattern = re.compile(
        r'(?:<<<PAGE_(\d+)>>>\s*)?([A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇ][A-Za-zà-ÿ\s/’\'-]+?)\n\s*(Arcana|Divina|Universal)\s+([1-5])\s*\((Abjura[çc][ãa]o|Adivinha[çc][ãa]o|Convoca[çc][ãa]o|Encantamento|Evoca[çc][ãa]o|Ilus[ãa]o|Necromancia|Transmuta[çc][ãa]o)\)',
        re.IGNORECASE
    )
    
    matches = list(spell_header_pattern.finditer(text_norm))
    spells = []
    
    for i, m in enumerate(matches):
        spell_name = clean_text(m.group(2))
        spell_name = re.sub(r'(?:Capítulo\s+Quatro|Novas\s+Magias|Novas\s+Magias\s+Arcanas|\d+)', '', spell_name).strip()
        if not spell_name or len(spell_name) < 3:
            continue
            
        spell_type = m.group(3).capitalize()
        circle = int(m.group(4))
        school = m.group(5).capitalize()
        
        start_pos = m.end()
        end_pos = matches[i+1].start() if i + 1 < len(matches) else len(text_norm)
        
        body = text_norm[start_pos:end_pos]
        
        page_matches = re.findall(r'<<<PAGE_(\d+)>>>', text_norm[m.start():end_pos])
        current_page = int(page_matches[0]) if page_matches else base_page
        
        body = re.sub(r'<<<PAGE_\d+>>>', '', body)
        
        exec_m = re.search(r'Execu[çc][ãa]o:\s*([^;]+?);', body, re.IGNORECASE)
        alcance_m = re.search(r'Alcance:\s*([^;]+?);', body, re.IGNORECASE)
        alvo_m = re.search(r'(Alvo|Área|Efeito):\s*([^;]+?);', body, re.IGNORECASE)
        duracao_m = re.search(r'Dura[çc][ãa]o:\s*([^;\.\n]+?)(?:;|\.|\n)', body, re.IGNORECASE)
        res_m = re.search(r'Resist[êe]ncia:\s*([^\.\n]+?)(?:\.|\n)', body, re.IGNORECASE)
        
        execucao = clean_text(exec_m.group(1)) if exec_m else "Padrão"
        alcance = clean_text(alcance_m.group(1)) if alcance_m else "Curto"
        alvo_area = clean_text(alvo_m.group(2)) if alvo_m else ""
        duracao = clean_text(duracao_m.group(1)) if duracao_m else "Instantânea"
        resistencia = clean_text(res_m.group(1)) if res_m else None
        
        enhancements = []
        desc_start = 0
        param_matches = [m_p for m_p in [exec_m, alcance_m, alvo_m, duracao_m, res_m] if m_p]
        if param_matches:
            last_param = max(param_matches, key=lambda x: x.end())
            desc_start = last_param.end()
        
        spell_content = body[desc_start:].strip()
        enh_parts = re.split(r'(\+(?:\d+)\s*PM:?|Truque:?)', spell_content)
        
        main_desc = clean_text(enh_parts[0])
        for idx in range(1, len(enh_parts), 2):
            cost_tag = enh_parts[idx].strip().rstrip(':')
            enh_text = clean_text(enh_parts[idx+1]) if idx+1 < len(enh_parts) else ""
            if enh_text:
                enhancements.append({
                    "cost": cost_tag,
                    "description": enh_text
                })
        
        mana_cost_map = {1: 1, 2: 3, 3: 6, 4: 10, 5: 15}
        mana_cost = mana_cost_map.get(circle, 1)
        
        slug_id = f"magia-{spell_name.lower().replace(' ', '-').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('é', 'e').replace('ó', 'o').replace('ú', 'u').replace('ê', 'e').replace('á', 'a').replace('ô', 'o')}"
        slug_id = re.sub(r'[^a-z0-9\-]', '', slug_id)
        
        subcategory = f"Magias {spell_type}s"
        if "Ameaças" in book_name:
            subcategory = "Magias de Ameaças"
        elif "Heróis" in book_name:
            subcategory = "Magias de Heróis"
            
        spells.append({
            "id": slug_id,
            "name": spell_name,
            "category": "magia",
            "subcategory": subcategory,
            "spellType": spell_type,
            "circle": circle,
            "school": school,
            "manaCost": mana_cost,
            "execution": execucao,
            "range": alcance,
            "targetOrArea": alvo_area,
            "duration": duracao,
            "resistance": resistencia,
            "summary": f"{spell_type} {circle} ({school}). {main_desc[:100]}...",
            "description": main_desc,
            "enhancements": enhancements,
            "sources": [{
                "book": book_name,
                "page": current_page,
                "section": "Magias",
                "version": "v1.0+"
            }],
            "tags": ["magia", spell_name.lower(), spell_type.lower(), f"{circle}º círculo", school.lower(), book_name.lower()]
        })
        
    return spells

all_spells = {}

# 1. Jogo do Ano (págs 184 a 217)
print("Extraindo magias de Tormenta20: Jogo do Ano...")
r_jda = pypdf.PdfReader(pdf_jda)
txt_jda = ""
for p in range(183, 217):
    txt_jda += f"\n<<<PAGE_{p+1}>>>\n" + r_jda.pages[p].extract_text() + "\n"

spells_jda = parse_spells_from_text(txt_jda, "Tormenta20 - Jogo do Ano (v1.3)", 184)
for s in spells_jda:
    all_spells[s["id"]] = s

# 2. Ameaças de Arton (págs 406 a 417)
print("Extraindo magias de Ameaças de Arton...")
r_ameacas = pypdf.PdfReader(pdf_ameacas)
txt_ameacas = ""
for p in range(405, 417):
    txt_ameacas += f"\n<<<PAGE_{p+1}>>>\n" + r_ameacas.pages[p].extract_text() + "\n"

spells_ameacas = parse_spells_from_text(txt_ameacas, "Ameaças de Arton (v1.0)", 406)
for s in spells_ameacas:
    if s["id"] in all_spells:
        # Se já existir, adiciona fonte canônica
        all_spells[s["id"]]["sources"].append(s["sources"][0])
    else:
        all_spells[s["id"]] = s

# 3. Heróis de Arton (págs 254 a 258)
print("Extraindo magias de Heróis de Arton...")
r_herois = pypdf.PdfReader(pdf_herois)
txt_herois = ""
for p in range(253, 258):
    txt_herois += f"\n<<<PAGE_{p+1}>>>\n" + r_herois.pages[p].extract_text() + "\n"

spells_herois = parse_spells_from_text(txt_herois, "Heróis de Arton (v1.1)", 254)
for s in spells_herois:
    if s["id"] in all_spells:
        all_spells[s["id"]]["sources"].append(s["sources"][0])
    else:
        all_spells[s["id"]] = s

spells_list = list(all_spells.values())
with open("data/categories/magias.json", "w", encoding="utf-8") as f:
    json.dump(spells_list, f, ensure_ascii=False, indent=2)

print(f"Total de Magias Consolidadas dos 3 Livros: {len(spells_list)} registros em data/categories/magias.json")
