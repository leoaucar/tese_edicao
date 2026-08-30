#!/usr/bin/env node
// Export one chapter (or main.tex) to DOCX for advisor review.
//
// Why this exists instead of a plain `pandoc chapter.tex -o out.docx`:
// pandoc's LaTeX reader doesn't understand the thesis's abntex2 preamble
// or csvsimple tables, and its docx writer silently drops \textcolor
// (the \aiflag{...} AI-suggestion marking convention from
// specs/constitution.md would render as plain black text). This script
// wraps the chapter in a minimal pandoc-readable preamble (real natbib,
// so \citep/\citet/\citeyearpar resolve via citeproc), inlines
// \csvautotabular{...} calls as real tables, and runs pandoc with a Lua
// filter + custom reference.docx so the AI markup keeps its color.
//
// Usage:
//   node scripts/export_docx/export.js <chapter.tex> [output.docx]
//
// Example:
//   node scripts/export_docx/export.js "chapters/04-Processo de industrialização (1808-1973).tex" outputs/cap04.docx
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { csvToLatex } = require('./csv_to_latex');

const scriptDir = __dirname;
const projectRoot = path.resolve(scriptDir, '..', '..');

const chapterArg = process.argv[2];
if (!chapterArg) {
  console.error('Usage: node scripts/export_docx/export.js <chapter.tex> [output.docx]');
  process.exit(1);
}
const chapterPath = path.resolve(projectRoot, chapterArg);
const outPath = path.resolve(
  projectRoot,
  process.argv[3] || path.join('outputs', path.basename(chapterPath, '.tex') + '.docx')
);

let body = fs.readFileSync(chapterPath, 'utf8');

body = body.replace(/\\csvautotabular\{([^}]+)\}/g, (_match, csvRel) => {
  const csvAbs = path.join(projectRoot, csvRel);
  return csvToLatex(csvAbs).trim();
});

const preamble = `\\documentclass[12pt]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{graphicx}
\\usepackage{xcolor}
\\usepackage[normalem]{ulem}
\\usepackage{natbib}
\\usepackage{booktabs}

\\newcommand{\\aiflag}[1]{\\textcolor{red}{#1}}
\\newenvironment{esboco}{%
  \\par\\noindent\\textcolor{gray}{\\textbf{[ESBOÇO --- A DESENVOLVER]}}\\par
  \\begin{quotation}\\color{gray}\\itshape
}{%
  \\end{quotation}
}

\\begin{document}
`;

const closing = `

\\bibliographystyle{apalike}
\\bibliography{references}
\\end{document}
`;

fs.mkdirSync(path.dirname(outPath), { recursive: true });
const tmpTexPath = path.join(
  require('os').tmpdir(),
  `tese_export_${path.basename(chapterPath, '.tex')}.tex`
);
fs.writeFileSync(tmpTexPath, preamble + body + closing, 'utf8');

const pandocArgs = [
  tmpTexPath,
  '-o', outPath,
  '--citeproc',
  '--bibliography', path.join(projectRoot, 'references.bib'),
  '--resource-path', projectRoot,
  '--lua-filter', path.join(scriptDir, 'aiflag_style.lua'),
  '--reference-doc', path.join(scriptDir, 'reference.docx'),
];

execFileSync('pandoc', pandocArgs, { stdio: 'inherit', cwd: projectRoot });
console.log('Wrote', outPath);
