# -*- coding: utf-8 -*-
"""Dump temporal del texto de las paginas de Poderes (JDA y Herois) para inspeccion y carga."""
import pypdf
import os

os.makedirs("scripts/tmp_dump", exist_ok=True)

def dump(pdf_path, start_idx, end_idx, out_name):
    r = pypdf.PdfReader(pdf_path)
    with open(f"scripts/tmp_dump/{out_name}.txt", "w", encoding="utf-8") as fd:
        for i in range(start_idx, end_idx + 1):
            fd.write(f"\n===== PAGE_INDEX_{i} (printed {i+1}) =====\n")
            fd.write(r.pages[i].extract_text())
            fd.write("\n")

# JDA Poderes Gerais: paginas impresas 130-143 => indices 129-142
dump("Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf", 129, 142, "jda_poderes_130_143")

# Herois Novos Poderes Gerais (80-85), Raca (86-93), Grupo (94-97) => indices 79-96
dump("T20-Herois-de-Arton-v1-1_compressed.pdf", 79, 96, "herois_poderes_80_97")

# Herois Distinciones: pages 104-215 => indices 103-214
dump("T20-Herois-de-Arton-v1-1_compressed.pdf", 103, 214, "herois_distinciones_104_215")

print("DUMP OK")