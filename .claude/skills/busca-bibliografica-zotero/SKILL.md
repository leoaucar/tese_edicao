---
name: busca-bibliografica-zotero
description: "Preenche uma pasta temática do Zotero (ex.: '1 Tese > 02 Teoria > A. 1 Sociologia Econômica') com os textos relevantes, priorizando a biblioteca do próprio usuário e usando OpenAlex/Crossref só para completar lacunas e medir impacto. Lê a nota-critério na raiz da pasta e o trecho do capítulo correspondente, propõe candidatos em níveis (núcleo/complementar/online) ligados às marcas \\todouser{fonte} do texto, e só grava após aprovação. Usar quando o usuário pedir para 'preencher a pasta', 'buscar referências para a seção', 'achar textos para o bloco X', 'resolver os citar fonte' ou revisar a nota de uma pasta do Zotero."
---

# Busca bibliográfica por pasta do Zotero

Monta, para uma pasta do Zotero que corresponde a um bloco do capítulo, a lista de
textos relevantes. **A biblioteca do usuário vem primeiro**: a maioria das obras já
está lá, inclusive como capítulo de handbook ou como PDF sem registro. A busca online
completa lacunas e fornece métricas; ela não é a fonte principal.

Depende da skill `zotero-organization`, que fornece credenciais, `zapi.py`, vocabulário
de tags e regras de pastas. Siga as regras dela para qualquer escrita no Zotero.

## Escopo da área

A tese é de **sociologia econômica**, não de economia. Prefira autores, periódicos e
debates da sociologia. Economia institucional, geografia econômica e ciência política
entram só quando dialogam com a sociologia, e vão para o nível "complementar".

## Passos

