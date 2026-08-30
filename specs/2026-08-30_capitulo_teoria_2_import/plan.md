# Spec: Importação do Capítulo 2 (Teoria)

## Contexto

Segunda rodada de importação de capítulo, seguindo o workflow validado em `specs/2026-08-29_capitulo_historico_1_review/` (capítulo empírico 1).

Capítulo alvo: `chapters/02-Desindustrialização (Teoria).tex`.

**Estado real do arquivo hoje**: apenas um `\chapter{}` e um comentário `% TODO: importar conteúdo` — nenhum texto foi importado ainda, apesar de `specs/status_capitulos.md` marcar a etapa "Escrita" como `[~]` (parcial). Essa marcação está desatualizada (mesmo problema encontrado no capítulo empírico 1, cujo status "Completo" também não refletia a realidade) e será corrigida ao final desta rodada, uma vez confirmado o estado real após a importação.

Segundo o usuário, o material de origem (fora deste repositório) está "mais ou menos pela metade" e já tem uma bibliografia associada que precisa ser atualizada — o usuário vai fornecer um `.bib` adicional para conciliar com `references.bib` (hoje com 80 entradas: uma mistura de entradas reais, já com metadados completos, e stubs `@misc` autor/ano criados durante a importação do capítulo 1, ainda pendentes de confirmação).

## Entrada recebida

```
specs/2026-08-30_capitulo_teoria_2_import/Capítulo teorico.docx
specs/2026-08-30_capitulo_teoria_2_import/1 - Teoria.bib
```

## Descobertas da inspeção inicial

Conversão de teste (`pandoc "Capítulo teorico.docx" -t latex`) e leitura do `.bib` revelam uma estrutura mais específica do que a do capítulo 1:

1. **Bloco de esboço inicial** (linhas ~1–73 do texto extraído): lista de tópicos com estimativas de página (ex.: "Teoria Geral (15pg)", "principais linhas da soc econ") — claramente um blueprint/anotação do autor, não prosa. Vai para `\begin{esboco}`, igual ao tratamento dado a notas equivalentes no capítulo 1.

2. **Seção "Desindustrialização no Mundo"** (~780 linhas): revisão de literatura já escrita como prosa corrida, com citações no mesmo padrão do capítulo 1 — links do Google Docs/Zotero envolvendo o texto visível `(Autor, Ano[, p. X])` (ex.: `\href{https://www.zotero.org/google-docs/?SncwXs}{(Pula, 2017, p. 1)}`). Conversão para `\citep`/`\citet`/`\citeyearpar` segue o mesmo processo já validado no capítulo 1.

3. **Seção "Desindustrialização no Brasil" (~567 linhas) é, na verdade, um artigo autônomo colado por inteiro**: "Desafios da reindustrialização brasileira", com título, **currículo reduzido do autor**, **Resumo** e **Palavras-chave** próprios (formato de artigo/paper, não de subseção de tese) antes de entrar no conteúdo. O conteúdo argumentativo em si parece aproveitável, mas precisa ser adaptado para ler como subseção do capítulo, não como um paper independente — ver pergunta ao usuário abaixo.

4. **Notas de rodapé reais**: 9 notas (`word/footnotes.xml`), já convertidas corretamente por `pandoc` em `\footnote{...}`.

5. **2 tabelas reais do Word**: "Tabela 11: critérios de priorização de artigos" (2 colunas) e "Tabela 12: resumo dos casos de desindustrialização na literatura" (3 colunas, células com texto qualitativo/prosa, possivelmente com citações dentro das células). Por convenção do projeto (`specs/constitution.md`, Princípio 1 — tabelas em CSV externo, nunca hardcoded no `.tex`), ambas devem virar `tables/cap02/*.csv` referenciadas via `\csvautotabular`, como já feito no capítulo 1 — com atenção extra a células com citações/formatação, que não existiam nas tabelas puramente numéricas do capítulo 1.

6. **Lista de referências formatada ao final do docx** (~283 linhas, a partir de "Bibliografia"): é o output humano/Zotero já formatado — não deve ser importada para o `.tex` (substituída pela bibliografia gerada automaticamente via `references.bib` + `\bibliographystyle`), mas serve como checagem cruzada de cobertura do `.bib`.

