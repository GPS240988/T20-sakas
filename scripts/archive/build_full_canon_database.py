# -*- coding: utf-8 -*-
"""
COMPILADOR PRINCIPAL E CONSOLIDADOR EXAUSTIVO DE EQUIPAMENTOS (4 LIVROS DE ARTON)
Auditoria e consolidação integral de todas as tabelas e seções de Tormenta20.
"""

import json
import os

from build_jda_equipments import get_jda_equipments
from build_hda_equipments import get_hda_equipments
from build_ameacas_equipments import get_ameacas_equipments

os.makedirs('data/categories', exist_ok=True)

def build_all_equipments():
    print("=== INICIANDO CONSOLIDAÇÃO CANÔNICA DE TODOS OS EQUIPAMENTOS (4 LIVROS) ===")
    
    jda_items = get_jda_equipments()
    print(f"  [JdA v1.3] Itens compilados: {len(jda_items)}")
    
    hda_items = get_hda_equipments()
    print(f"  [HdA v1.1] Itens compilados: {len(hda_items)}")
    
    ameacas_items = get_ameacas_equipments()
    print(f"  [Ameaças v1.0] Itens compilados: {len(ameacas_items)}")
    
    all_items = []
    seen_ids = set()
    
    for item in jda_items + hda_items + ameacas_items:
        iid = item["id"]
        if iid in seen_ids:
            print(f"  [AVISO] ID duplicado detectado e ignorado: {iid}")
            continue
        seen_ids.add(iid)
        all_items.append(item)
        
    out_path = 'data/categories/equipamentos.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
        
    print("=" * 70)
    print(f"SUCESSO TOTAL! {len(all_items)} EQUIPAMENTOS CANÔNICOS SALVOS EM '{out_path}'")
    print("=" * 70)
    return all_items

if __name__ == '__main__':
    build_all_equipments()
