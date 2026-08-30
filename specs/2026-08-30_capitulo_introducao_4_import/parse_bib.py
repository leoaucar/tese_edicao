import re, unicodedata, json, sys

BIB_PATH = r"C:\Users\leoau\Documents\tese_edicao\references.bib"

def strip_accents(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))

def norm_surname(s):
    s = strip_accents(s).lower()
    s = re.sub(r'[{}\\]', '', s)
    s = re.sub(r'[^a-z]', '', s)
    return s

with open(BIB_PATH, encoding='utf-8') as f:
    text = f.read()

# split into entries by looking for lines starting with @word{key,
entry_pattern = re.compile(r'@(\w+)\{([^,\n]+),(.*?)(?=\n@\w+\{|\Z)', re.DOTALL)
entries = []
for m in entry_pattern.finditer(text):
    etype, key, body = m.group(1), m.group(2).strip(), m.group(3)
    author_m = re.search(r'author\s*=\s*\{(.*?)\}\s*,?\s*\n', body, re.DOTALL)
    editor_m = re.search(r'editor\s*=\s*\{(.*?)\}\s*,?\s*\n', body, re.DOTALL)
    year_m = re.search(r'year\s*=\s*\{([^}]*)\}', body)
    title_m = re.search(r'title\s*=\s*\{(.*?)\}\s*,?\s*\n', body, re.DOTALL)
    is_editor_only = False
    if author_m:
        author_raw = author_m.group(1).strip()
    elif editor_m:
        author_raw = editor_m.group(1).strip()
        is_editor_only = True
    else:
        author_raw = ""
    year = year_m.group(1).strip() if year_m else ""
    title = title_m.group(1).strip() if title_m else ""
    # split authors on ' and ' (top-level, not inside {{}})
    # handle double-braced institutional names {{...}}
    authors = []
    # naive split on ' and ' when not inside nested braces
    depth = 0
    buf = ""
    parts = []
    i = 0
    while i < len(author_raw):
        c = author_raw[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        if author_raw[i:i+5] == ' and ' and depth == 0:
            parts.append(buf)
            buf = ""
            i += 5
            continue
        buf += c
        i += 1
    parts.append(buf)
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # surname is text before first comma, strip braces
        surn = p.split(',')[0]
        surn = surn.strip('{}').strip()
        authors.append(norm_surname(surn))
    entries.append({
        "key": key,
        "type": etype,
        "authors_raw": [p.strip() for p in parts if p.strip()],
        "authors_norm": authors,
        "year": year,
        "title": title[:80],
        "is_editor_only": is_editor_only,
    })

with open(r"C:\Users\leoau\Documents\tese_edicao\specs\2026-08-30_capitulo_introducao_4_import\bib_entries.json", "w", encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=1)

print(f"Parsed {len(entries)} entries")
