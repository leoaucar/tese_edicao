# Ambiente

Ferramentas necessárias para rodar este projeto em qualquer máquina. Não há dependências Python neste momento — se alguma skill futura (`specs/proposed_skills.md`) for implementada em Python, um `requirements.txt`/`pyproject.toml` será adicionado então.

## Ferramentas

| Ferramenta | Uso | Versão testada |
|---|---|---|
| Git | controle de versão | - |
| Uma distribuição LaTeX (MiKTeX ou TeX Live) — fornece `pdflatex` | compilar `main.tex` | MiKTeX 25.12 |
| Pandoc | conversão docx → LaTeX (importação) e LaTeX → docx (exportação, ver `scripts/export_docx/`) | 3.8 |
| Node.js | roda `scripts/export_docx/export.js` | - |

### Pacotes LaTeX usados por `main.tex`

Desde a formatação ABNT (rodada atual), `main.tex` usa a classe `abntex2` (baseada em `memoir`) em vez de `report` puro — ela já configura margens (3cm/2cm/3cm/2cm), espaçamento 1,5 e idioma (`babel[brazil]`) por padrão, conforme ABNT NBR 14724. Pacotes carregados manualmente: `inputenc`, `fontenc` (T1), `mathptmx` (fonte Times), `indentfirst`, `graphicx`, `csvsimple`, `xcolor`, `ulem`, `url`, `longtable`, `booktabs`, `array`, `calc`, `microtype`, `abntex2cite` (citações/referências ABNT NBR 10520/6023, estilo `alf`) — distribuições completas (MiKTeX com instalação automática de pacotes, ou TeX Live `full`) já cobrem todos eles.

- **`natbib` foi removido** em favor de `abntex2cite`. `abntex2cite` não define `\citep`/`\citet`/`\citeyearpar` nativamente (usa `\cite`/`\citeonline`/`\citeyear`) — `main.tex` define wrappers de compatibilidade no preâmbulo para que as citações já escritas nos capítulos continuem funcionando sem editá-las.
- **`microtype` com `expansion=false`**: a expansão de fonte do `microtype` não funciona com o Times (`mathptmx`) nesta instalação MiKTeX (`pdfTeX error (font expansion): auto expansion is only possible with scalable fonts`). Mantido só o protrusion (`expansion=false`).
- **`\hypersetup{unicode=false}`**: a classe `abntex2` carrega `hyperref`+`bookmark`, que por padrão gravam os bookmarks de PDF (títulos de capítulo) em UTF-16 dentro de `main.aux` — isso inclui bytes NUL para caracteres ASCII, e o `bibtex` (parser não é 8-bit-clean) trava com `! Text line contains an invalid character.` ao ler esse `main.aux`. Como os acentos do português cabem em PDFDocEncoding (1 byte), forçar `unicode=false` evita os bytes NUL sem perder a acentuação nos bookmarks.

### Exportação LaTeX → DOCX (`scripts/export_docx/`)

`main.tex` não converte bem para DOCX diretamente via `pandoc main.tex -o saida.docx` — testado e descartado: o leitor LaTeX do pandoc não entende a classe `abntex2` nem `csvsimple` (capa/folha de rosto/resumo e todas as tabelas vindas de CSV somem silenciosamente), e o escritor docx do pandoc descarta `\textcolor{...}` (a convenção `\aiflag` de "sugestão em vermelho" da IA, exigida em `specs/constitution.md`, viraria texto preto comum).

`scripts/export_docx/export.js <capítulo.tex> [saída.docx]` resolve isso: envolve o capítulo num preâmbulo mínimo que o pandoc entende de verdade (sem `abntex2`, com `natbib` real para que `\citep`/`\citet`/`\citeyearpar` resolvam via `--citeproc`), converte cada `\csvautotabular{...}` numa tabela LaTeX de verdade antes de passar pelo pandoc, e roda o pandoc com um filtro Lua (`aiflag_style.lua`) + um `reference.docx` customizado (`reference.docx`, com estilos de caractere `AIFlagRed`/`EsbocoGray`) para que `\textcolor{red}{...}`/`\textcolor{gray}{...}` virem estilo de caractere do Word em vez de serem descartados. Exemplo:

