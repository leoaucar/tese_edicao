"""Converte referências de linha (l.71, l.56-78) em âncoras estáveis:
seção + início do parágrafo (ou o tópico, em listas de esboço).

Uso: python3 ancora_capitulo.py CAPITULO.tex FICHAS.md SAIDA.md
O .tex deve ser a MESMA versão usada para escrever as linhas nas fichas.
"""
import sys, re
tex, src, dst = sys.argv[1:4]
old = {i + 1: l for i, l in enumerate(open(tex, encoding='utf-8').read().split('\n'))}
def clean(s):
    s = re.sub(r'\\(todouser|todoaiflag)\{[^}]*\}\{[^}]*\}', '', s)
    s = re.sub(r'\\sout\{[^}]*\}', '', s)
    s = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()
counters = [0, 0, 0]; chap = 0; sec = {}; par = {}; cur = ''; start = None
for n in sorted(old):
    t = old[n]
    if t.startswith('\\chapter'): chap += 1; counters = [0, 0, 0]
    m = re.match(r'\\(sub)?(sub)?section\*?\{([^}]*)\}', t)
    if m:
        lvl = 2 if m.group(2) else (1 if m.group(1) else 0)
        counters[lvl] += 1; counters[lvl + 1:] = [0] * (2 - lvl)
        cur = '.'.join(str(c) for c in [chap or 2] + counters[:lvl + 1]) + f' ({m.group(3)[:40]})'
        start = None; sec[n] = cur; par[n] = None; continue
    if not t.strip(): start = None; sec[n] = cur; par[n] = None; continue
    if start is None: start = n
    sec[n] = cur; par[n] = start
def anchor(a):
    if old.get(a, '').lstrip().startswith('-'):
        return f'{sec.get(a, "")}, tópico “{clean(old[a]).lstrip("-").strip()[:70]}”'
    s = par.get(a); b = a
    while s is None and b in old: b += 1; s = par.get(b)
    return f'{sec.get(a, "")}, parágrafo “{" ".join(clean(old.get(s, "")).split()[:6])}…”'
def rep(m):
    a, b = int(m.group(1)), m.group(2)
    return anchor(a) + (' e seguintes' if b and par.get(int(b)) != par.get(a) else '')
open(dst, 'w').write(re.sub(r'\bl\.(\d+)(?:-(\d+))?', rep, open(src).read()))
print('ok ->', dst)
