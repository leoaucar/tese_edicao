# Spec: Importação do Capítulo 1 (Introdução)

## Contexto

Quarta rodada de importação de capítulo, seguindo o workflow validado em
`specs/2026-08-29_capitulo_historico_1_review/` (capítulo empírico 1) e
`specs/2026-08-30_capitulo_teoria_2_import/` (capítulo 2).

Capítulo alvo: `chapters/01-Introducao.tex`.

**Estado real do arquivo antes desta rodada**: apenas um `\chapter{Introdução}`
e um comentário `% TODO: importar conteúdo` — nenhum texto importado ainda.

Diferente das rodadas anteriores, nenhum `.bib` adicional foi fornecido nesta
rodada — apenas o `.docx`. `references.bib` já tinha 203 entradas (mistura de
stubs `@misc` autor/ano e entradas reais completas, mescladas nas três rodadas
anteriores).

## Entrada recebida

```
specs/2026-08-30_capitulo_introducao_4_import/Introdução.docx
```

## Descobertas da inspeção inicial

Conversão de teste (`pandoc "Introdução.docx" -t latex -o source_raw.tex`,
mais uma passada `-t markdown --extract-media=media_check` para inspeção)
revelou uma estrutura mais simples e mais "pronta" do que as três rodadas
anteriores:

1. **O docx é, do início ao fim, prosa finalizada** — não há bloco de
   esboço/blueprint (ao contrário do capítulo 2, que abria com uma lista de
   tópicos e estimativas de página). É o texto de um "Projeto de
   Qualificação" já escrito como texto corrido, incluindo notas de rodapé
   reais (8 `\footnote{}`, todas geradas corretamente pelo pandoc a partir de
   `word/footnotes.xml`). A única lista com bullets (seção "4. Objetivos",
   objetivos específicos da tese) usa frases completas e formatação padrão de
   lista de objetivos de projeto de pesquisa — tratada como prosa finalizada
   (`itemize`), não como esboço.
2. **Todas as citações usam o formato de link do Zotero/Google Docs**
   (`\href{https://www.zotero.org/google-docs/?...}{(Autor, Ano)}`) — não foi
   encontrada nenhuma citação em texto puro sem link (diferente do capítulo 2,
   que tinha uma seção inteira em texto puro).
3. **9 citações narrativas** (nome do autor já escrito em prosa antes do
   link, exigindo `\citet` + remoção do nome duplicado): Sobral (2016, p.
   198 — nota de fonte da Tabela 1), Santos (2006 — nota de rodapé), Sobral
   (2017), Granovetter (2007), Evans (1995), Cardoso de Mello (1982),
   Gerschenkron (1962), Hirschman (1958) e Thelen (2010). Este último caso é
   sutil: o link já continha o texto completo `(Thelen, 2010)` (não apenas o
   ano), então a busca automatizada por "link começa só com o ano" não o
   capturou — só foi identificado numa segunda varredura específica por
   "nome em prosa == nome dentro do link".
4. **1 tabela real do Word** ("Tabela 1: Empregos no setor de transformação
   entre 1985 e 2012 em estados selecionados", 4 colunas, 7 linhas incluindo
   uma linha de média) — extraída para `tables/cap01/*.csv` e referenciada
   via `\csvautotabular`, seguindo a convenção do projeto.
5. **1 figura embutida** (`media/image1.png`, um gráfico de taxa de
   crescimento dos subsetores industriais do RJ) — extraída para
   `figures/cap01/*.png` e inserida com `\includegraphics`+`\caption`.
   Nota técnica: `pandoc ... -t latex` sozinho **não** grava o arquivo de
   mídia em disco (apenas referencia `media/image1.png` no `.tex`); foi
   necessária uma segunda passada com `--extract-media=<pasta>` para
   recuperar o PNG de fato.
6. **Grande volume de citações genuinamente novas para o projeto**: como o
   capítulo de introdução cobre literatura própria (ABC paulista, Sul
   fluminense, CSN/Volta Redonda, institucionalismo comparado) ainda não
   coberta pelas três rodadas anteriores, a maioria das citações sem
   correspondência em `references.bib` são autores/obras realmente novos
   (Ramalho, Rodrigues, Santos, Sobral, CNI, IBGE, Consórcio ABC, SMABC,
   Valor Econômico, Thelen, Fligstein, Duina, Morgan, Scott, Hess, Sautu,
   Granovetter, Gerschenkron, Hirschman, entre outros), não apenas lacunas
   de conciliação de `.bib`.
