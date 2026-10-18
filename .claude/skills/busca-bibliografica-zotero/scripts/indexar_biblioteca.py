"""Baixa coleções, itens e anexos do Zotero e grava um índice TSV para busca local.

Uso: python3 indexar_biblioteca.py <pasta_saida>
Saída: cols.json, lib.json, att.json, index.tsv
(key, tipo, data, autores, título, livro, pastas, tags, resumo[:300], anexos)
Só leitura. Credenciais via zapi.py da skill zotero-organization.
"""
import sys, json, os
sys.path.insert(0, os.path.expanduser('~/.claude/skills/zotero-organization/scripts'))
from zapi import get_all

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
cols = get_all('/collections')
lib = get_all('/items/top?itemType=-attachment%20||%20note')
att = get_all('/items?itemType=attachment')
for n, d in [('cols', cols), ('lib', lib), ('att', att)]:
    json.dump(d, open(f'{out}/{n}.json', 'w'), ensure_ascii=False)

by = {c['key']: c['data'] for c in cols}
def path(k):
    d = by[k]; p = d['parentCollection']
    return (path(p) + '>' if p else '') + d['name']
files = {}
for a in att:
    p = a['data'].get('parentItem')
    if p: files.setdefault(p, []).append(a['data'].get('filename') or a['data'].get('title', ''))
clean = lambda s: (s or '').replace('\t', ' ').replace('\n', ' ')
with open(f'{out}/index.tsv', 'w') as f:
    for i in lib:
        d = i['data']
        au = '; '.join((c.get('lastName') or c.get('name', '')) for c in d.get('creators', [])[:4])
        f.write('\t'.join(map(clean, [d['key'], d['itemType'], d.get('date', '')[:10], au, d.get('title', ''),
            d.get('bookTitle', '') or d.get('publicationTitle', ''),
            ' | '.join(path(c) for c in d.get('collections', []) if c in by),
            ','.join(t['tag'] for t in d.get('tags', [])), (d.get('abstractNote') or '')[:300],
            ' ; '.join(files.get(d['key'], []))])) + '\n')
# PDFs soltos (sem registro pai) também podem ser obras procuradas
loose = [a['data'] for a in att if not a['data'].get('parentItem')]
with open(f'{out}/anexos_soltos.tsv', 'w') as f:
    for d in loose: f.write(f"{d['key']}\t{clean(d.get('filename') or d.get('title'))}\n")
print(f'{len(lib)} itens, {len(att)} anexos ({len(loose)} soltos), {len(cols)} pastas -> {out}')
