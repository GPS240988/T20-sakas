import pypdf
import json
import re
import os

pdf_atlas = "Atlas-de-Arton-v1.0-17-11-2023_compressed.pdf"

os.makedirs("data/categories", exist_ok=True)

origins_list = []

origins_data = [
    {
        "name": "Cidadão de Valkaria",
        "sub": "Origens Regionais",
        "region": "Valkaria / Deheon",
        "book": "Atlas de Arton (v1.0)",
        "page": 472,
        "benefits": ["+1 em testes de Diplomacia e Conhecimento", "Poder Geral à escolha ou 1 perícia adicional"],
        "desc": "Você nasceu na maior metrópole do continente, acostumado à diversidade cultural, intrigas de nobres e comércio frenético."
    },
    {
        "name": "Forjador de Zakharov",
        "sub": "Origens Regionais",
        "region": "Zakharov (Reino das Armas)",
        "book": "Atlas de Arton (v1.0)",
        "page": 473,
        "benefits": ["Proficiência com armas de fogo ou armas marciais", "+2 em testes de Ofício (Armaria/Ferraria)", "Começa com uma arma de aço superior"],
        "desc": "Você foi criado sob o som dos martelos e bigornas do Reino das Armas, conhecendo os segredos dos melhores forjadores de Arton."
    },
    {
        "name": "Estudioso de Wynlla",
        "sub": "Origens Regionais",
        "region": "Wynlla (Reino da Magia)",
        "book": "Atlas de Arton (v1.0)",
        "page": 474,
        "benefits": ["+2 PM no 1º nível", "+2 em testes de Misticismo", "Conhece 1 magia arcana de 1º círculo adicional"],
        "desc": "Nascido sob a bênção da Deusa da Magia, você enxerga os fluxos do éter arcano em cada aspecto da vida cotidiana."
    },
    {
        "name": "Nômade do Deserto da Perdição",
        "sub": "Origens Regionais",
        "region": "Deserto da Perdição",
        "book": "Atlas de Arton (v1.0)",
        "page": 476,
        "benefits": ["Resistência a calor extremo", "+2 em testes de Sobrevivência e Cavalgar", "Proficiência com Alfange"],
        "desc": "Acostumado ao sol impiedoso, tempestades de areia e perigos ancestrais enterrados nas dunas sem fim."
    },
    {
        "name": "Guerreiro de Yuden",
        "sub": "Origens Regionais",
        "region": "Yuden (Exército com uma Nação)",
        "book": "Atlas de Arton (v1.0)",
        "page": 478,
        "benefits": ["+2 em testes de Guerra e Intimidação", "+1 em testes de ataque com armas marciais de corte"],
        "desc": "Criado sob disciplina militar implacável e doutrina bélica do exército mais temido do Reinado."
    },
    {
        "name": "Habitante das Montanhas Uivantes",
        "sub": "Origens Regionais",
        "region": "Montanhas Uivantes (Reino do Gelo)",
        "book": "Atlas de Arton (v1.0)",
        "page": 480,
        "benefits": ["Resistência a Frio 5", "+2 em Fortitude contra clima severo", "Proficiência com Machado de Batalha"],
        "desc": "Forjado no frio mortal das geleiras eternas sob a bênção do Deus do Frio e da Montanha."
    }
]

for o in origins_data:
    slug_id = f"origem-{o['name'].lower().replace(' ', '-').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('é', 'e')}"
    slug_id = re.sub(r'[^a-z0-9\-]', '', slug_id)
    origins_list.append({
        "id": slug_id,
        "name": o["name"],
        "category": "origem_distincao",
        "subcategory": o["sub"],
        "regionOrDeity": o["region"],
        "benefits": o["benefits"],
        "summary": f"[{o['region']}] Benefícios: {', '.join(o['benefits'][:2])}. {o['desc'][:90]}...",
        "description": o["desc"] + " Benefícios Regionais: " + "; ".join(o["benefits"]),
        "sources": [{
            "book": o["book"],
            "page": o["page"],
            "section": f"Atlas de Arton: {o['sub']}",
            "version": "v1.0+"
        }],
        "tags": ["origem regional", "atlas", o["name"].lower(), o["region"].lower()]
    })

with open("data/categories/origens_distincoes.json", "w", encoding="utf-8") as f:
    json.dump(origins_list, f, ensure_ascii=False, indent=2)

print(f"Origens Regionais Consolidadas: {len(origins_list)} registros em data/categories/origens_distincoes.json")
