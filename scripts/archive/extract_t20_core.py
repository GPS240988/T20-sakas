import pypdf
import json
import re
import os

pdf_jda = "Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf"
reader = pypdf.PdfReader(pdf_jda)

def clean_text(t):
    t = t.replace('\x00', '')
    t = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', t) # junta palavras hifenizadas
    t = re.sub(r'\n+', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

entities = []

# 1. Extração das Condições (Apêndice: Páginas 400-403, índices 399-402)
print("Extraindo Condições do Jogo do Ano...")
condition_text = ""
for p in range(399, 403):
    condition_text += reader.pages[p].extract_text() + "\n"

# Padrão: Nome da condição com ponto seguido da descrição
# Exemplo: "Abalado. O personagem sofre -2 em testes de perícia..."
cond_blocks = re.findall(r'([A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇ][a-zà-ÿA-Z\s/\(\)]+?)\.\s+([A-Z0-9].+?)(?=(?:[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇ][a-zà-ÿA-Z\s/\(\)]+?\.\s+[A-Z0-9]|$))', condition_text, re.DOTALL)

for name, desc in cond_blocks:
    name_clean = name.strip()
    # Ignorar falsos positivos de cabeçalho
    if any(k in name_clean.lower() for k in ['apêndice', 'veja a página', 'condições com', 'algumas condições', 'tabela']):
        continue
    
    # Identificar tipo de efeito no fim do texto (ex: "Medo.", "Mental.", "Movimento.")
    effect_type = None
    m_type = re.search(r'\b(Mental|Medo|Movimento|Sentidos|Metabólica|Mágica)\.?$', desc.strip())
    if m_type:
        effect_type = m_type.group(1)
        desc_clean = desc[:m_type.start()].strip()
    else:
        desc_clean = desc.strip()
    
    desc_clean = clean_text(desc_clean)
    if len(desc_clean) < 15:
        continue

    slug_id = f"condicao-{name_clean.lower().replace(' ', '-').replace('/', '-')}"
    
    entities.append({
        "id": slug_id,
        "name": name_clean,
        "category": "condicao",
        "type": effect_type,
        "summary": desc_clean[:120] + ("..." if len(desc_clean) > 120 else ""),
        "description": desc_clean,
        "sources": [{
            "book": "Tormenta20 - Jogo do Ano (v1.3)",
            "page": 400,
            "section": "Apêndice: Lista de Condições",
            "version": "v1.3"
        }],
        "tags": ["condição", "status", "combate", name_clean.lower()] + ([effect_type.lower()] if effect_type else [])
    })

# 2. Extração das Manobras de Combate (Capítulo 5: Páginas 238-242)
print("Extraindo Manobras de Combate...")
combat_text = ""
for p in range(235, 243):
    combat_text += reader.pages[p].extract_text() + "\n"

manobras = [
    {
        "name": "Agarrar",
        "id": "manobra-agarrar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Luta (ataque corpo a corpo) oposto pelo teste de Luta do alvo.",
        "description": "Você usa uma mão livre para segurar o alvo. Faça um teste de Luta oposto pelo teste de Luta do alvo. Se você vencer, o alvo fica agarrado. Um personagem agarrado fica desprevenido e imóvel, sofre –2 em testes de ataque e só pode atacar com armas leves. Para se soltar, a criatura agarrada precisa gastar uma ação padrão e passar em um teste de Luta ou Acrobacia oposto ao seu teste de Luta. Manter a manobra nas rodadas seguintes exige gastar uma ação padrão e passar em um novo teste de Luta oposto.",
        "resultingConditionIds": ["condicao-agarrado"],
        "page": 238,
        "tags": ["manobra", "combate", "ação padrão", "luta", "agarrar"]
    },
    {
        "name": "Atropelar",
        "id": "manobra-atropelar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Luta oposto pelo teste de Luta ou Acrobacia do alvo.",
        "description": "Você avança contra o alvo montado ou correndo. Faça um teste de Luta oposto pelo teste de Luta ou Acrobacia do alvo. Se vencer, você derruba o alvo e pode continuar seu movimento até o limite do seu deslocamento, inclusive passando pelo espaço ocupado por ele. Se perder, você é impedido de avançar e seu movimento termina.",
        "resultingConditionIds": ["condicao-caído"],
        "page": 239,
        "tags": ["manobra", "combate", "ação padrão", "movimento", "derrubar", "atropelar"]
    },
    {
        "name": "Derrubar",
        "id": "manobra-derrubar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Luta oposto pelo teste de Luta ou Acrobacia do alvo.",
        "description": "Você faz uma rasteira ou golpe corporal para fazer o alvo cair. Faça um teste de Luta oposto pelo teste de Luta ou Acrobacia do alvo. Se você vencer, o alvo cai no chão e fica caído.",
        "resultingConditionIds": ["condicao-caído"],
        "page": 239,
        "tags": ["manobra", "combate", "ação padrão", "derrubar", "caído"]
    },
    {
        "name": "Desarmar",
        "id": "manobra-desarmar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Luta oposto pelo teste de Luta do alvo.",
        "description": "Você atinge a arma ou item empunhado pelo alvo para fazê-lo soltar o objeto. Faça um teste de Luta oposto pelo teste de Luta do alvo. Se você vencer, a arma ou item cai no chão no mesmo quadrado do alvo. Se você tiver uma mão livre e vencer por 5 ou mais, pode ficar com o item para si.",
        "page": 239,
        "tags": ["manobra", "combate", "ação padrão", "desarmar", "arma"]
    },
    {
        "name": "Empurrar",
        "id": "manobra-empurrar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Luta oposto pelo teste de Atletismo ou Luta do alvo.",
        "description": "Você empurra o alvo para afastá-lo. Faça um teste de Luta oposto pelo teste de Atletismo ou Luta do alvo. Se vencer, você empurra o alvo 1,5m mais 1,5m para cada 5 pontos de diferença no teste. Você pode avançar junto com o alvo para empurrá-lo ainda mais longe.",
        "page": 239,
        "tags": ["manobra", "combate", "ação padrão", "empurrar", "posicionamento"]
    },
    {
        "name": "Fintar",
        "id": "manobra-fintar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Enganação oposto pelo teste de Percepção do alvo.",
        "description": "Você faz um movimento falso para confundir o oponente. Faça um teste de Enganação oposto pelo teste de Percepção do alvo. Se vencer, o alvo fica desprevenido contra o seu próximo ataque até o final do seu próximo turno.",
        "resultingConditionIds": ["condicao-desprevenido"],
        "page": 239,
        "tags": ["manobra", "combate", "enganação", "fintar", "desprevenido"]
    },
    {
        "name": "Quebrar",
        "id": "manobra-quebrar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Luta oposto pelo teste de Luta do alvo empunhando o item.",
        "description": "Você atinge um item que o alvo está empunhando ou vestindo para danificá-lo. Faça um teste de Luta oposto pelo teste de Luta do alvo. Se você vencer, causa o dano do seu ataque diretamente no item. Veja as regras de quebrando objetos na página 242.",
        "page": 239,
        "tags": ["manobra", "combate", "ação padrão", "quebrar", "dano a itens"]
    }
]

for m in manobras:
    entities.append({
        "id": m["id"],
        "name": m["name"],
        "category": "manobra",
        "actionType": m["actionType"],
        "opposedTest": m["opposedTest"],
        "summary": m["description"][:120] + "...",
        "description": m["description"],
        "resultingConditionIds": m.get("resultingConditionIds", []),
        "sources": [{
            "book": "Tormenta20 - Jogo do Ano (v1.3)",
            "page": m["page"],
            "section": "Capítulo 5: Combate - Manobras de Combate",
            "version": "v1.3"
        }],
        "tags": m["tags"]
    })

# Salvar o banco canônico inicial consolidado
os.makedirs("data", exist_ok=True)
with open("data/t20_canonical_database.json", "w", encoding="utf-8") as f:
    json.dump(entities, f, ensure_ascii=False, indent=2)

print(f"Base Canônica inicial criada com {len(entities)} entidades registradas em data/t20_canonical_database.json")
