---
name: fichamento-zotero
description: "Lê os textos de uma pasta do Zotero (PDF anexado; escaneado via imagem; sem PDF via conhecimento da obra, sinalizado) e grava em cada item uma nota-filha 'Ficha IA' com resumo, como o texto aborda o tema da pasta, ideias úteis com página e onde usar no capítulo (âncora de seção + parágrafo). Gera também a lista de itens sem PDF (.txt). Usar quando o usuário pedir para 'fichar', 'resumir os textos da pasta', 'inserir notas nos itens', 'identificar as ideias relevantes' ou 'como cada texto aborda o tema', ou como etapa seguinte de busca-bibliografica-zotero."
---

# Fichamento de uma pasta do Zotero

Etapa seguinte de `busca-bibliografica-zotero`: depois que a pasta está montada, cada
texto ganha uma ficha que diz o que ele afirma e **para que serve no capítulo**. Também
roda sozinha, sobre qualquer pasta já montada.

Depende de `zotero-organization` (credenciais, `zapi.py`, regras de escrita).

## Antes de começar

- Ler a **nota-critério da pasta** (o tema que as fichas devem cobrir) e o trecho do
  capítulo correspondente, incluindo esboços (`\begin{esboco}` ou listas com "-") e as
  marcas `\todouser{fonte}`. O critério de leitura de cada texto é esse tema.
- Confirmar com o usuário (via `AskUserQuestion`) a pasta, a profundidade (ficha lida no
  PDF é o padrão) e o formato. Não reabrir isso a cada rodada se já foi decidido.

## Passos

1. **Triagem:** `python3 scripts/triagem_pdf.py <scratchpad>/fich COLKEY:rótulo …`
   - classifica cada item como `texto`, `escaneado` ou `sem PDF`, lista as notas que
     já existem e marca `FICHA` se já houver uma "Ficha IA";
   - grava `faltam_pdf.txt` (o usuário prefere a lista em **.txt**); copiar para a
     pasta de backup e informar ao usuário;
   - capítulo de livro "sem PDF" pode ter o PDF no registro do livro: seguir
     `relations: dc:relation` e usar as páginas do capítulo (no Handbook de Smelser &
     Swedberg, página do PDF = página impressa + 13).
2. **Ler as notas do usuário primeiro.** Fichamentos existentes (citações com página)
   são insumo e indicam o que o usuário já destacou. Nunca editar nem duplicar essas
   notas; a ficha da IA é uma nota separada.
3. **Ler o texto**, sempre registrando o que foi lido:
   - texto: `python3 scripts/extrato_pdf.py PDF SAIDA [pág_ini pág_fim] --kw termos`
     (início, conclusão antes da bibliografia e trechos com as palavras-chave do tema,
     com página impressa). Artigo curto sai inteiro;
   - livro: ler o sumário e depois a introdução, o capítulo relevante e a conclusão
     (passar o intervalo de páginas);
   - escaneado: `pdftoppm -r 90 -f N -l N -png PDF prefixo` e ler a imagem (não há
     OCR instalado nem sudo). Limitar a sumário e duas a quatro páginas-chave. Em
     edições brasileiras antigas, uma imagem costuma ter duas páginas impressas;
   - sem PDF: ficha baseada no conhecimento da obra, **sem números de página**, com
     "SEM PDF" e "conferir antes de citar" em "Fonte da ficha".
