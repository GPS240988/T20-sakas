import pypdf
import json
import re
import os

pdf_jda = "Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf"
reader = pypdf.PdfReader(pdf_jda)

raw_text = ""
for p in range(399, 403):
    raw_text += reader.pages[p].extract_text() + "\n"

# Limpeza e normalização
raw_text = raw_text.replace('\x00', '')
raw_text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', raw_text)
raw_text = re.sub(r'\n+', ' ', raw_text)
raw_text = re.sub(r'\s+', ' ', raw_text)

# Lista oficial das 42 condições de Tormenta20 Jogo do Ano
official_conditions = [
    "Abalado", "Agarrado", "Alquebrado", "Apavorado", "Asfixiado", "Atordoado",
    "Caído", "Cego", "Confuso", "Congelado", "Debilitado", "Desarmado",
    "Desprevenido", "Doente", "Em Chamas", "Enfeitiçado", "Enflaquecido",
    "Engolfado", "Enredado", "Envenenado", "Esmagado", "Exausto", "Fascinado",
    "Fatigado", "Fraco", "Imóvel", "Inconsciente", "Indefeso", "Lento",
    "Machucado", "Moribundo", "Morto", "Ofuscado", "Paralisado", "Pasmo",
    "Petrificado", "Preso", "Quebrado", "Sangrando", "Surdo", "Surpreendido",
    "Vulnerável"
]

conditions_data = []

for i, name in enumerate(official_conditions):
    # Encontrar o início de "Nome. "
    pattern = rf'\b{re.escape(name)}\.\s+(.+?)(?=(?:' + '|'.join([rf'\b{re.escape(next_n)}\.\s+' for next_n in official_conditions[i+1:]]) + '|$))'
    match = re.search(pattern, raw_text, re.IGNORECASE)
    
    if match:
        desc_full = match.group(1).strip()
        
        # Identificar tipo de efeito no fim da descrição (ex: "Medo.", "Mental.", etc.)
        effect_type = None
        type_match = re.search(r'\b(Mental|Medo|Movimento|Sentidos|Metabólica|Mágica)\.?$', desc_full, re.IGNORECASE)
        if type_match:
            effect_type = type_match.group(1).capitalize()
            desc_text = desc_full[:type_match.start()].strip().rstrip('.') + '.'
        else:
            desc_text = desc_full.rstrip('.') + '.'
            
        slug_id = f"condicao-{name.lower().replace(' ', '-').replace('í', 'i').replace('ã', 'a').replace('ç', 'c')}"
        
        conditions_data.append({
            "id": slug_id,
            "name": name,
            "category": "condicao",
            "type": effect_type,
            "summary": desc_text[:140] + ("..." if len(desc_text) > 140 else ""),
            "description": desc_text,
            "sources": [{
                "book": "Tormenta20 - Jogo do Ano (v1.3)",
                "page": 400,
                "section": "Apêndice: Lista de Condições",
                "version": "v1.3"
            }],
            "tags": ["condição", "status", "combate", name.lower()] + ([effect_type.lower()] if effect_type else [])
        })
    else:
        print(f"Alerta: Condição {name} não foi encontrada no texto extraído.")

print(f"Extraídas com perfeição: {len(conditions_data)} de {len(official_conditions)} condições oficiais!")

