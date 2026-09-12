# -*- coding: utf-8 -*-
import json

with open('data/categories/equipamentos.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

fixes = {
    "Adaga": "Adaga. Esta faca afiada é usada por muitos habitantes adultos do Reinado, embora seja favorita de ladrões e assassinos, por ser facilmente escondida (fornece +5 em testes de Ladinagem para ocultá-la). Quando ataca com uma adaga, você pode usar sua Destreza em vez de Força nos testes de ataque. Uma adaga pode ser arremessada.",
    "Lança Montada": "Lança Montada. A lança montada é uma arma alongada. Se você estiver montado, pode usá-la com apenas uma mão. Além disso, quando usada numa investida montada, causa +2d8 pontos de dano (note que dados extras não são multiplicados em caso de acerto crítico).",
    "Besta Pesada": "Besta Pesada. Versão maior e mais potente da besta leve. Recarregar uma besta pesada é uma ação padrão.",
    "Machado Táurico": "Machado Táurico. Uma haste comprida com uma lâmina extremamente grossa na ponta, esta é uma arma ancestral dos minotauros. Um machado táurico é uma arma desbalanceada. Além disso, é muito grande para ser usado sem treinamento especial; por isso, é uma arma exótica."
}

updated_count = 0
for item in items:
    name = item.get('name')
    if name in fixes:
        item['description'] = fixes[name]
        # Also update summary if needed
        summary_prefix = item['summary'].split('.')[0] if '.' in item['summary'] else item['summary']
        item['summary'] = f"{summary_prefix}. {fixes[name][:100]}..."
        updated_count += 1

with open('data/categories/equipamentos.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Successfully fixed {updated_count} weapon descriptions.")
