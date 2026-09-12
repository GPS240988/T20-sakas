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

database = []

# ==========================================
# 1. CONDIÇÕES OFICIAIS DE TORMENTA20
# ==========================================
print("Compilando Condições...")

appendix_conditions = [
    {
        "name": "Abalado",
        "type": "Medo",
        "desc": "O personagem sofre –2 em testes de perícia. Se ficar abalado novamente, em vez disso fica apavorado.",
        "page": 400
    },
    {
        "name": "Agarrado",
        "type": "Movimento",
        "desc": "O personagem fica desprevenido e imóvel, sofre –2 em testes de ataque e só pode atacar com armas leves. Ataques à distância contra um alvo envolvido em uma manobra agarrar têm 50% de chance de acertar o alvo errado.",
        "page": 400,
        "relatedIds": ["manobra-agarrar", "condicao-desprevenido", "condicao-imovel"]
    },
    {
        "name": "Alquebrado",
        "type": "Mental",
        "desc": "O custo em pontos de mana das habilidades do personagem aumenta em +1.",
        "page": 400
    },
    {
        "name": "Apavorado",
        "type": "Medo",
        "desc": "O personagem sofre –5 em testes de perícia e não pode se aproximar voluntariamente da fonte do medo.",
        "page": 400
    },
    {
        "name": "Atordoado",
        "type": "Mental",
        "desc": "O personagem fica desprevenido e não pode fazer ações.",
        "page": 400,
        "relatedIds": ["condicao-desprevenido"]
    },
    {
        "name": "Caído",
        "type": None,
        "desc": "O personagem sofre –5 na Defesa contra ataques corpo a corpo e recebe +5 na Defesa contra ataques à distância (cumulativos com outras condições). Além disso, sofre –5 em ataques corpo a corpo e seu deslocamento é reduzido a 1,5m.",
        "page": 400,
        "relatedIds": ["manobra-derrubar", "manobra-atropelar"]
    },
    {
        "name": "Cego",
        "type": "Sentidos",
        "desc": "O personagem fica desprevenido e lento, não pode fazer testes de Percepção para observar e sofre –5 em testes de perícias baseadas em Força ou Destreza. Todos os alvos de seus ataques recebem camuflagem total. Você é considerado cego enquanto estiver em escuridão total, a menos que tenha visão no escuro.",
        "page": 400,
        "relatedIds": ["condicao-desprevenido", "condicao-lento"]
    },
    {
        "name": "Confuso",
        "type": "Mental",
        "desc": "O personagem comporta-se de modo aleatório. No início de seu turno, role 1d6: 1) Movimenta-se em uma direção aleatória; 2-3) Não pode fazer ações e balbucia incoerentemente; 4-5) Ataca a criatura mais próxima ou a si mesmo se não houver criatura; 6) Age normalmente.",
        "page": 400
    },
    {
        "name": "Debilitado",
        "type": None,
        "desc": "O personagem sofre –5 em testes de atributos físicos (Força, Destreza, Constituição) e de perícias baseadas nesses atributos. Se ficar debilitado novamente, fica inconsciente.",
        "page": 400
    },
    {
        "name": "Desprevenido",
        "type": None,
        "desc": "O personagem sofre –5 na Defesa e em Reflexos. Você fica desprevenido contra inimigos que não possa ver.",
        "page": 400,
        "relatedIds": ["manobra-fintar"]
    },
    {
        "name": "Doente",
        "type": "Metabólica",
        "desc": "Sob efeito de uma enfermidade. Efeitos variam conforme a doença (veja Perigos, pág. 293).",
        "page": 400
    },
    {
        "name": "Em Chamas",
        "type": None,
        "desc": "O personagem sofre 1d6 pontos de dano de fogo no início de seus turnos. Pode apagar o fogo gastando uma ação padrão e passando em um teste de Reflexos (CD 15) ou se jogando no chão e rolando (recebe +5 no teste, mas fica caído).",
        "page": 400,
        "relatedIds": ["condicao-caido"]
    },
    {
        "name": "Enfeitiçado",
        "type": "Mental",
        "desc": "O personagem se torna prestativo em relação à fonte da condição. Ele não luta pela fonte, mas a enxerga como um amigo querido e faz tudo ao seu alcance para protegê-la e obedecê-la, desde que não vá contra sua natureza básica.",
        "page": 400
    },
    {
        "name": "Enjoado",
        "type": "Metabólica",
        "desc": "O personagem só pode realizar uma ação padrão ou de movimento por turno (não ambas).",
        "page": 400
    },
    {
        "name": "Enredado",
        "type": "Movimento",
        "desc": "O personagem fica lento, vulnerável e sofre –2 em testes de ataque.",
        "page": 401,
        "relatedIds": ["condicao-lento", "condicao-vulneravel"]
    },
    {
        "name": "Envenenado",
        "type": "Metabólica",
        "desc": "Sob efeito de uma toxina. Efeitos variam conforme o veneno (veja a página 297).",
        "page": 401
    },
    {
        "name": "Esmorecido",
        "type": "Mental",
        "desc": "O personagem sofre –5 em testes de atributos mentais (Inteligência, Sabedoria, Carisma) e de perícias baseadas nesses atributos.",
        "page": 401
    },
    {
        "name": "Exausto",
        "type": None,
        "desc": "O personagem fica debilitado, lento e vulnerável. Se ficar exausto novamente, fica inconsciente.",
        "page": 401,
        "relatedIds": ["condicao-debilitado", "condicao-lento", "condicao-vulneravel", "condicao-inconsciente"]
    },
    {
        "name": "Fascinado",
        "type": "Mental",
        "desc": "O personagem sofre –5 em Percepção e não pode fazer ações exceto observar a fonte do fascínio. Qualquer ação hostil contra o personagem ou seus aliados encerra a condição.",
        "page": 401
    },
    {
        "name": "Fatigado",
        "type": None,
        "desc": "O personagem fica fraco e vulnerável. Se ficar fatigado novamente, em vez disso fica exausto.",
        "page": 401,
        "relatedIds": ["condicao-fraco", "condicao-vulneravel", "condicao-exausto"]
    },
    {
        "name": "Fraco",
        "type": None,
        "desc": "O personagem sofre –2 em testes de atributos físicos (Força, Destreza, Constituição) e de perícias baseadas nesses atributos. Se ficar fraco novamente, em vez disso fica debilitado.",
        "page": 401,
        "relatedIds": ["condicao-debilitado"]
    },
    {
        "name": "Frustrado",
        "type": "Mental",
        "desc": "O personagem sofre –2 em testes de atributos mentais (Inteligência, Sabedoria, Carisma) e de perícias baseadas nesses atributos. Se ficar frustrado novamente, em vez disso fica esmorecido.",
        "page": 401,
        "relatedIds": ["condicao-esmorecido"]
    },
    {
        "name": "Imóvel",
        "type": "Movimento",
        "desc": "O deslocamento do personagem se torna 0m e ele não pode se movimentar.",
        "page": 401
    },
    {
        "name": "Inconsciente",
        "type": None,
        "desc": "O personagem fica indefeso e não pode fazer ações, inclusive reações. Balbucia inconscientemente ou fica totalmente apagado.",
        "page": 401,
        "relatedIds": ["condicao-indefeso"]
    },
    {
        "name": "Indefeso",
        "type": None,
        "desc": "O personagem fica desprevenido, sofre –10 na Defesa, falha automaticamente em testes de Reflexos e pode sofrer golpes de misericórdia.",
        "page": 401,
        "relatedIds": ["condicao-desprevenido"]
    },
    {
        "name": "Lento",
        "type": "Movimento",
        "desc": "O deslocamento do personagem é reduzido à metade e ele não pode correr ou fazer investidas.",
        "page": 401
    },
    {
        "name": "Ofuscado",
        "type": "Sentidos",
        "desc": "O personagem sofre –2 em testes de ataque e em testes de Percepção para observar.",
        "page": 401
    },
    {
        "name": "Paralisado",
        "type": "Movimento",
        "desc": "O personagem fica imóvel e indefeso e só pode realizar ações puramente mentais.",
        "page": 401,
        "relatedIds": ["condicao-imovel", "condicao-indefeso"]
    },
    {
        "name": "Pasmo",
        "type": "Mental",
        "desc": "O personagem não pode fazer ações.",
        "page": 401
    },
    {
        "name": "Petrificado",
        "type": None,
        "desc": "O personagem se transforma em pedra. Fica inconsciente e recebe redução de dano 10.",
        "page": 401,
        "relatedIds": ["condicao-inconsciente"]
    },
    {
        "name": "Sangrando",
        "type": "Metabólica",
        "desc": "No início de seu turno, o personagem deve fazer um teste de Constituição (CD 15). Se falhar, perde 1d6 pontos de vida e continua sangrando. Se passar, estabiliza e para de sangrar.",
        "page": 401
    },
    {
        "name": "Sobrecarregado",
        "type": None,
        "desc": "O personagem sofre penalidade de armadura –5 e seu deslocamento é reduzido em 3m.",
        "page": 401
    },
    {
        "name": "Surdo",
        "type": "Sentidos",
        "desc": "O personagem não pode fazer testes de Percepção para ouvir e sofre –5 em testes de Iniciativa. Além disso, sofre –2 em testes de Vontade contra efeitos sonoros ou dependentes de fala.",
        "page": 401
    },
    {
        "name": "Surpreendido",
        "type": None,
        "desc": "O personagem fica desprevenido e não pode realizar ações na primeira rodada de combate.",
        "page": 401,
        "relatedIds": ["condicao-desprevenido"]
    },
    {
        "name": "Vulnerável",
        "type": None,
        "desc": "O personagem sofre –2 na Defesa.",
        "page": 401
    },
    # Condições de Saúde e Combate (Páginas 240-244)
    {
        "name": "Machucado",
        "type": None,
        "desc": "O personagem está com metade ou menos de seus pontos de vida máximos. Certas habilidades e perigos têm efeitos especiais contra personagens machucados.",
        "page": 240
    },
    {
        "name": "Moribundo",
        "type": None,
        "desc": "Um personagem com 0 ou menos pontos de vida está inconsciente e sangrando. No início de cada turno, deve fazer um teste de Constituição (CD 15). Se falhar, perde 1d6 PV. Se passar, estabiliza.",
        "page": 242,
        "relatedIds": ["condicao-inconsciente", "condicao-sangrando"]
    },
    {
        "name": "Morto",
        "type": None,
        "desc": "O personagem morre quando seus pontos de vida negativos chegam à metade de seus PV máximos (ou ao falhar em três testes de Constituição enquanto moribundo). Sua alma deixa o corpo rumo ao reino de seu deus padroeiro.",
        "page": 242
    },
    {
        "name": "Asfixiado",
        "type": None,
        "desc": "Sem ar para respirar (sufocando ou afogando-se). Um personagem pode prender a respiração por um número de rodadas igual ao dobro de sua Constituição. Após isso, deve fazer um teste de Fortitude por rodada (CD 15 + 1 por teste anterior). Se falhar, fica inconsciente e perde 1d6 PV por rodada até respirar ou morrer.",
        "page": 244,
        "relatedIds": ["condicao-inconsciente"]
    },
    {
        "name": "Desarmado",
        "type": None,
        "desc": "O personagem não está empunhando nenhuma arma. Ao atacar desarmado sem possuir habilidades específicas, o ataque é considerado desarmado e causa dano não letal.",
        "page": 238,
        "relatedIds": ["manobra-desarmar"]
    },
    {
        "name": "Quebrado",
        "type": None,
        "desc": "Um item que tenha seus pontos de vida reduzidos a 0 fica quebrado. Não pode ser usado até ser consertado (com a perícia Ofício).",
        "page": 242,
        "relatedIds": ["manobra-quebrar"]
    }
]

