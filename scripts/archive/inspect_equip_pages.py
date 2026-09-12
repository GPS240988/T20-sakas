from pypdf import PdfReader

print("=== HEROIS DE ARTON ===")
r_hda = PdfReader("T20-Herois-de-Arton-v1-1_compressed.pdf")
print("Total pages in HDA:", len(r_hda.pages))
# Book page 216 is PDF page 218 (index 217)
for pno in range(215, 245):
    text = r_hda.pages[pno].extract_text()
    first_lines = text.split("\n")[:4]
    print(f"--- HDA PDF Page {pno+1} (Book Pág ~{pno+1-2}) ---")
    print("\n".join(first_lines))

print("\n=== AMEAÇAS DE ARTON ===")
r_ameacas = PdfReader("Ameacas-de-Arton-v1.0-17-11-2023_compressed.pdf")
print("Total pages in Ameacas:", len(r_ameacas.pages))
# Bazar Monstruoso starts at book page 390 (PDF page 392, index 391)
for pno in range(390, 404):
    text = r_ameacas.pages[pno].extract_text()
    first_lines = text.split("\n")[:4]
    print(f"--- Ameacas PDF Page {pno+1} (Book Pág ~{pno+1-2}) ---")
    print("\n".join(first_lines))
