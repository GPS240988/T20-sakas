import pypdf

reader = pypdf.PdfReader("Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf")

with open("data/chapter8_raw.txt", "w", encoding="utf-8") as f:
    # JDA book page 333 is around PDF page 338-340
    for p in range(330, 360):
        if p < len(reader.pages):
            text = reader.pages[p].extract_text() or ""
            f.write(f"\n=== PDF PAGE {p+1} (Book Page ~{p-5}) ===\n")
            f.write(text)

print("Chapter 8 extracted to data/chapter8_raw.txt")