7. **3 duplicatas detectadas em `references.bib`** (mesmo autor/ano com uma
   entrada stub vazia e outra já completa de rodada anterior): `mahoney2000`
   (stub) vs. `mahoney_path_2000` (completa); `abreu2014` (stub) vs.
   `abreu_ordem_2014` (completa); `souzaprevidelli2022` (stub) vs.
   `souza_historia_2022` (completa). Resolvidas usando a entrada completa em
   vez do stub — não é uma escolha ambígua de conteúdo bibliográfico (mesma
   obra, mesmo autor/ano), apenas preferir a entrada já enriquecida.
8. **Inconsistência do próprio texto-fonte**: o parágrafo de abertura afirma
   que o capítulo tem "quatro seções", mas em seguida enumera cinco (1 a 5,
   incluindo "5 - o cronograma proposto e a estrutura da tese"). A seção 5
   (cronograma) **não existe de fato no docx** — o texto termina após "4.
   Objetivos". Mantido como está (não é papel desta rodada corrigir a prosa
   do autor); sinalizado aqui para o usuário confirmar se o cronograma foi
   perdido na exportação do docx ou se nunca chegou a ser escrito.

## Decisões / ambiguidades que o usuário deve confirmar

1. **4 citações genuinamente ambíguas, marcadas com `\aiflag{}` em vez de
   resolvidas por adivinhação** (mais de uma obra candidata igualmente
   plausível em `references.bib`, sem forma de saber qual o autor tinha em
   mente):
   - `\aiflag{(High, 2013)}` — dois artigos distintos de Steven High em 2013
     já catalogados (`high_wounds_2013` "The Wounds of Class" e
     `high_beyond_2013` "Beyond Aesthetics").
   - `\aiflag{(Mahoney e Rueschemeyer, 2003)}` — pode ser o livro editado
     inteiro (`mahoney_comparative_2003`) ou o capítulo de introdução dos
     mesmos dois autores dentro dele (`mahoney_comparative_2003-1`).
   - `\aiflag{(Thelen e Mahoney, 2015)}` — mesmo padrão: livro editado
     (`mahoney_advances_2015`) vs. capítulo de Thelen e Mahoney dentro dele
     (`mahoney_comparative-historical_2015`).
   - `\aiflag{(Skocpol, 1984a)}` — o sufixo "a" indica que havia mais de um
     texto de Skocpol de 1984 na bibliografia original do autor; há dois
     capítulos de Skocpol de 1984 no mesmo volume já catalogados
     (`skocpol_emerging_1984` e `skocpol_sociologys_1984`), mas nenhuma forma
     confiável de saber qual corresponde a "1984a" sem a biblioteca Zotero
     original.
