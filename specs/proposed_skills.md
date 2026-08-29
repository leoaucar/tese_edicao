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

---
*Nenhuma dessas skills foi instalada ainda — esta é só a lista de propostas.*
