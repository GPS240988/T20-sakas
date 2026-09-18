import zipfile
import xml.etree.ElementTree as ET
import re
import json
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

def slugify(text):
    text = text.lower()
    text = re.sub(r'[áàâãä]', 'a', text)
    text = re.sub(r'[éèêë]', 'e', text)
    text = re.sub(r'[íìîï]', 'i', text)
    text = re.sub(r'[óòôõö]', 'o', text)
    text = re.sub(r'[úùûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def clean_text_artifacts(text):
    if not text:
        return text
    # Fix common docx line-break hyphenation/space artifacts
    text = re.sub(r'proficiên\s+cia', 'proficiência', text)
    text = re.sub(r'espí\s+ritos', 'espíritos', text)
    text = re.sub(r'mar\s+car', 'marcar', text)
    text = re.sub(r'pré\-re\s+quisitos?', lambda m: 'pré-requisito' if 'requisito' in m.group(0) and not m.group(0).endswith('s') else 'pré-requisitos', text, flags=re.IGNORECASE)
    text = re.sub(r'alcan\s+ce', 'alcance', text)
    text = re.sub(r'Purifica\s+dora', 'Purificadora', text)
    text = re.sub(r'ca\s+veleiro', 'cavaleiro', text)
    text = re.sub(r'ca\s+valeiro', 'cavaleiro', text)
    text = re.sub(r'to\s+das', 'todas', text)
    text = re.sub(r'as\s+sombrosas', 'assombrosas', text)
    text = re.sub(r'a partir Montaria Sagrada de você', 'a partir de você', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

KNOWN_TITLES = [
    # Arcanista
    "Arcano de Batalha", "Aumento de Atributo", "Caldeirão do Bruxo", "Conhecimento Mágico",
    "Contramágica Aprimorada", "Envolto em Mistério", "Escriba Arcano", "Especialista em Escola",
    "Familiar", "Fluxo de Mana", "Foco Vital", "Fortalecimento Arcano", "Herança Aprimorada",
    "Herança Superior", "Magia Pungente", "Mestre em Escola", "Poder Mágico", "Raio Arcano",
    "Raio Poderoso", "Tinta do Mago", "Alta Arcana",
    # Arcanista Variantes
    "Agrilhoar os Caídos", "Alquimia Arcana", "Apoteose Celestial", "Apoteose Dracônica",
    "Apoteose Feérica", "Apoteose Rubra", "Arcanista de Linha de Frente", "Asas de Sapo",
    "Contingência Arcana", "Contramágica Superior", "Especialista em Invocações",
    "Familiar Aprimorado", "Ingrediente Especial", "Magia Performática", "Memória Súbita",
    "O Próprio Sangue", "Raio Dividido", "Sifão de Mana", "Trama Célere", "Transliteração Impossível",
    # Paladino
    "Abençoado", "Código do Herói", "Golpe Divino", "Cura pelas Mãos", "Arma Sagrada",
    "Aura Antimagia", "Aura Ardente", "Aura de Cura", "Aura de Invencibilidade", "Aura Poderosa",
    "Fulgor Divino", "Julgamento Divino: Arrependimento", "Julgamento Divino: Autoridade",
    "Julgamento Divino: Coragem", "Julgamento Divino: Iluminação", "Julgamento Divino: Justiça",
    "Julgamento Divino: Libertação", "Julgamento Divino: Salvação", "Julgamento Divino: Vindicação",
    "Julgamento Divino: Zelo", "Orar", "Virtude Paladinesca: Caridade", "Virtude Paladinesca: Castidade",
    "Virtude Paladinesca: Compaixão", "Virtude Paladinesca: Humildade", "Virtude Paladinesca: Temperança",
    "Aura Sagrada", "Bênção da Justiça", "Égide Sagrada", "Montaria Sagrada", "Vingador Sagrado",
    # Paladino Variantes
    "Arma Juramentada", "Arma Sacramentada", "Aura Vingadora", "Bloqueio Divino", "Convicção Heróica",
    "Expurgo Sagrado", "Escudo Fraterno", "Escudo Sagrado", "Fulgor Ardente", "Hoste Celestial",
    "Investida Sagrada", "Julgamento Divino: Desafio", "Julgamento Divino: Proteção",
    "Julgamento Divino: Redenção", "Julgamento Divino: Retribuição", "Luz Purificadora",
    "Manto de Batalha", "Paladino do Reino", "Rajada Divina", "Sacrifício", "Sentença Dobrada",
    "Virtude Paladinesca: Paciência"
]

with zipfile.ZipFile('Poderes de classe e variantes.docx') as z:
    xml_content = z.read('word/document.xml')

root = ET.fromstring(xml_content)
raw_paragraphs = []
for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    texts = [node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
    full_text = ''.join(texts).strip()
    if full_text:
        raw_paragraphs.append(full_text)

current_class = None
is_variant = False
entries = []
seen_power_texts = set()

i = 0
while i < len(raw_paragraphs):
    p = raw_paragraphs[i]
    
    if p in ['ARCANISTA', 'PALADINO']:
        current_class = p.capitalize()
        is_variant = False
        i += 1
        continue
    m_var = re.match(r'PODERES VARIANTES \((.*?)\)', p, re.IGNORECASE)
    if m_var:
        current_class = m_var.group(1).strip().capitalize()
        is_variant = True
        i += 1
        continue
    
    if p in seen_power_texts:
        i += 1
        continue
    seen_power_texts.add(p)
    
    clean_p = re.sub(r'^[•\-\*]\s*', '', p).strip()
    clean_p = clean_text_artifacts(clean_p)
    
    # Merge continuation paragraph for Cura pelas Mãos
    if clean_p.startswith("A partir do 6º nível, você pode gastar +1 PM quando usa Cura pelas Mãos"):
        if entries and entries[-1]['base_name'] == "Cura pelas Mãos":
            entries[-1]['description'] += " " + clean_p
            i += 1
            continue
    
    matched_title = None
    for kt in sorted(KNOWN_TITLES, key=len, reverse=True):
        pattern = r'^' + re.escape(kt) + r'([\.\:\s]|$)'
        if re.search(pattern, clean_p):
            matched_title = kt
            break
    
    if not matched_title:
        print(f"WARNING: Could not match title for paragraph: {clean_p[:60]}")
        i += 1
        continue
    
    desc_part = clean_p[len(matched_title):].strip()
    desc_part = re.sub(r'^[\.\:]\s*', '', desc_part).strip()
    desc_part = clean_text_artifacts(desc_part)
    
    reqs = []
    m_req = re.search(r'Pré\-?re?\s*quisitos?\s*:\s*(.*?)\.?$', desc_part, re.IGNORECASE)
    if m_req:
        req_text = m_req.group(1).strip()
        req_items = [clean_text_artifacts(r.strip().rstrip('.')) for r in req_text.split(',') if r.strip()]
        reqs = req_items
    
    cost = None
    m_cost = re.search(r'(?:gastar|pagar)\s+(\d+\s*PM)', desc_part, re.IGNORECASE)
    if m_cost:
        cost = m_cost.group(1).upper()
    
    card_name = f"{matched_title} ({current_class})"
    item_id = f"poder-{slugify(matched_title)}-{slugify(current_class)}"
    
    book_name = "Heróis de Arton" if is_variant else "Tormenta20 - Jogo do Ano"
    version_str = "v1.1" if is_variant else "v1.3"
    
    summary_text = desc_part
    if len(summary_text) > 110:
        summary_text = summary_text[:107] + "..."
    summary = f"Classe. {summary_text}"
    
    tags = [
        "poder",
        card_name.lower(),
        matched_title.lower(),
        current_class.lower(),
        "classe",
        "poderes de classe"
    ]
    if is_variant:
        tags.append("poder variante")
    for r in reqs:
        tags.append(r.lower())
    
    entry = {
        "id": item_id,
        "name": card_name,
        "category": "poder",
        "subcategory": "Poderes de Classe",
        "powerType": "Classe",
        "subtype": current_class,
        "requirements": reqs,
        "cost": cost,
        "deity": None,
        "summary": summary,
        "description": desc_part,
        "sources": [
            {
                "book": book_name,
                "page": 1,
                "section": "Poderes: Poderes de Classe",
                "version": version_str
            }
        ],
        "tags": list(dict.fromkeys(tags)),
        "base_name": matched_title
    }
    
    entries.append(entry)
    i += 1

print(f"Extracted {len(entries)} class powers.")

# Clean internal fields
for e in entries:
    e.pop('base_name', None)

# Load existing poderes.json
with open('data/categories/poderes.json', 'r', encoding='utf-8') as f:
    existing_powers = json.load(f)

# Filter out any existing powers with subcategory "Poderes de Classe" or matching IDs to avoid duplicates
existing_ids = {p['id'] for p in existing_powers}

new_count = 0
for entry in entries:
    if entry['id'] in existing_ids:
        # replace existing item with clean version
        existing_powers = [p if p['id'] != entry['id'] else entry for p in existing_powers]
    else:
        existing_powers.append(entry)
        new_count += 1

print(f"Added {new_count} new entries. Total powers now: {len(existing_powers)}")

# Save updated poderes.json
with open('data/categories/poderes.json', 'w', encoding='utf-8') as f:
    json.dump(existing_powers, f, ensure_ascii=False, indent=2)

print("Updated data/categories/poderes.json successfully!")

# Run compilation script to sync canonical database
print("Running compile_all_categories.py...")
res = subprocess.run([sys.executable, 'scripts/compile_all_categories.py'], capture_output=True, text=True, encoding='utf-8')
print(res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)
