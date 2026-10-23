"""Write data/jobs.tsv, the style sheets the jobs minify, and the patterns.

rcssmin is the CSS minifier that webassets, django-compressor style
pipelines and static-site builds call to shrink style sheets before they
are served. Its test inputs (its own, and the ones it took from the YUI
compressor suite) are copied from vendor/tests into data/css, and the
snippets below add the cases a real sheet runs into: CRLF and form-feed
line ends, non-ASCII text, data: URLs with spaces, the Mac IE5 and IE7
comment hacks, and @-rules. data/site is a small site for the bundle
program, and data/pages holds a sheet with CRLF line ends for the
command.

data/patterns.txt holds the regular expressions the minifier builds in
_make_cssmin, read out of the vendored library's closures so the port
compiles the same patterns: one `<name> <flags> <hex of the pattern>` a
line.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, os.path.join(HERE, "vendor"))

import rcssmin  # noqa: E402


def closure(fn):
    return dict(zip(fn.__code__.co_freevars,
                    (c.cell_contents for c in fn.__closure__)))


_outer = closure(rcssmin._make_cssmin(python_only=True))
_inner = closure(_outer["main_subber"])
PATTERN_NAMES = ["main_sub", "space_sub_simple", "space_sub_banged",
                 "uri_data_plain", "uri_space_sub", "nl_unesc_sub",
                 "post_esc_sub"]
PATTERNS = []
for _name in PATTERN_NAMES:
    _fn = _outer.get(_name) or _inner[_name]
    PATTERNS.append((_name, _fn.__self__))

FILES = {}
TESTS = []
for sub in ("main", "yui"):
    for name in sorted(os.listdir(os.path.join(HERE, "vendor", "tests", sub))):
        with open(os.path.join(HERE, "vendor", "tests", sub, name),
                  encoding="utf-8", newline="") as fh:
            FILES["css/%s/%s" % (sub, name)] = fh.read()
        TESTS.append("%s/%s" % (sub, name))

FILES["pages/crlf.css"] = (
    "/* a sheet saved on Windows */\r\n"
    "body {\r\n    margin : 0 ;\r\n    color : #333 ;\r\n}\r\n"
    "\r\n"
    "a:hover ,\r\na:focus {\r\n    text-decoration : underline ;\r\n}\r\n"
    ".note::before { content : \"line one\\\r\nline two\" ; }\r\n"
    "/*! licence: keep me */\r\n"
    "@media print {\r\n    a[href]::after { content : \" (\" attr(href) \")\" ; }\r\n}\r\n"
)
FILES["pages/theme.css"] = """\
/*!
 * theme.css v2.1 (MIT)
 */
:root {
    --brand : #0055aa ;
    --gap   : calc( 1rem + 2px ) ;
}

/* layout */
.card , .panel
{
    padding : var( --gap ) ;
    border  : 1px solid rgba( 0 , 0 , 0 , .1 ) ;
    background : url( "/img/card bg.png" ) no-repeat ;
}

.card > .title:first-letter { font-size : 2em ; }

@supports ( display : grid ) {
    .grid { display : grid ; grid-template-columns : repeat( 3 , 1fr ) ; }
}

@-webkit-keyframes spin { from { -webkit-transform : rotate( 0deg ) } to { -webkit-transform : rotate( 360deg ) } }
@keyframes spin { from { transform : rotate( 0deg ) } to { transform : rotate( 360deg ) } }

