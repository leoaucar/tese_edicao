# Spec: Importação do Capítulo 3 (Metodologia)

## Contexto

Terceira rodada de importação de capítulo, seguindo o workflow validado em `specs/2026-08-29_capitulo_historico_1_review/` (capítulo empírico 1) e `specs/2026-08-30_capitulo_teoria_2_import/` (Teoria). Primeira rodada a usar as skills instaladas em `.claude/skills/` (`importar-docx-latex`, `consolidar-bibliografia-zotero`, `detectar-esboco`, `detectar-conteudo-nao-nativo`).

Capítulo alvo: `chapters/03-Metodologia.tex`.

**Estado real do arquivo hoje**: apenas `\chapter{Metodologia}` e um comentário `% TODO: importar conteúdo` — nenhum texto importado ainda, mesmo com `specs/status_capitulos.md` marcando "Escrita" como `[~]` (parcial). Mesma discrepância já vista nas duas rodadas anteriores; será corrigida ao final desta rodada.

## Entrada recebida

```
specs/2026-08-30_capitulo_metodologia_3_import/Metodologia.docx
specs/2026-08-30_capitulo_metodologia_3_import/metodologia.bib
```

## Descobertas da inspeção inicial

Conversão de teste (`pandoc "Metodologia.docx" -t markdown` → `source_raw.md`, 922 linhas) e leitura de `metodologia.bib` (44 entradas) contra `references.bib` (159 entradas):

1. **Estrutura**: 5 seções numeradas, prosa corrida completa, sem trechos incompletos — mais "limpo" que os capítulos 1 e 2:
   - 1. Estratégias de comparação histórica e seleção de casos (l. 11–280)
   - 2. Rastreamento de Processos e a comparação de sequências (l. 282–432)
   - 3. Recorte e indicadores (l. 434–592)
   - 4. Variáveis, unidades de análise e atores (l. 594–804)
   - 5. Materiais e métodos (l. 806–899)
   - Notas de rodapé (l. 901–922)

   O docx se autodenomina "Capítulo 2: Metodologia" (numeração interna desatualizada em relação ao projeto) — não deve afetar a importação, mas checar se algum trecho referencia "capítulo anterior/seguinte" por número (ver Decisão 2 abaixo).

2. **Esboço**: só um bloco pequeno no topo (l. 1–7) — 4 linhas soltas tipo outline do Google Docs ("Sociologia histórica processual", "Métodos mistos" etc.), antes do título real. Vai para `\begin{esboco}`. Fora isso, nada — resto é prosa finalizada.

3. **Citações**: único padrão, link Google Docs/Zotero `\href{zotero-url}{(Autor, Ano[, p. X])}` — 80 ocorrências. Diferente do capítulo 2, **não há citação em texto puro** aqui. Casos especiais presentes: narrativo com `\citet` implícito, multi-autor 3+, multi-ano mesmo autor (ex. "Streeck (2011, 2012)"). Sem "apud" nem "et al." literal.

4. **Conteúdo não-nativo**: nada a reportar — todo o texto é prosa nativa do capítulo, sem artigo colado, sem currículo, sem lista de referências formatada ao final.

5. **Tabelas**: 8 tabelas, todas com conteúdo textual/qualitativo (não puramente numéricas) — Tabelas 3–10 (as duplas 1–2 provavelmente já usadas em capítulos anteriores). A Tabela 6 (l. 540, indicadores da literatura) tem **citações dentro de células**, como já ocorreu no capítulo 2. Todas vão para `tables/cap03/*.csv` via `\csvautotabular` (Princípio 1 da constituição).

6. **Figuras**: 2 imagens em `word/media/` (`image1.png` 236KB — Figura 2, periodização, l. 55; `image2.png` 204KB — Figura 3, estratégia integrativa, l. 429), ambas já com legenda e fonte no texto. Extrair para `figures/cap03/`.

7. **Notas de rodapé**: 3 notas, convertidas corretamente pelo pandoc, conteúdo completo.

