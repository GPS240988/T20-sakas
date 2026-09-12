# -*- coding: utf-8 -*-
"""
COMPILADOR CANÔNICO EXAUSTIVO DE EQUIPAMENTOS (4 LIVROS DE ARTON)
Auditoria e consolidação integral de todas as tabelas e seções de Tormenta20.
"""

import json
import os
import re

os.makedirs('data/categories', exist_ok=True)

equipments = []
id_set = set()

def add_item(id_slug, name, subcategory, subtype, purpose, price, damage, critical, damage_type, range_val, defense_bonus, penalty, space, book, page, description, tags, is_magic=False, rarity=None):
    if id_slug in id_set:
        # If already exists, return existing
        return next(x for x in equipments if x["id"] == id_slug)
    id_set.add(id_slug)
    
    table_data = {}
    if price: table_data["price"] = price
    if subtype: table_data["subtype"] = subtype
    if purpose: table_data["purpose"] = purpose
    if space is not None: table_data["space"] = space
    if damage: table_data["damage"] = damage
    if critical: table_data["critical"] = critical
    if damage_type: table_data["damageType"] = damage_type
    if range_val: table_data["range"] = range_val
    if defense_bonus: table_data["defenseBonus"] = defense_bonus
    if penalty: table_data["armorPenalty"] = penalty
    
    summary_parts = []
    if subcategory: summary_parts.append(subcategory)
    if subtype and subtype != subcategory: summary_parts.append(subtype)
    if defense_bonus: summary_parts.append(f"Defesa {defense_bonus}")
    if damage: summary_parts.append(f"Dano {damage} ({critical})")
    if price: summary_parts.append(f"Preço: {price}")
    if space is not None and space != 0: summary_parts.append(f"Espaço: {space}")
    
    clean_desc = description.strip()
    summary = " | ".join(summary_parts) + f". {clean_desc[:90]}..."
    
    version = "v1.3" if "Jogo do Ano" in book else "v1.1" if "Heróis" in book else "v1.0"
    
    all_tags = set([
        "equipamento",
        subcategory.lower(),
        (subtype or "").lower(),
        (purpose or "").lower(),
        name.lower()
    ] + [t.lower() for t in tags if t])
    all_tags.discard("")
    
    item = {
        "id": id_slug,
        "name": name,
        "category": "equipamento",
        "subcategory": subcategory,
        "subtype": subtype,
        "proficiency": subtype, # Compatibilidade
        "purpose": purpose or subtype,
        "summary": summary,
        "description": clean_desc,
        "tableData": table_data,
        "sources": [{
            "book": book,
            "page": page,
            "section": f"Equipamentos: {subcategory} ({subtype})",
            "version": version
        }],
        "tags": sorted(list(all_tags))
    }
    
    if is_magic:
        item["isMagicItem"] = True
        item["magicRarity"] = rarity or "Menor"
        
    equipments.append(item)
    return item

book_jda = "Tormenta20 - Jogo do Ano (v1.3)"
book_hda = "Heróis de Arton (v1.1)"
book_ameacas = "Ameaças de Arton (v1.0)"

print("Iniciando cadastro completo e exaustivo de equipamentos...")