for c in appendix_conditions:
    slug_id = f"condicao-{c['name'].lower().replace(' ', '-').replace('í', 'i').replace('ã', 'a').replace('ç', 'c')}"
    tags = ["condição", "status", "combate", c["name"].lower()]
    if c["type"]:
        tags.append(c["type"].lower())
    
    database.append({
        "id": slug_id,
        "name": c["name"],
        "category": "condicao",
        "type": c["type"],
        "summary": c["desc"][:130] + ("..." if len(c["desc"]) > 130 else ""),
        "description": c["desc"],
        "relatedIds": c.get("relatedIds", []),
        "sources": [{
            "book": "Tormenta20 - Jogo do Ano (v1.3)",
            "page": c["page"],
            "section": "Apêndice: Condições / Combate",
            "version": "v1.3"
        }],
        "tags": tags
    })

# ==========================================
# 2. MANOBRAS DE COMBATE
# ==========================================
print("Compilando Manobras de Combate...")

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

for m in manobras:
    database.append({
        "id": m["id"],
        "name": m["name"],
        "category": "manobra",
        "actionType": m["actionType"],
        "opposedTest": m["opposedTest"],
        "summary": m["description"][:130] + "...",
        "description": m["description"],
        "relatedIds": m.get("resultingConditionIds", []),
        "sources": [{
            "book": "Tormenta20 - Jogo do Ano (v1.3)",
            "page": m["page"],
            "section": "Capítulo 5: Combate - Manobras de Combate",
            "version": "v1.3"
        }],
        "tags": m["tags"]
    })