8. **Bibliografia**: `metodologia.bib` tem 44 entradas, todas completas (nenhum stub `@misc`). **Zero colisões de chave** com `references.bib` — as 44 podem ser adicionadas diretamente, sem necessidade de resolução de conflito.

   Cobertura é parcial: o `.bib` cobre bem a literatura metodológica geral (Tilly, Skocpol, Mahoney, Bennett, Abbott, Abell, Clemens, Kreuzer, Locke e Thelen etc.), mas **bem mais de 15 citações** das seções 3–5 (indicadores, instituições, atores, materiais) não têm entrada em nenhum dos dois `.bib` — ex.: Morceiro (2021, distinto do `morceiro_sectoral_2023` já existente), Morceiro e Guilhoto (2020), Streeck (2011/2012), Thelen (2010), Pierson (2004), Scharpf (2018), Fligstein e Choo (2005), Santos (2019/2024), Perissinotto (2023a/b — ver Decisão 1), Rihoux e Ragin (2009), CNDI/MDIC (2024), IBGE [s.d.]. Candidatas a `\aiflag{}`.

## Decisões confirmadas com o usuário

1. **Perissinotto 2023a vs. 2023b**: confirmado — marcar ambas as citações com `\aiflag{}` até haver confirmação/metadados sobre se são de fato duas obras distintas ou um erro de sufixo no rascunho. Não resolver por adivinhação.
2. **Numeração "Capítulo 2" no docx**: confirmado — usar apenas `\chapter{Metodologia}`, sem numeração manual (LaTeX numera automaticamente pela ordem de `\input` em `main.tex`, igual aos demais capítulos). Nenhuma checagem adicional de referência cruzada por número necessária.

## Tarefas

1. **Conversão inicial** — `source_raw.md` já gerado; normalizar para NFC, promover níveis de seção/subseção conforme a hierarquia listada acima.
2. **Conciliação da bibliografia** — acrescentar as 44 entradas de `metodologia.bib` a `references.bib` (nenhuma colisão a resolver). Rodar `bibtex`/`latexmk` ao final para confirmar que nada quebrou.
3. **Limpeza e formatação do capítulo**
   - Bloco de esboço inicial (l. 1–7) → `\begin{esboco}...\end{esboco}`.
   - Converter as 80 citações em link Google Docs/Zotero para `\citep`/`\citet`/`\citeyearpar`, tratando multi-ano mesmo autor e narrativo `\citet` implícito.
   - Extrair as 8 tabelas para `tables/cap03/*.csv` (atenção especial à Tabela 6, com citações em células).
   - Extrair as 2 imagens para `figures/cap03/`, com `\includegraphics` + `\caption{}`.
   - Conferir os 3 `\footnote{}` gerados pelo pandoc.
   - Marcar com `\aiflag{}` toda citação sem entrada em nenhum `.bib` disponível (estimativa: 15+, concentradas nas seções 3–5) e a ambiguidade Perissinotto 2023a/b (Decisão 1).
   - Garantir acentuação/UTF-8 preservada (NFC).
4. **Checagem estrutural** — balanceamento de chaves/ambientes; compilar `main.tex` (`latexmk -pdf` + `bibtex`) confirmando 0 citações indefinidas fora das marcadas com `\aiflag{}`.
5. **Ciclo de revisão iterativo** (`specs/constitution.md`) — passada de IA sobre o capítulo recém-importado (gramática, ideias repetidas, formatação de citação), marcada em vermelho/tachado, nunca aplicada direto; usuário revisa; repete.
6. **Atualização de specs (fechamento, Princípio 7)** — `status_capitulos.md` (Escrita da Metodologia refletindo estado real), `roadmap.md`, e revisão de `proposed_skills.md`/`constitution.md`/`.claude/skills/*` à luz do que esta rodada revelar (ex.: se surgir algo novo além do que as 4 skills já cobrem).

## Validação

