import zipfile
import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

with zipfile.ZipFile('Poderes de classe e variantes.docx') as z:
    xml_content = z.read('word/document.xml')

root = ET.fromstring(xml_content)

for idx, p in enumerate(root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')):
    runs = list(p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r'))
    if not runs:
        continue
    p_text = ''.join([t.text for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text]).strip()
    if not p_text or p_text in ['ARCANISTA', 'PALADINO'] or 'PODERES VARIANTES' in p_text:
        continue
    
    first_run_text = ''.join([t.text for t in runs[0].iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
    print(f"P{idx:3d}: Run0=[{first_run_text}] | FULL=[{p_text[:70]}]")
