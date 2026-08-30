---
name: detectar-esboco
description: "Aponta, em um capítulo .tex, quais parágrafos parecem esboço/nota do autor (não prosa finalizada) vs. quais já estão prontos para revisão fina. Usar como checagem complementar após importar um capítulo, ou quando o usuário pedir para 'ver o que ainda é rascunho' / 'checar o que falta escrever' em um capítulo."
---

# Detectar esboço vs. prosa final

Varre um capítulo `.tex` e classifica cada parágrafo/trecho como esboço (nota do autor, não texto corrido) ou prosa finalizada — complementar à classificação automática feita durante `importar-docx-latex`, mas também útil isoladamente em rodadas de revisão futuras (o texto pode voltar a ter trechos de esboço depois de edições do usuário).

## Sinais de esboço

- Bullets ou listas soltas sem conectivos de prosa.
- ALL CAPS (ex.: "COMPARAR X COM Y", "VERIFICAR FONTE").
- Frases sem pontuação terminal ou claramente incompletas.
- Notas entre colchetes tipo `[FIGURA A INSERIR]`, `[falta dado]`.
- Já envolvido em `\begin{esboco}` — reportar como já tratado, não reclassificar.

## Saída

Lista por parágrafo/trecho (referenciando linha ou seção do `.tex`): classificação (esboço / prosa / incerto) + trecho curto de contexto. Trechos "incerto" vão para o usuário decidir — não marcar automaticamente como um ou outro no arquivo; esta skill só reporta, quem edita o `.tex` (envolvendo em `\begin{esboco}` ou não) é o usuário ou o passo de importação, nunca esta skill sozinha.

## Uso de contexto

Rodar sobre o `.tex` já convertido (não sobre o docx bruto) — o arquivo de capítulo já é razoável em tamanho, não precisa de subagente dedicado a menos que o capítulo seja incomumente longo (>150KB), caso em que vale delegar a leitura a um subagente e trazer só a lista classificada de volta.
