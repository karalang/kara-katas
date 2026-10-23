#!/usr/bin/env python3
"""Writes data/jobs.tsv: the BibTeX and catalogue files of a university
library's bibliography desk, and the jobs its tools run over them.

A job line is: name, files, then one op per field. Files are "name=hex"
pairs (comma-separated, "-" for none). An op is words separated by spaces;
"h:<hex>" is a UTF-8 string and "x:<hex>" is bytes. A chunk of an
incremental op is "n:<hex>" (not final), "f:<hex>" (final) or "r" (reset).

Run: python3 -s -P -B mk.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
F = {}
JOBS = []


def h(s):
    return "h:" + s.encode("utf-8").hex()


def x(b):
    return "x:" + b.hex()


def n(s):
    return "n:" + s.encode("utf-8").hex()


def f(s):
    return "f:" + s.encode("utf-8").hex()


def nb(b):
    return "n:" + b.hex()


def fb(b):
    return "f:" + b.hex()


def job(name, files, *ops):
    fs = ",".join(k + "=" + F[k].hex() for k in files) or "-"
    for o in ops:
        assert "\t" not in o and "\n" not in o, o
    JOBS.append("\t".join([name, fs] + list(ops)))


REFS = r"""% refs.bib -- exported from the reference manager
@article{muller2019,
  author  = {M{\"u}ller, J{\"o}rg and Erd\H{o}s, P\'al and Fran\c cois Truffaut},
  title   = {On $\alpha$-helices and \(\beta\)-sheets: a ``survey'' --- part~I},
  journal = {J. Struct. Biol. \& Med.},
  pages   = {12--34},
  note    = {100\% open access; see \S 3 \# 4 and file\_name},
}

@book{angstrom1868,
  author    = {\AA ngstr\"om, Anders Jonas and Stra\ss e, Hans},
  title     = {Recherches sur le spectre solaire\ldots{} \textemdash{} \oe uvres},
  publisher = {W.~Schultz},   % Uppsala
  year      = 1868,

  abstract  = {First paragraph.\par Second   paragraph,	with a tab.\\
Next line with \v{s}, \v s, \'{e}, {\'e}, \'\i, \c{c} and \ae\ \o.}
}
"""
F["refs.bib"] = REFS.encode("ascii")

NAMES = ("Müller, Jörg; Erdős, Pál; François Truffaut\n"
         "Ångström, Anders Jonas; Straße; Dvořák; Łukasiewicz; Øresund\n"
         "α-helices ≤ β-sheets ≥ ∞ “quoted” – — … ﬁne ½\n"
         "€ 12 · © 2024 · ™ · ☃ · 😀\n")
F["names.txt"] = NAMES.encode("utf-8")
F["names_crlf.txt"] = "Café\r\nNaïve\r\n".encode("utf-8")
F["latin1.txt"] = "Gödel, Escher, Bach; Ça va; señor; 25°C ±2".encode("latin-1")
F["cp1252.tex"] = b"\x93quoted\x94 \x80 5 \x97 done"
F["cp1252_bad.tex"] = b"abc \x81 def"
F["bad_utf8.tex"] = b"ok \xc3\xa9 then \xe9 bad"
F["trailing.tex"] = b"ends with a backslash \\"
F["math.tex"] = rb"$\alpha \leq \beta$, \(\infty\), $$x^2$$ and \textbackslash{} $\sim$ \~{} ~"

job("table", [], "table")

job("encode basics", [],
    "enc latex strict " + h("Müller"),
    "enc latex strict " + h("Erdős, Pál"),
    "enc latex strict " + h("Ångström"),
    "enc latex strict " + h("å b" + "åb" + "å"),
    "enc latex strict " + h("100% & #1 _x_ $5 {braces} \\back ~tilde ^hat"),
    "enc latex strict " + h("Straße and Œuvre, æther, ø"),
    "enc latex strict " + h("“quoted” – — … ‘single’ «guillemets»"),
    "enc latex strict " + h("α β γ Ω ∞ ≤ ≥ ≠ ∑"),
    "enc latex strict " + h("ﬁne ﬂow ﬀ ﬃ ﬆ"),
    "enc latex strict " + h("© ® ™ ° ± ² µ ¶ · ¿ ¡"),
    "enc latex strict " + h("tab\there\nnewline\r\nCRLF"),
    "enc latex strict " + h("\u200b\u200c\u200d\u2009\u2003 \ufffd \u00a0 \u00ad"),
    "enc latex strict " + h(""),
    "enc latex strict " + h("plain ASCII text 123"),
    "enc latex strict " + h("\\"),
    "enc latex strict " + h("\\\\ two"),
    "enc latex strict " + h("e\u0301 combining"),
    "enc latex strict " + h("Ⅻ"),
)

job("encode errors", [],
    "enc latex strict " + h("snow ☃ man"),
    "enc latex strict " + h("€ 12"),
    "enc latex strict " + h("emoji 😀"),
    "enc latex strict " + h("sep\u2028line"),
    "enc latex ignore " + h("snow ☃ man € 12"),
    "enc latex ignore " + h("\\aa ☃b"),
    "enc latex replace " + h("snow ☃ man € 12 😀"),
    "enc latex keep " + h("snow ☃ man"),
    "enc latex keep " + h("ascii only"),
    "enc ulatex keep " + h("snow ☃ man"),
    "enc latex backslashreplace " + h("☃"),
    "enc latex backslashreplace " + h("ok"),
    "enc ulatex foo " + h("é ☃"),
)

job("encode inputenc", [],
    "enc latex+latin1 strict " + h("Müller, Erdős, ½, ☃"),
    "enc latex+latin1 replace " + h("Müller, Erdős, ½, ☃"),
    "enc latex+utf8 strict " + h("Müller, Erdős, ☃ 😀 & 100%"),
    "enc latex+utf-8 strict " + h("Ångström"),
    "enc latex+latin-1 strict " + h("Ångström Œ"),
    "enc latex_utf8 strict " + h("é"),
    "enc latex-utf8 strict " + h("é"),
    "enc latex+cp1252 strict " + h("“€” Œ ½"),
    "enc latex+ascii strict " + h("é"),
    "enc latex+ strict " + h("é"),
    "enc LaTeX strict " + h("é"),
    "enc ulatex+utf8 strict " + h("é ☃ \\"),
    "enc ulatex+latin1 strict " + h("é ő"),
    "enc ulatex strict " + h("é ő"),
    "enc latex+klingon strict " + h("a"),
    "enc latex+klingon strict " + h("&"),
    "enc latex++x strict " + h("&é"),
    "enc latexx strict " + h("a"),
    "enc latex.utf8 strict " + h("a"),
    "enc latex+utf8+x strict " + h("é"),
)

job("str api", [],
    "strenc latex strict " + h("Müller"),
    "strenc latex+utf8 strict " + h("Müller ☃"),
    "strenc ulatex strict " + h("Müller"),
    "strenc latex strict " + h("☃"),
    "bdec latex strict " + x(b"M\\\"{u}ller"),
    "bdec latex+latin1 strict " + x("Gödel \\'e".encode("latin-1")),
    "bdec ulatex strict " + x(b"abc"),
    "bdec latex strict " + x(b"\\"),
)

job("decode basics", [],
    "dec latex strict " + x(rb"M\"uller and M{\"u}ller and M\"{u}ller"),
    "dec latex strict " + x(rb"Erd\H{o}s, P\'al, Fran\c cois, Fran\c{c}ois"),
    "dec latex strict " + x(rb"\AA ngstr\"om, \aa, Stra\ss e, \o, \ae\ \oe"),
    "dec latex strict " + x(rb"\'\i, \'i, \^\i, \"\i, \v\j, \i\j"),
    "dec latex strict " + x(rb"``quoted'' `single' -- --- - ?` !` ,,low''"),
    "dec latex strict " + x(rb"\& \% \# \_ \$ \{ \} \textbackslash \S \P"),
    "dec latex strict " + x(rb"$\alpha$ \(\beta\) $\gamma $ $ \delta$ $$\pi$$ \alpha"),
    "dec latex strict " + x(rb"\textemdash \textendash \ldots \copyright \textregistered \texttrademark"),
    "dec latex strict " + x(rb"a~b \quad c \ d \, e \- f"),
    "dec latex strict " + x(b"x\n\ny \\par z\n\n\nw"),
    "dec latex strict " + x(b"one\ntwo\n   three \\foo\n bar %comment\n  baz"),
    "dec latex strict " + x(b"tabs\t\tand  spaces   \\bar   \tqux"),
    "dec latex strict " + x(rb"\\ and \\% and \%comment"),
    "dec latex strict " + x(b"#1 # #a param"),
    "dec latex strict " + x(rb"\unknowncommand{arg} \relax\relax x"),
    "dec latex strict " + x(rb"{\"o} {\'e} \'{}e \^{} \~{} \"{}"),
    "dec latex strict " + x(b""),
    "dec latex strict " + x(b"   leading spaces"),
    "dec latex strict " + x(b"\n\nleading newlines"),
    "dec latex strict " + x(rb"\v s \v{s} \u a \k e \r A \H o \d D \textcommabelow S"),
    "dec latex strict " + x(rb"D\v Z dz LJ Lj lj NJ IJ ij fi fl ff ffi ffl st"),
    "dec latex strict " + x(rb"$\leq$\(\geq\)$\infty$ \leq $\neq$\neq"),
)

job("decode errors", [],
    "dec latex strict " + x(b"ab\\"),
    "dec latex+utf8 strict " + x(b"\xc3\xa9b\\"),
    "dec latex ignore " + x(b"ab\\"),
    "dec latex replace " + x(b"ab\\"),
    "dec latex foo " + x(b"ab\\"),
    "dec latex foo " + x(b"ok"),
    "dec latex strict " + x(b"caf\xe9"),
    "dec latex replace " + x(b"caf\xe9 \\'e"),
    "dec latex ignore " + x(b"caf\xe9 \\'e"),
    "dec latex foo " + x(b"caf\xe9"),
    "dec latex+utf8 strict " + x(b"ok \xc3\xa9 then \xe9 bad"),
    "dec latex+utf8 strict " + x(b"\xff"),
    "dec latex+utf8 strict " + x(b"cut \xe2\x82"),
    "dec latex+utf8 replace " + x(b"ok \xe9 bad \xe2\x82 \xff\xfe end \xf0\x9f"),
    "dec latex+utf8 strict " + x(b"\xed\xa0\x80 surrogate"),
    "dec latex+utf8 strict " + x(b"\xc0\xaf overlong"),
    "dec latex+latin1 strict " + x("Gödel \\\"o".encode("latin-1")),
    "dec latex+cp1252 strict " + x(b"\x93q\x94 \x80"),
    "dec latex+cp1252 strict " + x(b"abc \x81 def"),
    "dec latex+klingon strict " + x(b"abc"),
    "dec ulatex+klingon strict " + h("abc"),
    "dec ulatex strict " + h("é ☃ \\'e \\"),
    "dec ulatex replace " + h("é \\"),
    "dec ulatex strict " + h("M\\\"uller, ☃, \\textemdash"),
)

job("incremental encode", [],
    "ienc latex strict " + n("Å") + " " + n(" b") + " " + f("å"),
    "ienc latex strict " + n("\\aa") + " " + n("") + " " + f(" x"),
    "ienc latex strict " + n("å") + " r " + f(" x"),
    "ienc ulatex strict " + n("Erdős ") + " " + n("ø") + " " + f(" end"),
    "ienc latex strict " + n("ok ") + " " + n("☃") + " " + f("after"),
    "ienc latex+utf8 strict " + n("é") + " " + f("&"),
)

job("incremental decode", [],
    "idec latex strict " + nb(b"\\'") + " " + nb(b"e and -") + " " + nb(b"-") + " " + fb(b"- dash"),
    "idec latex strict " + nb(b"ends \\") + " " + fb(b"%"),
    "idec latex strict " + nb(b"ends \\") + " " + fb(b""),
    "idec latex+utf8 strict " + nb(b"split \xc3") + " " + nb(b"\xa9 \xe2\x80") + " " + fb(b"\x94 done"),
    "idec latex+utf8 strict " + nb(b"split \xc3") + " " + fb(b""),
    "idec latex+utf8 replace " + nb(b"split \xc3") + " " + fb(b" x"),
    "idec latex strict " + nb(b"\\AA") + " " + nb(b" ngstr") + " " + nb(b"\\\"") + " " + fb(b"om"),
    "idec latex strict " + nb(b"a\n") + " " + nb(b"\n") + " " + fb(b"b"),
    "idec latex strict " + nb(b"$\\al") + " " + nb(b"pha$") + " r " + fb(b"\\\"o"),
    "idec ulatex strict " + n("\\c") + " " + n(" c") + " " + f("ois"),
    "idec ulatex strict " + n("trailing \\") + " " + f(""),
)

job("lexer", [],
    "lex strict " + x(rb"\foo  bar \' e \\ x \% y %c" + b"\n" + rb"z #1 #a $m$ $$d$$ -- --- ``q'' ?` !`"),
    "lex strict " + x(b"a\n\nb\n  c\t\\par\n"),
    "lex strict " + x(rb"\1 \@ \ \~ \= \^ \! \. \" \` \{"),
    "lex strict " + x(b"end\\"),
    "lex replace " + x(b"end\\"),
    "lex ignore " + x(b"end\\"),
    "lex strict " + x(b""),
    "ilex strict " + nb(b"\\fo") + " " + nb(b"o bar \\") + " " + nb(b"\\ x -") + " " + fb(b"--"),
    "ilex strict " + nb(b"$x") + " " + nb(b"$ \n") + " " + fb(b"\n"),
    "plain strict " + x(rb"\foo bar \'e \\x %c" + b"\n" + b"y\n\nz"),
    "plain strict " + x(b"caf\xe9"),
    "plain replace " + x(b"caf\xe9 \\"),
)

job("files", ["refs.bib", "names.txt", "names_crlf.txt", "latin1.txt", "cp1252.tex", "cp1252_bad.tex", "bad_utf8.tex", "trailing.tex", "math.tex"],
    "read refs.bib latex strict",
    "read math.tex latex strict",
    "read latin1.txt latex+latin1 strict",
    "read cp1252.tex latex+cp1252 strict",
    "read cp1252_bad.tex latex+cp1252 strict",
    "read bad_utf8.tex latex+utf8 strict",
    "read bad_utf8.tex latex+utf8 replace",
    "read trailing.tex latex strict",
    "read missing.tex latex strict",
    "read refs.bib ulatex strict",
    "write out.tex latex strict " + h("Müller & Erdős — 100%"),
    "write out2.tex latex strict " + h("☃ snowman"),
    "write out3.tex latex replace " + h("☃ snowman"),
    "write out4.tex ulatex strict " + h("plain"),
    "write out5.tex latex+utf8 strict " + h("Müller & ☃"),
)

job("convert", ["refs.bib", "names.txt", "names_crlf.txt", "latin1.txt", "math.tex", "trailing.tex"],
    "convert refs.bib refs.txt latex utf-8 strict",
    "convert names.txt names.bib utf-8 latex replace",
    "convert names.txt names_strict.bib utf-8 latex strict",
    "convert names.txt names_u8.bib utf-8 latex+utf8 strict",
    "convert names_crlf.txt crlf.bib utf-8 latex strict",
    "convert latin1.txt latin1.bib latin-1 latex strict",
    "convert latin1.txt latin1_l1.bib latin-1 latex+latin1 strict",
    "convert math.tex math.txt latex utf-8 strict",
    "convert trailing.tex trailing.txt latex utf-8 replace",
    "convert refs.txt refs_again.bib utf-8 latex strict",
    "convert refs.bib refs.bib latex utf-8 strict",
)

with open(os.path.join(HERE, "data", "jobs.tsv"), "w", encoding="utf-8") as fh:
    for j in JOBS:
        fh.write(j + "\n")
print(len(JOBS), "jobs")
