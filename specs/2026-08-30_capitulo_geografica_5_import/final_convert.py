import re, json, unicodedata
from collections import defaultdict

BASE = r"C:\Users\leoau\Documents\tese_edicao\specs\2026-08-30_capitulo_geografica_5_import"

def strip_accents(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))

def norm_surname(s):
    s = strip_accents(s).lower()
    s = re.sub(r'[{}\\]', '', s)
    s = re.sub(r'[^a-z]', '', s)
    return s

with open(f"{BASE}\\bib_entries.json", encoding='utf-8') as f:
    entries = json.load(f)

by_year_authors = defaultdict(list)
by_year_first = defaultdict(list)
by_year_supersets = defaultdict(list)
for e in entries:
    y = e["year"]
    auths = tuple(e["authors_norm"])
    fs = frozenset(auths)
    by_year_authors[(y, fs)].append(e["key"])
    if auths:
        by_year_first[(y, auths[0])].append(e["key"])
    by_year_supersets[y].append((fs, e["key"]))

# ---- manual overrides (see plan.md for rationale) ----
# duplicates: prefer the fuller real entry over a stale bare stub
DUP_OVERRIDE = {
    (frozenset({'mahoney'}), '2000'): 'mahoney_path_2000',
    (frozenset({'pierson'}), '2015'): 'mahoney_power_2015',
}
# genuinely ambiguous: multiple distinct works, cannot resolve silently -> aiflag
AMBIGUOUS = {
    (frozenset({'high'}), '2013'): ['high_wounds_2013', 'high_beyond_2013'],
}
# institutional "[s.d.]" citations resolved by direct inspection of the docx's
# own (dropped) reference list
SD_OVERRIDE = {
    'CNI': 'cni_sd',
    'IBGE': 'ibge_contas_nodate',
}
# narrative citations (author named in prose, href contains only the year) --
# resolved by the unique Zotero query-string id of each \href, read directly
# from source_raw.tex context (see plan.md "Citações narrativas").
NARRATIVE_BY_ID = {
    'N5g7Uw': ('aiflag', '(Skocpol, 1984) %% AMBIGUO: 3 candidatos em references.bib (skocpol_vision_1984, skocpol_emerging_1984, skocpol_sociologys_1984) -- revisar qual o autor tinha em mente'),
    'H0ADAb': ('cite', 'tilly_big_1984'),
    'Ic6cdI': ('cite', 'kreuzer_grammar_2023'),
    'MfNH7j': ('cite', 'linkon_half-life_2018'),
    'KF8pD8': ('cite', 'rodrik_premature_2016'),
    'hrJ4AN': ('cite', 'oreiro_desindustrializacao_2010'),
    'yaPvp0': ('cite', 'morceiro2021'),
    'GHtpZP': ('cite', 'morceiro_adensamento_2020'),
    'aTAxBm': ('cite', 'maia_ha_2020'),
    '1SorMi': ('cite', 'feijo_financial_2019'),
    'zV6TKb': ('cite', 'sobral2016'),
    'gibX7I': ('cite', 'vianna_da_cruz_os_2013'),
    'oj5qly': ('cite', 'souza_producao_2019'),
}
# Nassif (2008; 2015): single href with two year groups, same narrative author
NARRATIVE_NASSIF_ID = 'Lcq024'
NARRATIVE_NASSIF = {
    '2008': ('cite', 'nassif_ha_2008'),
    '2015': ('aiflag', '(Nassif, 2015) %% NAO ENCONTRADO: nenhuma entrada de Nassif 2015 no .bib fornecido nem na lista de referencias do docx com esse autor isolado -- so existe NASSIF, L.; TEIXEIRA, L.; ROCHA, F. 2015 (3 autores); revisar se e a mesma obra'),
}

def preprocess(raw):
    raw = raw.strip('()')
    raw = re.sub(r'\\emph\{([^{}]*)\}', r'\1', raw)
    raw = raw.replace('{[}', '[').replace('{]}', ']')
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

