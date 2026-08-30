import re, json, unicodedata
from collections import defaultdict, Counter

BASE = r"C:\Users\leoau\Documents\tese_edicao\specs\2026-08-30_capitulo_introducao_4_import"

with open(f"{BASE}\\bib_entries.json", encoding='utf-8') as f:
    entries = json.load(f)

def strip_accents(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))

def norm_surname(s):
    s = strip_accents(s).lower()
    s = re.sub(r'[{}\\]', '', s)
    s = re.sub(r'[^a-z]', '', s)
    return s

by_year_authors = defaultdict(list)   # (year, frozenset(authors)) -> [keys]  exact set match
by_year_first = defaultdict(list)     # (year, first_author) -> [keys]  for et al.
by_year_any_author = defaultdict(list)
by_year_supersets = defaultdict(list) # (year,) -> [(frozenset(authors), key)]  for subset fallback

for e in entries:
    y = e["year"]
    auths = tuple(e["authors_norm"])
    fs = frozenset(auths)
    by_year_authors[(y, fs)].append(e["key"])
    if auths:
        by_year_first[(y, auths[0])].append(e["key"])
        for a in auths:
            by_year_any_author[(y, a)].append(e["key"])
    by_year_supersets[y].append((fs, e["key"]))

with open(f"{BASE}\\source_raw.tex", encoding='utf-8') as f:
    text = unicodedata.normalize("NFC", f.read())

href_pattern = re.compile(r'\\href\{https://www\.zotero\.org/google-docs/\?[^}]+\}\{(\([^{}]*(?:\{[^{}]*\}[^{}]*)*\))\}')
matches = list(href_pattern.finditer(text))
print(f"Total zotero href citations found: {len(matches)}")

def preprocess(raw):
    raw = raw.strip('()')
    # unwrap \emph{...}
    raw = re.sub(r'\\emph\{([^{}]*)\}', r'\1', raw)
    # unescape pandoc bracket escaping {[}s.d.{]} -> [s.d.]
    raw = raw.replace('{[}', '[').replace('{]}', ']')
    # collapse all whitespace (incl newlines) to single space
    raw = re.sub(r'\s+', ' ', raw).strip()
    return raw

def parse_author_list(author_str):
    author_str = author_str.strip()
    et_al = False
    if re.search(r'\bet al\.?\s*$', author_str, re.IGNORECASE):
        et_al = True
        author_str = re.sub(r'\s*et al\.?\s*$', '', author_str, flags=re.IGNORECASE).strip()
    m = re.search(r'^(.*)\s+e\s+([^,]+)$', author_str)
    if m:
        head, last = m.group(1), m.group(2)
        head_parts = [p.strip() for p in head.split(',') if p.strip()]
        parts = head_parts + [last.strip()]
    else:
        parts = [p.strip() for p in author_str.split(',') if p.strip()]
    return parts, et_al

records = []
for m in matches:
    raw = preprocess(m.group(1))
    groups = [g.strip() for g in raw.split(';')]
    parsed_groups = []
    for g in groups:
        page = None
        pg_m = re.search(r',\s*p\.\s*([\d\-\u2013]+)\s*$', g)
        if pg_m:
            page = pg_m.group(1)
            g = g[:pg_m.start()].strip()
        # institutional "sem data" case: "<Inst> [s.d.]"
        sd_m = re.search(r'^(.*?),?\s*\[s\.d\.\]\s*$', g)
        if sd_m:
            author_part = sd_m.group(1).strip()
            authors, et_al = parse_author_list(author_part) if author_part else ([], False)
            parsed_groups.append({"authors": authors, "years": ["sd"], "page": page, "et_al": et_al, "raw": g})
            continue
        yr_m = re.search(r',\s*((?:\d{4}[a-z]?)(?:\s*,\s*\d{4}[a-z]?)*)\s*$', g)
        if not yr_m:
            yr_only = re.match(r'^(\d{4}[a-z]?)$', g.strip())
            if yr_only:
                parsed_groups.append({"authors": None, "years": [yr_only.group(1)], "page": page, "et_al": False, "raw": g})
                continue
            parsed_groups.append({"authors": None, "years": None, "page": page, "et_al": False, "raw": g})
            continue
        years_str = yr_m.group(1)
        years = [y.strip() for y in years_str.split(',')]
        author_part = g[:yr_m.start()].strip()
        if author_part.endswith(','):
            author_part = author_part[:-1]
        authors, et_al = parse_author_list(author_part) if author_part else ([], False)
        parsed_groups.append({"authors": authors, "years": years, "page": page, "et_al": et_al, "raw": g})
    records.append({
        "span": m.span(),
        "full_href": m.group(0),
        "raw_text": raw,
        "groups": parsed_groups,
    })

def try_match(authors, year, et_al):
    if authors is None:
        return None, "narrative_needs_context"
    norm_auth = tuple(norm_surname(a) for a in authors)
    fs = frozenset(norm_auth)
    if et_al:
        key_ = (year, norm_auth[0]) if norm_auth else None
        cands = by_year_first.get(key_, []) if key_ else []
        if not cands:
            cands = by_year_any_author.get(key_, []) if key_ else []
        cands = list(dict.fromkeys(cands))
        if len(cands) == 1:
            return cands[0], "matched_etal"
        elif len(cands) > 1:
            return None, f"ambiguous_etal:{cands}"
        else:
            return None, "no_match"
    else:
        cands = by_year_authors.get((year, fs), [])
        if len(cands) == 1:
            return cands[0], "matched"
        elif len(cands) > 1:
            return None, f"ambiguous:{cands}"
        # subset fallback: cited authors are a subset of some entry's author/editor list for same year
        sub_cands = [k for (efs, k) in by_year_supersets.get(year, []) if fs and fs.issubset(efs)]
        sub_cands = list(dict.fromkeys(sub_cands))
        if len(sub_cands) == 1:
            return sub_cands[0], "matched_subset"
        elif len(sub_cands) > 1:
            return None, f"ambiguous_subset:{sub_cands}"
        return None, "no_match"

results = []
for rec in records:
    for g in rec["groups"]:
        if g["years"] is None:
            results.append({"raw": g["raw"], "status": "unparsed", "key": None, "authors": g["authors"], "page": g.get("page")})
            continue
        for y in g["years"]:
            key, status = try_match(g["authors"], y, g["et_al"])
            results.append({
                "authors": g["authors"], "year": y, "page": g.get("page"),
                "raw": g["raw"], "status": status, "key": key
            })

status_summary = Counter(r["status"].split(':')[0] for r in results)
print("Status summary:", status_summary)

with open(f"{BASE}\\citation_match_results.json", "w", encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=1)

with open(f"{BASE}\\citation_unresolved.txt", "w", encoding='utf-8') as f:
    for r in results:
        if r["status"].startswith("no_match") or r["status"].startswith("ambiguous") or r["status"] == "unparsed":
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("Wrote citation_match_results.json and citation_unresolved.txt")