7. **Conciliação de `references.bib` é mais simples do que o previsto**: `1 - Teoria.bib` tem 82 entradas, todas já com metadados completos (nenhum stub `@misc`). Apenas 3 chaves colidem com `references.bib` atual (`evans_dependent_1979`, `pedreira_historiografia_2024`, `silva_formacao_2024`) — comparação campo a campo confirma que as 3 são **idênticas** nos dois arquivos (mesmo item do Zotero, provavelmente compartilhado entre os capítulos). Nenhum conflito real encontrado. A tarefa se resume a acrescentar as 79 entradas novas a `references.bib`, sem sobrescrever nada.

## Decisão: seção "Desindustrialização no Brasil" (achado 3)

Confirmado com o usuário: remover Resumo/Palavras-chave/currículo reduzido do autor ao importar essa seção, mantendo apenas o conteúdo argumentativo. Títulos de seção do artigo viram `\subsection`/`\subsubsection` normais do capítulo (não headings de paper independente).

## Tarefas

1. **Conversão inicial (pandoc)**
   - `pandoc source.docx -o source_raw.tex` como primeira passada, gerando rascunho intermediário nesta mesma pasta (não é o capítulo final).
   - Normalizar para NFC logo em seguida (nota de `specs/environment.md`: pandoc costuma gerar `.tex` em NFD, o que quebra buscas por string exata).

2. **Conciliação da bibliografia (`references.bib`)**
   - Acrescentar as 79 entradas de `1 - Teoria.bib` que não colidem com `references.bib`; pular as 3 chaves duplicadas idênticas (achado 7 acima) para não gerar aviso de "repeated entry" do `bibtex`.
   - Rodar `bibtex`/`latexmk` ao final para confirmar que nenhuma citação existente (capítulo 1 e capítulo 2) ficou indefinida por causa da conciliação.

3. **Limpeza manual e formatação do capítulo**
   - Mover/adaptar o conteúdo de `source_raw.tex` para `chapters/02-Desindustrialização (Teoria).tex`, substituindo o placeholder atual.
   - Bloco de esboço inicial (achado 1) → `\begin{esboco}...\end{esboco}`.
   - Converter citações em link do Google Docs/Zotero para `\citep`/`\citet`/`\citeyearpar` (achado 2), incluindo grupos multi-ano do mesmo autor (ex. "Tomlinson, 2016, 2020" deve virar duas chaves, não uma).
   - Seção "Desindustrialização no Brasil": aplicar a decisão do usuário sobre Resumo/Palavras-chave/currículo (achado 3); retitular headings de artigo para headings de subseção de capítulo.
   - Extrair as 2 tabelas do Word para `tables/cap02/*.csv`, referenciadas via `\csvautotabular` (achado 5) — atenção a células com citações/texto formatado.
   - Notas de rodapé: conferir que os 9 `\footnote{}` gerados pelo pandoc vieram completos (achado 4).
   - Marcar com `\aiflag{}` qualquer citação incompleta/placeholder que não puder ser resolvida com o `.bib` disponível.
   - Garantir acentuação/UTF-8 preservada.

4. **Checagem estrutural**
   - Balanceamento de chaves e ambientes.
   - Compilar `main.tex` (`latexmk -pdf` + `bibtex`, ver `specs/environment.md`) como confirmação real — 0 citações indefinidas esperado (exceto as que genuinamente não tiverem entrada em nenhum `.bib`, marcadas com `\aiflag{}`).

5. **Ciclo de revisão iterativo** (`specs/constitution.md`, "Ciclo de Revisão Iterativo" e "Papel da IA na Revisão de Texto")
   - Passada de IA sobre o capítulo recém-importado: gramática/ortografia em português, ideias repetidas, formatação de citações, frases mais concisas — tudo marcado em vermelho (`\aiflag{}`)/tachado (`\sout{}`), nunca aplicado direto.
   - Usuário trabalha sobre o capítulo; nova passada de IA sobre a versão atualizada; repete até o usuário considerar pronto.

6. **Atualização de specs (fechamento da rodada — Princípio 7 da constituição, obrigatório)**
   - `specs/status_capitulos.md`: corrigir a etapa "Escrita" da Teoria para refletir o estado real pós-importação (provavelmente volta para `[~]` ou `[ ]` dependendo do que o docx trouxer, não necessariamente o que estava marcado antes).
   - `specs/roadmap.md`: marcar os itens correspondentes.
   - `specs/proposed_skills.md` e `specs/constitution.md`: revisar à luz do que esta segunda rodada de importação revelar (ex.: se o processo de conciliação de bibliografia se mostrar repetível, propor uma skill dedicada).

## Validação

