# Writes data/: S-expression files as tools write them (a KiCad 8
# schematic and its footprint library table, OCaml dune files, an Emacs
# package archive index and custom-set-variables, an SMT-LIB query, a
# Guix-style Scheme manifest), files for the corners of the reader, broken
# files, values to dump, and jobs.tsv, the jobs oracle.py and
# mini_sexpdata.kara run.
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def put(rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


KICAD_SCH = """\
(kicad_sch
\t(version 20231120)
\t(generator "eeschema")
\t(generator_version "8.0")
\t(uuid "8c4a2b1e-1d3f-4c55-9a77-0b6c1f2e3d4a")
\t(paper "A4")
\t(title_block
\t\t(title "USB-C power input")
\t\t(date "2024-03-09")
\t\t(rev "B")
\t\t(company "Example Labs")
\t)
\t(lib_symbols
\t\t(symbol "Device:R"
\t\t\t(pin_numbers hide)
\t\t\t(pin_names
\t\t\t\t(offset 0)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(property "Reference" "R"
\t\t\t\t(at 2.032 0 90)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t)
\t)
\t(symbol
\t\t(lib_id "Device:R")
\t\t(at 120.65 76.2 0)
\t\t(unit 1)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(uuid "3f1e7c2a-0000-4000-8000-000000000001")
\t\t(property "Reference" "R1"
\t\t\t(at 123.19 74.93 0)
\t\t)
\t\t(property "Value" "5.1k"
\t\t\t(at 123.19 77.47 0)
\t\t)
\t\t(property "Footprint" "Resistor_SMD:R_0603_1608Metric"
\t\t\t(at 118.872 76.2 90)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t)
\t(symbol
\t\t(lib_id "Device:R")
\t\t(at 130.81 76.2 0)
\t\t(unit 1)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "R2"
\t\t\t(at 133.35 74.93 0)
\t\t)
\t\t(property "Value" "5.1k"
\t\t\t(at 133.35 77.47 0)
\t\t)
\t\t(property "Footprint" "Resistor_SMD:R_0603_1608Metric"
\t\t\t(at 129.032 76.2 90)
\t\t)
\t)
\t(symbol
\t\t(lib_id "Device:C")
\t\t(at 101.6 88.9 0)
\t\t(unit 1)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "C1"
\t\t\t(at 104.14 87.63 0)
\t\t)
\t\t(property "Value" "10u"
\t\t\t(at 104.14 90.17 0)
\t\t)
\t\t(property "Footprint" "Capacitor_SMD:C_0805_2012Metric"
\t\t\t(at 102.5652 92.71 0)
\t\t)
\t\t(property "Description" "Bulk cap, X5R \\"16V\\" rated"
\t\t\t(at 101.6 88.9 0)
\t\t)
\t)
\t(symbol
\t\t(lib_id "power:GND")
\t\t(at 101.6 95.25 0)
\t\t(unit 1)
\t\t(in_bom no)
\t\t(on_board yes)
\t\t(property "Reference" "#PWR01"
\t\t\t(at 101.6 101.6 0)
\t\t)
\t\t(property "Value" "GND"
\t\t\t(at 101.6 99.06 0)
\t\t)
\t)
\t(wire
\t\t(pts
\t\t\t(xy 101.6 85.09) (xy 101.6 76.2)
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t)
)
"""

FP_LIB_TABLE = """\
(fp_lib_table
  (version 7)
  (lib (name "Connector_USB")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Connector_USB.pretty")(options "")(descr "USB connectors"))
  (lib (name "Resistor_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Resistor_SMD.pretty")(options "")(descr "Resistor SMD footprints"))
  (lib (name "project")(type "KiCad")(uri "${KIPRJMOD}/footprints/project.pretty")(options "")(descr "Footprints made for this board") (disabled))
)
"""

DUNE_LIB = """\
; build rules for the parser library
(library
 (name kara_parse)
 (public_name kara.parse)
 (libraries str unix
  ; menhir runtime for the generated parser
  menhirLib)
 (preprocess
  (pps ppx_deriving.show ppx_sexp_conv))
 (flags
  (:standard -w +a-4-40-42-44 -strict-sequence)))

(menhir
 (modules grammar)
 (flags --explain --table))

(ocamllex lexer)
"""

DUNE_PROJECT = """\
(lang dune 3.11)
(name kara)
(generate_opam_files true)
(source (github karalang/kara-ocaml))
(license BSD-2-Clause)
(authors "Kara contributors")
(package
 (name kara)
 (synopsis "Tools for the Kara language")
 (depends
  (ocaml (>= 4.14))
  (menhir (>= 20230608))
  (ppx_deriving :with-test)))
"""

ARCHIVE_CONTENTS = """\
(1
 (magit .
        [(20240301 1458)
         ((emacs (25 1)) (compat (29 1 4 4)) (dash (2 19 1)) (transient (0 5 0)) (with-editor (3 3 2)))
         "A Git porcelain inside Emacs." tar
         ((:commit . "fe0c8a2b") (:url . "https://github.com/magit/magit") (:keywords "git" "tools" "vc"))])
 (dash .
       [(20240103 1301)
        ((emacs (24)))
        "A modern list library for Emacs" tar
        ((:url . "https://github.com/magnars/dash.el") (:keywords "extensions" "lisp"))])
 (rainbow-delimiters .
                     [(20210515 1254)
                      nil
                      "Highlight brackets according to their depth" single
                      ((:url . "https://github.com/Fanael/rainbow-delimiters") (:keywords "faces" "convenience" "lisp" "tools"))]))
"""

CUSTOM_EL = """\
;;; custom.el --- written by Emacs's Customize
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 '(column-number-mode t)
 '(fill-column 80)
 '(indent-tabs-mode nil)
 '(package-selected-packages '(magit dash rainbow-delimiters))
 '(tab-width 4)
 '(user-mail-address "dev@example.org"))
(custom-set-faces
 '(default ((t (:family "Iosevka" :height 120)))))
"""

SMT = """\
; is there an x with 0 < x < 10 and 2x = 7?
(set-logic QF_LIA)
(declare-fun x () Int)
(assert (and (> x 0) (< x 10)))
(assert (= (* 2 x) 7))
(check-sat)
(get-model)
"""

SCHEME = """\
;; manifest.scm
(specifications->manifest
 (list "emacs" "git" "guile@3.0.9" "python-sexpdata"))
(define %load-hook #t)
(define-public answer #x2A)
"""

CORNERS = {
    "numbers.sexp": "(42 -7 +3 007 1_000 1__0 _1 1_ 0x10 1e3 1E-2 .5 5. -.5e+1 inf -inf +Infinity nan NaN 1e400 "
                    "123456789012345678901234567890 1.5e 1.2.3 \u0663\u0664 \u0661_\u0662 12\u00a0 \u00a034 -0 -0.0 1/2)",
    "strings.sexp": "(\"plain\" \"tab\\there\" \"line\\nbreak\" \"quote \\\" inside\" \"back\\\\slash\" \"bell\\a and \\q\" \"\" "
                    "\"multi\nline\" \"caf\u00e9 \u2603\" \"sem;colon\" \"paren(\")",
    "symbols.sexp": "(foo-bar :keyword &rest a.b . \\(x\\) with\\ space \\#hash ok? q\\?uery \\,comma back\\\\slash "
                    "#t #f #:kw sym\\q 1+ <= \u00e9t\u00e9)",
    "quotes.sexp": "('a '(1 2) '[x] ''b (f 'x y) ('a b c) '\"s\" '; comment after quote\n z)",
    "comments.sexp": "; leading comment\n(a ; trailing\n b ;; another\n c) ; last\n(d)",
    "brackets.sexp": "[1 (2 [3 4]) []] () [] (())",
    "atoms.sexp": "(nil t f nilly tt () (nil))",
    "adjacent.sexp": "(a\"b\"c(d)e[f]g)",
    "whitespace.sexp": "\t (\x0ba\x0cb\rc\r\n d )\n\n",
    "unicode-ws.sexp": "(a\u00a0b c\u2003d)",
    "comment-eof.sexp": "(x) ; no newline after this",
    "empty.sexp": "",
    "only-comment.sexp": ";; nothing here\n",
    "dotted.sexp": "((a . 1) (b . (2 3)) (c 4) (d . e . f) (. g) (h .) (i))",
    "deep.sexp": "(((((((((((deep)))))))))))",
}

BROKEN = {
    "unclosed.sexp": "(a (b c)",
    "unclosed-bracket.sexp": "[1 2",
    "mismatch.sexp": "(a b]",
    "mismatch2.sexp": "[a (b c])",
    "extra-close.sexp": "(a b))",
    "stray-close.sexp": ")",
    "quote-end.sexp": "(a ')",
    "quote-eof.sexp": "'",
    "quote-comment.sexp": "' ; nothing quoted\n",
    "string-open.sexp": "(\"never closed",
    "string-backslash.sexp": "\"ends with a backslash\\",
    "symbol-backslash.sexp": "abc\\",
    "two-top.sexp": "(a) (b)",
}

# Python values (as JSON) for the dump jobs
VALUES = {
    "config.json": {"name": "kara", "version": [1, 2, 0], "debug": False, "tags": ["a b", "c\"d"], "ratio": 0.25,
                    "nested": {"x": None, "y": True}},
    "list.json": [1, "two", 3.0, None, True, [], [[]], ["deep", ["er"]]],
    "string.json": "line one\nline \"two\"\tend\\",
    "number.json": 12345678901234567890,
    "float.json": 1e-7,
    "empty-list.json": [],
    "empty-dict.json": {},
}


def main():
    shutil.rmtree(DATA, ignore_errors=True)
    put("kicad/power.kicad_sch", KICAD_SCH)
    put("kicad/fp-lib-table", FP_LIB_TABLE)
    put("dune/lib/dune", DUNE_LIB)
    put("dune/dune-project", DUNE_PROJECT)
    put("emacs/archive-contents", ARCHIVE_CONTENTS)
    put("emacs/custom.el", CUSTOM_EL)
    put("smt/query.smt2", SMT)
    put("guix/manifest.scm", SCHEME)
    for name, text in CORNERS.items():
        put("corner/" + name, text)
    for name, text in BROKEN.items():
        put("broken/" + name, text)
    for name, v in VALUES.items():
        put("values/" + name, json.dumps(v))

    jobs = []
    real = ["kicad/power.kicad_sch", "kicad/fp-lib-table", "dune/lib/dune", "dune/dune-project",
            "emacs/archive-contents", "emacs/custom.el", "smt/query.smt2", "guix/manifest.scm"]
    for f in real + ["corner/" + n for n in sorted(CORNERS)] + ["broken/" + n for n in sorted(BROKEN)]:
        jobs.append(["parse", f])
    for f in ["kicad/power.kicad_sch", "emacs/archive-contents", "corner/brackets.sexp", "corner/numbers.sexp",
              "broken/two-top.sexp", "corner/empty.sexp"]:
        jobs.append(["loads", f])
    jobs += [
        ["parse", "guix/manifest.scm", "nil=()", "true=#t", "false=#f"],
        ["parse", "corner/atoms.sexp", "nil=", "true=tt", "false=f"],
        ["parse", "corner/atoms.sexp", "true=nil"],
        ["parse", "corner/strings.sexp", "string_to=Symbol"],
        ["parse", "corner/strings.sexp", "string_to=String"],
        ["parse", "corner/comments.sexp", "line_comment=#"],
        ["parse", "guix/manifest.scm", "line_comment=#"],
    ]
    for f in real + ["corner/" + n for n in ["numbers.sexp", "strings.sexp", "symbols.sexp", "quotes.sexp",
                                             "brackets.sexp", "dotted.sexp", "deep.sexp", "atoms.sexp"]]:
        jobs.append(["roundtrip", f])
    jobs += [
        ["roundtrip", "dune/lib/dune", "pretty_print"],
        ["roundtrip", "emacs/archive-contents", "pretty_print", "indent_as=\\t"],
        ["roundtrip", "corner/deep.sexp", "pretty_print", "indent_as=."],
        ["roundtrip", "corner/brackets.sexp", "pretty_print"],
        ["roundtrip", "corner/quotes.sexp", "pretty_print"],
        ["roundtrip", "corner/strings.sexp", "str_as=symbol"],
        ["roundtrip", "corner/atoms.sexp", "true_as=#t", "false_as=#f", "none_as=nil"],
    ]
    for name in sorted(VALUES):
        jobs.append(["dumps", "values/" + name])
    jobs += [
        ["dumps", "values/config.json", "str_as=symbol"],
        ["dumps", "values/config.json", "pretty_print"],
        ["dumps", "values/list.json", "pretty_print", "indent_as=    "],
        ["dumps", "values/list.json", "false_as=nil", "true_as=T", "none_as=NIL"],
        ["dumps", "values/list.json", "str_as=keyword"],
        ["dumps", "values/list.json", "tuple_as=array"],
        ["dumps", "values/config.json", "tuple_as=vector"],
        ["carcdr", "corner/dotted.sexp"],
        ["carcdr", "emacs/archive-contents"],
        ["bom", "kicad/power.kicad_sch"],
        ["libs", "kicad/fp-lib-table"],
        ["deps", "dune/lib/dune"],
        ["deps", "dune/dune-project"],
        ["packages", "emacs/archive-contents"],
        ["customs", "emacs/custom.el"],
        ["smt", "smt/query.smt2"],
    ]
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as f:
        for j in jobs:
            f.write("\t".join(j) + "\n")


main()
