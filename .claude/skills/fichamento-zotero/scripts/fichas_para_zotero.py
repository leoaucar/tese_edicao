"""Grava fichas (Markdown) como notas-filhas "Ficha IA" no Zotero.

Uso: python3 fichas_para_zotero.py FICHAS.md BACKUP_DIR [--apply]
Formato de FICHAS.md: um bloco por item, começando por "### ITEMKEY", com as linhas
  Pasta: … / Resumo: … / Como aborda o tema: … / Ideias para o capítulo: (lista "- ")
  / Onde usar: … / Fonte da ficha: …
Sem --apply só mostra o que faria. Item que já tem nota "Ficha IA" tem a nota
ATUALIZADA (nunca duplicada); os outros ganham nota nova. As notas do usuário
nunca são tocadas. Grava BACKUP_DIR/fichas_notas.json (item -> nota) e uma cópia
das notas antigas antes de atualizá-las.
"""
import sys, os, re, json, html, datetime
sys.path.insert(0, os.path.expanduser('~/.claude/skills/zotero-organization/scripts'))
from zapi import req, get_all, write

src, bdir = sys.argv[1], sys.argv[2]; APPLY = '--apply' in sys.argv
os.makedirs(bdir, exist_ok=True); today = datetime.date.today().isoformat()
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    return re.sub(r'(?<!\*)\*(?!\*)(.+?)\*', r'<em>\1</em>', s)
LABELS = r'(Resumo|Como aborda o tema|Ideias para o capítulo|Onde usar|Fonte da ficha|[A-ZÁÉ][^:]{2,40})'
def render(body):
    pasta = next((l.split(':', 1)[1].strip() for l in body if l.startswith('Pasta:')), '')
    out, inlist = [f'<h2>Ficha IA: {inline(pasta)} ({today})</h2>'], False
    for l in body:
        if l.startswith('Pasta:'): continue
        if l.startswith('- '):
            if not inlist: out.append('<ul>'); inlist = True
            out.append(f'<li>{inline(l[2:])}</li>'); continue
        if inlist: out.append('</ul>'); inlist = False
        if not l.strip(): continue
        m = re.match(r'^(Resumo|Como aborda o tema|Ideias para o capítulo|Onde usar|Fonte da ficha):(.*)$', l)
        out.append(f'<p><strong>{m.group(1)}:</strong>{inline(m.group(2))}</p>' if m else f'<p>{inline(l)}</p>')
    if inlist: out.append('</ul>')
    out.append('<p><em>Ficha gerada por IA (Claude) a partir da leitura descrita em "Fonte da ficha". '
               'Âncoras: seção e início do parágrafo do capítulo.</em></p>')
    return '<div data-schema-version="9">' + '\n'.join(out) + '</div>'
fichas = {}
for b in re.split(r'^### ', open(src).read(), flags=re.M)[1:]:
    lines = b.strip().split('\n'); fichas[lines[0].strip()] = render(lines[1:])
create, update, backup = [], [], {}
for k, h in fichas.items():
    old = [c['data'] for c in get_all(f'/items/{k}/children')
           if c['data']['itemType'] == 'note' and 'Ficha IA' in (c['data'].get('note') or '')]
    if old:
        backup[k] = old[0]['note']; update.append({'key': old[0]['key'], 'version': old[0]['version'], 'note': h})
    else:
        create.append({'itemType': 'note', 'parentItem': k, 'note': h, 'tags': []})
print(f'{len(fichas)} fichas: {len(create)} novas, {len(update)} a atualizar')
if not APPLY: print('DRY RUN (use --apply)'); sys.exit()
json.dump(backup, open(f'{bdir}/fichas_notas_antes_{today}.json', 'w'), ensure_ascii=False, indent=1)
mapping = {}
for s in range(0, len(create), 50):
    r = req('POST', '/items', create[s:s + 50])
    print('criadas', len(r.get('success', {})), 'falhas', r.get('failed'))
    for i, nk in r.get('success', {}).items(): mapping[create[s + int(i)]['parentItem']] = nk
if update: print('atualizadas', write(update))
json.dump(mapping, open(f'{bdir}/fichas_notas.json', 'w'), indent=1)
