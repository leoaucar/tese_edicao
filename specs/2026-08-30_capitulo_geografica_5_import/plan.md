# Spec: Importação do Capítulo 6 (A Desindustrialização em Perspectiva Geográfica)

## Contexto

Quinta rodada de importação de capítulo, seguindo o workflow validado em
`specs/2026-08-29_capitulo_historico_1_review/` (capítulo empírico 1),
`specs/2026-08-30_capitulo_teoria_2_import/` (capítulo 2),
`specs/2026-08-30_capitulo_metodologia_3_import/` (capítulo 3) e
`specs/2026-08-30_capitulo_introducao_4_import/` (capítulo 1/Introdução).

Capítulo alvo: `chapters/06-A desindustrialização em perspectiva geográfica.tex`
— **Capítulo empírico 3**, conforme `specs/status_capitulos.md`.

**Estado real do arquivo antes desta rodada**: apenas um `\chapter{}` e dois
comentários de placeholder (`% TODO: importar conteúdo` e uma nota de
status/prazo) — nenhum texto importado ainda.

Diferente dos capítulos "Demais" (Introdução, Teoria, Metodologia, Discussão,
Conclusão), um capítulo empírico passa por 5 etapas no workflow
(`specs/constitution.md`, "Workflow de Capítulos"), não 2:

1. Revisão de literatura
2. Coleta de dados secundários
3. Produção de imagens e tabelas
4. Escrita do texto
5. Revisão de texto e citações

Todas as 5 etapas estão hoje marcadas `[ ]` (pendente) em
`specs/status_capitulos.md`. Esta rodada foca especificamente na etapa
**4 (Escrita do texto)** — importar o conteúdo já escrito pelo usuário a
partir do `.docx` fornecido — e no reconhecimento de imagens/tabelas que já
existam no próprio docx (etapa 3, parcialmente).

## Entrada recebida

```
specs/2026-08-30_capitulo_geografica_5_import/Capitulo empírico_geografico.docx
specs/2026-08-30_capitulo_geografica_5_import/cap empirico geo. Fluminense.bib   (66 entradas)
```

## Descobertas da inspeção inicial

Conversão de teste (`pandoc "Capitulo empírico_geografico.docx" -t latex -o
source_raw.tex`, mais uma passada `-t markdown --extract-media=media_check`)
revelou uma estrutura bem diferente das quatro rodadas anteriores:

1. **O docx, do início ao fim, é um único artigo acadêmico completo** —
   "Indústria e crescimento econômico do Rio de Janeiro (2002-2021):
   características setoriais e intensidade da desindustrialização
   fluminense" —, com Resumo/Palavras-chave em português E Abstract/Keywords
   em inglês (linhas 1-36), seções próprias de Introdução/Métodos/
   Resultados/Discussão, e uma **lista de referências formatada ao final**
   (linhas ~970-1235, 66 entradas, batendo com o `.bib` fornecido).
   Diferente da rodada do capítulo 2 (onde um artigo estranho foi colado
   *dentro* de um capítulo que também tinha texto genuíno da tese), aqui não
   há prosa "de tese" separada — o artigo inteiro é o conteúdo desta rodada,
   e seu tema bate exatamente com o título do capítulo 6. Tudo indica que é
   o próprio artigo do usuário (formato comum em teses com capítulos em
   formato de artigo) reaproveitado como capítulo empírico, não um erro de
   colagem — mas isso precisa ser confirmado, junto com o que fazer com os
   elementos "de artigo" (resumo/abstract bilíngue, lista de referências
   formatada) que não têm paralelo nos outros capítulos da tese.
2. **Headings não vieram como heading styles do Word** — pandoc converteu
   todos para `\textbf{}` simples, não `\section{}` (diferente dos outros
   capítulos, onde o heading style foi preservado). 6 headings de nível
   único, todos ao mesmo nível no artigo original: "Introdução", "História,
   ritmo e mudança social", "Desindustrialização do Brasil e do estado do
   Rio de Janeiro", "Métodos", "Resultados", "Discussão e conclusões".
3. **111 ocorrências de `\href` do Zotero/Google Docs** (algumas agrupadas
   multi-fonte, ex. "(High, 2013; Lawson, 2020; Strangleman, Rhodes e
   Linkon, 2013)" → 3 citações atômicas). Pelo menos algumas são
   narrativas (nome do autor em prosa antes do link, link contendo só o
   ano) — ex. `Skocpol \href{...}{(1984)}`, `Tilly \href{...}{(1984)}`,
   `Kreuzer \href{...}{(2023)}argumenta` (este último sem espaço antes do
   verbo — aparente artefato do docx/pandoc, não é papel desta rodada
   corrigir). Quantificação exata das narrativas fica para a conversão.
