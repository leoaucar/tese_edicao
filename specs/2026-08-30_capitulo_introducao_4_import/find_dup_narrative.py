# -*- coding: utf-8 -*-
import re, unicodedata
BASE = r"C:\Users\leoau\Documents\tese_edicao\specs\2026-08-30_capitulo_introducao_4_import"
with open(f"{BASE}\\source_raw.tex", encoding='utf-8') as f:
    text = unicodedata.normalize('NFC', f.read())
pattern = re.compile(r'([A-Z\u00c0-\u00da][a-z\u00e0-\u00fa\-]+)\s*\\href\{https://www\.zotero\.org/google-docs/\?[^}]+\}\{\(([A-Z\u00c0-\u00da][a-z\u00e0-\u00fa\-]+)')
for m in pattern.finditer(text):
    prose_name, cite_name = m.group(1), m.group(2)
    if prose_name == cite_name:
        start = max(0, m.start()-40)
        with open(f"{BASE}\\dup_narrative_hits.txt", "a", encoding='utf-8') as out:
            out.write(repr(text[start:m.end()+25]) + "\n---\n")
print("done")
