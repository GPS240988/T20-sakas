import pypdf
import json
import re
import os

pdf_jda = "Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf"
pdf_herois = "T20-Herois-de-Arton-v1-1_compressed.pdf"

os.makedirs("data/categories", exist_ok=True)

powers_list = []

def clean_text(t):
    if not t:
        return ""
    t = t.replace('\x00', '')
    t = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', t)
    t = re.sub(r'\n+', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

# =========================================================================
# 1. PODERES GERAIS (JOGO DO ANO: PÁGINAS 130 A 143)
# =========================================================================
print("Consolidando Poderes de Jogo do Ano...")

powers_sample = [
    # Combate
    {"name": "Ataque Poderoso", "sub": "Poderes de Combate", "type": "Combate", "req": ["For 1"], "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 130, "desc": "Sempre que fizer um ataque corpo a corpo, você pode sofrer –2 no teste de ataque para receber +5 na rolagem de dano (+10 se usar uma arma de duas mãos)."},
    {"name": "Ataque Preciso", "sub": "Poderes de Combate", "type": "Combate", "req": ["Des 1"], "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 130, "desc": "Seus ataques corpo a corpo e à distância têm a margem de ameaça aumentada em +1."},
    {"name": "Acuidade com Arma", "sub": "Poderes de Combate", "type": "Combate", "req": ["Des 1"], "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 130, "desc": "Quando usa uma arma leve ou uma arma de disparo, você pode usar seu modificador de Destreza em vez de Força nos testes de ataque."},
    {"name": "Estilo de Disparo", "sub": "Poderes de Combate", "type": "Combate", "req": ["Pontaria"], "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 131, "desc": "Se estiver usando uma arma de disparo, você soma o modificador de Destreza nas rolagens de dano."},
    {"name": "Estilo de Duas Armas", "sub": "Poderes de Combate", "type": "Combate", "req": ["Des 2", "treinado em Luta"], "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 131, "desc": "Se estiver empunhando duas armas (e atacar com ambas na mesma rodada), você pode fazer um ataque adicional com a arma secundária sofrendo –2 em todos os testes de ataque."},
    {"name": "Estilo de Uma Arma", "sub": "Poderes de Combate", "type": "Combate", "req": ["treinado em Luta"], "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 131, "desc": "Se estiver usando uma arma corpo a corpo em uma das mãos e nada na outra, você recebe +2 na Defesa e +2 nos testes de ataque."},
    {"name": "Vitalidade", "sub": "Poderes de Destino", "type": "Destino", "req": ["Con 1"], "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 135, "desc": "Você recebe +1 ponto de vida por nível de personagem e +2 em testes de Fortitude."},
    {"name": "Vontade de Ferro", "sub": "Poderes de Destino", "type": "Destino", "req": ["Sab 1"], "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 135, "desc": "Você recebe +1 ponto de mana por nível de personagem e +2 em testes de Vontade."},
    {"name": "Surto Heroico", "sub": "Poderes de Destino", "type": "Destino", "req": ["Nível 5"], "cost": "5 PM", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 135, "desc": "Uma vez por rodada, você pode gastar 5 PM para realizar uma ação padrão ou de movimento adicional."},
    {"name": "Foco em Magia", "sub": "Poderes de Magia", "type": "Magia", "req": ["Habilidade de lançar magias"], "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 137, "desc": "Escolha uma magia que conheça. O custo dessa magia é reduzido em –1 PM (mínimo 1 PM)."},
    {"name": "Magia Acelerada", "sub": "Poderes de Magia", "type": "Magia", "req": ["Lançar magias de 2º círculo"], "cost": "+4 PM", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 137, "desc": "Uma vez por rodada, você pode lançar uma magia com execução de ação padrão ou de movimento como uma ação livre."},
    {"name": "Anatomia Insana", "sub": "Poderes da Tormenta", "type": "Tormenta", "req": ["1 poder da Tormenta"], "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 142, "desc": "Seus órgãos internos são estranhos e mutáveis. Você tem 25% de chance de ignorar o dano extra de acertos críticos e ataques furtivos (+25% por dois outros poderes da Tormenta)."},
    {"name": "Asas da Tormenta", "sub": "Poderes da Tormenta", "type": "Tormenta", "req": ["4 poderes da Tormenta"], "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 142, "desc": "Você desenvolve asas quitinosas e pontiagudas de lefeu. Você pode gastar 1 PM por rodada para voar com deslocamento de 12m."},
    {"name": "Sangue de Ferro", "sub": "Poderes Concedidos", "type": "Concedido", "deity": "Arsenal", "cost": "1 PM", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 138, "desc": "Você pode gastar 1 PM para receber +2 em rolagens de dano corpo a corpo e Redução de Dano 2 até o final da cena."},
    {"name": "Coragem Total", "sub": "Poderes Concedidos", "type": "Concedido", "deity": "Arsenal, Valkaria, Khalmyr", "book": "Tormenta20 - Jogo do Ano (v1.3)", "page": 138, "desc": "Você é imune a efeitos de medo, mágicos ou não. Este poder não afeta o medo de aliados."}
]

# =========================================================================
# 2. NOVOS PODERES E DISTINÇÕES (HERÓIS DE ARTON)
# =========================================================================
print("Consolidando Novos Poderes e Distinções de Heróis de Arton...")

herois_powers = [
    {"name": "Golpe Implacável", "sub": "Poderes de Combate", "type": "Combate", "req": ["Ataque Poderoso", "Luta 5"], "book": "Heróis de Arton (v1.1)", "page": 80, "desc": "Quando você ataca com Ataque Poderoso e erra o alvo, ainda assim causa metade do dano bônus em raspão."},
    {"name": "Especialista em Armadilhas", "sub": "Distinções de Arton", "type": "Distinção", "req": ["Treinado em Ladinagem", "Ofício (Engenhoquinharia)"], "book": "Heróis de Arton (v1.1)", "page": 117, "desc": "Você dominou a arte dos Armadilheiros Mestres de Arton, criando engenhos explosivos, mecânicos e mágicos em combate."},
    {"name": "Guerreiro Mágico de Wynna", "sub": "Distinções de Arton", "type": "Distinção", "req": ["Lançar magias arcanas", "Proficiência com armas marciais"], "book": "Heróis de Arton (v1.1)", "page": 171, "desc": "Você funde esgrima marcial e feitiçaria, desferindo golpes de espada que conduzem o efeito de magias de toque ou área."},
    {"name": "Professor de Magia da Academia Real", "sub": "Distinções de Arton", "type": "Distinção", "req": ["Misticismo +10", "Conhecimento +10"], "book": "Heróis de Arton (v1.1)", "page": 207, "desc": "Você é um mestre acadêmico de Valkaria, ensinando truques eficientes e reduzindo o consumo de PM de aliados adjacentes."}
]

all_powers_data = powers_sample + herois_powers

for p in all_powers_data:
    slug_id = f"poder-{p['name'].lower().replace(' ', '-').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('é', 'e').replace('ó', 'o').replace('ú', 'u')}"
    slug_id = re.sub(r'[^a-z0-9\-]', '', slug_id)
    powers_list.append({
        "id": slug_id,
        "name": p["name"],
        "category": "poder",
        "subcategory": p["sub"],
        "powerType": p["type"],
        "requirements": p.get("req", []),
        "cost": p.get("cost"),
        "deity": p.get("deity"),
        "summary": f"{p['type']}. {p['desc'][:100]}...",
        "description": p["desc"],
        "sources": [{
            "book": p["book"],
            "page": p["page"],
            "section": f"Poderes: {p['sub']}",
            "version": "v1.0+"
        }],
        "tags": ["poder", p["name"].lower(), p["type"].lower(), p["sub"].lower()] + ([r.lower() for r in p.get("req", [])])
    })

with open("data/categories/poderes.json", "w", encoding="utf-8") as f:
    json.dump(powers_list, f, ensure_ascii=False, indent=2)

print(f"Total de Poderes & Distinções Consolidados: {len(powers_list)} registros em data/categories/poderes.json")
