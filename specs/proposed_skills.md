# Skills Propostas (não instaladas)

Lista de skills sugeridas para o projeto, a instalar/configurar quando fizer sentido (ver item "configurar skills" no roadmap). Esta lista é viva — atualizada a cada rodada de revisão, conforme a regra de manutenção de documentação em `specs/constitution.md`.

- **`revisar-capitulo`** — roda a revisão de IA completa em um capítulo, conforme as regras da seção "Papel da IA na Revisão de Texto" em `specs/constitution.md` (gramática/ortografia, ideias repetidas, sugestão de posição para tabelas/imagens, checagem de consistência com `tables/`/`figures/`, formatação de citações), inserindo as marcações em vermelho/tachado diretamente no `.tex`.
- **`importar-revisao-docx`** — extrai alterações rastreadas e comentários de um `.docx` devolvido pelo orientador e gera `advisor_reviews/<data>_<descrição>/review_task_lists.md`.
- **`exportar-copiao`** — compila `main.tex` (todos os capítulos) em PDF e exporta a versão unificada também em DOCX.
- **`checar-citacoes`** — verifica todas as `\cite{}` dos capítulos contra `references.bib`, sinalizando chaves ausentes ou formatação incorreta.
- **`atualizar-status`** — varre os capítulos em busca de marcações de revisão da IA (vermelho/tachado) e sugere atualizações nos checkboxes de `specs/status_capitulos.md`.
- **`nova-rodada-revisao`** — cria uma nova branch `YYYY-MM-DD-descrição` e as pastas correspondentes em `specs/` e `advisor_reviews/` ao iniciar uma rodada de revisão.

## Adicionadas após a rodada `2026-08-29_capitulo_historico_1_review` (primeiro teste real)

- **`importar-docx-latex`** — automatiza o que foi feito manualmente nesta rodada para o Capítulo empírico 1: primeira passada via `pandoc`, normalização NFC, promoção de níveis de seção, conversão de citações do Zotero (`\href{zotero-url}{...}` → `\citep`/`\citet`/`\citeyearpar` + entradas stub em `references.bib`), extração de imagens para `figures/<capítulo>/` com `\caption{}`, e envolvimento de trechos de esboço/nota em `\begin{esboco}`. Alto valor: essa conversão consumiu a maior parte do esforço desta rodada e é bem mecânica.
- **`detectar-esboco`** — dado um capítulo `.tex`, aponta quais parágrafos parecem esboço/nota (bullets, ALL CAPS, sem pontuação terminal) vs. prosa finalizada, como checagem complementar ao que a `importar-docx-latex` classifica automaticamente — útil também para revisões futuras, não só na importação inicial.
- **`consolidar-bibliografia-zotero`** — quando a biblioteca real do Zotero for exportada (`.bib`), casa as entradas *stub* já usadas nos capítulos (por autor/ano) com as entradas reais, atualizando `references.bib` e sinalizando ambiguidades (mesmo autor/ano, obras diferentes).

## Adicionadas/ajustadas após a rodada `2026-08-30_capitulo_teoria_2_import` (segundo teste real)

- **`importar-docx-latex`** (ajuste) — a rodada do capítulo 2 mostrou que **o mesmo docx pode misturar dois formatos de citação**: parte do capítulo ("Desindustrialização no Mundo") usava links do Google Docs/Zotero (`\href{...}{(Autor, Ano)}`, igual ao capítulo 1), mas outra parte (um artigo à parte, colado por inteiro) usava citações em **texto puro** `(Autor, Ano)`, sem link algum. A skill precisa detectar e converter os dois formatos, não assumir um único padrão por capítulo. Também precisa lidar com: grupos de autores "A, B e C" (3+ nomes), citações multi-ano do mesmo autor ("Tomlinson, 2016, 2020"), citações "et al.", construções "apud" (citação indireta), e citações onde o ano fica no link mas o nome do autor é texto narrativo antes dele (`\citet` implícito) — nesses casos a conversão precisa também remover o nome duplicado do texto ao inserir o `\citet{}`.
- **`detectar-conteudo-nao-nativo`** (nova proposta) — dado um capítulo importado de docx, aponta trechos que parecem ser um documento diferente colado por inteiro (título + resumo + palavras-chave + currículo de autor, ou uma lista de referências formatada ao final que duplica `references.bib`) — sinal de que o trecho precisa de adaptação estrutural (não é só limpeza de citação) antes de virar prosa de capítulo. Achado nesta rodada: metade do capítulo 2 era um artigo publicável separado, não uma subseção de tese.
- **`consolidar-bibliografia-zotero`** (ajuste) — cobre também o caso de mesclar um arquivo `.bib` novo e completo (não só stubs) a um `references.bib` existente: checar colisões de chave, pular duplicatas idênticas, e sinalizar (não silenciar) quando uma citação do capítulo não tem entrada em *nenhum* dos `.bib` disponíveis — nesta rodada, ~38 de 66 citações da seção brasileira do capítulo 2 caíram nesse caso porque cobriam um universo bibliográfico (economia política brasileira) fora do escopo do `.bib` fornecido.

---
*Nenhuma dessas skills foi instalada ainda — esta é só a lista de propostas.*