# ==========================================
# 3. REGRAS GERAIS DE COMBATE E AÇÕES
# ==========================================
print("Compilando Regras de Combate...")

regras_combate = [
    {
        "id": "regra-acao-padrao",
        "name": "Ação Padrão",
        "chapter": "Combate",
        "subchapter": "Tipos de Ações",
        "description": "Uma ação padrão representa a coisa mais importante que você faz em seu turno. Atacar com uma arma ou lançar uma magia comum são os exemplos mais típicos de ações padrão.",
        "page": 236,
        "tags": ["combate", "ação", "ação padrão", "turno"]
    },
    {
        "id": "regra-acao-de-movimento",
        "name": "Ação de Movimento",
        "chapter": "Combate",
        "subchapter": "Tipos de Ações",
        "description": "Uma ação de movimento representa deslocamento físico ou manipulação rápida de objetos. Exemplos: andar até o seu deslocamento, sacar ou guardar uma arma, levantar-se do chão, abrir uma porta não trancada.",
        "page": 236,
        "tags": ["combate", "ação", "movimento", "deslocamento", "sacar arma"]
    },
    {
        "id": "regra-acao-completa",
        "name": "Ação Completa",
        "chapter": "Combate",
        "subchapter": "Tipos de Ações",
        "description": "Uma ação completa consome todo o seu esforço e tempo do turno. Se fizer uma ação completa, você não pode fazer nenhuma ação padrão nem de movimento. Exemplos: Investida, Golpe de Misericórdia, Correr.",
        "page": 236,
        "tags": ["combate", "ação", "ação completa", "investida", "correr"]
    },
    {
        "id": "regra-acao-livre",
        "name": "Ação Livre",
        "chapter": "Combate",
        "subchapter": "Tipos de Ações",
        "description": "Ações livres consomem pouquíssimo tempo e esforço. Você pode realizar qualquer quantidade razoável de ações livres por turno, a critério do mestre. Exemplos: falar uma frase curta, soltar um item empunhado.",
        "page": 236,
        "tags": ["combate", "ação", "ação livre"]
    },
    {
        "id": "regra-reacao",
        "name": "Reação",
        "chapter": "Combate",
        "subchapter": "Tipos de Ações",
        "description": "Uma reação é uma resposta instantânea a um gatilho específico, que pode acontecer fora do seu turno. Você só pode reagir se não estiver indefeso ou sob efeito que impeça ações. Exemplos: teste de Reflexos contra uma bola de fogo, teste de Percepção contra Furtividade.",
        "page": 236,
        "tags": ["combate", "ação", "reação", "resposta"]
    },
    {
        "id": "regra-investida",
        "name": "Investida",
        "chapter": "Combate",
        "subchapter": "Ações Completas",
        "description": "Você avança até o dobro de seu deslocamento em linha reta e faz um ataque corpo a corpo no final do movimento. Você recebe +2 no teste de ataque, mas sofre –2 na Defesa até o início do seu próximo turno.",
        "page": 237,
        "tags": ["combate", "investida", "ação completa", "ataque corpo a corpo"]
    },
    {
        "id": "regra-golpe-de-misericordia",
        "name": "Golpe de Misericórdia",
        "chapter": "Combate",
        "subchapter": "Ações Completas",
        "description": "Você desfere um golpe letal contra um alvo indefeso adjacente. Como uma ação completa, você acerta automaticamente e causa um acerto crítico automático. O alvo deve fazer um teste de Fortitude (CD 10 + dano sofrido) ou morre imediatamente.",
        "page": 237,
        "relatedIds": ["condicao-indefeso"],
        "tags": ["combate", "golpe de misericórdia", "indefeso", "morte", "crítico"]
    },
    {
        "id": "regra-acumulo-de-bonus",
        "name": "Acúmulo de Bônus e Efeitos",
        "chapter": "Regras do Jogo",
        "subchapter": "Benefícios e Penalidades",
        "description": "Bônus de mesma fonte (duas magias, dois itens com o mesmo encanto, ou a mesma habilidade usada duas vezes) NÃO se acumulam — aplique apenas o maior. Bônus de tipos e fontes diferentes (um item, uma magia e uma habilidade de classe) se acumulam normalmente. Penalidades sempre se acumulam, a menos que venham da mesma condição ou efeito idêntico.",
        "page": 226,
        "tags": ["regras", "acúmulo", "bônus", "magias", "itens"]
    },
    {
        "id": "regra-descanso",
        "name": "Descanso e Recuperação",
        "chapter": "Jogando",
        "subchapter": "Recuperação",
        "description": "Um descanso de 8 horas permite recuperar Pontos de Vida (PV) e Pontos de Mana (PM). Condições de descanso: 1) Ruim (acampamento exposto): PV e PM = nível; 2) Normal (estalagem comum, barraca confortável): PV e PM = dobro do nível; 3) Confortável (quarto de luxo, mansão): PV e PM = triplo do nível; 4) Luxuoso (palácio): PV e PM = quatro vezes o nível.",
        "page": 224,
        "tags": ["descanso", "recuperação", "pv", "pm", "cura", "estalagem"]
    }
]