1. **Ler os critérios.** Ler a nota na raiz da pasta (campos "Tópico principal",
   "Subtópicos", "O que não incluir", "O que priorizar", "Origem geográfica", "Período
   de Publicação") e o trecho do capítulo que o bloco alimenta.
   - **Revisar a estrutura da nota antes de buscar.** Já encontramos: tópico principal
     copiado de outra pasta, subtópicos que invadem a pasta vizinha, "O que não incluir"
     vazio e erro de digitação no nome da pasta. Propor o texto corrigido e gravar só
     com aprovação; a nota antiga vai para o backup.
   - Quando o capítulo e a nota divergirem sobre o que entra no bloco (ex.: uma
     subseção que não cabe em nenhuma pasta), perguntar ao usuário. Não criar pasta
     sem pedido explícito.
2. **Indexar a biblioteca** (só leitura):
   `python3 scripts/indexar_biblioteca.py <scratchpad>/zot`. Isso gera `index.tsv`
   (itens com pastas, tags, resumo e nome dos PDFs) e `anexos_soltos.tsv`. Guardar uma
   cópia de `lib.json` em `~/Zotero-reorg-review/<data>_<descrição>/` como backup.
3. **Listar as lacunas do texto:** `python3 scripts/lacunas_citacao.py <capítulo.tex>
   [linha_ini linha_fim]`. Cada `\todouser{}{citar fonte}`, "(fonte)" ou "FULANO" é uma
   pergunta a responder com um item da biblioteca. Nomes informais também contam
   (ex.: "Cristiano e Rafael" era Monteiro & Lima 2021, já no Zotero).
4. **Buscar na biblioteca primeiro**, nesta ordem:
   - pastas temáticas próximas (`3 Temas > …`, `4 Métodos`, outras pastas da Tese);
   - grep no `index.tsv` por autores-chave e termos do tópico (título, resumo, tags);
   - **capítulos dentro de livros já salvos**: handbooks e coletâneas costumam ter
     capítulos que cobrem lacunas (ler o sumário com `pdftotext -f 5 -l 12 -layout`).
     Se o capítulo não tem registro próprio, propor um `bookSection` com páginas,
     editores e `relations: dc:relation` apontando para o livro (o PDF fica no livro);
   - `anexos_soltos.tsv` e nomes de PDF (obras sem registro);
   - antes de chamar algo de "online", confirmar que não está na biblioteca com outro
     título ou em outra pasta (ex.: Viterna & Robertson 2015 estava em "Territórios e
     desenvolvimento").
5. **Completar online** só o que falta: OpenAlex para descobrir e medir, Crossref para
   confirmar metadados (aceitar só título com similaridade > 0.9 e tipo coerente).
   OpenAlex é ruim para livros (resenhas aparecem no lugar da obra); confirme livros
   pela editora ou pelo Crossref.
6. **Pesar o impacto:** `python3 scripts/metricas_citacao.py <lib.json> KEY …` ou
   `--doi DOI …`.
   - Usar o **percentil normalizado por área e ano** (`pct`, `fwci`), não a contagem
     bruta: a média de citações varia muito entre áreas e entre décadas.
   - O OpenAlex classifica muita sociologia econômica como "Economics and
     Econometrics". O percentil serve como sinal de impacto, mas a área é decidida
     pelo periódico e pelo conteúdo.
   - Dar peso a artigos revisados por pares em periódicos de referência: AJS, ASR,
     Annual Review of Sociology, Theory and Society, Sociological Theory,
     Socio-Economic Review; no Brasil, RBCS, Tempo Social, Sociologias, Dados,
     Sociologia & Antropologia. Textos brasileiros têm contagem baixa por natureza;
     a nota da pasta pode pedir ênfase neles.
   - Livros e traduções vêm partidos entre edições: "sem dado" não quer dizer obra
     pouco citada.
   - **Limite do OpenAlex:** sem chave há um orçamento diário por IP, e a busca por
     título esgota primeiro (consulta por DOI dura mais). O script imprime `LIMITE
     OPENALEX` e cai no Crossref (contagem bruta) quando há DOI. Chave grátis em
     `~/.config/openalex/key` ou na variável `OPENALEX_API_KEY`.
7. **Propor, não gravar.** Escrever um relatório Markdown no scratchpad com:
   - notas propostas (texto completo);
   - por pasta, tabelas **Núcleo** / **Complementar** / **Online**, com key, obra,
     métrica e **uso no capítulo** (linha + lacuna que o item resolve);
   - "Fora" com o motivo;
   - outros achados: metadados quebrados (ex.: autor gravado como "work(s):") e
     erros no texto do capítulo, só como aviso, sem editar o `.tex`.
   Perguntar com `AskUserQuestion` (até 3 perguntas por vez): o que arquivar, quais
   correções de estrutura aplicar, quais itens novos criar.
8. **Gravar após aprovação**, seguindo `zotero-organization`: plano como dados, dry-run
   impresso, escrita em lotes de 50 com `key` e `version`, e assert de que nenhuma pasta
   é removida (só adicionar). Itens de fora vão para `1 Tese > A avaliar`, com
   `extra: "Sugerido para <pasta> (busca <data>)"` e tags do vocabulário. Renomear ou
   criar coleções usa `POST /collections` com `key` e `version`.
9. **Verificar e registrar:** recontar as pastas, salvar `change_log.json` e o relatório
   na pasta de backup e informar as contagens ao usuário.
10. **Oferecer o fichamento:** a etapa seguinte é `fichamento-zotero` (uma nota "Ficha
    IA" por item, com resumo e onde usar no capítulo). Perguntar antes de iniciar.

No relatório, indicar o lugar do capítulo por **âncora** (seção + início do parágrafo),
e não por número de linha, porque o usuário edita o arquivo durante o trabalho. Quando o
usuário mandar uma lista própria de referências (título, autor, justificativa), procurar
cada uma na biblioteca (com PDF) e online, e avaliar o encaixe com o mesmo critério.

## Regras fixas

- Nunca editar o texto do capítulo; citações sugeridas ficam no relatório.
- Nunca remover itens de `1 Tese` ou `5 Leituras`; arquivar é só adicionar pasta.
- Não inventar metadados: páginas, edição ou ano não verificados vão no `extra` como
  "conferir".

## Relação com `verificacao-citacoes` (academic-writing-skills)

Esta skill faz manualmente o que a V2 de `verificacao-citacoes` (Projeto A3 do roadmap
de `~/Documents/academic-writing-skills`) pretende automatizar: sugerir referências da
biblioteca para afirmações sem citação. Os achados daqui (biblioteca primeiro, capítulos
de handbook, normalização por área, limite do OpenAlex, nomes informais nas marcas)
servem de insumo para o item 15/16 daquele roadmap.
