# Spec: Revisão do Capítulo Histórico 1 (Capítulo Empírico 1)

## Contexto

Primeira rodada real de trabalho no projeto — serve como teste de ponta a ponta do workflow definido em `specs/constitution.md` e como primeira feature implementada: importação de docx → LaTeX seguida de revisão automatizada de texto.

Capítulo alvo: `chapters/04-Processo de industrialização (1808-1973).tex` (Capítulo empírico 1).

## Entrada esperada

Depositar o `.docx` original em:

```
specs/2026-08-29_capitulo_historico_1_review/source.docx
```

## Tarefas

1. **Conversão inicial (pandoc)**
   - Rodar `pandoc source.docx -o source_raw.tex` como primeira passada, gerando um rascunho intermediário em `specs/2026-08-29_capitulo_historico_1_review/source_raw.tex` (não é o capítulo final).

2. **Limpeza manual e formatação**
   - Mover/adaptar o conteúdo para `chapters/04-Processo de industrialização (1808-1973).tex`, substituindo o placeholder atual.
   - Corrigir citações para comandos LaTeX apropriados (`\cite{}` etc.).
   - Ajustar estrutura de seções (`\section`, `\subsection`) preservando a hierarquia original do docx.
   - Para imagens/tabelas mencionadas no docx: referenciar arquivos já existentes em `figures/`/`tables/` via `\includegraphics`/`csvsimple`, ou deixar um comentário `TODO` apontando o que falta.
   - Garantir acentuação/caracteres especiais em português preservados (UTF-8).

3. **Checagem estrutural**
   - Balanceamento de chaves e ambientes (`\begin`/`\end`).
   - Confirmar que o `\input` em `main.tex` aponta para o arquivo certo.
   - Assim que o MiKTeX (instalação em andamento) estiver pronto, compilar `main.tex` de fato como confirmação real.

4. **Ciclo de revisão iterativo** (conforme `specs/constitution.md`, seções "Ciclo de Revisão Iterativo" e "Papel da IA na Revisão de Texto")
   - Passada de IA: gramática/ortografia em português, ideias repetidas, pontos de inserção de tabela/imagem, consistência entre o texto e `tables/*.csv`/`figures/*`, formatação de citações, frases mais concisas — tudo marcado em **vermelho** (`xcolor`)/**tachado** (`ulem`) diretamente no `.tex`, um commit por passada.
   - Usuário trabalha sobre o capítulo (aceita/rejeita sugestões, reescreve trechos).
   - Nova passada de IA sobre a versão atualizada — repete até o usuário considerar o capítulo pronto. Não é um processo de uma única rodada.

5. **Atualização de specs**
   - `specs/status_capitulos.md`: atualizar etapas do Capítulo empírico 1 conforme progresso real (escrita e demais etapas anteriores já estavam marcadas como concluídas; "Revisão de texto e citações" só fecha depois que o usuário aceitar/rejeitar as sugestões da IA).
   - `specs/roadmap.md`: marcar os itens da Semana 1 correspondentes.

6. **Fechamento da rodada** (Princípio 7 da constituição — obrigatório, não pular)
   - Revisar `specs/proposed_skills.md` (ex.: propor uma skill `importar-docx-latex` dedicada, se o processo de conversão pandoc + limpeza manual se mostrar repetível).
   - Revisar `specs/constitution.md` incorporando qualquer regra nova percebida durante a conversão real (ex.: convenção para notas de rodapé, tipo de citação usado).
   - Confirmar que roadmap/status_capitulos refletem o estado real.
   - Propor melhorias de spec/skills com base no que esta rodada revelar.

## Validação

- [x] Todo o conteúdo textual do docx original está presente no `.tex` (nenhuma perda de parágrafos/seções) — conversão via pandoc + limpeza manual, nada omitido; trechos de esboço do autor foram preservados dentro de blocos `esboco`, não descartados.
- [x] Nenhuma ideia central foi alterada ou removida silenciosamente.
- [x] Nenhuma citação nova foi inserida diretamente no texto pela IA — todas as ~130 citações convertidas já existiam no docx (como link do Zotero ou texto simples); nenhuma citação foi adicionada que não estivesse lá.
- [x] Todas as sugestões da IA aparecem marcadas em vermelho/tachado no `.tex` (`\aiflag{}`/`\sout{}`) — nada foi aplicado como texto final.
- [x] Citações existentes usam comando LaTeX válido (`\citep`/`\citet`/`\citeyearpar`, `natbib`).
- [x] `main.tex` compila sem erros — validado com MiKTeX 25.12 (`pdflatex` + `bibtex` + 2 passes), 73 páginas, 0 citações indefinidas, apenas overfull/underfull hbox cosméticos.
- [x] `specs/status_capitulos.md` e `specs/roadmap.md` atualizados.
- [x] `specs/proposed_skills.md` e `specs/constitution.md` revisados (Princípio 7).

## Resultado real (achados desta rodada)

O docx acabou sendo um rascunho de trabalho bem menos pronto do que o status "Completo" sugeria:

- ~130 citações no formato de link do Zotero (`\href{zotero-url}{(Autor, Ano)}`) foram convertidas para `\citep`/`\citet`/`\citeyearpar`; ~85 citações incompletas (placeholders como `(fonte)`, `(autor, ano)`, nomes em minúsculo) foram marcadas com `\aiflag{}` em vez de resolvidas.
- Aproximadamente metade do capítulo (a partir de ~2/3 da seção "1945-1964") é esboço/nota de rascunho (bullets, listas de nomes, instruções tipo "COMPARAR X COM Y"), não prosa finalizada — preservado em blocos `\begin{esboco}`.
- 2 tabelas (`longtable`) e 4 figuras do docx foram incorporadas com `\caption{}` apropriado; `figures/cap04/` criado para as imagens extraídas.
- `references.bib` populado com 23 entradas *stub* (autor/ano apenas) — a biblioteca real do Zotero ainda precisa ser exportada e conciliada (`specs/environment.md` tem a nota técnica).
- Foram necessárias correções técnicas no `main.tex` durante a validação de compilação: pacotes `natbib`, `url`, `longtable`/`booktabs`/`array`/`calc`, e um `\DeclareUnicodeCharacter` para um caractere raro (ver `specs/environment.md`).
- Um bug real de normalização Unicode (NFD vs. NFC) no arquivo gerado pelo pandoc quebrou buscas de string exata durante a limpeza — documentado em `specs/environment.md` para as próximas rodadas.

## Próximo passo (fora desta rodada)

O ciclo iterativo de revisão (`specs/constitution.md`, "Ciclo de Revisão Iterativo") começa agora: o usuário trabalha sobre `chapters/04-...tex` — aceitando/rejeitando as ~85 marcações `\aiflag{}`, escrevendo a prosa que hoje está em blocos `esboco` — e uma nova passada de IA acontece sobre a versão atualizada, quantas vezes forem necessárias.

## Observações

Esta rodada testou o fluxo fim-a-fim (docx bruto → LaTeX → revisão de IA marcada → aceite humano) pela primeira vez, com sucesso, mas revelou que o estado real do conteúdo é mais cru do que o status registrado indicava — a lição principal fica registrada em `specs/status_capitulos.md` e nas skills propostas.
