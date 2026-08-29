# Ambiente

Ferramentas necessárias para rodar este projeto em qualquer máquina. Não há dependências Python neste momento — se alguma skill futura (`specs/proposed_skills.md`) for implementada em Python, um `requirements.txt`/`pyproject.toml` será adicionado então.

## Ferramentas

| Ferramenta | Uso | Versão testada |
|---|---|---|
| Git | controle de versão | - |
| Uma distribuição LaTeX (MiKTeX ou TeX Live) — fornece `pdflatex` | compilar `main.tex` | MiKTeX 25.12 |
| Pandoc | conversão inicial docx → LaTeX | - |

### Pacotes LaTeX usados por `main.tex`

`inputenc`, `fontenc` (T1), `babel` (brazil), `graphicx`, `csvsimple`, `xcolor`, `ulem`, `natbib`, `url`, `longtable`, `booktabs`, `array`, `calc` — distribuições completas (MiKTeX com instalação automática de pacotes, ou TeX Live `full`) já cobrem todos eles.

### Notas de importação docx → LaTeX (aprendido na rodada `2026-08-29_capitulo_historico_1_review`)

- **Normalizar para NFC**: arquivos `.tex` gerados por `pandoc` a partir de `.docx` do Word costumam vir em Unicode NFD (acentos como caractere base + combining mark), o que quebra buscas/substituições por string exata. Rodar uma normalização NFC (`unicodedata.normalize("NFC", texto)` em Python) logo após a conversão, antes de qualquer edição manual.
- **Caracteres Unicode incomuns**: qualquer caractere fora de ASCII/Latin-1 básico que não seja uma letra acentuada comum (setas `→`, combinações raras como "e com til" `ẽ`) trava o `pdflatex` com `inputenc`/`utf8`. Ou substituir por um comando LaTeX equivalente (ex.: `$\rightarrow$`), ou declarar via `\DeclareUnicodeCharacter{XXXX}{...}` no preâmbulo.
- **Tabelas do Word**: pandoc converte para `longtable` com larguras de coluna calculadas via `\real{}` — isso requer o pacote `calc`, que não vem com um preâmbulo mínimo.
- **Citações do Zotero (plugin do Google Docs/Word)**: viram `\href{https://www.zotero.org/...}{(Autor, Ano)}` — não são links reais e precisam ser convertidos manualmente/por script para `\citep`/`\citet`/`\citeyearpar` (`natbib`), gerando ao mesmo tempo entradas *stub* em `references.bib` até a biblioteca real do Zotero ser exportada.

## Instalação por sistema

**Windows**
```powershell
winget install --id MiKTeX.MiKTeX -e
winget install --id JohnMacFarlane.Pandoc -e
```

**macOS**
```bash
brew install --cask mactex-no-gui   # ou basictex + tlmgr install dos pacotes acima
brew install pandoc
```

**Linux (Debian/Ubuntu)**
```bash
sudo apt install texlive-full pandoc
```

## Clonar o projeto em outra máquina

```bash
git clone https://github.com/leoaucar/tese_edicao.git
cd tese_edicao
git checkout <branch-da-rodada-em-andamento>
```

Depois de instaladas as ferramentas acima, `pdflatex main.tex` deve compilar sem configuração adicional.

## Compilar manualmente durante a revisão

```powershell
pdflatex -interaction=nonstopmode -output-directory=outputs main.tex
```

- Rodar **duas vezes** sempre que citações, referências cruzadas (`\ref`/`\label`) ou o sumário mudarem — a primeira passada escreve o `.aux`, a segunda resolve as referências contra ele.
- Rodar `bibtex` entre duas passadas de `pdflatex` sempre que entradas `\citep`/`\citet` forem adicionadas/alteradas (o `natbib` só recarrega o `.bbl` depois disso):
  ```powershell
  pdflatex -interaction=nonstopmode -output-directory=outputs main.tex
  bibtex outputs\main
  pdflatex -interaction=nonstopmode -output-directory=outputs main.tex
  pdflatex -interaction=nonstopmode -output-directory=outputs main.tex
  ```
- Alternativa mais simples: `latexmk -pdf -output-directory=outputs main.tex` — detecta sozinho quantas passadas (e se `bibtex`) são necessárias e reroda até estabilizar. Preferível para iteração rápida durante revisão.
- Se `pdflatex`/`latexmk` não forem encontrados no PATH mesmo após instalar o MiKTeX, abra um terminal novo (o PATH de usuário só é lido na criação do processo).
