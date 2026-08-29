# Constituição do Projeto

Rascunho inicial (a ser revisado pelo usuário) com base no que já está implícito no README e nas decisões tomadas até aqui.

## Propósito

Apoiar a revisão e finalização da tese, automatizando tarefas manuais repetitivas do processo de edição — sem interferir na produção do texto em si.

## Princípios

1. **Formatos**: o corpo da tese é escrito em LaTeX. `main.tex` importa cada capítulo de `chapters/*.tex` via `\input`. Figuras ficam em `figures/` (PNG); tabelas ficam em `tables/` (CSV), referenciadas a partir do LaTeX — nunca com dados hardcoded no texto.
2. **Exportação**: deve sempre ser possível gerar uma versão em DOCX da tese (ou de capítulos individuais) para envio ao orientador.
3. **Fluxo de revisão do orientador**: cada rodada de revisão gera uma pasta `advisor_reviews/YYYY-MM-DD_descrição/`, contendo o `.docx` recebido de volta e um `review_task_lists.md` com as alterações/comentários extraídos.
4. **Branches**: cada rodada de revisão roda em uma branch própria, nomeada `YYYY-MM-DD-descrição`. Não revisar diretamente na `main`.
5. **Processo guiado por specs**: `specs/constitution.md`, `roadmap.md`, `status_capitulos.md` e `cronograma.md` são a fonte da verdade para escopo, status e prazos. Specs de rodadas individuais de revisão (`specs/YYYY-MM-DD_descrição/`) documentam decisões específicas daquela rodada.
6. **Antes de gravar em disco**: mudanças estruturais (novas specs, reorganização de capítulos, etc.) devem ser esclarecidas com o usuário antes, agrupando dúvidas em blocos de até 3 perguntas via `AskUserQuestion`.
7. **Documentação sempre atualizada**: ao final de cada spec/rodada de revisão, antes de considerá-la encerrada, revisitar e atualizar:
   - `specs/proposed_skills.md` — adicionar/ajustar skills propostas se necessário;
   - `specs/constitution.md` — refletir qualquer regra nova ou ajustada que tenha surgido durante o trabalho;
   - `specs/roadmap.md` e `specs/status_capitulos.md` — refletir o progresso real;
   - propor melhorias de specs/skills com base no que o trabalho daquela rodada revelou (ex.: se surgiu a necessidade de revisão de literatura estruturada, propor uma skill `revisao-literatura`).

   Esse é um passo de fechamento obrigatório, não opcional — uma rodada só é considerada concluída depois dele.

## Workflow de Capítulos

Todo capítulo avança por um conjunto fixo de etapas, dependendo do seu tipo. O status de cada capítulo, por etapa, é rastreado em `specs/status_capitulos.md`.

- **Capítulos empíricos** (capítulos que apresentam e analisam dados originais — ex.: capítulos empíricos 1, 2 e 3):
  1. Revisão de literatura
  2. Coleta de dados secundários
  3. Produção de imagens e tabelas
  4. Escrita do texto
  5. Revisão de texto e citações

- **Demais capítulos** (Introdução, Teoria, Metodologia, Discussão, Conclusão):
  1. Escrita
  2. Revisão de texto e citações

Um capítulo só é considerado pronto para envio ao orientador (`advisor_reviews/`) quando todas as suas etapas estiverem marcadas como concluídas em `specs/status_capitulos.md`.

## Papel da IA na Revisão de Texto

Durante a etapa "Revisão de texto e citações" (ver Workflow de Capítulos), a IA deve:

- Verificar gramática e ortografia (em português).
- Identificar ideias repetidas ao longo do texto.
- Sugerir pontos onde uma tabela ou imagem poderia ser inserida.
- Apontar inconsistências entre os argumentos do texto e os dados/imagens/tabelas fornecidos — comparando com os arquivos originais em `tables/*.csv` e `figures/*`, não apenas com tabelas/imagens já inseridas no capítulo.
- Verificar formatação incorreta de citações (comando/estilo de citação) — correção de *conteúdo* bibliográfico (autor, ano, etc.) é sempre uma sugestão marcada, nunca uma correção silenciosa, mesmo quando a citação já existe no texto.
- Sugerir frases mais concisas/claras, marcando a sugestão conforme a convenção de marcação abaixo.

A IA NÃO deve:

- Alterar ou inserir ideias centrais do texto.
- Adicionar novas citações diretamente no texto (pode sugeri-las fora do corpo principal, para o usuário avaliar).
- Alterar o texto final diretamente — a IA só sugere; quem revisa e escreve a versão final é o usuário.

### Convenção de marcação

- Texto sugerido pela IA é escrito diretamente no `.tex` do capítulo, em **vermelho**, usando os pacotes `xcolor` (cor) e `ulem`/`soul` (tachado) — assim a sugestão aparece no PDF compilado e é carregada também na exportação para DOCX.
- Texto que a IA sugere remover fica **tachado** no próprio arquivo, nunca apagado — a decisão de remover é do usuário.
- Toda sugestão deve ser claramente visível e reversível pelo leitor; nenhuma edição da IA deve ser indistinguível do texto original.
- `main.tex` inclui `xcolor` e `ulem` (modo `normalem` para não afetar `\emph`) no preâmbulo para suportar essa convenção.

### Princípio geral

Foco em mensagem clara, preservação da intenção autoral, reprodutibilidade e consistência, automatizando o trabalho mecânico de revisão — nunca o raciocínio ou a argumentação por trás do texto.

## Fora de escopo

- Este projeto não gera nem edita o conteúdo argumentativo da tese — apenas organiza, converte formatos e rastreia status/revisões.

---
*Este documento é um rascunho inicial — revisar e ajustar conforme necessário.*
