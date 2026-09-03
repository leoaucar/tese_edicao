# Ambiente

Ferramentas necessárias para rodar este projeto em qualquer máquina. Não há dependências Python neste momento — se alguma skill futura (`specs/proposed_skills.md`) for implementada em Python, um `requirements.txt`/`pyproject.toml` será adicionado então.

## Ferramentas

| Ferramenta | Uso | Versão testada |
|---|---|---|
| Git | controle de versão | - |
| Uma distribuição LaTeX (MiKTeX ou TeX Live) — fornece `pdflatex` | compilar `main.tex` | MiKTeX 25.12 |
| Perl (ex.: Strawberry Perl no Windows) | `latexmk` é um script Perl — sem isso ele falha na inicialização com `MiKTeX could not find the script engine 'perl'`, mesmo com o `.tex` compilando normalmente via `pdflatex` puro | Strawberry Perl (winget) |
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

### Problema de compilação em `\caption{}` (aprendido na rodada `2026-08-30_capitulo_metodologia_3_import`)

- **`\footnote{}` dentro de `\caption{}` quebra a Lista de Tabelas**: o pandoc às vezes converte uma nota do Word que originalmente ancorava numa legenda de tabela para dentro do próprio `\caption{...}` gerado. Isso causa `! Runaway argument?`/`! File ended while scanning use of \@caption` — fatal, aborta a compilação inteira — porque o mecanismo de Lista de Tabelas do LaTeX reprocessa o conteúdo do `\caption` num contexto que não aceita notas de rodapé. Correção: mover a nota para uma frase do corpo do texto que introduz a tabela (antes ou depois do `\begin{table}`), preservando o conteúdo da nota, em vez de deixá-la dentro do `\caption{}`.

## Instalação por sistema

