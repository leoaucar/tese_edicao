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

## Configuração do VS Code / LaTeX Workshop

`.vscode/settings.json` é ignorado pelo git (`.gitignore`, configuração pessoal de editor) — o conteúdo abaixo é a referência para recriá-lo em qualquer máquina.

```json
{
  "latex-workshop.latex.outDir": "%DIR%/outputs",

  // Fonte um pouco maior e mais legível para edição de prosa em .tex.
  "[latex]": {
    "editor.fontSize": 16,
    "editor.lineHeight": 26
  },
  "[tex]": {
    "editor.fontSize": 16,
    "editor.lineHeight": 26
  },

  // Colore pares de {...}/[...] aninhados — LaTeX aninha chaves com
  // frequência (\citep[p.~91]{buescu1984}) e isso facilita ver o par.
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": "active",

  // Cores mais contrastantes/diferenciadas para tokens LaTeX (ajustado para
  // o tema "Visual Studio Dark"). Atuam sobre escopos TextMate, então valem
  // para qualquer \comando / ambiente / comentário, mas NÃO conseguem
  // distinguir um macro específico como \aiflag — escopos TextMate não
  // diferenciam pelo nome literal do comando, só pelo papel sintático
  // (ver highlight.regexes abaixo para isso).
  "editor.tokenColorCustomizations": {
    "textMateRules": [
      {
        "scope": "comment.line.percentage.tex",
        "settings": { "foreground": "#6A9955", "fontStyle": "italic" }
      },
      {
        "scope": ["support.function.general.tex", "support.function.section.latex"],
        "settings": { "foreground": "#4EC9B0", "fontStyle": "bold" }
      },
      {
        "scope": "keyword.control.tex",
        "settings": { "foreground": "#C586C0", "fontStyle": "bold" }
      },
      {
        "scope": "constant.character.escape.tex",
        "settings": { "foreground": "#D7BA7D" }
      },
      {
        "scope": ["punctuation.definition.arguments.begin.latex", "punctuation.definition.arguments.end.latex"],
        "settings": { "foreground": "#D4D4D4" }
      }
    ]
  },

  // Requer a extensão "Highlight" (fabiospampinato.vscode-highlight) —
  // instalar manualmente via Ctrl+Shift+X, buscar "Highlight". Destaca
  // \aiflag{...} (sugestão da IA, ver specs/constitution.md) e blocos
  // \begin{esboco}...\end{esboco} (rascunho do autor) com fundo chamativo
  // para não passarem despercebidos durante a leitura/edição.
  "highlight.regexes": {
    "(\\\\aiflag\\{)": {
      "filterFileRegex": ".*\\.tex$",
      "decorations": [
        { "backgroundColor": "#ff000055", "color": "#ffffff", "fontWeight": "bold" }
      ]
    },
    "(\\\\begin\\{esboco\\}[\\s\\S]*?\\\\end\\{esboco\\})": {
      "filterFileRegex": ".*\\.tex$",
      "decorations": [
        { "backgroundColor": "#88888833" }
      ]
    }
  },

  // Requer a extensão "LTeX+" (ltex-plus.vscode-ltex-plus) — instalar
  // manualmente via Ctrl+Shift+X, buscar "LTeX+". A extensão original
  // valentjn.vscode-ltex está depreciada/arquivada; este é o fork
  // atualmente mantido, mas manteve as mesmas chaves "ltex.*" abaixo.
  // Verificação ortográfica/gramatical consciente de LaTeX (ignora
  // corretamente \comandos e chaves de citação); português brasileiro.
  "ltex.language": "pt-BR",
  "ltex.enabled": ["latex", "tex"],
  // Nomes próprios e termos do projeto que são sinalizados como erro de
  // ortografia — adicionar conforme novos falsos positivos aparecerem.
  "ltex.dictionary": {
    "pt-BR": [
      "Furtado", "Suzigan", "Tavares", "Mello", "Prado", "Fernandes",
      "Buescu", "Nogueira", "Wallerstein", "Braudel", "Mahoney", "Falleti",
      "Pierson", "Vargas", "Jânio", "Jango", "Kubitschek", "SUMOC", "BNDE",
      "CEPAL", "CMBEU", "Zotero", "aiflag", "esboco"
    ]
  }
}
```

- **Extensões necessárias**: `james-yu.latex-workshop` (já instalada); para o destaque de `\aiflag`/`esboco`, `fabiospampinato.vscode-highlight`; para a correção ortográfica em português, `ltex-plus.vscode-ltex-plus` ("LTeX+" no Marketplace — **não** instalar `valentjn.vscode-ltex`, que está depreciado/arquivado desde abril de 2026). Todas de instalação manual — o CLI `code --install-extension` está quebrado nesta máquina por um conflito de `PATH` com o Anaconda, não relacionado ao projeto.
- `ltex-plus.vscode-ltex-plus` baixa seu próprio runtime + modelos de idioma na primeira ativação (download maior, ocorre uma vez; depois funciona offline). Falsos positivos recorrentes (nomes próprios, siglas) devem ser adicionados a `ltex.dictionary.pt-BR` em vez de ignorados manualmente a cada vez.
- Após criar/editar `.vscode/settings.json`, recarregar a janela do VS Code (`Ctrl+Shift+P` → "Reload Window") para aplicar.
- `latex-workshop.latex.outDir` mantém o build automático do LaTeX Workshop (que roda a cada save) escrevendo em `outputs/`, em vez de poluir a raiz do projeto — ver a seção de compilação manual acima para o motivo.
