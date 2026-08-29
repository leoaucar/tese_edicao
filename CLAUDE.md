# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is not a software project — it is a workspace for editing and finalizing a thesis ("tese") written in LaTeX. Its purpose is to assist with repetitive manual review/editing tasks (importing advisor feedback, tracking chapter status, exporting drafts) without interfering with the actual writing of the text.

The repository is currently in its initial setup phase: only `README.md` and `.gitignore` exist. None of the directories or files described below have been created yet — they represent the target structure to build out, not the current state. Always check what actually exists before assuming a file or folder is present.

## Intended project structure

Per the README, the project should converge on:

```
tese_edicao/
├── main.tex (or main.md)
├── references.bib
├── specs/
│   ├── constitution.md
│   ├── roadmap.md
│   ├── cronograma.md
│   ├── status_capitulos.md
│   └── YYYY-MM-DD_example_review/
├── chapters/
│   ├── 01-Introducao.tex
│   ├── 02-Desindustrialização (Teoria).tex
│   ├── 03-Metodologia.tex
│   ├── 04-Processo de industrialização (1808-1973).tex
│   ├── 05-Processo de desindustrialização (1974-2025).tex
│   ├── 06-A desindustrialização em perspectiva geográfica.tex
│   ├── 07-Discussão.tex
│   └── 09-Conclusão.tex
├── advisor_reviews/
│   ├── reviewed_doc.docx
│   └── review_task_lists.md
├── figures/       (PNG figures)
├── tables/        (CSV tables, referenced externally from LaTeX rather than hardcoded)
└── outputs/       (build output, gitignored)
```

## Workflow conventions

- **Format**: main content is LaTeX; figures are PNG; tables are external CSV files referenced from the LaTeX source (not inlined).
- **Export**: the thesis must be exportable to DOCX for advisor review.
- **Advisor review loop**: reviewed DOCX files land in `advisor_reviews/`. Changes and comments from those files need to be extracted into a task list (tracked in a `review_task_lists.md`-style file).
- **Branching**: each round of revision happens on its own branch, named `YYYY-MM-DD-description`.
- **Spec-driven process**: project direction lives under `specs/`, notably `constitution.md` (project principles), `roadmap.md` (planned features/phases), `status_capitulos.md` (per-chapter status), and `cronograma.md` (schedule). Treat these as the source of truth for scope and sequencing once they exist — check them before proposing structural changes.
- Initial roadmap items called out in the README: preparing the project (importing DOCX text into chapters + bibliography), exporting a unified draft ("copiao"), and configuring review-assistance skills.

## Working style for this repository

The README explicitly asks that Claude Code operate this way here:

- Before writing anything to disk (new specs, chapters, restructuring), clarify open questions with the user first using `AskUserQuestion`, grouped in batches of up to 3 questions at a time.
- When the README itself is ambiguous or incomplete for a task, propose concrete additions to it rather than guessing silently.
- This is a slower, confirm-before-acting workflow compared to a typical code repo — prioritize alignment over speed here.

## Commands

There is no build/lint/test tooling yet. Once `main.tex` exists, LaTeX compilation (e.g., `latexmk`) and DOCX export tooling (e.g., `pandoc`) will need to be set up — check for a Makefile or build script before assuming a specific toolchain.
