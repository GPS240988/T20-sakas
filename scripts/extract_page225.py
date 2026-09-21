import fitz
import os

os.makedirs('public/images/regras', exist_ok=True)
doc = fitz.open('Tormenta20-Edicao-Jogo-do-Ano-v1.3_compressed.pdf')
page = doc[230]

# 1. Extract raw images from page
for img in page.get_images():
    xref = img[0]
    base = doc.extract_image(xref)
    ext = base['ext']
    filename = f"public/images/regras/page225_img_{xref}.{ext}"
    with open(filename, 'wb') as f:
        f.write(base['image'])
    print(f"Saved: {filename} ({base['width']}x{base['height']})")

# 2. Render page 225 at 300 DPI
pix = page.get_pixmap(dpi=300)
pix.save('public/images/regras/page225_full.png')
print("Saved public/images/regras/page225_full.png")