def resolve(authors, year, et_al, raw_group):
    if authors is None:
        return ('narrative', None, None)
    norm_auth = tuple(norm_surname(a) for a in authors)
    fs = frozenset(norm_auth)
    if et_al:
        key_ = (year, norm_auth[0]) if norm_auth else None
        cands = list(dict.fromkeys(by_year_first.get(key_, [])))
        if len(cands) == 1:
            return ('cite', cands[0])
        return ('aiflag', raw_group)
    cands = by_year_authors.get((year, fs), [])
    if len(cands) == 1:
        return ('cite', cands[0])
    if (fs, year) in DUP_OVERRIDE:
        return ('cite', DUP_OVERRIDE[(fs, year)])
    if (fs, year) in AMBIGUOUS:
        return ('aiflag', raw_group)
    if len(cands) > 1:
        return ('aiflag', raw_group)
    sub_cands = list(dict.fromkeys([k for (efs, k) in by_year_supersets.get(year, []) if fs and fs.issubset(efs)]))
    if len(sub_cands) == 1:
        return ('cite', sub_cands[0])
    return ('aiflag', f"({raw_group}) %% NAO ENCONTRADO - revisar")

with open(f"{BASE}\\source_raw.tex", encoding='utf-8') as f:
    text = unicodedata.normalize("NFC", f.read())

href_pattern = re.compile(r'\\href\{https://www\.zotero\.org/google-docs/\?([^}]+)\}\{(\([^{}]*(?:\{[^{}]*\}[^{}]*)*\))\}')

def replace_citation(m):
    zid = m.group(1)
    raw = preprocess(m.group(2))

    if zid == NARRATIVE_NASSIF_ID:
        kind, val = NARRATIVE_NASSIF['2008']
        kind2, val2 = NARRATIVE_NASSIF['2015']
        return f"\\citep{{{val}}} \\aiflag{{{val2}}}"

    if zid in NARRATIVE_BY_ID:
        kind, val = NARRATIVE_BY_ID[zid]
        if kind == 'cite':
            return f"\\citet{{{val}}}"
        return f"\\aiflag{{{val}}}"

    # institutional "[s.d.]" citations
    sd_whole = re.match(r'^\(?\s*([A-ZÀ-Ú]+),?\s*\[s\.d\.\]\s*\)?$', raw)
    if sd_whole and sd_whole.group(1) in SD_OVERRIDE:
        return f"\\citep{{{SD_OVERRIDE[sd_whole.group(1)]}}}"

    groups = [g.strip() for g in raw.split(';')]
    outputs = []
    for g in groups:
        page = None
        pg_m = re.search(r',\s*p\.\s*([\d\-\u2013]+)\s*$', g)
        gg = g
        if pg_m:
            page = pg_m.group(1)
            gg = g[:pg_m.start()].strip()
        sd_m = re.search(r'^(.*?),?\s*\[s\.d\.\]\s*$', gg)
        if sd_m:
            author_part = sd_m.group(1).strip()
            if author_part.upper() in SD_OVERRIDE:
                outputs.append(('cite', SD_OVERRIDE[author_part.upper()], page))
                continue
            authors, et_al = parse_author_list(author_part) if author_part else ([], False)
            years = ['sd']
        else:
            yr_m = re.search(r',\s*((?:\d{4}[a-z]?)(?:\s*,\s*\d{4}[a-z]?)*)\s*$', gg)
            if not yr_m:
                yr_only = re.match(r'^(\d{4}[a-z]?)$', gg.strip())
                if yr_only:
                    outputs.append(('RAW', f"({gg}) %% NARRATIVA NAO MAPEADA POR ID -- revisar", page))
                    continue
                outputs.append(('RAW', gg, page))
                continue
            years_str = yr_m.group(1)
            years = [y.strip() for y in years_str.split(',')]
            author_part = gg[:yr_m.start()].strip()
            if author_part.endswith(','):
                author_part = author_part[:-1]
            authors, et_al = parse_author_list(author_part) if author_part else ([], False)
        for y in years:
            kind, val = resolve(authors, y, et_al, f"({g})")
            outputs.append((kind, val, page))

    parts = []
    cite_buffer = []
    def flush():
        if cite_buffer:
            keys = ",".join(k for k in cite_buffer)
            parts.append(f"\\citep{{{keys}}}")
            cite_buffer.clear()
    for kind, val, page in outputs:
        if kind == 'cite':
            if page:
                flush()
                parts.append(f"\\citep[p.~{page}]{{{val}}}")
            else:
                cite_buffer.append(val)
        elif kind == 'aiflag':
            flush()
            parts.append(f"\\aiflag{{{val}}}")
        else:
            flush()
            parts.append(f"\\aiflag{{({val})}}")
    flush()
    return " ".join(parts)

new_text, n = href_pattern.subn(replace_citation, text)
print(f"Replaced {n} citation spans")

with open(f"{BASE}\\converted_body.tex", "w", encoding='utf-8') as f:
    f.write(new_text)
print("Wrote converted_body.tex")