4. **8 figuras** (Gráfico 1 a 8, todas gráficos de séries temporais/médias
   móveis de taxas de crescimento), já extraídas para
   `media_check/media/image1.png`–`image8.png`.
5. **4 tabelas de dados reais** via `\begin{longtable}` do pandoc: Tabela 1
   (crescimento real do PIB/setores por período), Tabela 2 (diferença RJ vs.
   Brasil), Tabela 3 (correlação de Pearson entre séries), e "Anexo 1 -
   erros da média móvel" (tabela de métricas de erro do modelo, após a
   seção de conclusões) — sem "Tabela N" na prosa, é um apêndice.
6. **`.bib` fornecido (66 entradas) sem nenhuma sobreposição de chave** com
   o `references.bib` atual do projeto (252 entradas) — merge deve ser
   direto via skill `consolidar-bibliografia-zotero`, mas ainda é preciso
   checar duplicatas por autor/ano (não só por chave) durante o merge, como
   nas rodadas anteriores.
7. **Nenhum bloco de esboço/nota de rascunho identificado** — texto parece
   prosa acadêmica finalizada do início ao fim (a confirmar com a skill
   `detectar-esboco` durante a conversão real).

## Tarefas previstas (a confirmar/ajustar após receber o docx)

Baseado no padrão repetido nas 4 rodadas anteriores:

1. **Conversão inicial (pandoc)**: `pandoc <arquivo>.docx -t latex -o source_raw.tex`, mais uma passada `-t markdown --extract-media=media_check` para inspeção e extração de imagens embutidas.
2. **Normalização NFC** do texto antes de qualquer edição.
3. **Triagem de conteúdo**: usar as skills `detectar-conteudo-nao-nativo` e `detectar-esboco` para checar se há blocos coláveis de outro documento ou trechos de rascunho/nota (`\begin{esboco}...\end{esboco}`) em vez de prosa finalizada.
4. **Conversão de citações**: extrair citações (formato de link Zotero/Google Docs ou texto puro, a confirmar), casar autor+ano contra `references.bib`, gerar `\citep`/`\citet`/`\aiflag{}` conforme o caso — nenhuma citação resolvida por adivinhação quando houver ambiguidade real.
5. **Citações narrativas**: revisão manual de casos onde o nome do autor já aparece em prosa antes da citação (exige `\citet` + remoção do nome duplicado).
6. **Tabelas**: qualquer tabela do Word extraída para `tables/cap06/*.csv`, referenciada via `\csvautotabular`, com `\label`.
7. **Figuras**: qualquer imagem embutida extraída para `figures/cap06/*.png`, inserida com `\includegraphics`+`\caption`+`\label`.
8. **Referências cruzadas**: menções em prosa a tabelas/figuras convertidas para `Tabela~\ref{...}`/`Figura~\ref{...}`.
9. **Bibliografia**: se um `.bib` específico do capítulo for fornecido, usar a skill `consolidar-bibliografia-zotero` para mesclar com `references.bib` (casar stubs existentes, sinalizar colisões/ausências). Se não houver `.bib`, seguir o padrão da rodada 4 (Introdução): novas entradas stub `@misc` (autor/ano, `note = {stub}`) para citações sem correspondência.
10. **Checagem estrutural**: chaves/ambientes balanceados (`table`, `figure`, `itemize`/`enumerate` etc.).
11. **Compilação real**: `latexmk -pdf -output-directory=outputs main.tex` — validar 0 citações indefinidas.

## Decisões confirmadas com o usuário (após revisão deste plano)

1. **Bloco Resumo/Palavras-chave/Abstract/Keywords (linhas 1-36)**:
   **remover** — não entra no `.tex`. A tese já tem introdução e resumo
   próprios; o bloco bilíngue de artigo seria redundante no capítulo.
2. **Estrutura de headings**: os 6 `\textbf{}` (achado 2) viram `\section{}`
   no mesmo nível, **fiel à estrutura plana do artigo original** — sem
   reorganizar em subseções.
3. **Lista de referências formatada ao final (linhas ~970-1235)**:
   **remover** do `.tex`, consistente com as rodadas 1, 3 e 4. As 66
   entradas do `.bib` fornecido serão mescladas em `references.bib` via a
   skill `consolidar-bibliografia-zotero`; citações no corpo resolvem via
   `\cite`/`\citep`/`\citet`.

## Ambiguidades a resolver durante a implementação (não estruturais)