- [x] Todo o conteúdo textual do docx está presente no `.tex` (nenhuma perda de parágrafo/seção), com o bloco de esboço preservado em `\begin{esboco}`.
- [x] Nenhuma ideia central alterada ou removida silenciosamente (inclusive um erro de digitação pré-existente do autor, "serão são enfocadas", foi mantido verbatim — não corrigido silenciosamente).
- [x] Nenhuma citação nova inserida diretamente no texto pela IA — as ~80 citações em link já existiam no docx.
- [x] Toda lacuna/sugestão da IA marcada em vermelho (`\aiflag{}`), nunca resolvida por adivinhação — 27 pares autor/ano (37 ocorrências no `.tex`, incluindo 2 em células de tabela).
- [x] Citações usam comando válido (`\citep`/`\citet`/`\citeyearpar`/`\citeauthor`+`\citeyear` para listas mistas resolvido/não-resolvido).
- [x] `references.bib` conciliado: 44 entradas novas adicionadas, 0 colisões, nenhuma citação existente (capítulos 1 e 2) quebrada.
- [x] `main.tex` compila sem erros (`pdflatex`+`bibtex`), 118 páginas, 0 citações indefinidas fora das marcadas com `\aiflag{}`.
- [x] 8 tabelas extraídas para `tables/cap03/*.csv`, referenciadas via `\csvautotabular`.
- [x] 2 figuras extraídas para `figures/cap03/`.
- [x] `specs/status_capitulos.md` e `specs/roadmap.md` atualizados.
- [x] `specs/proposed_skills.md` e `specs/constitution.md` revisados (Princípio 7) — `constitution.md` não precisou de mudanças; `proposed_skills.md` ganhou seção de validação das 4 skills; `specs/environment.md` ganhou um gotcha novo (footnote dentro de `\caption{}`).

## Resultado real (achados desta rodada)

Rodada mais "limpa" das três até agora: capítulo 100% prosa nativa (nenhum documento externo colado, ao contrário do capítulo 2), único formato de citação (link Google Docs/Zotero, sem mistura com texto puro), `.bib` fornecido sem nenhum stub e sem colisão de chave com `references.bib`.

Das ~80 citações, a maioria resolveu diretamente contra `references.bib`+`metodologia.bib` (29 `\citep`, 7 `\citet` narrativo, 12 `\citeauthor`+`\citeyear` em listas mistas). 27 pares autor/ano (37 ocorrências, incluindo 2 dentro de células da Tabela 6) não tinham entrada em nenhum `.bib` disponível e foram marcados com `\aiflag{}` — mais numerosos e mais espalhados pelo capítulo do que a estimativa inicial de "15+, concentrados nas seções 3–5" (achado 8 do plano): apareceram também nas seções 1–2, em referências centrais da discussão metodológica (Bennett e Checkel, Skocpol 1984b, Anckar, Rihoux e Ragin). A ambiguidade Perissinotto 2023a/2023b (Decisão 1) foi tratada como acordado, com `\aiflag{}` em ambas as ocorrências.

8 tabelas extraídas para `tables/cap03/*.csv`; a Tabela 6 (indicadores da literatura) é a primeira do projeto com citações dentro de células, tratadas com as mesmas regras do corpo do texto (`\citeyearpar`/`\aiflag`). 2 figuras extraídas de `word/media/` para `figures/cap03/`. 3 notas de rodapé preservadas — uma delas precisou ser movida de dentro de um `\caption{}` para uma frase do corpo do texto, porque nota de rodapé dentro de legenda quebra a compilação (`Runaway argument`) — gotcha novo, documentado em `specs/environment.md`.

`main.tex` compila limpo: 118 páginas, 0 citações indefinidas, apenas avisos pré-existentes benignos (depreciação de babel/memoir).

## Próximo passo (fora desta rodada)

Como nos capítulos 1 e 2, o ciclo iterativo de revisão (`specs/constitution.md`, "Ciclo de Revisão Iterativo") começa agora: o usuário trabalha sobre `chapters/03-Metodologia.tex`, em especial decidindo o que fazer com as 27 lacunas `\aiflag{}` (a maioria exigirá um `.bib` adicional cobrindo literatura institucionalista/metodológica mais específica e dados setoriais brasileiros; a ambiguidade Perissinotto 2023a/b exige esclarecimento direto) — e uma nova passada de IA acontece sobre a versão atualizada.
