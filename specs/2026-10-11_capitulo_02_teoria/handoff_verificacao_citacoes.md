# Passagem para a skill `verificacao-citacoes` (academic-writing-skills)

Escrito em 2026-10-18, ao fim da sessão de referências do cap. 2 da tese. Leitura para a
sessão que vai abrir o Projeto A2 do roadmap de `~/Documents/academic-writing-skills`
(itens 8 a 11: extração de citações, construção da skill, cenários, validação).

## Caso de teste pronto: capítulo 2 da tese

- Capítulo: `~/Documents/tese_edicao/chapters/02-Desindustrialização (Teoria).tex`
  (198 `\cite*`: 147 `\citep`, 51 `\citet`, 21 `\citeauthor`, 21 `\citeyear`; bibliografia
  em `references.bib`, estilo abntex2-alf).
- Lacunas marcadas pelo autor: `\todouser{}{fonte}`, `(fonte)`, `FULANO`, nomes informais
  ("Cristiano e Rafael" = Monteiro & Lima 2021).
- Gabarito de "qual fonte resolve qual lacuna" para a seção 2.1:
  `specs/2026-10-11_capitulo_02_teoria/analise_teoria_geral_2-1.md`. Para A.0 e A.2, as notas
  "Ficha IA" no Zotero (29 fichas, cada uma com resumo, ideias com página e "onde usar").
- Stub conhecido: `sautuetal2005` em `references.bib` (autor "Sautu, ... and others"), útil
  para testar a detecção de entrada incompleta.

## O que a sessão de referências aprendeu (vale para a V1 e para a V2)

1. **Biblioteca primeiro.** Quase tudo já estava no Zotero, inclusive como capítulo dentro
   de handbook (PDF no registro do livro) ou com título diferente. A busca online
   completava pouco.
2. **PDFs:** dá para triar texto, escaneado ou sem PDF contando palavras em páginas do meio.
   Escaneados podem ser lidos renderizando páginas (`pdftoppm`); não há OCR nem sudo na
   máquina. A página impressa difere da do PDF: detectar o número impresso no topo ou no
   rodapé, ou registrar o deslocamento (Handbook de Smelser & Swedberg: PDF = impressa + 13).
3. **Âncoras e não números de linha:** o autor edita durante o trabalho. Usar seção + início
   do parágrafo (script `ancora_capitulo.py` na skill `fichamento-zotero`).
4. **Métricas:** usar o percentil OpenAlex normalizado por área e ano, não a contagem bruta.
   O OpenAlex classifica sociologia econômica como "Economics"; decidir a área pelo
   periódico. Sem chave de API, a busca por título esgota o orçamento diário (consulta por
   DOI dura mais); Crossref como plano B.
5. **Marcação:** a IA não insere citação direto (constitution da tese); sugere em
   `\aiflag{\citep{...}}` ao lado do `\todouser`. Não usar `%` dentro de `\aiflag{}`.
   Substituições por padrão devem evitar casar dentro de trechos já marcados (limite de
   palavra) e terminar com compilação de teste.
6. **Ficha = "o que a obra diz" + "para que serve no trecho"**: é exatamente a coluna
   "resumo de cada obra ao lado do que o texto atribui a ela" do README da skill.
7. **VS Code:** o editor pode manter um buffer antigo não salvo do capítulo
   (`~/.config/Code/Backups`); avisar o usuário para recarregar e não salvar por cima.

## `fichamento-zotero` como base da `verificacao-citacoes`

Decisão do autor (2026-10-18): usar a skill `fichamento-zotero`
(`~/Documents/tese_edicao/.claude/skills/fichamento-zotero/`) como **base e referência**
para a checagem. Usar como referência, não copiar: a checagem tem de servir a qualquer
texto, e não só à tese e ao Zotero do autor.

O que já existe e corresponde a partes da V1/V2:

| Na fichamento-zotero | Na verificacao-citacoes |
|---|---|
| Ficha: "Como aborda o tema" + "Ideias (p.)" | V1, coluna "resumo de cada obra ao lado do que o texto atribui a ela" |
| Mapa de afirmações (texto → fontes), com força direta/apoio/contraponto e lacunas | V1, "a afirmação atribuída é o que a fonte diz" (sustentada / parcial / não encontrada / contradita); V2, sugestão de fontes para lacunas |
| `extrato_pdf.py`: texto por página com número impresso, início, fim e palavras-chave, cortando a bibliografia | V1, conferir citação direta e página no PDF |
| `triagem_pdf.py`: texto / escaneado / sem PDF; lista do que falta | V1, limites conhecidos (PDF escaneado, sem PDF), reportados e não escondidos |
| `ancora_capitulo.py`: seção + início do parágrafo | localização estável dos achados no relatório |
| Notas "Ficha IA" no Zotero (29, pastas A.0 e A.2) | insumo já pronto: a V1 pode ler a ficha antes de reabrir o PDF |
| Regras: nunca editar o original; sugestões marcadas; fichas "SEM PDF" sinalizadas | mesmo princípio da revisao-academica-ptbr e da constitution da tese |

O que muda na checagem:
- **Direção:** a fichamento parte de uma pasta de fontes; a checagem parte das citações
  (`\cite*`) e das marcas de lacuna do texto.
- **Escala de veredito:** harmonizar direta/apoio/contraponto (fichamento) com
  sustentada/parcial/não encontrada/contradita (README da skill). Sugestão: usar a
  escala do README e mapear "contraponto" para "parcial ou contradita, com nota".
- **Escrita:** a checagem não precisa gravar no Zotero; o relatório é a saída. Gravar
  fichas fica opcional, via fichamento-zotero.
- **Generalidade:** credenciais, nomes de pastas e convenções da tese
  (`\todouser`, `\aiflag`, constitution) devem virar configuração ou perfil, e não
  ficar fixos no código.

Sugestão de spec: o item 8 (extração em `shared/`) junta o parser de `\cite*` com
`lacunas_citacao.py` e `ancora_capitulo.py`. O item 9 começa pelo "mapa de afirmações"
da fichamento-zotero, aplicado às citações existentes.

## Código reaproveitável (no repositório da tese)

- `.claude/skills/busca-bibliografica-zotero/scripts/`: `indexar_biblioteca.py` (índice da
  biblioteca e dos anexos), `metricas_citacao.py` (OpenAlex/Crossref, percentil),
  `lacunas_citacao.py` (lista `\todouser`/“(fonte)” por seção).
- `.claude/skills/fichamento-zotero/scripts/`: `triagem_pdf.py`, `extrato_pdf.py` (texto por
  página com número impresso), `ancora_capitulo.py`, `fichas_para_zotero.py`.
- `~/.claude/skills/zotero-organization/scripts/zapi.py`: acesso à Web API do Zotero.

Sugestão: o item 8 do roadmap (extração de citações em `shared/`) pode partir de
`lacunas_citacao.py` e de um parser de `\cite*` com opcionais de página.