.icon { background-image : url( 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg"></svg>' ) ; }
.badge::after { content : "\\2713  done" ; color : green !important ; }
"""

SITE = {
    "reset.css": """\
/* reset */
html , body , h1 , p { margin : 0 ; padding : 0 ; }
*, *::before, *::after { box-sizing : border-box ; }
""",
    "layout.css": """\
/*! layout.css */
.wrap { max-width : 60rem ; margin : 0 auto ; }
@media ( max-width : 40rem ) {
    .wrap { padding : 0 1rem ; }
    .sidebar { display : none ; }
}
""",
    "print.css": """\
@media print {
    nav , .sidebar , footer { display : none !important ; }
    a::after { content : " <" attr( href ) ">" ; }
}
""",
    "fonts.css": """\
@font-face {
    font-family : "Body Text" ;
    src : url( "/fonts/body text.woff2" ) format( "woff2" ) ,
          url( /fonts/body.woff ) format( "woff" ) ;
}
""",
}
for _n, _t in SITE.items():
    FILES["site/css/" + _n] = _t
FILES["site/manifest.txt"] = """\
# bundle order: each line is a sheet and its flags
reset.css
layout.css bang
fonts.css
missing.css
print.css bang
"""
FILES["site/out/.keep"] = ""

SNIPPETS = [
    "a { color : red ; }",
    "a{color:red;;;}",
    "a { color : red ; } ; b { }",
    "  /* lead */  a { b : c }  ",
    "a { b : c } /* trailing */",
    "/* only a comment */",
    "",
    "   \\t\\n  ",
    "a /* x */ b { c : d }",
    "a/* x */b{c:d}",
    "/*! keep */ a { b : c }",
    "/*!keep*/a{b:c}/* drop */",
    "/* \\\\*/ .mac { color : red } /* */ .all { color : blue }",
    "/*\\\\*/.mac{a:b}/**/.x{c:d}",
    "/*! a *//*! b */ a { }",
    "a > /**/ b { c : d }",
    "html >/**/ body { color : red }",
    ".x { a : b ; } html>/**/body .y { c : d }",
    "a:first-line , b:first-letter { x : y }",
    "a:FIRST-LINE{x:y}",
    "p:first-letter /* c */ { x : y }",
    "a:first-lines { x : y }",
    "@media screen and ( max-width : 100px ) { a { b : c } }",
    "@MEDIA print{a{b:c}}",
    "@supports ( display : flex ) { a { display : flex } }",
    "@-webkit-keyframes x { from { a : b } to { a : c } }",
    "@-moz-keyframes x{0%{a:b}}",
    "@keyframes x { 50% { a : b } }",
    "@keyframesx { a : b }",
    "@import url( foo.css ) screen ;",
    "@charset \"utf-8\" ; a { }",
    "@font-face { font-family : x ; src : url( a.woff ) }",
    "@page :first { margin : 1in }",
    "a::before { content : \"a  b\" }",
    "a::before { content : 'it''s' }",
    "a::before { content : \"say \\\\\"hi\\\\\"\" }",
    "a::before { content : \"one\\\\\\ntwo\" }",
    "a::before { content : 'one\\\\\\r\\ntwo' }",
    "a::before { content : \"open",
    "a { background : url( foo.png ) }",
    "a { background : url(  \"foo bar.png\"  ) }",
    "a { background : url( 'foo.png' ) }",
    "a { background : url( foo\\\\ bar.png ) }",
    "a { background : url( a b c ) }",
    "a { background : url( \"data:image/png;base64,iVBO Rw0K\" ) }",
    "a { background : url( 'data:image/svg+xml,<svg a=\"1\"> </svg>' ) }",
    "a { background : url( \"data:text/plain;charset=utf-8,a b\" ) }",
    "a { background : url( data:image/gif;base64,R0lG ODlh ) }",
    "a { background : url( \"DATA:image/png;BASE64,AA AA\" ) }",
    "a { b : myurl( x y ) }",
    "a { b : -url( x ) }",
    "a { b : \\\\75 rl( x ) }",
    "a { margin : 0 0 0 0 ; padding : 0px }",
    "a { width : calc( 100% - 2 * 10px ) }",
    "a { width : calc( 1px+2px ) }",
    "a { color : red ! important }",
    "a , b , c { d : e }",
    "a + b ~ c > d { e : f }",
    "a[ href = \"x\" ] { b : c }",
    "a:not( .b ) { c : d }",
    "a:hover { b : c } a : hover { b : c }",
    ".a\\\\:b { c : d }",
    ".\\\\31 0 { c : d }",
    ".x\\\\\\n y { }",
    "#\\\\#id { }",
    "a\\\\\\t b { }",
    "\\\\e9 t\\\\e9  { }",
    ".café , .naïve { content : \"日本 語\" }",
    "a { b : c }\\r\\nd { e : f }\\r\\n",
    "a\\f{\\fb\\f:\\fc\\f}",
    "a\\r{\\rb:c\\r}",
    "a { b : c ;\\n}\\n\\n\\nd { e : f }",
    "a{b:c}/*",
    "a { b : c } /* unclosed",
    "a{} b{} c{}",
    "{ } ;",
    "a { b : c d e }",
    "a { font : 12px / 1.5 \"Helvetica Neue\" , Arial , sans-serif }",
    "a { filter : progid:DXImageTransform.Microsoft.Alpha( Opacity = 80 ) }",
    "* html a { _height : 1px ; *zoom : 1 }",
    "a { b : c ; } @media x { d { e : f ; } } g { h : i ; }",
    "@media x { @media y { a { b : c ; } } }",
    "a { --x : { b : c } ; }",
    "a{b:c;}\\u2028d{e:f}",
    "a { b : \\u00a0c }",
]

BANG_SNIPPETS = {
    "/*! keep */ a { b : c }", "/*!keep*/a{b:c}/* drop */",
    "/* \\\\*/ .mac { color : red } /* */ .all { color : blue }",
    "/*\\\\*/.mac{a:b}/**/.x{c:d}", "/*! a *//*! b */ a { }",
    "html >/**/ body { color : red }", "a > /**/ b { c : d }",
    "/* only a comment */", "  /* lead */  a { b : c }  ",
}

BYTES = [
    "a { content : \"\\u00e9t\\u00e9\" }",
    "/*! \\u00a9 2024 */ b { c : d }",
]

CLI = [
    ["pages/theme.css"],
    ["-b", "pages/theme.css"],
    ["-p", "pages/theme.css"],
    ["-bp", "pages/crlf.css"],
    ["-pb", "pages/crlf.css"],
    ["pages/crlf.css"],
    ["-x", "-b", "css/main/comment_00.css"],
]


def esc(s):
    return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")


def main():
    for name, text in FILES.items():
        path = os.path.join(DATA, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
    with open(os.path.join(DATA, "patterns.txt"), "w", encoding="utf-8") as fh:
        for name, rx in PATTERNS:
            fh.write("%s %d %s\n" % (name, rx.flags,
                                     rx.pattern.encode("utf-8").hex()))
    jobs = []
    jobs.append("# the library's test inputs")
    for name in TESTS:
        jobs.append("file\tcss/" + name)
        jobs.append("file\tcss/" + name + "\tbang")
    jobs.append("# snippets")
    for css in SNIPPETS:
        jobs.append("snippet\t" + css)
        if css in BANG_SNIPPETS:
            jobs.append("snippet\t" + css + "\tbang")
    jobs.append("# bytes in, bytes out")
    for css in BYTES:
        jobs.append("bytes\t" + css)
        jobs.append("bytes\t" + css + "\tbang")
    jobs.append("# the rcssmin command")
    for args in CLI:
        jobs.append("\t".join(["cli"] + args))
    jobs.append("# programs")
    jobs.append("bundle\tsite/manifest.txt\tout/site.min.css")
    jobs.append("bundle\tsite/nope.txt\tout/nope.min.css")
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(jobs) + "\n")
    files = ["patterns.txt"] + sorted(FILES)
    with open(os.path.join(DATA, "files.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(files) + "\n")


main()
