import zipfile
import xml.etree.ElementTree as ET
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with zipfile.ZipFile('Poderes de classe e variantes.docx') as z:
    xml_content = z.read('word/document.xml')

root = ET.fromstring(xml_content)
paragraphs = []
for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    texts = [node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
    full_text = ''.join(texts).strip()
    if full_text:
        paragraphs.append(full_text)

print(f"Total non-empty paragraphs: {len(paragraphs)}")

current_class = None
is_variant = False
items = []

for i, p in enumerate(paragraphs):
    if p in ['ARCANISTA', 'PALADINO']:
        current_class = p.capitalize()
        is_variant = False
        continue
    m_var = re.match(r'PODERES VARIANTES \((.*?)\)', p, re.IGNORECASE)
    if m_var:
        current_class = m_var.group(1).strip().capitalize()
        is_variant = True
        continue
    
    clean_p = re.sub(r'^[•\-\*]\s*', '', p).strip()
    items.append({
        'idx': i,
        'class': current_class,
        'is_variant': is_variant,
        'raw': clean_p
    })

for item in items:
    var_str = "Var" if item['is_variant'] else "Base"
    print(f"P{item['idx']:3d} [{item['class']}] ({var_str}): {item['raw'][:100]}")