- [x] Todo o conteúdo textual do docx original está presente no `.tex` (nenhuma perda de parágrafos/seções) — bloco de esboço preservado em `\begin{esboco}`, seção brasileira preservada exceto Resumo/Palavras-chave/currículo (removidos por decisão do usuário) e a lista de referências final (substituída por `references.bib`).
- [x] Nenhuma ideia central foi alterada ou removida silenciosamente.
- [x] Nenhuma citação nova foi inserida diretamente no texto pela IA — todas as 182 citações em link (Google Docs/Zotero) e as 66 em texto puro já existiam no docx.
- [x] Todas as sugestões/lacunas da IA aparecem marcadas em vermelho no `.tex` (`\aiflag{}`) — 42 citações sem entrada em nenhum `.bib` disponível (4 na seção mundial, 38 na seção brasileira) foram marcadas, não resolvidas por adivinhação.
- [x] Citações existentes usam comando LaTeX válido (`\citep`/`\citet`/`\citeyearpar`, além de `\citeauthor`+`\citeyear` para os poucos casos de página individual por fonte dentro de uma citação múltipla).
- [x] `references.bib` conciliado: 79 entradas novas de `1 - Teoria.bib` adicionadas, 3 duplicatas idênticas puladas, nenhuma citação existente (capítulo 1) quebrada.
- [x] `main.tex` compila sem erros (`latexmk` + `bibtex`) — 103 páginas, 0 citações indefinidas fora das marcadas com `\aiflag{}`.
- [x] `specs/status_capitulos.md` e `specs/roadmap.md` atualizados para refletir o estado real.
- [x] `specs/proposed_skills.md` e `specs/constitution.md` revisados (Princípio 7) — `constitution.md` não precisou de mudanças (a convenção `\aiflag{}` já cobriu todos os casos novos encontrados).

## Resultado real (achados desta rodada)

- O `.tex` do capítulo 2 acabou sendo bem mais heterogêneo do que o esperado: um bloco de esboço/blueprint no início (`\begin{esboco}`), uma seção "Desindustrialização no Mundo" com prosa finalizada (~780 linhas) citando via link do Google Docs/Zotero (mesmo padrão do capítulo 1), e uma seção "Desindustrialização no Brasil" que era, na prática, **um artigo à parte colado por inteiro** ("Desafios da reindustrialização brasileira", com Resumo/Palavras-chave/currículo próprios) citando em **texto puro**, sem links.
- 182 citações em link + 66 em texto puro (248 no total) foram convertidas para `\citep`/`\citet`/`\citeyearpar`. 206 resolveram diretamente contra a bibliografia; 42 não tinham entrada em nenhum `.bib` disponível e foram marcadas com `\aiflag{}` em vez de resolvidas por adivinhação — a maioria (38) na seção brasileira, cujo universo bibliográfico (economia política brasileira: Ramalho, Bresser-Pereira, Arbix, CNI, Amsden, Gerschenkron, Thelen, Giambiagi etc.) não é coberto por `1 - Teoria.bib`. Duas citações "apud" (citação indireta) foram construídas manualmente com `\citeauthor`+`\citeyear` para a fonte secundária, mantendo a fonte primária (não catalogada) como texto simples.
- 2 tabelas do Word (critérios de seleção de artigos; resumo de casos de desindustrialização por região) foram extraídas para `tables/cap02/*.csv` e referenciadas via `\csvautotabular`, seguindo a convenção do projeto.
- `references.bib` cresceu de 80 para 159 entradas (79 novas de `1 - Teoria.bib`; 3 duplicatas idênticas identificadas e não repetidas).
- Duas entradas do `.bib` fornecido tinham problemas de formatação que quebravam a compilação do `main.tex` inteiro (não só do capítulo 2) — corrigidas e documentadas em `specs/environment.md`: um autor institucional com vírgulas demais no nome, e um caractere Unicode turco (`Ş`) que corrompia a geração de rótulo de citação do `bibtex`.

## Próximo passo (fora desta rodada)

Como no capítulo 1, o ciclo iterativo de revisão (`specs/constitution.md`, "Ciclo de Revisão Iterativo") começa agora: o usuário trabalha sobre `chapters/02-Desindustrialização (Teoria).tex` — em especial decidindo o que fazer com as 38 citações `\aiflag{}` da seção brasileira (fornecer um `.bib` adicional cobrindo essas fontes é o caminho mais direto) — e uma nova passada de IA acontece sobre a versão atualizada.
