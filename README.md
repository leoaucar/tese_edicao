# Projeto de revisão e finalizaçao da tese
Esse projeto deve auxiliar e facilitar os processos de revisão e edição da tese, facilitando processos manuais repetitivos, mas não interferindo na produção de texto.

Usaremos formato latex, com figuras em png e tabelas CSV externas salvas nmas pastas figures e tables, respectivamente.

O projeto deve exportar o arquivo em DOCx. Os capítulos serão periodicamente enviados para revisão em docx. Deverá ser possivel importar o arquivo docx par aa pasta advisor_reviews e extrair alterações de texto e comentários em uma tasklist.

Trabalharemos as revisoes sempre em branchs únicos, marcados no formado YYYY-MM-DD-description. O fluxo de trabalho se assemelhará a um projeto spec driven. Teremos uma pasta specs para o projeto com uma constitution.md, roadmap.md e status_capitulos e cronograma.md. O roadmap deve prever entregáveis semanais de forma a viabilizar o projeto.

## Estrutura do projeto
tese_edicao/
├── .gitignore
├── README.md
├── main.tex (or main.md)
├── references.bib
├── specs/
├───├── constitution.md
├───├── roadmap.md
├───├── cronograma.md
│   ├── status_capitulos.md
│   ├── YYYY-MM-DD_example_review/
├── chapters/
│   ├── 01-Introducao.tex
│   ├── 02-Desindustrialização (Teoria).tex
│   ├── 03-Metodologia.tex
│   ├── 04-Processo de industrialização (1808-1973).tex
│   ├── 05-Processo de desindustrialização (1974-2025).tex
│   ├── 06-A desindustrialização em perspectiva geográfica.tex
│   ├── 07-Discussão.tex
│   └── 08-Conclusão.tex
├── advisor_reviews/
│   ├── reviewed_doc.docx
│   └── review_task_lists.md
├── figures/
│   ├── exempo.png
│   └── exemplo.pdf
├── tables/
│   ├── exemplo.csv
│   └── exemplot.png
└── outputs/

## Como iniciar o projeto
--> use as imagens cronograma.png; status_capitulos.png e os nomes de capítulos acima para estruturar o projeto inicialmente. Depois delete as imagens.

Em seguida, constitua um roadmap de features. Inicialmente insira:
-preparar projeto (inclui importar textos em docx para os capítulos e bibliografia)
-exportar copiao (vamos exportar uma versao com os capitulos unificados)
-configurar skills (vamos configurar skills para o processo de revisão de texto)

## Você deve:
Usar a ferramenta AskUserInput. Agrupe as perguntas em blocos de 3. Esclareça dúvidas antes de realizar gravações em disco. Proponha complementos necessários a proposição desse readme.
