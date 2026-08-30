---
name: importar-docx-latex
description: "Converte um capítulo da tese de .docx para .tex, aplicando as convenções do projeto (specs/constitution.md). Usar quando o usuário pedir para importar/converter um capítulo a partir de um .docx recebido (dropado em specs/YYYY-MM-DD_descrição/ ou advisor_reviews/), ou mencionar 'importar capítulo', 'converter docx', 'passar o word pro latex'."
---

# Importar DOCX → LaTeX

Converte um `.docx` de capítulo para `.tex`, replicando o processo manual usado nas rodadas `2026-08-29_capitulo_historico_1_review` e `2026-08-30_capitulo_teoria_2_import` (ver `plan.md` de cada uma para o histórico completo de decisões).

## Uso de contexto

O `.docx` de um capítulo costuma gerar 50–150KB de texto bruto via pandoc — não vale a pena manter isso na conversa principal. Delegue os passos 1–5 abaixo a um subagente (`Agent`, `subagent_type: general-purpose` ou fork), que deve devolver apenas: o `.tex` resultante já escrito em disco, e um resumo curto (contagem de citações convertidas, stubs de bibliografia criados, trechos marcados como esboço/não-nativo, ambiguidades). A leitura fina do resultado (passo 6) acontece na sessão principal, sobre o `.tex` já pronto — não sobre o dump bruto do pandoc.

## Passos

1. **Primeira passada**: `pandoc docx -t <arquivo>.docx -o source_raw.tex` (ou markdown intermediário, conforme o que render melhor) dentro da pasta `specs/YYYY-MM-DD_descrição/` da rodada. Guardar o `source_raw.tex` como registro do estado bruto.
2. **Normalização**: converter para NFC (evita bugs de acentuação duplicada comuns em export do Google Docs/Word), promover níveis de seção (`\section`/`\subsection`) conforme a hierarquia real do capítulo.
3. **Citações**: detectar e converter **ambos** os formatos observados até agora — não assumir um único padrão por capítulo, pois já apareceram misturados no mesmo arquivo:
   - Links do Google Docs/Zotero: `\href{zotero-url}{(Autor, Ano)}` → `\citep`/`\citet`/`\citeyearpar`, com entrada *stub* em `references.bib` (autor/ano, sem metadados completos) quando a entrada real ainda não existir.
   - Texto puro sem link: `(Autor, Ano)` → mesma conversão, mesma criação de stub.
   - Casos especiais a cobrir: grupos de 3+ autores ("A, B e C"), citações multi-ano do mesmo autor ("Tomlinson, 2016, 2020"), "et al.", "apud" (citação indireta), e o caso em que o nome do autor já está como texto narrativo antes do link de ano (`\citet` implícito) — aqui é preciso remover o nome duplicado do texto ao inserir `\citet{}`.
4. **Figuras**: extrair imagens embutidas para `figures/<capítulo>/`, inserindo `\includegraphics` + `\caption{}` no ponto correspondente do texto.
5. **Tabelas**: extrair cada tabela para `tables/<capítulo>/*.csv`, referenciada via `\csvautotabular` + `\caption{}`/`\label{}` (Princípio 1 de `specs/constitution.md`). **Checar se o `\begin{longtable}` gerado pelo pandoc veio vazio** (achado na rodada `2026-08-30_capitulo_geografica_5_import`: uma tabela com `<w:tblGridChange>` no XML do docx — sinal de colunas redimensionadas manualmente no Word — foi silenciosamente esvaziada tanto na saída `-t latex` quanto `-t markdown` do pandoc, sem nenhum aviso). Se vazio, recuperar os dados direto do XML: o `.docx` é um zip; abrir `word/document.xml` (`zipfile` + `lxml`), localizar o `<w:p>` com a legenda da tabela e o `<w:tbl>` irmão seguinte, extrair o texto de cada `<w:tc>`. **Escapar `%` → `\%` e `_` → `\_`** em toda célula do CSV (não só na última coluna) — `\csvautotabular` expande o CSV como LaTeX, então `%` não escapado inicia um comentário (quebrando o resto da linha do CSV) e `_` tenta entrar em modo matemático; ambos geram erro fatal de compilação ou tabela corrompida silenciosamente.
6. **Esboço**: envolver trechos que são claramente anotação/rascunho do autor (bullets soltos, ALL CAPS, sem pontuação terminal, notas tipo "COMPARAR X COM Y") em `\begin{esboco}...\end{esboco}` — ver convenção completa em `specs/constitution.md`. Na dúvida entre esboço e prosa final, marcar como esboço e sinalizar para o usuário decidir (nunca decidir silenciosamente).
7. **Artigo publicado reaproveitado como capítulo**: um docx pode ser um artigo acadêmico completo do próprio usuário (Resumo/Abstract bilíngues, seções em formato de artigo, lista de referências formatada ao final) em vez de prosa de capítulo — não é necessariamente um erro de colagem (ver `detectar-conteudo-nao-nativo`), mas também não tem paralelo direto na estrutura padrão de capítulo. Perguntar ao usuário via `AskUserQuestion` o que fazer com os elementos "de artigo" sem paralelo (bloco de resumo bilíngue, lista de referências formatada) antes de converter.
8. **Revisão pelo usuário**: devolver o `.tex` gerado + resumo de decisões (quantas citações de cada tipo, quantos stubs criados, quantos trechos de esboço, quaisquer ambiguidades) para o usuário revisar antes de qualquer commit.

## Regras fixas (constitution.md)

- Nunca inserir citações novas que não existiam no docx original.
- Nunca decidir silenciosamente conteúdo bibliográfico (autor/ano) — se o docx tem uma citação ambígua ou incompleta, marcar com `\aiflag{}`, não adivinhar.
- Esboço vs. prosa final: usar o ambiente `esboco`, nunca apagar ou reescrever o texto do autor.
- Nunca incluir um `%` não escapado dentro do argumento de `\aiflag{}` (nem como separador de anotação, ex. `%%`) — comenta o resto da linha e quebra a compilação (`Runaway argument?`). Usar `--` ou `,` como separador.
