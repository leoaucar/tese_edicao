---
name: consolidar-bibliografia-zotero
description: "Mescla um arquivo .bib (exportado do Zotero, real ou parcial) com o references.bib do projeto, casando entradas stub existentes e sinalizando colisões/ausências. Usar quando o usuário dropar um .bib para um capítulo, pedir para 'consolidar bibliografia', 'importar .bib do Zotero', ou 'mesclar referências'."
---

# Consolidar bibliografia do Zotero

Mescla um `.bib` novo (exportado do Zotero, cobrindo um capítulo ou a biblioteca inteira) com o `references.bib` do projeto.

## Uso de contexto

`references.bib` já passa de 190KB. Não é necessário nem desejável ler o arquivo inteiro na conversa principal para fazer a mesclagem — delegue a um subagente (`Agent`, `general-purpose` ou fork) que: lê os dois `.bib`, faz o casamento de chaves, escreve o `references.bib` atualizado, e devolve só um resumo (quantas entradas casadas, quantas coladas, quantas colisões, quantas citações do capítulo sem entrada em nenhum dos dois arquivos). A sessão principal revisa esse resumo, não o diff bruto do `.bib`.

## Passos

1. **Casar stubs existentes**: para cada entrada *stub* já usada nos capítulos (criada por `importar-docx-latex`, identificada por autor/ano sem metadados completos), procurar a entrada correspondente no `.bib` novo por autor + ano. Ao encontrar, substituir o stub pela entrada completa, preservando a *chave* de citação já usada no `.tex` (para não quebrar `\citep`/`\citet` existentes) ou, se for preciso trocar a chave, atualizar todas as ocorrências no capítulo.
2. **Detectar ambiguidades**: mesmo autor/ano mas obras diferentes (ex.: dois artigos do mesmo autor no mesmo ano sem sufixo a/b) — sinalizar para o usuário decidir, nunca escolher silenciosamente. **Importante**: "é ambíguo se essa entrada deve substituir/mesclar com um stub existente" é uma pergunta distinta de "essa entrada deve existir em `references.bib`" — sinalizar a primeira nunca deve significar pular a segunda. Uma entrada nova e válida do `.bib` do capítulo deve ser adicionada a `references.bib` (sob sua própria chave) mesmo quando fica em aberto se ela duplica um stub antigo; do contrário uma citação do capítulo fica sem entrada nenhuma, o que só aparece como erro na compilação final (achado na rodada `2026-08-30_capitulo_geografica_5_import`, ver `specs/proposed_skills.md`).
3. **Mesclar `.bib` completo**: quando o arquivo novo não é só stubs mas uma exportação real e completa,
   - checar colisões de *chave* (mesma chave, conteúdo diferente) e sinalizar;
   - pular duplicatas idênticas (mesma chave, mesmo conteúdo);
   - adicionar entradas novas sem chave conflitante diretamente.
4. **Cobertura**: verificar se toda `\cite*{}` do capítulo em questão tem entrada em algum dos `.bib` (existente ou novo). Sinalizar (não silenciar) as que não têm — na rodada do capítulo 2, ~38 de 66 citações de uma seção ficaram fora do universo bibliográfico do `.bib` fornecido; isso é esperado e deve ser reportado ao usuário como lista, não escondido ou preenchido com stub genérico.

## Regras fixas (constitution.md)

- Correção de conteúdo bibliográfico é sempre sugestão marcada — nunca reescrever uma citação existente no texto silenciosamente, mesmo ao consolidar o `.bib`.
- Reportar sempre, nunca assumir: colisões, ambiguidades e citações sem entrada correspondente vão para o usuário decidir.
