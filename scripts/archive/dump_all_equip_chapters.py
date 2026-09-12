import pypdf
import os

def dump_pages(pdf_path, start_page, end_page, output_txt):
    reader = pypdf.PdfReader(pdf_path)
    with open(output_txt, 'w', encoding='utf-8') as f:
        for p in range(start_page, min(end_page + 1, len(reader.pages))):
            f.write(f"\n{'='*30} PDF PAGE {p} (Book page ~{p-3 if 'Tormenta20' in pdf_path else p-1}) {'='*30}\n")
            f.write(reader.pages[p].extract_text() or '')
            f.write("\n")

print("Dumping JDA Equipment pages 145-175...")
dump_pages("Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf", 145, 175, "scripts/jda_equip_full_dump.txt")

print("Dumping HDA Equipment pages 215-260...")
dump_pages("T20-Herois-de-Arton-v1-1_compressed.pdf", 215, 260, "scripts/hda_equip_full_dump.txt")

print("Dumping Ameacas Equipment pages 390-410...")
dump_pages("Ameacas-de-Arton-v1.0-17-11-2023_compressed.pdf", 390, 410, "scripts/ameacas_equip_full_dump.txt")

print("All dumps completed successfully!")
