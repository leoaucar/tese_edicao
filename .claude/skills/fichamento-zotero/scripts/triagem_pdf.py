"""Triagem dos itens de uma ou mais pastas do Zotero para fichamento.

Uso: python3 triagem_pdf.py <saida_dir> COLKEY[:rótulo] [COLKEY[:rótulo] ...]
Gera:
  triagem.json        um registro por item: key, pasta, tipo, autores, título, PDFs
                      (chave do anexo, caminho, nº de páginas, palavras numa amostra
                      do meio), notas-filhas existentes e se já há "Ficha IA"
  faltam_pdf.txt      itens sem PDF e com PDF escaneado (sem texto), para o usuário
Só leitura.
"""
import sys, os, json, glob, subprocess
sys.path.insert(0, os.path.expanduser('~/.claude/skills/zotero-organization/scripts'))
from zapi import get_all

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
rows = []
for arg in sys.argv[2:]:
    col, _, label = arg.partition(':')
    for t in get_all(f'/collections/{col}/items/top'):
        d = t['data']
        if d['itemType'] in ('note', 'attachment'): continue
        kids = get_all(f"/items/{d['key']}/children")
        notes = [c['data'] for c in kids if c['data']['itemType'] == 'note']
        pdfs = []
        for c in kids:
            a = c['data']
            if a.get('contentType') != 'application/pdf': continue
            fs = glob.glob(os.path.expanduser(f"~/Zotero/storage/{a['key']}/*.pdf"))
            if not fs: pdfs.append({'key': a['key'], 'path': None}); continue
            info = subprocess.run(['pdfinfo', fs[0]], capture_output=True, text=True).stdout
            n = next((int(l.split()[-1]) for l in info.splitlines() if l.startswith('Pages')), 0)
            mid = max(1, n // 2)
            w = len(subprocess.run(['pdftotext', '-f', str(mid), '-l', str(min(n, mid + 2)), fs[0], '-'],
                                   capture_output=True, text=True).stdout.split())
            pdfs.append({'key': a['key'], 'path': fs[0], 'pages': n, 'mid_words': w, 'scanned': w < 150})
        rows.append({'key': d['key'], 'pasta': label or col, 'type': d['itemType'], 'title': d.get('title', ''),
                     'date': d.get('date', ''), 'authors': '; '.join((c.get('lastName') or c.get('name', ''))
                                                                     for c in d.get('creators', [])[:3]),
                     'pdfs': pdfs, 'n_notes': len(notes),
                     'user_notes': [n['key'] for n in notes if 'Ficha IA' not in (n.get('note') or '')],
                     'has_ficha_ia': any('Ficha IA' in (n.get('note') or '') for n in notes)})
json.dump(rows, open(f'{out}/triagem.json', 'w'), ensure_ascii=False, indent=1)
nopdf = [r for r in rows if not any(p.get('path') for p in r['pdfs'])]
scan = [r for r in rows if r not in nopdf and all(p.get('scanned', True) for p in r['pdfs'] if p.get('path'))]
with open(f'{out}/faltam_pdf.txt', 'w') as f:
    f.write('Itens sem PDF utilizável\n\nSEM PDF ANEXADO\n')
    for r in nopdf: f.write(f"{r['pasta']}  {r['key']}  {r['authors']} ({r['date'][:4]}). {r['title']}\n")
    f.write('\nPDF ESCANEADO, SEM TEXTO (precisa de OCR ou de outro arquivo)\n')
    for r in scan: f.write(f"{r['pasta']}  {r['key']}  {r['authors']} ({r['date'][:4]}). {r['title']}\n")
for r in rows:
    st = 'sem PDF' if r in nopdf else ('escaneado' if r in scan else 'texto')
    print(f"{r['pasta']}\t{r['key']}\t{st}\tnotas={r['n_notes']}{' FICHA' if r['has_ficha_ia'] else ''}\t{r['authors'][:25]} | {r['title'][:60]}")
