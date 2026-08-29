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

4. **Revisão de IA** (conforme `specs/constitution.md`, seção "Papel da IA na Revisão de Texto")
   - Gramática/ortografia em português.
   - Identificar ideias repetidas.
   - Sugerir pontos de inserção de tabela/imagem.
   - Checar consistência entre o texto e `tables/*.csv`/`figures/*` existentes.
   - Checar formatação de citações (não o conteúdo bibliográfico).
   - Sugestões de frase mais concisa, marcadas em **vermelho** (`xcolor`) e **tachado** (`ulem`) diretamente no `.tex`.

5. **Atualização de specs**
   - `specs/status_capitulos.md`: atualizar etapas do Capítulo empírico 1 conforme progresso real (escrita e demais etapas anteriores já estavam marcadas como concluídas; "Revisão de texto e citações" só fecha depois que o usuário aceitar/rejeitar as sugestões da IA).
   - `specs/roadmap.md`: marcar os itens da Semana 1 correspondentes.

6. **Fechamento da rodada** (Princípio 7 da constituição — obrigatório, não pular)
   - Revisar `specs/proposed_skills.md` (ex.: propor uma skill `importar-docx-latex` dedicada, se o processo de conversão pandoc + limpeza manual se mostrar repetível).
   - Revisar `specs/constitution.md` incorporando qualquer regra nova percebida durante a conversão real (ex.: convenção para notas de rodapé, tipo de citação usado).
   - Confirmar que roadmap/status_capitulos refletem o estado real.
   - Propor melhorias de spec/skills com base no que esta rodada revelar.

## Validação

- [ ] Todo o conteúdo textual do docx original está presente no `.tex` (nenhuma perda de parágrafos/seções).
- [ ] Nenhuma ideia central foi alterada ou removida silenciosamente.
- [ ] Nenhuma citação nova foi inserida diretamente no texto pela IA.
- [ ] Todas as sugestões da IA aparecem marcadas em vermelho/tachado no `.tex` — nada foi aplicado como texto final.
- [ ] Citações existentes usam comando LaTeX válido.
- [ ] `main.tex` compila sem erros (validação real após o MiKTeX estar pronto) — na ausência disso, checagem estrutural manual documentada aqui.
- [ ] `specs/status_capitulos.md` e `specs/roadmap.md` atualizados.
- [ ] `specs/proposed_skills.md` e `specs/constitution.md` revisados (Princípio 7).

## Observações

Esta rodada testa o fluxo fim-a-fim (docx bruto → LaTeX → revisão de IA marcada → aceite humano) pela primeira vez. É esperado que o processo revele lacunas na constituição/roadmap — documentar tudo no fechamento.
