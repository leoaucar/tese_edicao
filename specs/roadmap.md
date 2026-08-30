# Roadmap

Alinhado ao workflow de capítulos definido em `specs/constitution.md` e ao status em `specs/status_capitulos.md`.

## Hoje (29/08/2026)

- [x] **Preparar projeto** — importado o docx do Capítulo empírico 1 (ver `specs/2026-08-29_capitulo_historico_1_review/`); bibliografia populada como stubs em `references.bib` (autor/ano; falta exportação real do Zotero).
- [~] **Exportar para DOCX** — tooling criado em `scripts/export_docx/` (ver `specs/environment.md`) e testado exportando o Capítulo 4 completo (tabelas + marcação `\aiflag` em vermelho preservadas). Falta apenas a exportação do "copião" unificado (`main.tex` inteiro) — não bloqueante, já que o fluxo de revisão é por capítulo.
- [~] **Configurar skills** — 4 skills instaladas em `.claude/skills/` (`importar-docx-latex`, `consolidar-bibliografia-zotero`, `detectar-esboco`, `detectar-conteudo-nao-nativo`), diretamente necessárias para a rodada `2026-08-30_capitulo_metodologia_3_import`; as demais seguem como propostas em `specs/proposed_skills.md`, a instalar quando sua fase do roadmap chegar.

## Semana 1 (01–07/09/2026) — Finalizar Capítulo Empírico 1

- [~] Revisão de literatura -- citações no texto convertidas para `\citep`/`\citeyearpar`; bibliografia real pendente.
- [~] Coleta de dados secundários -- parcial, ver `specs/status_capitulos.md`.
- [~] Produção de imagens e tabelas -- 2 tabelas + 4 figuras incorporadas; vários `[FIGURA A INSERIR]` pendentes no texto.
- [~] Escrita do texto -- ~metade do capítulo é esboço/nota, não prosa (ver blocos `esboco` no `.tex`).
- [ ] Revisão de texto e citações -- primeira passada de IA aplicada; ciclo iterativo com o usuário ainda não começou.
- [~] Exportação -- tooling pronto (`scripts/export_docx/`) e já usado para gerar um DOCX do capítulo; repetir a exportação a cada rodada de revisão antes de enviar para `advisor_reviews/`.

## Restante do roadmap (estruturado para viabilizar `specs/cronograma.md`)

### Capítulo empírico 2 (entrega 30/09/2026)

- [ ] **Semana 2 (08–14/09/2026)** — Revisão de literatura; coleta de dados secundários.
- [ ] **Semana 3 (15–21/09/2026)** — Produção de imagens e tabelas; escrita do texto.
- [ ] **Semana 4 (22–28/09/2026)** — Revisão de texto e citações (entrega 30/09).

### Capítulo empírico 3 (entrega 30/10/2026)

- [ ] **Semana 5 (29/09–05/10/2026)** — Revisão de literatura; coleta de dados secundários.
- [ ] **Semana 6 (06–12/10/2026)** — Produção de imagens e tabelas.
- [ ] **Semana 7 (13–19/10/2026)** — Escrita do texto.
- [ ] **Semana 8 (20–26/10/2026)** — Revisão de texto e citações (entrega 30/10).

### Revisão de texto e citações — Introdução → Teoria → Metodologia → Conclusão

Escrita já concluída para estes capítulos (ver `specs/status_capitulos.md`); resta apenas a etapa de revisão de texto e citações.

- [ ] **Semana 9 (27/10–02/11/2026)** — Transição / preparação da revisão textual geral.
- [ ] **Semana 10 (03–09/11/2026)** — Revisão de texto e citações: Introdução.
- [ ] **Semana 11 (10–15/11/2026)** — Revisão de texto e citações: Introdução (fechamento, entrega 15/11).
- [ ] **Semana 12 (16–22/11/2026)** — Revisão de texto e citações: Teoria.
- [ ] **Semana 13 (23–30/11/2026)** — Revisão de texto e citações: Teoria (fechamento, entrega 30/11).
- [ ] **Semana 14 (01–07/12/2026)** — Revisão de texto e citações: Metodologia.
- [ ] **Semana 15 (08–15/12/2026)** — Revisão de texto e citações: Metodologia (fechamento, entrega 15/12).
- [ ] **Semana 16 (16–22/12/2026)** — Revisão de texto e citações: Conclusão.
- [ ] **Semana 17 (23–30/12/2026)** — Revisão de texto e citações: Conclusão (fechamento, entrega 30/12) + conteúdo completo (31/12).

### Discussão (sem prazo definido)

- [ ] Escrita (sem data — ver nota em `specs/status_capitulos.md`)
- [ ] Revisão de texto e citações
- [ ] Encaixar no cronograma assim que a escrita tiver uma data prevista.

### Revisão final e entrega

- [ ] **Semana 18 (31/12/2026–07/01/2027)** — Revisão de texto e citações completa (todos os capítulos, incluindo Discussão se já escrita).
- [ ] **Semana 19 (08–15/01/2027)** — Revisões textuais finais + envio para a banca (entrega 15/01).

### Banca

- [ ] **Fevereiro/2027** — Buffer / ajustes enquanto aguarda a banca.
- [ ] **Março/2027 (3ª semana)** — Defesa.
- [ ] **Março/2027 (2ª ou 4ª semana — ver nota de inconsistência em `specs/status_capitulos.md`)** — Revisões pós-defesa.

---
*Datas por semana são uma proposta inicial derivada de `specs/cronograma.md` — ajustar conforme o andamento real.*