- Quantificação exata das citações narrativas vs. citações padrão (achado
  3) — feita citação por citação durante a conversão, com `\aiflag{}` para
  qualquer caso genuinamente ambíguo (mais de uma obra candidata em
  `references.bib`/no `.bib` do capítulo).
- Duplicatas autor/ano entre o `.bib` do capítulo e `references.bib` que não
  sejam capturadas apenas por comparação de chave (achado 6) — a skill
  `consolidar-bibliografia-zotero` deve sinalizar essas colisões.
- Qualquer trecho que a skill `detectar-esboco` apontar como não-prosa
  finalizada (achado 7 assumia que não havia, mas a checagem formal ainda
  não rodou).

## Validação (checklist a preencher ao final)

- [x] Todo o conteúdo textual do docx original está presente no `.tex` (nenhuma perda de parágrafos/seções) — inclusive a Tabela 2, cujos dados o `pandoc` não conseguiu converter (tabela vazia tanto no `.tex` quanto no `.md` de teste); recuperados diretamente do XML do `.docx` (`word/document.xml`, via `zipfile`/`lxml`) e conferidos contra o texto (nota de rodapé da tabela batendo com o prosa).
- [x] Nenhuma ideia central foi alterada ou removida silenciosamente.
- [x] Nenhuma citação nova foi inserida diretamente no texto pela IA — as citações resolvidas já existiam como link no docx; as 4 novas entradas de `references.bib` (Pierson 2004, Evans 2018, Shin 2017, Cosenza 2022) foram transcritas da própria lista de referências formatada do docx (removida do `.tex` por decisão do usuário), não inventadas.
- [x] Todas as lacunas de citação aparecem marcadas em vermelho (`\aiflag{}`) — 2 casos: `(Skocpol, 1984)` (3 candidatos em `references.bib`, ambíguo) e `(Nassif, 2015)` (nenhuma entrada correspondente a um "Nassif" isolado em 2015 — só há um trabalho de 3 autores "Nassif, Teixeira e Rocha" nesse ano). Mais um caso pré-existente reaberto por esta rodada: `(High, 2013)`, mesma ambiguidade `high_wounds_2013`/`high_beyond_2013` já vista na rodada do capítulo 2.
- [x] Citações existentes usam comando LaTeX válido (`\citep`/`\citet`, `natbib`/wrappers do `abntex2cite`).
- [x] `references.bib` conciliado — ver "Resultado real" abaixo.
- [x] `main.tex` compila sem erros (`latexmk -pdf -output-directory=outputs`) — **150 páginas, 0 citações indefinidas**. Avisos cosméticos remanescentes: 3 ocorrências de "Missing character"/"Command invalid in math mode" nas fórmulas da seção Métodos (linhas ~247-260 do capítulo) — o docx original tem palavras acentuadas em português (`PREÇOS`, `Participação`, `Transformação`) soltas dentro de `\(...\)`, sem `\text{}`; pré-existente no conteúdo original, não introduzido por esta rodada, não corrigido por não ser esta uma rodada de revisão de texto.
- [x] `specs/status_capitulos.md`, `specs/roadmap.md`, `specs/proposed_skills.md`, `specs/constitution.md` — atualizados a pedido do usuário ao final desta rodada (ver seções acima e abaixo); `.claude/skills/importar-docx-latex/SKILL.md` e `.claude/skills/consolidar-bibliografia-zotero/SKILL.md` também ajustados com os achados técnicos desta rodada.

## Resultado real (achados desta rodada)

