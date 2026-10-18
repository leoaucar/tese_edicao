"""Métricas de citação no OpenAlex, normalizadas por área e ano.

Uso:
  python3 metricas_citacao.py <lib.json> KEY [KEY ...]   # itens do Zotero
  python3 metricas_citacao.py --doi DOI [DOI ...]        # obras de fora
Imprime TSV: id, ano, citações, fwci, percentil (0-1), tipo, periódico, subárea OpenAlex, título.

Busca por DOI; sem DOI, por título (similaridade > 0.8 e sobrenome do 1º autor),
pegando a edição mais citada. Livros e traduções vêm partidos entre edições:
"sem dado" não quer dizer obra pouco citada.
"""
import sys, os, json, re, difflib, urllib.request, urllib.parse, urllib.error
# E-mail opcional para o "polite pool" do OpenAlex/Crossref: variável OPENALEX_MAILTO.
MAIL = ('mailto=' + os.environ['OPENALEX_MAILTO']) if os.environ.get('OPENALEX_MAILTO') else ''
# O OpenAlex tem orçamento diário gratuito por IP; com chave própria (grátis) o limite é seu.
# Chave: variável OPENALEX_API_KEY ou arquivo ~/.config/openalex/key (nunca imprimir).
_kf = os.path.expanduser('~/.config/openalex/key')
KEY = os.environ.get('OPENALEX_API_KEY') or (open(_kf).read().strip() if os.path.exists(_kf) else '')

class RateLimited(Exception): pass

def get(u):
    q = '&'.join(x for x in [MAIL, f'api_key={KEY}' if KEY and 'openalex' in u else ''] if x)
    try: return json.load(urllib.request.urlopen(u + ((('&' if '?' in u else '?') + q) if q else ''), timeout=30))
    except urllib.error.HTTPError as e:
        if e.code == 429: raise RateLimited(u.split('?')[0])
        return None
    except Exception: return None

def crossref_count(doi):
    """Plano B para obras com DOI: só a contagem bruta do Crossref (sem normalização)."""
    doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi.strip())
    m = get('https://api.crossref.org/works/' + urllib.parse.quote(doi)) if doi else None
    return m and m['message'].get('is-referenced-by-count')

def by_doi(doi):
    doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi.strip())
    return get('https://api.openalex.org/works/doi:' + urllib.parse.quote(doi)) if doi else None

def by_title(title, author):
    r = get('https://api.openalex.org/works?per-page=10&search=' + urllib.parse.quote(title[:150])) or {}
    ok = []
    for w in r.get('results', []):
        if w['type'] == 'book-review' or not w.get('title'): continue
        sim = difflib.SequenceMatcher(None, title.lower()[:80], w['title'].lower()[:80]).ratio()
        names = ' '.join(a['author']['display_name'] for a in w['authorships']).lower()
        if sim > 0.8 and author and author.lower()[:5] in names: ok.append(w)
    return max(ok, key=lambda w: w['cited_by_count']) if ok else None

def row(ident, w):
    if not w: return f'{ident}\tsem dado'
    src = ((w.get('primary_location') or {}).get('source') or {})
    pct = (w.get('citation_normalized_percentile') or {}).get('value')
    sub = ((w.get('primary_topic') or {}).get('subfield') or {}).get('display_name')
    return '\t'.join(map(str, [ident, w['publication_year'], w['cited_by_count'], w.get('fwci'),
                               round(pct, 3) if pct is not None else None, w['type'], src.get('display_name'), sub, w['title']]))

def run(ident, doi, title='', author=''):
    try:
        print(row(ident, by_doi(doi) or (by_title(title, author) if title else None)), flush=True)
    except RateLimited:
        c = crossref_count(doi) if doi else None
        print(f'{ident}\tLIMITE OPENALEX\tcrossref={c}' if c is not None else f'{ident}\tLIMITE OPENALEX', flush=True)

if sys.argv[1] == '--doi':
    for d in sys.argv[2:]: run(d, d)
else:
    lib = {i['key']: i['data'] for i in json.load(open(sys.argv[1]))}
    for k in sys.argv[2:]:
        d = lib[k]
        au = next((c.get('lastName') or c.get('name') for c in d.get('creators', [])), '') or ''
        run(k, d.get('DOI') or '', d.get('title', ''), au)
