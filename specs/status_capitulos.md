# Status dos Capítulos

Estrutura por etapas, conforme o workflow definido em `specs/constitution.md` (seção "Workflow de Capítulos").

Convenção de status: `[ ]` pendente · `[~]` parcial · `[x]` concluído.

## Capítulos empíricos

Etapas: revisão de literatura → coleta de dados secundários → produção de imagens e tabelas → escrita do texto → revisão de texto e citações.

> Nota: o capítulo empírico 1 estava marcado como "Completo" no status original — mantido concluído abaixo. Os capítulos empíricos 2 e 3 já tinham escrita parcial/pendente registrada anteriormente; por decisão do usuário, suas etapas ficam marcadas como não realizadas por hora, e serão atualizadas conforme o trabalho avançar.

### Capítulo empírico 1 — `chapters/04-Processo de industrialização (1808-1973).tex`

> Atualizado em 29/08/2026 após a rodada `specs/2026-08-29_capitulo_historico_1_review/`: a importação do docx original revelou que o capítulo está bem menos pronto do que o status "Completo" indicava. Aproximadamente metade do texto é esboço/nota de rascunho (não texto corrido), e há dezenas de citações incompletas (`\aiflag{...}` no `.tex`). Ver `specs/2026-08-29_capitulo_historico_1_review/plan.md` para o relato completo.

- [~] Revisão de literatura -- citações presentes ao longo do texto, mas a bibliografia em `references.bib` é só stub (autor/ano); falta exportar a biblioteca real do Zotero.
- [~] Coleta de dados secundários -- 2 tabelas e 4 figuras já incorporadas; múltiplos pontos ainda marcados `[FIGURA A INSERIR: ...]` no texto.
- [~] Produção de imagens e tabelas -- idem acima; parte dos gráficos planejados pelo autor ainda não existem como arquivo.
- [~] Escrita do texto -- cerca de metade do capítulo (especialmente da seção "1945-1964" em diante) é esboço/anotação, não prosa finalizada (ver blocos `\begin{esboco}` no `.tex`).
- [ ] Revisão de texto e citações -- primeira passada de IA já aplicada (marcações em vermelho/tachado no `.tex`); aguardando o ciclo iterativo com o usuário (ver "Ciclo de Revisão Iterativo" em `specs/constitution.md`).

Prazo final: -

### Capítulo empírico 2 — `chapters/05-Processo de desindustrialização (1974-2025).tex`

- [ ] Revisão de literatura
- [ ] Coleta de dados secundários
- [ ] Produção de imagens e tabelas
- [ ] Escrita do texto
- [ ] Revisão de texto e citações

Prazo final: 30/09/2026

### Capítulo empírico 3 — `chapters/06-A desindustrialização em perspectiva geográfica.tex`

- [ ] Revisão de literatura
- [ ] Coleta de dados secundários
- [ ] Produção de imagens e tabelas
- [ ] Escrita do texto
- [ ] Revisão de texto e citações

Prazo final: 30/10/2026

## Demais capítulos

Etapas: escrita → revisão de texto e citações.

> Nota: para Introdução, Teoria, Metodologia e Conclusão, a escrita está marcada como parcial (status anterior "Revisão textual" indicava um rascunho já existente, ainda sujeito a ajustes antes da revisão de texto e citações).

### Introdução — `chapters/01-Introducao.tex`

- [~] Escrita
- [ ] Revisão de texto e citações

Prazo final: 15/11/2026

### Teoria — `chapters/02-Desindustrialização (Teoria).tex`

- [~] Escrita
- [ ] Revisão de texto e citações

Prazo final: 30/11/2026

### Metodologia — `chapters/03-Metodologia.tex`

- [~] Escrita
- [ ] Revisão de texto e citações

Prazo final: 15/12/2026

### Discussão — `chapters/07-Discussão.tex`

- [ ] Escrita
- [ ] Revisão de texto e citações

Prazo final: TBD (não constava em `status_capitulos.png` original — ver nota histórica abaixo)

### Conclusão — `chapters/08-Conclusão.tex`

- [~] Escrita
- [ ] Revisão de texto e citações

Prazo final: 30/12/2026

## Marcos de entrega

| Marco | Prazo final |
|---|---|
| Conteúdo completo | 31/12/2026 |
| Revisões textuais finais | 15/01/2027 |
| Envio para a banca | 15/01/2027 |
| Defesa | 3ª semana de março/2027 |
| Revisões pós-defesa | 2ª semana de março/2027 |

> ⚠️ Inconsistência na fonte original: "Revisões pós-defesa" (2ª semana de março) aparece *antes* de "Defesa" (3ª semana de março) na tabela. Provavelmente uma troca de datas no documento original — confirmar com o orientador antes de tratar essas datas como definitivas.

## Nota histórica

A estrutura acima substitui a tabela original transcrita de `status_capitulos.png` (colunas: Status do texto / Dados coletados? / Dados analisados?). Essa tabela indicava a linha "Discussão" como ausente da imagem original.
