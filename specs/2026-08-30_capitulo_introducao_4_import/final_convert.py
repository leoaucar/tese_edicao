import re, json, unicodedata

BASE = r"C:\Users\leoau\Documents\tese_edicao\specs\2026-08-30_capitulo_introducao_4_import"

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

from collections import defaultdict
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
# duplicates: prefer the fuller real entry over the stale stub
DUP_OVERRIDE = {
    (frozenset({'souza', 'previdelli'}), '2022'): 'souza_historia_2022',
    (frozenset({'abreu'}), '2014'): 'abreu_ordem_2014',
    (frozenset({'mahoney'}), '2000'): 'mahoney_path_2000',
}
# genuinely ambiguous: multiple distinct works, cannot resolve silently -> aiflag
AMBIGUOUS = {
    (frozenset({'high'}), '2013'): ['high_wounds_2013', 'high_beyond_2013'],
    (frozenset({'mahoney', 'rueschemeyer'}), '2003'): ['mahoney_comparative_2003', 'mahoney_comparative_2003-1'],
    (frozenset({'thelen', 'mahoney'}), '2015'): ['mahoney_comparative-historical_2015', 'mahoney_advances_2015'],
    (frozenset({'skocpol'}), '1984a'): ['skocpol_emerging_1984', 'skocpol_sociologys_1984'],
}
# brand-new stubs to be appended to references.bib
NEW_STUBS = {
    (frozenset({'ibge'}), 'sd'): ('ibge_sd', 'IBGE'),
    (frozenset({'vianna', 'villela'}), '2015'): ('viannavillela2015', 'Vianna, ... and Villela, ...'),
    (frozenset({'morceiro'}), '2021'): ('morceiro2021', 'Morceiro, Paulo César'),
    (frozenset({'cni'}), '2021'): ('cni2021', 'CNI'),
    (frozenset({'cni'}), 'sd'): ('cni_sd', 'CNI'),
    (frozenset({'governodoestadodesaopaulo'}), 'sd'): ('governoestadosp_sd', 'Governo do Estado de São Paulo'),
    (frozenset({'consorcioabc'}), 'sd'): ('consorcioabc_sd', 'Consórcio ABC'),
    (frozenset({'ibge'}), '2017'): ('ibge2017', 'IBGE'),
    (frozenset({'ramalho', 'santos'}), '2022'): ('ramalhosantos2022', 'Ramalho, José Ricardo Garcia Pereira and Santos, Rodrigo Salles Pereira dos'),
    (frozenset({'rodrigues', 'ramalho'}), '2007'): ('rodriguesramalho2007', 'Rodrigues, Iram Jácome and Ramalho, José Ricardo Garcia Pereira'),
    (frozenset({'amsden'}), '2003'): ('amsden2003', 'Amsden, Alice H.'),
    (frozenset({'berger', 'musso', 'wicke'}), '2022'): ('bergermussowicke2022', 'Berger, ... and Musso, ... and Wicke, ...'),
    (frozenset({'oreiro', 'marconi'}), '2012'): ('oreiromarconi2012', 'Oreiro, José Luis and Marconi, Nelson'),
    (frozenset({'bresserpereira'}), '2020'): ('bresserpereira2020', 'Bresser-Pereira, Luiz Carlos'),
    (frozenset({'ramalho'}), '2004'): ('ramalho2004', 'Ramalho, José Ricardo Garcia Pereira'),
    (frozenset({'ramalho'}), '2015'): ('ramalho2015', 'Ramalho, José Ricardo Garcia Pereira'),
    (frozenset({'bridi', 'oliveira', 'salas'}), '2023'): ('bridioliveirasalas2023', 'Bridi, ... and Oliveira, ... and Salas, ...'),
    (frozenset({'dulci'}), '2021'): ('dulci2021', 'Dulci, Otávio Soares'),
    (frozenset({'consorcioabc'}), '2024'): ('consorcioabc2024', 'Consórcio ABC'),
    (frozenset({'ramalho', 'rodrigues'}), '2013'): ('ramalhorodrigues2013', 'Ramalho, José Ricardo Garcia Pereira and Rodrigues, Iram Jácome'),
    (frozenset({'ramalho', 'rodrigues'}), '2018'): ('ramalhorodrigues2018', 'Ramalho, José Ricardo Garcia Pereira and Rodrigues, Iram Jácome'),
    (frozenset({'fontes'}), '2023'): ('fontes2023', 'Fontes, Paulo'),
    (frozenset({'sobral'}), '2016'): ('sobral2016', 'Sobral'),
    (frozenset({'smabc'}), '2004'): ('smabc2004', 'SMABC'),
    (frozenset({'valoreconomico'}), '2019'): ('valoreconomico2019', 'Valor Econômico'),
    (frozenset({'reis'}), '2007'): ('reis2007', 'Reis'),
    (frozenset({'ramalho', 'rodrigues'}), '2010'): ('ramalhorodrigues2010', 'Ramalho, José Ricardo Garcia Pereira and Rodrigues, Iram Jácome'),
    (frozenset({'ramalho', 'conceicao'}), '2024'): ('ramalhoconceicao2024', 'Ramalho, José Ricardo Garcia Pereira and Conceição, ...'),
    (frozenset({'ramalho', 'santos', 'lima'}), '2013'): ('ramalhosantoslima2013', 'Ramalho, José Ricardo Garcia Pereira and Santos, Rodrigo Salles Pereira dos and Lima, ...'),
    (frozenset({'morel'}), '1989'): ('morel1989', 'Morel'),
    (frozenset({'ramalho'}), '1989'): ('ramalho1989', 'Ramalho, José Ricardo Garcia Pereira'),
    (frozenset({'abreu', 'beynon', 'ramalho'}), '2000'): ('abreubeynonramalho2000', 'Abreu, ... and Beynon, ... and Ramalho, José Ricardo Garcia Pereira'),
    (frozenset({'santos'}), '2021'): ('santos2021', 'Santos, Rodrigo Salles Pereira dos'),
    (frozenset({'ramalho'}), '2005'): ('ramalho2005', 'Ramalho, José Ricardo Garcia Pereira'),
    (frozenset({'piquet'}), '2021'): ('piquet2021', 'Piquet'),
    (frozenset({'sobral'}), '2017'): ('sobral2017', 'Sobral'),
    (frozenset({'sautu'}), '2005'): ('sautuetal2005', 'Sautu, ... and others'),
    (frozenset({'thelen'}), '2010'): ('thelen2010', 'Thelen, Kathleen'),
    (frozenset({'duina'}), '2011'): ('duina2011', 'Duina'),
    (frozenset({'morgan'}), '2010'): ('morganetal2010', 'Morgan, ... and others'),
    (frozenset({'scott'}), '2014'): ('scott2014', 'Scott'),
    (frozenset({'hess'}), '2004'): ('hess2004', 'Hess, Martin'),
    (frozenset({'fligstein'}), '1996'): ('fligstein1996', 'Fligstein, Neil'),
    (frozenset({'allen', 'wood', 'keller'}), '2022'): ('allenwoodkeller2022', 'Allen, ... and Wood, ... and Keller, ...'),
    (frozenset({'henderson'}), '2002'): ('hendersonetal2002', 'Henderson, Jeffrey and others'),
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
    """Returns ('cite', key) or ('aiflag', text) or ('narrative', authors, year)"""
    if authors is None:
        return ('narrative', None, None)
    norm_auth = tuple(norm_surname(a) for a in authors)
    fs = frozenset(norm_auth)
    if et_al:
        if (fs, year) in NEW_STUBS:
            return ('cite', NEW_STUBS[(fs, year)][0])
        key_ = (year, norm_auth[0]) if norm_auth else None
        cands = list(dict.fromkeys(by_year_first.get(key_, [])))
        if len(cands) == 1:
            return ('cite', cands[0])
        return ('aiflag', raw_group)
    # exact
    cands = by_year_authors.get((year, fs), [])
    if len(cands) == 1:
        return ('cite', cands[0])
    if (fs, year) in DUP_OVERRIDE:
        return ('cite', DUP_OVERRIDE[(fs, year)])
    if (fs, year) in AMBIGUOUS:
        return ('aiflag', raw_group)
    if (fs, year) in NEW_STUBS:
        return ('cite', NEW_STUBS[(fs, year)][0])
    if len(cands) > 1:
        return ('aiflag', raw_group)
    # subset fallback
    sub_cands = list(dict.fromkeys([k for (efs, k) in by_year_supersets.get(year, []) if fs and fs.issubset(efs)]))
    if len(sub_cands) == 1:
        return ('cite', sub_cands[0])
    return ('aiflag', f"({raw_group}) %% NAO ENCONTRADO EM NEW_STUBS - revisar")

with open(f"{BASE}\\source_raw.tex", encoding='utf-8') as f:
    text = unicodedata.normalize("NFC", f.read())

href_pattern = re.compile(r'\\href\{https://www\.zotero\.org/google-docs/\?[^}]+\}\{(\([^{}]*(?:\{[^{}]*\}[^{}]*)*\))\}')

def replace_citation(m):
    raw = preprocess(m.group(1))
    groups = [g.strip() for g in raw.split(';')]
    outputs = []
    is_narrative = False
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
            authors, et_al = parse_author_list(author_part) if author_part else ([], False)
            years = ['sd']
        else:
            yr_m = re.search(r',\s*((?:\d{4}[a-z]?)(?:\s*,\s*\d{4}[a-z]?)*)\s*$', gg)
            if not yr_m:
                yr_only = re.match(r'^(\d{4}[a-z]?)$', gg.strip())
                if yr_only:
                    # narrative: only year, no author text in this group
                    is_narrative = True
                    outputs.append(('NARR', yr_only.group(1), page))
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
    # Build replacement text
    # Separate consecutive 'cite' entries (combine into one \citep{k1,k2}) vs aiflag entries (standalone)
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
        elif kind == 'NARR':
            flush()
            parts.append(f"__NARRATIVE_YEAR_{val}_PAGE_{page}__")
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
