// Convert a simple CSV file into a LaTeX tabular block (booktabs style).
// Used by export.js to inline \csvautotabular{...} tables before handing
// the chapter to pandoc, since pandoc's LaTeX reader doesn't understand
// csvsimple (it would silently drop the table otherwise).
const fs = require('fs');

function escapeLatex(s) {
  return s
    .replace(/\\/g, '\\textbackslash{}')
    .replace(/&/g, '\\&')
    .replace(/%/g, '\\%')
    .replace(/\$/g, '\\$')
    .replace(/#/g, '\\#')
    .replace(/_/g, '\\_')
    .replace(/\{/g, '\\{')
    .replace(/\}/g, '\\}')
    .replace(/~/g, '\\textasciitilde{}')
    .replace(/\^/g, '\\textasciicircum{}');
}

function parseCsvLine(line) {
  // Simple split — fine for this project's tables (no quoted commas).
  return line.split(',');
}

function csvToLatex(csvPath) {
  const raw = fs.readFileSync(csvPath, 'utf8').replace(/\r\n/g, '\n').trim();
  const rows = raw.split('\n').map(parseCsvLine);
  const nCols = rows[0].length;
  const align = 'l' + 'r'.repeat(nCols - 1);
  const header = rows[0].map(escapeLatex).join(' & ');
  const body = rows.slice(1).map(r => r.map(escapeLatex).join(' & ')).join(' \\\\\n');
  return [
    `\\begin{tabular}{${align}}`,
    '\\toprule',
    `${header} \\\\`,
    '\\midrule',
    `${body} \\\\`,
    '\\bottomrule',
    '\\end{tabular}',
  ].join('\n');
}

module.exports = { csvToLatex };

if (require.main === module) {
  process.stdout.write(csvToLatex(process.argv[2]) + '\n');
}
