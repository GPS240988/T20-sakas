# -*- coding: utf-8 -*-
import json

with open('data/categories/equipamentos.json', 'r', encoding='utf-8') as f:
    equips = json.load(f)

fixes = {
    "Pique": "Pique. Essencialmente uma lança muito longa (entre 3 e 4,5m). O pique é uma arma alongada. Uma arma alongada dobra o seu alcance natural, mas não permite que você ataque um inimigo adjacente.",
    "Tacape": "Tacape. Versão maior e/ou com pregos de uma clava. Um tacape é uma arma pesada; você não pode aplicar aprimoramentos de agilidade a ele. Usada com as duas mãos por humanoides primitivos ou brutais.",
    "Machado Anão": "Machado Anão. Uma arma de guerra tradicional dos anões forjada em Doherimm, feita para cortar através de armaduras pesadas. Uma criatura com proficiência em armas marciais pode usar um machado anão como uma arma de duas mãos.",
    "Pistola": "Pistola. A arma de fogo de uma mão mais comum do Reinado. Recarregar uma pistola é uma ação padrão. Dispara balas com pólvora causando grande impacto e dano perfurante.",
    "Armadura Acolchoada": "Armadura Acolchoada. Mais grossa que uma roupa comum, esta armadura é feita de várias camadas de tecido acolchoado com lã ou algodão. É a armadura mais leve disponível.",
    "Óleo": "Óleo. Um frasco de cerâmica ou vidro com óleo mineral inflamável para lampiões. Uma dose dura 6 horas no lampião. Pode ser arremessado ou derramado no chão para ser incendiado com fogo.",
    "Estábulo (por dia)": "Estábulo. Inclui alimentação com feno fresco, água limpa e acomodação segura para o animal em cocheiras de estalagens ou postos de troca.",
    "Estadia Comum": "Estadia Comum. Inclui uma cama de palha em dormitório coletivo e uma refeição simples em uma estalagem ou taverna de vilarejo.",
    "Estadia Confortável": "Estadia Confortável. Inclui uma cama macia em quarto privativo, banho quente e desjejum completo em estalagem conceituada.",
    "Espinhoso (Escudo)": "Espinhoso (Escudo). O escudo possui espigões ou lâminas adicionais forjadas em sua face externa. Aumenta o dano de um ataque com escudo em um passo.",
    "Tai-tai": "Tai-tai. Esta arma tribal de arremesso consiste em uma vara flexível com cordão elástico, usada para disparar dardos pesados com grande impacto contundente a média distância.",
    "Arcabuz": "Arcabuz. Versão mais pesada e potente da arma de fogo longa, disparando projéteis de chumbo de grosso calibre que perfuram até as armaduras mais espessas.",
    "Presa de Serpente": "Presa de Serpente. Lâmina curva excepcional forjada a partir de presas de serpentes marinhas lendárias de Khubar. É uma arma ágil com margem de ameaça 17 formidável."
}

fixed_count = 0
for eq in equips:
    name = eq['name']
    if name in fixes:
        eq['description'] = fixes[name]
        table_data = eq.get("tableData", {})
        summary_parts = []
        if eq.get("subcategory"): summary_parts.append(eq["subcategory"])
        if eq.get("subtype") and eq["subtype"] != eq["subcategory"]: summary_parts.append(eq["subtype"])
        if table_data.get("defenseBonus"): summary_parts.append(f"Defesa {table_data['defenseBonus']}")
        if table_data.get("damage"): summary_parts.append(f"Dano {table_data['damage']} ({table_data.get('critical', 'x2')})")
        if table_data.get("price"): summary_parts.append(f"Preço: {table_data['price']}")
        if table_data.get("space") is not None and table_data["space"] != 0: summary_parts.append(f"Espaço: {table_data['space']}")
        eq["summary"] = " | ".join(summary_parts) + f". {fixes[name][:90]}..."
        fixed_count += 1

print(f"Itens ajustados com texto literal refinado: {fixed_count}")

with open('data/categories/equipamentos.json', 'w', encoding='utf-8') as f:
    json.dump(equips, f, ensure_ascii=False, indent=2)

print("Database 'data/categories/equipamentos.json' 100% polida!")
