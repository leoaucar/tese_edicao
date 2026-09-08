use Cwd;

# bibtex/biber resolve BIBINPUTS relative to their own working directory, which
# latexmk sets to the aux/output directory (e.g. outputs/) when -output-directory
# is used. Without this, "references.bib" isn't found next to main.tex and
# kpathsea falls back to an unrelated same-named file bundled with a MiKTeX
# package template, silently producing an empty bibliography.
my $root = getcwd();
# Normalize an MSYS/Cygwin-style "/c/Users/..." path (as seen when latexmk runs
# under Git Bash) to Windows "C:/Users/..." form, since bibtex/kpsewhich are
# native Windows binaries that only understand drive-letter paths.
if ($root =~ m{^/([A-Za-z])/(.*)$}) {
    $root = "$1:/$2";
}
# Path-list separator differs by platform: Windows uses ';', POSIX (Linux/macOS,
# including MSYS/Git Bash since it still invokes native Windows binaries) uses ':'.
my $sep = ($^O eq 'MSWin32' || $^O eq 'msys' || $root =~ m{^[A-Za-z]:/}) ? ';' : ':';
$ENV{'BIBINPUTS'} = $root . $sep . ($ENV{'BIBINPUTS'} // '');

# All build artifacts (main.pdf, .aux, .log, ...) go to outputs/ instead of
# cluttering the project root, matching the gitignored outputs/ convention.
$out_dir = 'outputs';
$pdf_mode = 1;
