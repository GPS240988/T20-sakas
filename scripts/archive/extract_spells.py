import pypdf
import json
import re
import os

pdf_jda = "Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf"
reader = pypdf.PdfReader(pdf_jda)

def clean_text(t):
    if not t:
        return ""
    t = t.replace('\x00', '')
    t = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', t)
    t = re.sub(r'\n+', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

# As magias na Jogo do Ano vão da página 184 (index 183) até a página 217 (index 216)
print("Extraindo texto das páginas de magias (184 a 217)...")
full_spells_text = ""
page_map = {}

for p_idx in range(183, 217):
    p_num = p_idx + 1
    t = reader.pages[p_idx].extract_text()
    lines = t.split('\n')
    # Registrar página aproximada para cada bloco
    full_spells_text += f"\n<<<PAGE_{p_num}>>>\n" + t + "\n"

# Normalizar quebras hifenizadas no texto das magias
text_norm = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', full_spells_text)

# Padrão de cabeçalho de magia:
# Nome da Magia na linha anterior
# (Arcana|Divina|Universal) (1|2|3|4|5) \((Abjuração|Adivinhação|Convocação|Encantamento|Evocação|Ilusão|Necromancia|Transmutação)\)
spell_header_pattern = re.compile(
    r'(?:<<<PAGE_(\d+)>>>\s*)?([A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇ][A-Za-zà-ÿ\s/’\'-]+?)\n\s*(Arcana|Divina|Universal)\s+([1-5])\s*\((Abjuração|Adivinhação|Convocação|Encantamento|Evocação|Ilusão|Necromancia|Transmutação)\)',
    re.MULTILINE
)

matches = list(spell_header_pattern.finditer(text_norm))
print(f"Cabeçalhos de magias detectados: {len(matches)}")

extracted_spells = []
current_page = 184

for i, m in enumerate(matches):
    spell_name = clean_text(m.group(2))
    # Limpar qualquer resto de cabeçalho como 'Capítulo Quatro'
    spell_name = re.sub(r'Capítulo\s+Quatro', '', spell_name).strip()
    
    spell_type = m.group(3)
    circle = int(m.group(4))
    school = m.group(5)
    
    start_pos = m.end()
    end_pos = matches[i+1].start() if i + 1 < len(matches) else len(text_norm)
    
    body = text_norm[start_pos:end_pos]
    
    # Identificar se há marcador de página dentro do bloco
    page_matches = re.findall(r'<<<PAGE_(\d+)>>>', text_norm[m.start():end_pos])
    if page_matches:
        current_page = int(page_matches[0])
    
    body = re.sub(r'<<<PAGE_\d+>>>', '', body)
    
    # Extrair parâmetros: Execução, Alcance, Alvo/Área/Efeito, Duração, Resistência
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
    
    # Separar descrição e aprimoramentos
    enhancements = []
    
    # O texto da descrição vem depois dos parâmetros
    desc_start = 0
    param_matches = [m_p for m_p in [exec_m, alcance_m, alvo_m, duracao_m, res_m] if m_p]
    if param_matches:
        last_param = max(param_matches, key=lambda x: x.end())
        desc_start = last_param.end()
    
    spell_content = body[desc_start:].strip()
    
    # Buscar aprimoramentos (+X PM: ... ou Truque: ...)
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
    
    extracted_spells.append({
        "id": slug_id,
        "name": spell_name,
        "category": "magia",
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
            "book": "Tormenta20 - Jogo do Ano (v1.3)",
            "page": current_page,
            "section": "Capítulo 4: Magia - Descrição das Magias",
            "version": "v1.3"
        }],
        "tags": ["magia", spell_name.lower(), spell_type.lower(), f"{circle}º círculo", school.lower()]
    })

print(f"Total de magias extraídas com sucesso: {len(extracted_spells)}")

# Carregar banco canônico existente e mesclar
with open("data/t20_canonical_database.json", "r", encoding="utf-8") as f:
    current_db = json.load(f)

# Remover magias anteriores se houver e adicionar novas
current_db = [item for item in current_db if item.get("category") != "magia"]
current_db.extend(extracted_spells)

with open("data/t20_canonical_database.json", "w", encoding="utf-8") as f:
    json.dump(current_db, f, ensure_ascii=False, indent=2)

print(f"Banco Canônico atualizado com {len(current_db)} entidades no total!")
