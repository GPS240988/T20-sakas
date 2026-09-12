import pypdf
import os
import json

pdfs = {
    "Jogo do Ano": "Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf",
    "Ameacas": "Ameacas-de-Arton-v1.0-17-11-2023_compressed.pdf",
    "Atlas": "Atlas-de-Arton-v1.0-17-11-2023_compressed.pdf",
    "Herois": "T20-Herois-de-Arton-v1-1_compressed.pdf"
}

def extract_outline_tree(reader, outline):
    result = []
    for item in outline:
        if isinstance(item, list):
            result.append(extract_outline_tree(reader, item))
        else:
            try:
                title = item.title
                page_num = reader.get_destination_page_number(item) + 1
                result.append({"title": title, "page": page_num})
            except Exception:
                result.append({"title": getattr(item, 'title', str(item)), "page": None})
    return result

data = {}
for name, filename in pdfs.items():
    if os.path.exists(filename):
        reader = pypdf.PdfReader(filename)
        data[name] = {
            "total_pages": len(reader.pages),
            "outline": extract_outline_tree(reader, reader.outline) if reader.outline else []
        }

os.makedirs("data", exist_ok=True)
with open("data/pdf_outlines.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Outlines extraídos com sucesso para data/pdf_outlines.json")