4. **Escrever a ficha** em `<scratchpad>/fichas.md`, um bloco por item:

   ```
   ### ITEMKEY
   Pasta: <nome da pasta>
   Resumo: <3 a 5 frases: argumento central, objeto, método>
   Como aborda o tema: <como o texto trata o tema da pasta, com citações curtas e página>
   Ideias para o capítulo:
   - <ideia> (p. X): <para que serve; **negrito** quando resolve um \todouser>
   Onde usar: <âncoras no capítulo>
   Fonte da ficha: <páginas lidas; "PDF escaneado, lido em imagem"; "SEM PDF">
   ```

   - **Âncoras, e não números de linha**: "2.1, parágrafo “Poderia ser argumentado
     que…”" ou "2.2.3, tópico “o poder e a violência não simbólica”". Os números de
     linha mudam a cada edição. Se escrever com linhas durante o trabalho, converter
     no fim com `python3 scripts/ancora_capitulo.py CAP.tex fichas.md saida.md`,
     usando a mesma versão do `.tex` em que as linhas foram anotadas (guardar uma
     cópia no início).
   - Ser honesto sobre o encaixe: se o texto é mais metodológico, fraco para o tema ou
     não deveria estar na pasta, dizer isso na ficha. Se o registro estiver duplicado
     ou o PDF trouxer mais de uma obra (ex.: newsletter inteira), apontar e sugerir
     um registro próprio.
   - Peso das fontes (mesma regra da busca): artigos revisados por pares e muito
     citados primeiro; working papers, newsletters e textos de intervenção marcados
     como tal.
5. **Gravar no Zotero:** `python3 scripts/fichas_para_zotero.py fichas.md BACKUP_DIR`
   (dry-run) e depois `--apply`. Item sem ficha ganha nota nova; item com "Ficha IA"
   tem a nota atualizada, com backup da versão anterior. As notas do usuário nunca são
   tocadas.
6. **Registrar:** copiar `fichas.md` e `faltam_pdf.txt` para
   `~/Zotero-reorg-review/<data>_<descrição>/` e informar contagens (fichas por pasta;
   quantas lidas no PDF, em imagem, sem PDF).

## Mapa de afirmações: do texto para as fontes

As fichas vão da fonte para o texto. Para inserir citações é preciso o caminho inverso.
Depois de fichar, gerar `mapa_afirmacoes_<seção>.md` na pasta da rodada em `specs/`:

| Âncora (seção + parágrafo) | Afirmação do texto (resumida) | Marca do autor | Fontes que sustentam (key, página) | Força | Lacuna |
|---|---|---|---|---|---|

- Uma linha por afirmação que pede fonte: toda marca `\todouser{fonte}`, "(fonte)" ou
  "FULANO", mais afirmações fortes sem marca (ex.: termo técnico como "ciência normal" sem
  autor).
- Força: **direta** (a fonte diz isso, com página), **apoio** (sustenta em parte ou por
  extensão), **contraponto** (relativiza a afirmação; avisar o autor).
- Lacuna: nenhuma fonte na biblioteca. Sugerir obras a buscar (via
  `busca-bibliografica-zotero`).
- Afirmações que as fontes contradizem ou só sustentam em parte viram observação para o
  autor (ex.: "paralisia" vs. "perda de centralidade"), nunca correção no texto.
- Exemplo pronto: `specs/2026-10-11_capitulo_02_teoria/analise_teoria_geral_2-1.md`.
  É desse mapa que sai a etapa de sugerir `\aiflag{\citep{…}}` (ver
  `guia_insercao_fontes.txt` na mesma pasta).

## Saídas que costumam vir junto (oferecer, não presumir)

- **Análise do trecho do capítulo**: quais afirmações já têm fonte nas fichas, quais
  lacunas restam e quais clássicos ou textos da área faltam na biblioteca, verificados
  na biblioteca primeiro e depois no Crossref/OpenAlex, com métricas normalizadas por
  área (ver `busca-bibliografica-zotero`).
- **Correções no texto** pedidas pelo usuário: sempre `\sout{antigo}\aiflag{novo}`
  (`specs/constitution.md`), por padrão de texto e restritas ao trecho combinado, com
  dry-run de contagens, cuidado com padrões que casam dentro de outros já marcados
  (usar limites de palavra) e compilação de teste (`pdflatex` em diretório do
  scratchpad). Nunca inserir citações no texto; sugestões ficam no relatório.

## Relação com `verificacao-citacoes` (academic-writing-skills)

A ficha ("o que a obra diz" + "para que serve no capítulo") é o mesmo objeto que o
README de `verificacao-citacoes` prevê: "resumo de cada obra citada ao lado do que o
texto atribui a ela". As fichas gravadas no Zotero podem servir de insumo para a V1
(checagem afirmação × fonte) e de teste para a V2 (sugestão de referências).
