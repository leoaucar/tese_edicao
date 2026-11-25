# Passagem: de volta à construção das skills (2026-11-25)

Para a sessão que retoma `~/Documents/academic-writing-skills`. Complementa
`handoff_verificacao_citacoes.md` (2026-10-18), que segue válido. Aqui só o que mudou
desde então.

## Estado das duas frentes

**Tese, cap. 2** (branch `2026-10-11_capitulo_02_teoria`, em dia com `main` em 2026-11-25):

- Seção "Os objetos onde esse enraizamento se desenvolve": o autor transformou as notas de IA
  em prosa; as 22 obras citadas ali foram exportadas do Zotero para `references.bib` e as
  citações viraram `\citep`/`\citet` (commit `7925d64`). Pendências do autor: reescrever
  as frases ainda endereçadas a ele no parágrafo "Dessa maneira, em vez de uma dominância
  culturalista..." ("Ligação com...", "Formule assim...", "Papel da tese:"); conferir nas
  páginas as obras fora de Vereta-Nahoum (aviso `\todoaiflag` reposto); "(fonte)" do
  empreendedorismo como ideologia segue sem fonte.
- Erro de compilação **anterior** a esta sessão: cap. 4, linha 1339 ("Too many }'s" num
  `\aiflag`; causa não investigada). O PDF sai com `latexmk -f`, mas o erro precisa ser corrigido.

**Skill `revisao-academica-ptbr`, teste em "Teoria do quê?"** (cap. 2, linhas 3-112),
fora do Projeto B formal:

- Passo 1 rodado. Pasta da rodada:
  `chapters/revisao/02-Desindustrialização (Teoria)/secao-3-112/`; lista de termos em
  `chapters/revisao/02-Desindustrialização (Teoria)/termos.tsv` (40 candidatos `proposto`).
- **Parado à espera do autor**: decidir cada termo (`aprovado` / `rejeitado` /
  `retomada`). Só depois vêm os passos 2 a 5.
- Medidas: 1.705 palavras, 17 parágrafos, 25,1 palavras por frase; 14 sinais de "que"
  (D9), concentrados nas linhas 29-36, 65-70, 77-92.
- Tudo o que essa rodada ensinar sobre a skill vai para o roadmap de
  `academic-writing-skills` como observação do Projeto B.

## Onde fica o plano do Projeto B

Proposta (a confirmar com o autor): o spec do Projeto B fica em `tese_edicao/specs/`,
porque trata do texto da tese, das branches por capítulo e do `status_capitulos.md`.
O roadmap de `academic-writing-skills` (itens 12-14) aponta para esse spec, em vez de
duplicá-lo. Observações sobre o comportamento da skill continuam a ir para
`academic-writing-skills`.

## Próximo passo nas skills: Projeto A2, item 8 (extração de citações)

O roadmap de `academic-writing-skills` diz "Start here: plan Project A2, item 8". Material
pronto para partir:

| Peça | Onde | Serve para |
|---|---|---|
| `zapi.local_find` | `~/Documents/agent-skills/skills/zotero-organization/scripts/zapi.py` | busca somente leitura em todas as bibliotecas (pessoal e grupos) numa cópia do `zotero.sqlite`; já indicada pelo roadmap |
| `zotero_bib_export.py` (novo) | `tese_edicao/scripts/` | gera BibTeX de chaves Zotero a partir da cópia do `zotero.sqlite`, com chave no padrão nativo do Zotero; resolve a falta de Better BibTeX e do Zotero aberto |
| `lacunas_citacao.py` | `.claude/skills/busca-bibliografica-zotero/scripts/` | lista `\todouser` / "(fonte)" por seção |
| `indexar_biblioteca.py` | idem | índice da biblioteca e dos anexos |
| `extrato_pdf.py`, `triagem_pdf.py`, `ancora_capitulo.py` | `.claude/skills/fichamento-zotero/scripts/` | página impressa, PDF escaneado ou ausente, âncora estável no capítulo |
| `consolidar-bibliografia-zotero` | `.claude/skills/` | mescla `.bib`, colisões, cobertura das `\cite*` |

O que esta sessão aprendeu e vale para o item 8:

1. **Sem Better BibTeX.** O Zotero não tem o plugin, e a API local (porta 23119) não
   responde com o Zotero fechado. As chaves de `references.bib` seguem o padrão nativo
   (`sobrenome_primeirapalavra_ano`, stopwords inglesas removidas: `santos_o_2007` mantém
   o "o"). Um extrator que resolva citações deve gerar e casar chaves nesse padrão.
2. **Citação em texto simples é o caso comum** quando o autor transforma notas de IA em
   prosa: "Lima e Higgins (2018, p. 13)", "(pp. 34-37)" sem obra, "(Distinction)" no lugar
   do ano. O extrator precisa reconhecer citação em texto simples, não só `\cite*`, e
   marcar páginas órfãs (página sem obra) para ligar à obra citada antes.
3. **Grupos duplicam registros** (Vereta-Nahoum em Personal e DTA_biblioteca; Druck,
   Filgueiras, Marcelino em Mozona). Preferir o registro pessoal e dizer onde está o PDF.
4. **Sobrenomes compostos** (Chaves Jardim, Boito Jr., Vereta-Nahoum, Pinheiro-Machado)
   quebram o casamento "sobrenome no texto = sobrenome no registro" e mudam a forma ABNT
   impressa. Bom cenário plantado para o item 10.
5. **Avisos de verificação somem na reescrita.** O aviso "conferido só por resumos" saiu
   junto com a nota de IA e teve de ser reposto. A checagem deve tratar uma obra sem página
   conferida como "não verificada" mesmo sem marca no texto.

## Pendências abertas no roadmap de `academic-writing-skills` (inalteradas)

- Item 6b: gatilho da proposta de reescrita de parágrafo (A1) e `terms.py candidates` em
  texto de um parágrafo (F1).
- Item 1b: fontes adiadas do guia de estilo.
- Decisão em aberto: ordem entre Projeto B e A3.