for r in regras_combate:
    database.append({
        "id": r["id"],
        "name": r["name"],
        "category": "regra",
        "chapter": r["chapter"],
        "subchapter": r.get("subchapter", ""),
        "summary": r["description"][:130] + ("..." if len(r["description"]) > 130 else ""),
        "description": r["description"],
        "relatedIds": r.get("relatedIds", []),
        "sources": [{
            "book": "Tormenta20 - Jogo do Ano (v1.3)",
            "page": r["page"],
            "section": f"Capítulo: {r['chapter']}",
            "version": "v1.3"
        }],
        "tags": r["tags"]
    })

# ==========================================
# 4. PERÍCIAS OFICIAIS DE TORMENTA20
# ==========================================
print("Compilando Perícias Oficiais...")

pericias = [
    {"name": "Acrobacia", "attr": "DES", "trained": False, "armor": True, "page": 120, "desc": "Você consegue fazer proezas acrobáticas como equilíbrio, amortecer queda, escapar de amarras e passar por espaço apertado."},
    {"name": "Adestramento", "attr": "CAR", "trained": True, "armor": False, "page": 120, "desc": "Você sabe cuidar de animais e monstros irracionais, ensinando truques, acalmando feras e manejando montarias."},
    {"name": "Atletismo", "attr": "FOR", "trained": False, "armor": True, "page": 120, "desc": "Você usa sua força física para correr, escalar, nadar e saltar grandes distâncias ou alturas."},
    {"name": "Atuação", "attr": "CAR", "trained": True, "armor": False, "page": 121, "desc": "Você sabe cantar, dançar, atuar, contar histórias e entreter plateias, além de impressionar nobres."},
    {"name": "Cavalgar", "attr": "DES", "trained": False, "armor": False, "page": 121, "desc": "Você sabe conduzir montarias comuns como cavalos, trobos e grifos, inclusive durante o combate montado."},
    {"name": "Conhecimento", "attr": "INT", "trained": True, "armor": False, "page": 122, "desc": "Você possui saber acadêmico sobre história, lendas, geografia, ciências naturais e culturas de Arton."},
    {"name": "Cura", "attr": "SAB", "trained": False, "armor": False, "page": 122, "desc": "Você sabe tratar ferimentos, estabilizar moribundos, cuidar de doentes e prestar primeiros socorros."},
    {"name": "Diplomacia", "attr": "CAR", "trained": False, "armor": False, "page": 123, "desc": "Você persuade pessoas com argumentos racionais, etiqueta, negociação de preços e resolução de conflitos."},
    {"name": "Enganação", "attr": "CAR", "trained": False, "armor": False, "page": 123, "desc": "Você mente com convicção, disfarça-se, forja documentos, cria distrações e realiza a manobra Fintar."},
    {"name": "Fortitude", "attr": "CON", "trained": False, "armor": False, "page": 124, "desc": "Sua resistência física contra venenos, doenças, fadiga, privação de ar e magias de morte ou vigor."},
    {"name": "Furtividade", "attr": "DES", "trained": False, "armor": True, "page": 124, "desc": "Você se esgueira nas sombras, move-se silenciosamente e oculta-se dos sentidos alheios."},
    {"name": "Guerra", "attr": "INT", "trained": True, "armor": False, "page": 124, "desc": "Você entende de táticas militares, logística, cerco, reconhecimento de terreno e liderança marcial em combate."},
    {"name": "Iniciativa", "attr": "DES", "trained": False, "armor": False, "page": 125, "desc": "Sua velocidade de reação ao perigo no começo de combates e cenas de ação."},
    {"name": "Intimidação", "attr": "CAR", "trained": False, "armor": False, "page": 125, "desc": "Você coage outros pelo medo, presença física ameaçadora ou violência psicológica para obter cooperação ou desmoralizar inimigos."},
    {"name": "Intuição", "attr": "SAB", "trained": False, "armor": False, "page": 125, "desc": "Você percebe segundas intenções, lê linguagem corporal, detecta mentiras e prevê reações instintivas."},
    {"name": "Investigação", "attr": "INT", "trained": False, "armor": False, "page": 126, "desc": "Você busca pistas, vasculha cenas de crime, decifra enigmas e reúne informações em vilas e cidades."},
    {"name": "Jogatina", "attr": "CAR", "trained": True, "armor": False, "page": 126, "desc": "Você conhece regras de jogos de azar, calcula probabilidades, trapaceia e percebe trapaças alheias."},
    {"name": "Ladinagem", "attr": "DES", "trained": True, "armor": True, "page": 126, "desc": "Você bate carteiras, abre fechaduras com gazuas, desarma armadilhas e sabota mecanismos."},
    {"name": "Luta", "attr": "FOR", "trained": False, "armor": False, "page": 127, "desc": "Sua perícia em combate corpo a corpo (com armas marciais, armas simples ou desarmado) e para realizar e resistir a Manobras de Combate."},
    {"name": "Misticismo", "attr": "INT", "trained": True, "armor": False, "page": 127, "desc": "Você compreende a teoria mágica, identifica magias lançadas, analisa itens arcanos e lida com fenômenos sobrenaturais."},
    {"name": "Nobreza", "attr": "INT", "trained": True, "armor": False, "page": 128, "desc": "Você conhece a heráldica, genealogia, leis, etiqueta da alta corte e a política das nações do Reinado."},
    {"name": "Ofício", "attr": "INT", "trained": True, "armor": False, "page": 128, "desc": "Você sabe fabricar, avaliar e consertar itens de uma profissão específica (ex: Alquimia, Armaria, Culinária, Engenharia)."},
    {"name": "Percepção", "attr": "SAB", "trained": False, "armor": False, "page": 128, "desc": "Sua acuidade sensorial para notar criaturas escondidas, ouvir ruídos distantes e avistar perigos."},
    {"name": "Pilotagem", "attr": "DES", "trained": True, "armor": False, "page": 129, "desc": "Você sabe conduzir veículos terrestres, aquáticos ou aéreos (como carruagens, navios e balões de ar quente)."},
    {"name": "Pontaria", "attr": "DES", "trained": False, "armor": False, "page": 129, "desc": "Sua habilidade em ataques à distância (arcos, bestas, armas de fogo e arremesso)."},
    {"name": "Reflexos", "attr": "DES", "trained": False, "armor": False, "page": 129, "desc": "Sua agilidade para esquivar de explosões, armadilhas de mola, desabamentos e magias de área."},
    {"name": "Religião", "attr": "SAB", "trained": True, "armor": False, "page": 129, "desc": "Você conhece os dogmas do Panteão, ritos sagrados, símbolos divinos e a hierarquia eclesiástica de Arton."},
    {"name": "Sobrevivência", "attr": "SAB", "trained": False, "armor": False, "page": 130, "desc": "Você sabe rastrear presas, forragear comida e água, orientar-se no ermo e prever o clima."},
    {"name": "Vontade", "attr": "SAB", "trained": False, "armor": False, "page": 130, "desc": "Sua força de vontade e sanidade contra efeitos mentais, ilusões, fascínio, possessões e magias psíquicas."}
]