```powershell
node scripts/export_docx/export.js "chapters/04-Processo de industrialização (1808-1973).tex"
```

Gera em `outputs/` (gitignored). Ainda não cobre a exportação do `main.tex` inteiro ("copião" unificado, item pendente em `specs/roadmap.md`) — só capítulos individuais, o que já atende ao fluxo de revisão por capítulo de `specs/constitution.md`.

### Notas de importação docx → LaTeX (aprendido na rodada `2026-08-29_capitulo_historico_1_review`)

- **Normalizar para NFC**: arquivos `.tex` gerados por `pandoc` a partir de `.docx` do Word costumam vir em Unicode NFD (acentos como caractere base + combining mark), o que quebra buscas/substituições por string exata. Rodar uma normalização NFC (`unicodedata.normalize("NFC", texto)` em Python) logo após a conversão, antes de qualquer edição manual.
- **Caracteres Unicode incomuns**: qualquer caractere fora de ASCII/Latin-1 básico que não seja uma letra acentuada comum (setas `→`, combinações raras como "e com til" `ẽ`) trava o `pdflatex` com `inputenc`/`utf8`. Ou substituir por um comando LaTeX equivalente (ex.: `$\rightarrow$`), ou declarar via `\DeclareUnicodeCharacter{XXXX}{...}` no preâmbulo.
- **Texto Word com realce (highlight) branco**: colar texto de outra fonte no Word às vezes carrega `w:highlight w:val="white"` — invisível no documento original, mas o `pandoc` converte para `\hl{...}` (pacote `soul`, que não está no preâmbulo). Como é sempre ruído de formatação (branco = sem efeito visual), a limpeza remove o `\hl{}` mantendo o conteúdo, em vez de adicionar o pacote.

### Problemas de qualidade de dados em `references.bib` (aprendido na rodada `2026-08-30_capitulo_teoria_2_import`)

Ao mesclar um `.bib` exportado do Zotero, duas categorias de erro já quebraram a compilação inteira (não só a entrada afetada) porque o `bibtex` aborta o processamento do arquivo inteiro ao encontrar uma entrada malformada:

- **Nome de autor institucional com vírgulas demais**: um campo `author`/`editor` tipo `{CNDI, Conselho Nacional de... and MDIC, Indústria, Comércio e Serviços, Ministério do Desenvolvimento}` quebra o parser de nomes do BibTeX (`Too many commas in name`) porque o segundo "autor" tem 3 vírgulas (o máximo aceito é 2, para o formato `von Last, Jr, First`). Correção: envolver cada nome institucional em chaves duplas — `{{CNDI, Conselho Nacional de Desenvolvimento Industrial} and {MDIC, ...}}` — para o BibTeX tratar a vírgula interna como parte de um nome literal, não como separador.
- **Caracteres Unicode fora do repertório português/francês/alemão comum** (ex.: `Ş`/`ş` turco) podem corromper a saída (`Invalid UTF-8 byte sequence`) quando o estilo `abntex2-alf.bst` gera rótulos de citação via `change.case$` — o BibTeX clássico não é Unicode-aware e processa nomes byte a byte, o que pode cortar um caractere UTF-8 multibyte ao meio dependendo do algoritmo de truncamento do estilo. Correção: escrever o caractere problemático em forma de comando LaTeX (`{\c S}evket` em vez de `Şevket`) em vez de UTF-8 bruto. Acentos comuns (á, ã, ç, é, ô, ú etc.) não tiveram esse problema — parece ser específico de caracteres realmente incomuns no corpus (não vale a pena converter o `.bib` inteiro preventivamente; corrigir pontualmente quando a compilação apontar o erro).
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