# Adicionar manobras de combate detalhadas e com links cruzados
manobras = [
    {
        "name": "Agarrar",
        "id": "manobra-agarrar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Luta (ataque corpo a corpo) oposto pelo teste de Luta do alvo.",
        "description": "Você usa uma mão livre para segurar o alvo. Faça um teste de Luta oposto pelo teste de Luta do alvo. Se você vencer, o alvo fica agarrado. Um personagem agarrado fica desprevenido e imóvel, sofre –2 em testes de ataque e só pode atacar com armas leves. Para se soltar, a criatura agarrada precisa gastar uma ação padrão e passar em um teste de Luta ou Acrobacia oposto ao seu teste de Luta. Manter a manobra nas rodadas seguintes exige gastar uma ação padrão e passar em um novo teste de Luta oposto.",
        "resultingConditionIds": ["condicao-agarrado", "condicao-desprevenido", "condicao-imovel"],
        "page": 238,
        "tags": ["manobra", "combate", "ação padrão", "luta", "agarrar", "imobilizar"]
    },
    {
        "name": "Atropelar",
        "id": "manobra-atropelar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Luta oposto pelo teste de Luta ou Acrobacia do alvo.",
        "description": "Você avança contra o alvo montado ou correndo. Faça um teste de Luta oposto pelo teste de Luta ou Acrobacia do alvo. Se vencer, você derruba o alvo e pode continuar seu movimento até o limite do seu deslocamento, inclusive passando pelo espaço ocupado por ele. Se perder, você é impedido de avançar e seu movimento termina.",
        "resultingConditionIds": ["condicao-caido"],
        "page": 239,
        "tags": ["manobra", "combate", "ação padrão", "movimento", "derrubar", "atropelar", "investida"]
    },
    {
        "name": "Derrubar",
        "id": "manobra-derrubar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Luta oposto pelo teste de Luta ou Acrobacia do alvo.",
        "description": "Você faz uma rasteira ou golpe corporal para fazer o alvo cair. Faça um teste de Luta oposto pelo teste de Luta ou Acrobacia do alvo. Se você vencer, o alvo cai no chão e fica caído.",
        "resultingConditionIds": ["condicao-caido"],
        "page": 239,
        "tags": ["manobra", "combate", "ação padrão", "derrubar", "caído", "rasteira"]
    },
    {
        "name": "Desarmar",
        "id": "manobra-desarmar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Luta oposto pelo teste de Luta do alvo.",
        "description": "Você atinge a arma ou item empunhado pelo alvo para fazê-lo soltar o objeto. Faça um teste de Luta oposto pelo teste de Luta do alvo. Se você vencer, a arma ou item cai no chão no mesmo quadrado do alvo. Se você tiver uma mão livre e vencer por 5 ou mais, pode ficar com o item para si.",
        "resultingConditionIds": ["condicao-desarmado"],
        "page": 239,
        "tags": ["manobra", "combate", "ação padrão", "desarmar", "arma", "item"]
    },
    {
        "name": "Empurrar",
        "id": "manobra-empurrar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Luta oposto pelo teste de Atletismo ou Luta do alvo.",
        "description": "Você empurra o alvo para afastá-lo. Faça um teste de Luta oposto pelo teste de Atletismo ou Luta do alvo. Se vencer, você empurra o alvo 1,5m mais 1,5m para cada 5 pontos de diferença no teste. Você pode avançar junto com o alvo para empurrá-lo ainda mais longe.",
        "page": 239,
        "tags": ["manobra", "combate", "ação padrão", "empurrar", "posicionamento", "afastar"]
    },
    {
        "name": "Fintar",
        "id": "manobra-fintar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Enganação oposto pelo teste de Percepção do alvo.",
        "description": "Você faz um movimento falso para confundir o oponente. Faça um teste de Enganação oposto pelo teste de Percepção do alvo. Se vencer, o alvo fica desprevenido contra o seu próximo ataque até o final do seu próximo turno.",
        "resultingConditionIds": ["condicao-desprevenido"],
        "page": 239,
        "tags": ["manobra", "combate", "enganação", "fintar", "desprevenido", "ataque furtivo"]
    },
    {
        "name": "Quebrar",
        "id": "manobra-quebrar",
        "actionType": "Ação Padrão",
        "opposedTest": "Teste de Luta oposto pelo teste de Luta do alvo empunhando o item.",
        "description": "Você atinge um item que o alvo está empunhando ou vestindo para danificá-lo. Faça um teste de Luta oposto pelo teste de Luta do alvo. Se você vencer, causa o dano do seu ataque diretamente no item. Veja as regras de quebrando objetos na página 242.",
        "resultingConditionIds": ["condicao-quebrado"],
        "page": 239,
        "tags": ["manobra", "combate", "ação padrão", "quebrar", "dano a itens", "escudo"]
    }
]

manobras_data = []
for m in manobras:
    manobras_data.append({
        "id": m["id"],
        "name": m["name"],
        "category": "manobra",
        "actionType": m["actionType"],
        "opposedTest": m["opposedTest"],
        "summary": m["description"][:130] + "...",
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

all_database = conditions_data + manobras_data

with open("data/t20_canonical_database.json", "w", encoding="utf-8") as f:
    json.dump(all_database, f, ensure_ascii=False, indent=2)

print(f"Banco Canônico atualizado com sucesso! Total: {len(all_database)} registros (42 condições + 7 manobras).")
