"""Extrato de leitura de um PDF com número de página impressa.

Uso: python3 extrato_pdf.py PDF SAIDA [pág_ini pág_fim] [--kw termo1,termo2,...]
Textos curtos (até ~2.500 palavras) saem inteiros. Nos longos: início (~2.200
palavras), fim antes da bibliografia (~1.300) e trechos com as palavras-chave.
Cada página vem marcada como [p.pdf N | impr. M] (M = número impresso detectado;
pode faltar). Para livros, passe o intervalo do capítulo relevante.
PDF escaneado sai vazio: renderize páginas com
  pdftoppm -r 90 -f N -l N -png PDF prefixo
e leia a imagem.
"""
import sys, subprocess, re
LIMIT, HEAD, TAIL, KWMAX = 2500, 2200, 1300, 22
pdf, out = sys.argv[1], sys.argv[2]
rest = sys.argv[3:]; kw = []
if '--kw' in rest:
    i = rest.index('--kw'); kw = rest[i + 1].split(','); rest = rest[:i] + rest[i + 2:]
args = rest
N = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
a, b = (int(args[0]), int(args[1])) if len(args) >= 2 else (1, N)
pages = []
for p in range(a, b + 1):
    t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), '-layout', pdf, '-'], capture_output=True, text=True).stdout
    lines = [l.strip() for l in t.splitlines() if l.strip()]
    num = None
    for l in lines[:2] + lines[-2:]:
        m = re.fullmatch(r'(\d{1,4})|(\d{1,4})\s{2,}.*|.*\s{2,}(\d{1,4})', l)
        if m: num = next(x for x in m.groups() if x); break
    pages.append((p, num, re.sub(r'\s+', ' ', t)))
for i, (_, _, t) in enumerate(pages):  # corta a bibliografia (metade final)
    if i > len(pages) // 2 and re.search(r'\b(Referências|Referencias|References|Bibliografia|Bibliography)\b\s+[A-ZÁÉ]', t):
        pages = pages[:i + 1]; break
W = lambda s: len(s.split())
total = sum(W(t) for _, _, t in pages)
with open(out, 'w') as f:
    f.write(f'# {pdf}\n# pdf pages {a}-{b}, {total} words\n')
    pr = lambda p, n, t: f.write(f'\n[p.pdf {p} | impr. {n}] {t}\n')
    if total <= LIMIT:
        for x in pages: pr(*x)
    else:
        acc = 0
        for x in pages:
            if acc > HEAD: break
            pr(*x); acc += W(x[2])
        f.write('\n## ... FIM DO TEXTO ...\n')
        tail, acc = [], 0
        for x in reversed(pages):
            if acc > TAIL: break
            tail.insert(0, x); acc += W(x[2])
        for x in tail: pr(*x)
        if kw:
            f.write('\n## TRECHOS COM PALAVRAS-CHAVE\n'); seen = 0
            for p, n, t in pages:
                for k in kw:
                    for m in re.finditer(re.escape(k), t, re.I):
                        if seen > KWMAX: break
                        f.write(f'[p.pdf {p} | impr. {n}] …{t[max(0, m.start() - 250):m.end() + 250]}…\n'); seen += 1
print(out, total, 'words')