**Windows**
```powershell
winget install --id MiKTeX.MiKTeX -e
winget install --id StrawberryPerl.StrawberryPerl -e
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
- Alternativa mais simples: `latexmk -pdf main.tex` — detecta sozinho quantas passadas (e se `bibtex`) são necessárias e reroda até estabilizar; a saída já vai para `outputs/` porque `.latexmkrc` define `$out_dir = 'outputs'` (não precisa mais passar `-output-directory=outputs` manualmente). Preferível para iteração rápida durante revisão. Requer Perl (ver tabela de ferramentas acima).
- Se `pdflatex`/`latexmk` não forem encontrados no PATH mesmo após instalar o MiKTeX (ou o Perl), abra um terminal novo (o PATH de usuário só é lido na criação do processo).

## Configuração do VS Code / LaTeX Workshop

`.vscode/settings.json` é ignorado pelo git (`.gitignore`, configuração pessoal de editor) — o conteúdo abaixo é a referência para recriá-lo em qualquer máquina.

```json
{
  // Light theme for the whole window (VS Code themes are global, not
  // per-language) — chosen for readability while writing prose-heavy .tex.
  // "Light+" is this VS Code install's actual stored id for the built-in
  // light theme (NOT "Default Light+", which looked right but silently
  // matched nothing in the scoped customizations below).
  "workbench.colorTheme": "Light+",

  // O sidebar (explorer/busca/etc.) do tema claro é muito lavado — fundo
  // cinza-claro e texto cinza de baixo contraste. Escurece o fundo e leva o
  // texto para preto, para legibilidade. Deixado sem escopo de tema (fora de
  // uma chave "[Nome do Tema]") para funcionar não importa qual tema claro
  // esteja ativo.
  //
  // O terminal é mantido deliberadamente numa paleta escura fixa (cores
  // clássicas do Dark+) independente do tema do editor/sidebar — pedido
  // explícito do usuário, já que o tema claro é para legibilidade de prosa
  // nos .tex, não para o terminal.
  "workbench.colorCustomizations": {
    "sideBar.background": "#DCDCDC",
    "sideBar.foreground": "#000000",
    "sideBarTitle.foreground": "#000000",
    "sideBarSectionHeader.background": "#CCCCCC",
    "sideBarSectionHeader.foreground": "#000000",
    "list.inactiveSelectionBackground": "#C4C4C4",
    "list.hoverBackground": "#CACACA",
    "list.activeSelectionBackground": "#B8B8B8",
    "list.activeSelectionForeground": "#000000",
    "list.focusForeground": "#000000",
    "list.inactiveSelectionForeground": "#000000",

    "terminal.background": "#1E1E1E",
    "terminal.foreground": "#CCCCCC",
    "terminalCursor.foreground": "#FFFFFF",
    "terminal.ansiBlack": "#000000",
    "terminal.ansiRed": "#CD3131",
    "terminal.ansiGreen": "#0DBC79",
    "terminal.ansiYellow": "#E5E510",
    "terminal.ansiBlue": "#2472C8",
    "terminal.ansiMagenta": "#BC3FBC",
    "terminal.ansiCyan": "#11A8CD",
    "terminal.ansiWhite": "#E5E5E5",
    "terminal.ansiBrightBlack": "#666666",
    "terminal.ansiBrightRed": "#F14C4C",
    "terminal.ansiBrightGreen": "#23D18B",
    "terminal.ansiBrightYellow": "#F5F543",
    "terminal.ansiBrightBlue": "#3B8EEA",
    "terminal.ansiBrightMagenta": "#D670D6",
    "terminal.ansiBrightCyan": "#29B8DB",
    "terminal.ansiBrightWhite": "#E5E5E5"
  },

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

  // Cores mais contrastantes/diferenciadas para tokens LaTeX. Escopadas por
  // nome de tema (o VS Code só aplica o bloco correspondente quando aquele
  // tema está ativo) — as regras originais, ajustadas para fundo escuro,
  // continuam funcionando se você voltar para "Visual Studio Dark"; um
  // segundo conjunto, com cores mais escuras/legíveis em fundo claro, vale
  // para "Light+" (id real do tema claro embutido — não "Default Light+",
  // que parecia certo mas não casava com nada). Atuam sobre escopos
  // TextMate, então valem para qualquer \comando / ambiente / comentário,
  // mas NÃO conseguem distinguir um macro específico como \aiflag — escopos
  // TextMate não diferenciam pelo nome literal do comando, só pelo papel
  // sintático (ver highlight.regexes abaixo para isso).
  "editor.tokenColorCustomizations": {
    "[Visual Studio Dark]": {
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
    "[Light+]": {
      "textMateRules": [
        {
          "scope": "comment.line.percentage.tex",
          "settings": { "foreground": "#4B8B3B", "fontStyle": "italic" }
        },
        {
          "scope": ["support.function.general.tex", "support.function.section.latex"],
          "settings": { "foreground": "#0E7490", "fontStyle": "bold" }
        },
        {
          "scope": "keyword.control.tex",
          "settings": { "foreground": "#A626A4", "fontStyle": "bold" }
        },
        {
          "scope": "constant.character.escape.tex",
          "settings": { "foreground": "#986801" }
        },
        {
          "scope": ["punctuation.definition.arguments.begin.latex", "punctuation.definition.arguments.end.latex"],
          "settings": { "foreground": "#444444" }
        }
      ]
    }
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

### Salvando um Profile do VS Code para edição de LaTeX

Como `code --install-extension` está quebrado nesta máquina (achado acima) e
`.vscode/settings.json` é pessoal (fora do git), a forma mais rápida de
reaplicar toda a configuração acima — extensões e settings juntos — em
qualquer instalação do VS Code é exportar um **Profile** nativo, em vez de
reinstalar cada extensão manualmente e recolar o JSON deste documento.

**Exportar o profile atual** (depois de já ter as 3 extensões instaladas e o
`.vscode/settings.json` configurado conforme acima):

1. `Ctrl+Shift+P` → "**Profiles: Export Profile...**".
2. Marcar pelo menos "Settings" e "Extensions" (Keybindings/Snippets/UI
   State são opcionais). Isso inclui `.vscode/settings.json` do jeito que
   estiver na hora do export, não só o que está documentado aqui — mantenha
   os dois sincronizados manualmente se editar um dos dois depois.
3. Duas opções de destino:
   - **"Export Profile (in File)..."** — salva um arquivo
     `.code-profile` local. Guardar fora deste repositório (ex.:
     `C:\Users\leoau\Documents\vscode-profiles\latex-tese.code-profile`) —
     é configuração pessoal de máquina, não conteúdo da tese.
   - **"Export Profile (in GitHub)..."** — salva como Gist na conta
     GitHub do usuário; mais durável entre máquinas/reinstalações
     (recomendado se o objetivo é "sempre poder recuperar", já que não
     depende de copiar um arquivo local).

**Reimportar** (nesta máquina após reinstalar o VS Code, ou em outra
máquina): `Ctrl+Shift+P` → "**Profiles: Import Profile...**" → apontar para
o arquivo `.code-profile` ou colar a URL do Gist → nomear o profile (ex.:
"LaTeX - Tese") → ativar via ícone de Profile no canto inferior esquerdo
(ou `code --profile "LaTeX - Tese"`, quando o CLI `code` não estiver
quebrado).

Alternativa para sincronização contínua (em vez de um snapshot pontual):
**Settings Sync** (`Ctrl+Shift+P` → "Settings Sync: Turn On...") mantém
profiles, extensões e settings sincronizados automaticamente entre todas as
instalações logadas na mesma conta — mais indicado se o usuário troca de
máquina com frequência, em vez de fazer um export manual só quando lembra.

- **Ativar**: ícone de conta (canto inferior esquerdo) → "Backup and Sync
  Settings..." — ou `Ctrl+Shift+P` → "Settings Sync: Turn On" — logar com
  GitHub ou Microsoft, marcar pelo menos Settings, Extensions, Keybindings e
  Profiles. Depois disso sincroniza sozinho em background a cada mudança.
- **Conferir o que está sincronizado**: `Ctrl+Shift+P` → "Settings Sync:
  Show Synced Data".
- **Forçar sincronização manual** (normalmente desnecessário, já é
  automático): `Ctrl+Shift+P` → "Settings Sync: Sync Now".
- **Desativar**: `Ctrl+Shift+P` → "Settings Sync: Turn Off".