2. **Título da seção wrapper**: o docx tem um heading de nível 1 ("Capítulo
   1: Projeto de qualificação") que ficou como `\section{}` logo abaixo do
   `\chapter{Introdução}` — mantido literalmente (nunca reescrevo texto do
   autor), mas é redundante/estranho como heading dentro do capítulo já
   chamado "Introdução". O usuário pode preferir removê-lo ou renomeá-lo na
   sua própria revisão.
3. Dois pontos de pontuação ausentes no docx original (espaço duplo antes de
   ponto final, ou citação sem ponto final antes de quebra de parágrafo) —
   preservados como estão, por não ser esta a rodada de revisão de texto.

## Tarefas

1. **Conversão inicial (pandoc)**: `pandoc "Introdução.docx" -t latex -o source_raw.tex` (+ passada `-t markdown --extract-media=media_check` para inspeção e extração da imagem) — ambas preservadas na pasta da rodada.
2. **Normalização NFC** do texto antes de qualquer edição.
3. **Conversão de citações**: script Python (`match_citations.py`/`final_convert.py`, preservados na pasta da rodada) para extrair as 119 citações em link do Zotero, casar autor+ano normalizado contra `references.bib` (parseado por `parse_bib.py`), e gerar `\citep`/`\citet`/`\aiflag` conforme o caso — revisão manual de cada citação não resolvida automaticamente.
4. **9 citações narrativas** corrigidas manualmente (remoção do nome duplicado da prosa, ver Descoberta 3).
5. **Tabela 1** extraída para `tables/cap01/empregos_transformacao_1985_2012.csv`, referenciada via `\csvautotabular` com `\label{tab:cap01-empregos-transformacao}`; a nota de fonte que estava dentro do `multicolumn` do `longtable` do pandoc foi movida para texto corrido após `\end{table}` (mesmo cuidado de "nota dentro de `\caption`" documentado em `specs/environment.md`, embora aqui a nota estivesse fora do `\caption` propriamente).
6. **Figura 1** extraída para `figures/cap01/taxa_crescimento_subsetores_pib_rj.png`, inserida com `\caption`+`\label{fig:cap01-taxa-crescimento-subsetores}`.
7. **Referências cruzadas**: as menções em prosa "(cf. tabela 1 abaixo)", "(cf. figura 1 abaixo)" e "(tabela 1, p.14)" foram convertidas para `Tabela~\ref{...}`/`Figura~\ref{...}`, apontando para os labels criados nos passos 5–6.
8. **49 novas entradas stub `@misc`** acrescentadas a `references.bib` (autor/ano apenas, `title = {TODO -- confirmar...}`, `note = {stub}`, seguindo exatamente o formato das stubs já existentes) — ver lista completa no "Resultado real" abaixo.
9. **3 duplicatas resolvidas** a favor da entrada completa (achado 7).
10. **Checagem estrutural**: chaves/ambientes balanceados (`table`, `figure`, `itemize` todos com par correspondente).
11. **Compilação real**: `latexmk -pdf -output-directory=outputs main.tex`.

## Validação

- [x] Todo o conteúdo textual do docx original está presente no `.tex` (nenhuma perda de parágrafos/seções) — não havia esboço nem seção de "artigo colado" para remover nesta rodada; a única omissão deliberada é a lista de referências formatada (não existe no docx — a bibliografia do capítulo é só via `references.bib`/`\bibliographystyle`, não havia lista ao final deste docx específico).
- [x] Nenhuma ideia central foi alterada ou removida silenciosamente.
- [x] Nenhuma citação nova foi inserida diretamente no texto pela IA — as 119 citações em link já existiam no docx.
- [x] Todas as lacunas de citação aparecem marcadas em vermelho (`\aiflag{}`) — 4 citações genuinamente ambíguas (achado/decisão 1), nenhuma resolvida por adivinhação.
- [x] Citações existentes usam comando LaTeX válido (`\citep`/`\citet`, `natbib`/wrappers do `abntex2cite`).
- [x] `references.bib` conciliado: 49 entradas stub novas acrescentadas; 3 duplicatas identificadas e resolvidas a favor da entrada completa (nenhuma duplicata nova criada).
- [x] `main.tex` compila sem erros (`latexmk -pdf`) — 132 páginas, **0 citações indefinidas** (as 4 lacunas ficaram como `\aiflag{}` em texto simples, não como `\cite{}`, então não aparecem como "undefined" — comportamento esperado e consistente com as rodadas anteriores).
- [ ] `specs/status_capitulos.md`, `specs/roadmap.md`, `specs/proposed_skills.md`, `specs/constitution.md` — **não tocados nesta rodada**, por instrução explícita da tarefa (atualização acontece depois, na sessão principal, após revisão do usuário).

## Resultado real (achados desta rodada)

- **119 citações em link do Zotero** encontradas no docx, desdobradas em
  **140 citações atômicas** (grupos multi-fonte separados por `;` e
  multi-ano do mesmo autor, ex. "Ramalho, 2004, 2015" → 2 citações). No
  `.tex` final: **108 `\citep{}`**, **9 `\citet{}`** (citações narrativas) e
  **4 `\aiflag{}`** (lacunas genuinamente ambíguas).
- **49 novas entradas stub `@misc` em `references.bib`** (203 → 252
  entradas): `ibge_sd`, `cni_sd`, `viannavillela2015`, `morceiro2021`,
  `cni2021`, `governoestadosp_sd`, `consorcioabc_sd`, `ibge2017`,
  `ramalhosantos2022`, `rodriguesramalho2007`, `hendersonetal2002`,
  `amsden2003`, `bergermussowicke2022`, `oreiromarconi2012`,
  `bresserpereira2020`, `ramalho2004`, `ramalho2015`, `bridioliveirasalas2023`,
  `dulci2021`, `consorcioabc2024`, `ramalhorodrigues2013`,
  `ramalhorodrigues2018`, `fontes2023`, `sobral2016`, `smabc2004`,
  `valoreconomico2019`, `reis2007`, `ramalhorodrigues2010`,
  `ramalhoconceicao2024`, `ramalhosantoslima2013`, `morel1989`,
  `ramalho1989`, `abreubeynonramalho2000`, `santos2021`, `ramalho2005`,
  `piquet2021`, `sobral2017`, `sautuetal2005`, `thelen2010`, `duina2011`,
  `morganetal2010`, `scott2014`, `hess2004`, `fligstein1996`,
  `allenwoodkeller2022`, `santos2006`, `granovetter2007`, `gerschenkron1962`,
  `hirschman1958`.
  Nomes completos só foram preenchidos quando **já confirmados em outra
  entrada do próprio `references.bib`** para a mesma pessoa (ex.: Ramalho →
  "José Ricardo Garcia Pereira", confirmado via `rodrigues_o_2007`; Santos →
  "Rodrigo Salles Pereira dos", confirmado via `santos_desenvolvimento_2016`
  e `rodrigues_o_2007`; Thelen → "Kathleen", Hess → "Martin", Henderson →
  "Jeffrey", Oreiro → "José Luis", Marconi → "Nelson", Fontes → "Paulo",
  Morceiro → "Paulo César", Bresser-Pereira → "Luiz Carlos"). Todas as
  demais (Amsden, Dulci, Fligstein, Granovetter, Gerschenkron, Hirschman,
  Sobral, Reis, Piquet, Morel, Duina, Scott, Sautu, Morgan, Berger/Musso/
  Wicke, Bridi/Oliveira/Salas, Vianna/Villela, Allen/Wood/Keller,
  Abreu/Beynon, Lima, Conceição, SMABC, Valor Econômico, CNI, IBGE,
  Consórcio ABC, Governo do Estado de São Paulo) ficaram apenas com o
  sobrenome citado no docx — nunca completadas por suposição/conhecimento
  geral, mesmo quando o nome completo do autor é de conhecimento comum.
- **3 duplicatas de `references.bib` resolvidas** a favor da entrada
  completa (achado 7): citações a `Mahoney, 2000` agora usam
  `mahoney_path_2000`; `Abreu, 2014` usa `abreu_ordem_2014`; `Souza e
  Previdelli, 2022` usa `souza_historia_2022`.
- **0 blocos de esboço** — todo o capítulo é prosa finalizada (achado 1).
- **1 tabela** extraída (`tables/cap01/empregos_transformacao_1985_2012.csv`)
  e **1 figura** extraída (`figures/cap01/taxa_crescimento_subsetores_pib_rj.png`),
  ambas com `\label` e referenciadas em prosa via `\ref`.
- `main.tex` compila sem erros — **132 páginas, 0 citações indefinidas**,
  apenas avisos cosméticos pré-existentes (depreciação do `babel[brazil]` e
  do `\settocpreprocessor` do `memoir`, ambos anteriores a esta rodada e não
  relacionados ao capítulo 1).

## Próximo passo (fora desta rodada)

Como nas rodadas anteriores, o ciclo iterativo de revisão
(`specs/constitution.md`, "Ciclo de Revisão Iterativo") começa agora: o
usuário decide as 4 citações `\aiflag{}` (achado/decisão 1) — o caminho mais
direto é consultar a biblioteca Zotero original do autor para desambiguar
qual dos dois candidatos cada uma indica — e revisa o heading redundante
"Capítulo 1: Projeto de qualificação" (decisão 2). Também vale confirmar se
a seção 5 (cronograma), mencionada na prosa introdutória mas ausente do
docx, foi de fato perdida ou nunca escrita (achado 8).
