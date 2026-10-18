"""Lista as marcas de citação pendente de um capítulo .tex, com a seção onde estão.

Uso: python3 lacunas_citacao.py <capitulo.tex> [linha_inicial linha_final]
Pega \\todouser{...}{...} que pedem fonte e "(fonte)"/"(FULANO)" em texto puro.
"""
import sys, re
path = sys.argv[1]
a, b = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1, 10**9)
pat = re.compile(r'\\todouser\{[^}]*\}\{([^}]*)\}|\((fonte[^)]*|FULANO[^)]*|[^)]{0,25}fonte)\)', re.I)
sec = ''
for n, line in enumerate(open(path, encoding='utf-8'), 1):
    m = re.match(r'\\(sub)*section\{([^}]*)\}', line)
    if m: sec = m.group(2)
    if a <= n <= b:
        for h in pat.finditer(line):
            ctx = line[max(0, h.start() - 90):h.start()].strip().replace('\n', ' ')
            print(f'l.{n}\t{sec[:40]}\t{(h.group(1) or h.group(2)).strip()}\t…{ctx}')