for p in pericias:
    slug_id = f"pericia-{p['name'].lower().replace(' ', '-').replace('í', 'i').replace('ã', 'a').replace('ç', 'c')}"
    database.append({
        "id": slug_id,
        "name": p["name"],
        "category": "pericia",
        "keyAttribute": p["attr"],
        "onlyTrained": p["trained"],
        "armorPenalty": p["armor"],
        "summary": f"[{p['attr']}] {'Treinada. ' if p['trained'] else ''}{'Penalidade de Armadura. ' if p['armor'] else ''}{p['desc'][:110]}...",
        "description": p["desc"],
        "sources": [{
            "book": "Tormenta20 - Jogo do Ano (v1.3)",
            "page": p["page"],
            "section": "Capítulo 2: Perícias & Poderes",
            "version": "v1.3"
        }],
        "tags": ["perícia", p["name"].lower(), p["attr"].lower()] + (["treinada"] if p["trained"] else []) + (["penalidade de armadura"] if p["armor"] else [])
    })

# Salvar o banco canônico atualizado
with open("data/t20_canonical_database.json", "w", encoding="utf-8") as f:
    json.dump(database, f, ensure_ascii=False, indent=2)

print("\n=======================================================")
print("BANCO CANONICO CONSOLIDADO COM SUCESSO!")
print(f"Total de Entidades: {len(database)}")
print(f"- Condicoes: {len([e for e in database if e['category'] == 'condicao'])}")
print(f"- Manobras: {len([e for e in database if e['category'] == 'manobra'])}")
print(f"- Regras de Combate: {len([e for e in database if e['category'] == 'regra'])}")
print(f"- Pericias Oficiais: {len([e for e in database if e['category'] == 'pericia'])}")
print("Arquivo gerado: data/t20_canonical_database.json")
print("=======================================================\n")
