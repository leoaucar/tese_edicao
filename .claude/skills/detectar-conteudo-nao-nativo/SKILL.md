---
name: detectar-conteudo-nao-nativo
description: "Aponta trechos de um capítulo importado que parecem ser um documento diferente colado por inteiro (artigo publicável separado, currículo, lista de referências duplicada) em vez de prosa nativa do capítulo. Usar após importar um docx, ou quando o usuário suspeitar que 'colou o artigo errado' ou pedir para checar se 'isso aqui é do capítulo mesmo'."
---

# Detectar conteúdo não-nativo colado no capítulo

Identifica, em um capítulo `.tex` recém-importado, trechos que na verdade são um documento diferente colado por inteiro — sinal de que precisam de adaptação estrutural antes de virarem prosa de capítulo, não apenas limpeza de citação. Achado na rodada do capítulo 2 (`specs/2026-08-30_capitulo_teoria_2_import/plan.md`): metade do capítulo era um artigo publicável separado, não uma subseção da tese.

## Sinais de conteúdo não-nativo

- Bloco com título + resumo/abstract + palavras-chave — estrutura de artigo, não de subseção de capítulo.
- Currículo ou informações de autoria de um artigo (afiliação, "Recebido em... Aceito em...").
- Lista de referências formatada ao final do trecho, que duplica (parcial ou totalmente) entradas já em `references.bib` — indício de que é a bibliografia de um artigo colado, não uma seção do capítulo.
- Mudança abrupta de voz/estrutura em relação ao resto do capítulo (ex.: introdução e conclusão próprias, numeração de seção reiniciando).

## Saída

Para cada trecho suspeito: localização no `.tex`, o sinal que motivou a suspeita, e uma sugestão do tipo de adaptação necessária (ex.: "extrair como subseção com transição própria", "resumir e citar como referência ao invés de colar", "confirmar com o usuário se este trecho pertence ao capítulo"). Não editar o `.tex` diretamente — apenas reportar; a decisão de reestruturar é do usuário, alinhada com a regra de não alterar ideias centrais do texto (`specs/constitution.md`).

## Uso de contexto

Mesma lógica de `detectar-esboco`: roda sobre o `.tex` já convertido. Só delegar a um subagente se o capítulo for incomumente longo.