- **O docx é um artigo acadêmico completo do próprio usuário**: "Indústria e
  crescimento econômico do Rio de Janeiro (2002-2021): características
  setoriais e intensidade da desindustrialização fluminense", incluindo
  Resumo/Abstract bilíngues, Introdução, Métodos, Resultados, Discussão e
  conclusões, e uma lista de referências formatada. Confirmado pelo próprio
  usuário durante a implementação: adicionou uma nota de rodapé no início do
  capítulo ("O Conteúdo deste capítulo absorve de forma levemente alterada o
  artigo 'Indústria e Crescimento Econômico no Rio de Janeiro', publicado na
  revista Cadernos do Desenvolvimento Fluminense") — não tocada por esta
  rodada.
- **Decisões estruturais** (confirmadas via `AskUserQuestion` antes da
  implementação, ver seção acima): bloco Resumo/Abstract removido; 6
  headings viraram `\section{}` em estrutura plana (Introdução; História,
  ritmo e mudança social; Desindustrialização do Brasil e do estado do Rio
  de Janeiro; Métodos; Resultados; Discussão e conclusões); lista de
  referências formatada removida do `.tex`.
- **58 citações atômicas** processadas (script `match_citations.py` +
  `final_convert.py`, adaptados dos scripts da rodada 4, preservados nesta
  pasta): **47 resolvidas automaticamente** por autor+ano exato, **13
  citações narrativas** (nome do autor em prosa, link só com o ano)
  resolvidas manualmente por inspeção do contexto e mapeadas pelo id único
  do link Zotero (não por autor+ano, que seria ambíguo entre elas) —
  convertidas para `\citet{}` —, e **2 lacunas genuínas** marcadas
  `\aiflag{}` (Skocpol 1984, ambíguo entre 3 obras; Nassif 2015, sem
  correspondência).
- **8 figuras** (Gráfico 1-8, incluindo o "Grafico 7" grafado sem acento no
  docx original — motivo de não ter sido pego pela primeira varredura por
  "Gráfico") extraídas para `figures/cap06/*.png` com nomes descritivos,
  cada uma com `\caption`+`\label`.
- **4 tabelas** extraídas para `tables/cap06/*.csv` e referenciadas via
  `\csvautotabular`: Tabela 1 e Anexo 1 (extração direta do texto/XML sem
  problema); Tabela 2 (dados recuperados do XML do docx, ver checklist
  acima); Tabela 3 (cabeçalho original de dois níveis — agrupando R/R2
  sobre Brasil/PIB(RJ) — achatado em uma linha por decisão editorial da
  IA, sinalizada com `\aiflag{}` dentro do `\begin{table}` para o usuário
  avaliar se prefere outro formato).
  - **Achado de escaping LaTeX/CSV**: `%` e `_` em valores de CSV quebram
    `\csvautotabular` se não escapados (`\%`, `\_`) — `%` vira comentário
    LaTeX (rompe o resto da linha do CSV, não só da célula, se houver mais
    colunas depois), `_` tenta entrar em modo matemático. O CSV do
    capítulo 1 (`empregos_transformacao_1985_2012.csv`, rodada 4) só não
    quebrou porque o `%` sempre é o último caractere da última coluna de
    cada linha. Vale documentar essa regra em `specs/constitution.md` para
    as próximas rodadas.
- **`references.bib`: 252 → 285 entradas.** Merge do `.bib` do capítulo
  (66 entradas) delegado a um subagente (skill
  `consolidar-bibliografia-zotero`): 27 novas, 5 stubs enriquecidos
  (chave antiga preservada), 33 já presentes sob a mesma chave (bibliografia
  compartilhada com os capítulos 2-4, sobre desindustrialização/sociologia
  histórica), 1 flag ambíguo (`ibge_contas_nodate` vs. stubs `ibge_sd`/
  `estatisticasseculoxx_sd`, nenhum resolvido). Depois do merge, a IA ainda
  precisou:
  - Adicionar manualmente **4 entradas novas** (Pierson 2004, Evans 2018,
    Shin 2017, Cosenza 2022) — citadas no corpo do artigo mas ausentes do
    `.bib` fornecido; recuperadas por transcrição direta da lista de
    referências formatada do próprio docx (não fabricadas).
  - Adicionar **`ibge_contas_nodate`** como entrada própria (o subagente só
    tinha sinalizado a ambiguidade, sem adicioná-la) — necessário porque a
    citação do corpo (dados das Contas Regionais do IBGE) bate
    especificamente com o título dessa entrada, não com os dois stubs
    genéricos concorrentes.
  - Enriquecer o stub `cni_sd` com título/URL reais (mesma lógica).
  - Aplicar 2 overrides de duplicata (`Mahoney 2000` → `mahoney_path_2000`;
    `Pierson 2015` → `mahoney_power_2015`), mesmo padrão de "preferir a
    entrada completa sobre o stub antigo" já usado na rodada 4.
- **0 blocos de esboço** — todo o artigo é prosa acadêmica finalizada
  (confirmado por leitura integral do corpo durante a conversão, não só
  por inspeção de amostra; a skill `detectar-esboco` não foi invocada
  separadamente por já ter sido coberta por essa leitura linha a linha).

## Próximo passo

Ciclo iterativo de revisão (`specs/constitution.md`, "Ciclo de Revisão
Iterativo") começa agora: o usuário decide as 2 citações `\aiflag{}` deste
capítulo (Skocpol 1984, Nassif 2015) e a formatação da Tabela 3 (cabeçalho
achatado). Também pendente, fora desta rodada: resolver a ambiguidade
`ibge_contas_nodate`/`ibge_sd`/`estatisticasseculoxx_sd` e a antiga
ambiguidade `High 2013` (arrastada da rodada do capítulo 2). Ao final do
ciclo, atualizar `specs/status_capitulos.md` e demais specs (pendência
sinalizada no checklist acima).
