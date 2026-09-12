import re
from pypdf import PdfReader

def get_text(pdf_path, start_page, end_page):
    reader = PdfReader(pdf_path)
    full_text = ""
    for p in range(start_page - 1, end_page):
        t = reader.pages[p].extract_text()
        full_text += f"\n=== [PAGE {p+1}] ===\n" + t
    return full_text

# JDA Equipamentos: PDF pages 148 to 175
jda_text = get_text("Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf", 148, 175)
with open("scripts/jda_equip_dump.txt", "w", encoding="utf-8") as f:
    f.write(jda_text)

# HDA Equipamentos: PDF pages 216 to 246
hda_text = get_text("T20-Herois-de-Arton-v1-1_compressed.pdf", 216, 246)
with open("scripts/hda_equip_dump.txt", "w", encoding="utf-8") as f:
    f.write(hda_text)

# Ameacas Bazar: PDF pages 392 to 404
ameacas_text = get_text("Ameacas-de-Arton-v1.0-17-11-2023_compressed.pdf", 392, 404)
with open("scripts/ameacas_equip_dump.txt", "w", encoding="utf-8") as f:
    f.write(ameacas_text)

print("Dumped raw text for all 3 books.")
