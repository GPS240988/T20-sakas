# -*- coding: utf-8 -*-
import json

with open('data/categories/equipamentos.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

fixes = {
    "Shuriken": "Shuriken. Pequenos projéteis metálicos para arremesso, em forma de estrelas ou dardos. Uma vez por rodada, quando ataca com uma shuriken, você pode gastar 1 PM para fazer um ataque adicional de shuriken contra o mesmo alvo. Se tiver Arremesso Múltiplo, em vez disso você não paga PM para usar esse poder.",
    "Tetsubo": "Tetsubo. Uma versão mais pesada e sofisticada do tacape, geralmente reforçado com anéis metálicos, rebites e/ou cravos. É uma arma versátil, fornecendo +2 em testes para derrubar ou empurrar.",
    "Mordida do Diabo": "Mordida do Diabo. Esta arma é formada por um aparato em forma de mandíbula preso a uma empunhadura. A mandíbula pode ser usada para agarrar e, graças a uma longa corrente, pode se destacar do cabo e alcançar alvos a até 3m. Por exigir movimentos precisos e coordenados, é uma arma exótica. A mordida pode ser feita de metal, mas ossos e dentes de feras aquáticas também são usados. É uma arma ágil e versátil, fornecendo +2 em testes para agarrar e desarmar.",
    "Presa de Serpente": "Presa de Serpente. Espada de obsidiana, um vidro vulcânico negro formado quando a lava esfria rapidamente. Por sua origem, as voracis acreditam que esse material é uma dádiva da Divina Serpente. Mais afiada que o aço, causa ferimentos terríveis; em um acerto crítico, o dano aumenta em um passo (antes de ser multiplicado). Uma presa de serpente não pode receber a melhoria material especial e exige treinamento especial para ser empunhada sem quebrar, por isso é uma arma exótica. É uma arma ágil."
}

updated = 0
for item in items:
    name = item.get('name')
    if name in fixes:
        item['description'] = fixes[name]
        summary_prefix = item['summary'].split('.')[0] if '.' in item['summary'] else item['summary']
        item['summary'] = f"{summary_prefix}. {fixes[name][:100]}..."
        updated += 1

with open('data/categories/equipamentos.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Fixed {updated} Ameaças de Arton weapon descriptions.")
