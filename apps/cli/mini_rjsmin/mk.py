"""Write data/jobs.tsv, the scripts the jobs minify, and the patterns.

rJSmin is the JavaScript minifier Python web stacks (django-compressor,
webassets, Flask-Assets) call to shrink scripts before serving them. Its
test scripts are copied from vendor/tests into data/js, and two of the
real-world scripts from its benchmark set (Django admin's calendar
widget and Google's MarkerManager, each under its own licence header)
into data/bench. The snippets below add the cases scripts run into:
regular expressions after `)` and `return`, `+ +` and `- -`, template
literals, line continuations, unterminated literals, bang comments,
CRLF and other line ends, and non-ASCII text. data/site is a small site
for the bundle program, and data/pages a script with CRLF line ends for
the command.

data/patterns.txt holds the regular expressions the minifier builds in
_make_jsmin, read out of the vendored library's closures, and the two
literal patterns of jsmin_for_posers, so the port compiles the same
patterns: one `<name> <flags> <hex of the pattern>` a line.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, os.path.join(HERE, "vendor"))

import rjsmin  # noqa: E402


def closure(fn):
    return dict(zip(fn.__code__.co_freevars,
                    (c.cell_contents for c in fn.__closure__)))


_outer = closure(rjsmin._make_jsmin(python_only=True))
_banged_subber = _outer["banged"].args[0]
_keep = closure(_banged_subber)["keep"].__self__


def _posers_patterns():
    """The `rex` literals of jsmin_for_posers, one per branch."""
    consts = rjsmin.jsmin_for_posers.__code__.co_consts
    found = [c for c in consts if isinstance(c, str) and c.startswith("([^")]
    keep = [c for c in consts if isinstance(c, str) and c.startswith("[\\000")]
    assert len(found) == 2 and len(keep) == 1, (len(found), len(keep))
    return found[0], found[1], keep[0]


_p_simple, _p_banged, _p_keep = _posers_patterns()
PATTERNS = [
    ("space_sub_simple", _outer["simple"].func.__self__.pattern,
     _outer["simple"].func.__self__.flags),
    ("space_sub_banged", _outer["banged"].func.__self__.pattern,
     _outer["banged"].func.__self__.flags),
    ("keep", _keep.pattern, _keep.flags),
    ("posers_simple", _p_simple, re.compile(_p_simple).flags),
    ("posers_banged", _p_banged, re.compile(_p_banged).flags),
    ("posers_keep", _p_keep, re.compile(_p_keep).flags),
]

FILES = {}
TESTS = []
for name in sorted(os.listdir(os.path.join(HERE, "vendor", "tests", "js"))):
    with open(os.path.join(HERE, "vendor", "tests", "js", name),
              encoding="utf-8", newline="") as fh:
        FILES["js/" + name] = fh.read()
    TESTS.append("js/" + name)
for name in ("DateTimeShortcuts.js", "markermanager.js"):
    with open(os.path.join(HERE, "vendor", "bench", name),
              encoding="utf-8", newline="") as fh:
        FILES["bench/" + name] = fh.read()
    TESTS.append("bench/" + name)

FILES["pages/crlf.js"] = (
    "/*! app.js (c) 2024 Example, MIT */\r\n"
    "'use strict';\r\n"
    "\r\n"
    "// read the settings\r\n"
    "var settings = {\r\n    debug : false ,\r\n    retries : 3\r\n} ;\r\n"
    "function retry ( fn , n ) {\r\n"
    "    for ( var i = 0 ; i < n ; i ++ ) {\r\n"
    "        try { return fn ( ) ; } catch ( e ) { /* again */ }\r\n"
    "    }\r\n"
    "    return null ;\r\n"
    "}\r\n"
    "var msg = \"line one \\\r\nline two\" ;\r\n"
)

SITE = {
    "vendor.js": """\
/*! tiny-dom 1.0 | MIT */
(function ( root ) {
    var $ = function ( sel ) { return document.querySelectorAll( sel ) ; } ;
    root.$ = $ ;
}) ( this ) ;
""",
    "util.js": """\
// helpers
function slug ( s ) {
    return s.toLowerCase ( )
            .replace ( /[^a-z0-9]+/g , '-' )
            .replace ( /^-|-$/g , '' ) ;
}
function pad ( n , w ) {
    var s = '' + n ;
    while ( s.length < w ) s = '0' + s ;
    return s ;
}
""",
    "app.js": """\
/* main entry */
var count = 0 ;
document.addEventListener ( 'click' , function ( ev ) {
    count = count + + 1 ;
    var label = `clicked ${ count } times` ;
    if ( /^btn-/.test ( ev.target.id ) ) console.log ( label ) ;
} ) ;
""",
}
for _n, _t in SITE.items():
    FILES["site/js/" + _n] = _t
FILES["site/manifest.txt"] = """\
# bundle order: each line is a script and its flags
vendor.js bang
util.js
missing.js
app.js
"""
FILES["site/out/.keep"] = ""

SNIPPETS = [
    "var a = 1 ;",
    "var  a  =  1 ;  var b = 2",
    "a = b\\nc = d",
    "a = b\\n\\n\\nc = d",
    "a = b ;\\n  // comment\\n  c = d",
    "if ( a ) {\\n  b ( ) ;\\n}\\nelse {\\n  c ( ) ;\\n}",
    "a = b + + c ; d = e - - f ; g = h + ++i ; j = k - --l",
    "a = b++ + c ; d = e-- - f",
    "a = b / c / d",
    "a = b / c ; d = /re/g.test ( x )",
    "x = ( 1 ) / 2 / 3",
    "x = foo ( ) /bar/i",
    "x = ( a ) /b/.source",
    "x = [ /a/ , /b/ ]",
    "return /x/",
    "return\\n/x/",
    "  return  /x/g  ;",
    "function f ( ) { return /*! keep */ /x/ }",
    "a = ! b ; c = !\\n d",
    "a\\n!b",
    "a\\n+b\\nc\\n-d",
    "a\\n(b)",
    "a\\n[b]",
    "a\\n{b}",
    "a = \"x  y\" + 'p  q' + `t  ${ v }  u`",
    "a = 'it\\\\'s' ; b = \"say \\\\\"hi\\\\\"\"",
    "a = \"one \\\\\\ntwo\"",
    "a = 'one \\\\\\r\\ntwo'",
    "a = `multi\\nline  template`",
    "a = \"unterminated",
    "a = 'unterminated\\nb = 1",
    "a = /unterminated",
    "a = 1 /* unterminated",
    "a = 1 /*! unterminated bang",
    "/* only a comment */",
    "/*! only a bang comment */",
    "// only a line comment",
    "",
    "   \\t\\n  ",
    "/*! one */ /*! two */ a ( )",
    "a ( ) ; /*! mid */ b ( )",
    "a /*! inline */ = 1",
    "x = a /* c */ / b",
    "x = a/*c*/+/*d*/b",
    "x = [ 1 , 2 , 3 , ] ;",
    "x = { a : 1 , 'b' : 2 } ;",
    "for ( var i = 0 ; i < 10 ; i ++ ) { }",
    "x = a ? b : c",
    "x = typeof a === 'undefined'",
    "x = a instanceof B",
    "x = new Date ( ) . getTime ( )",
    "label : for ( ; ; ) break label",
    "x = 1.5e-3 + .5 + 0x1F",
    "x = a.b.c ( d ) [ e ]",
    "x = /[/]/.test ( s )",
    "x = /a\\\\/b/",
    "x = s.replace ( /\\\\s+/g , ' ' )",
    "if ( /^\\\\d+$/.test ( s ) ) n = + s",
    "a = b\\r\\nc = d\\r\\n",
    "a = b\\rc = d",
    "a = b\\fc\\u000bd",
    "a = b\\u2028c = d",
    "a = 'caf\\u00e9' ; \\u00e9t\\u00e9 = 1",
    "var \\u03c0 = 3.14 ; x = \\u03c0 * 2",
    "a = b\\u00a0+ c",
    "x = a\\n++b",
    "x = a\\n--b",
    "x = a++\\nb",
    "x = 'a' in b",
    "x = $ ( '#id' ) . hide ( )",
    "_a = $b + _c",
    "x = ( ) => { return 1 }",
    "async function f ( ) { await g ( ) }",
    "x = a <!-- b",
    "x = </script>",
    "/",
    "x = a / /b/",
]

BANG_SNIPPETS = {
    "function f ( ) { return /*! keep */ /x/ }",
    "/*! only a bang comment */",
    "/*! one */ /*! two */ a ( )",
    "a ( ) ; /*! mid */ b ( )",
    "a /*! inline */ = 1",
    "a = 1 /*! unterminated bang",
    "a = ( 1 ) /*! k */\\n/x/.test ( y )",
    "x = [ /*! k */ /a/ ]",
    "return /*! k */\\n/x/\\n/*! after */",
}

BYTES = [
    "a = 'caf\\u00e9' ;",
    "/*! \\u00a9 2024 */ b ( )",
]

CLI = [
    ["pages/crlf.js"],
    ["-b", "pages/crlf.js"],
    ["-p", "pages/crlf.js"],
    ["-bp", "pages/crlf.js"],
    ["-pb", "js/basic.js"],
    ["-x", "js/issue8.js"],
]

POSERS = ["js/basic.js", "js/issue13.js", "pages/crlf.js",
          "bench/DateTimeShortcuts.js"]


def main():
    for name, text in FILES.items():
        path = os.path.join(DATA, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
    with open(os.path.join(DATA, "patterns.txt"), "w", encoding="utf-8") as fh:
        for name, pattern, flags in PATTERNS:
            fh.write("%s %d %s\n" % (name, flags,
                                     pattern.encode("utf-8").hex()))
    jobs = []
    jobs.append("# the library's test scripts, and two real ones")
    for name in TESTS:
        jobs.append("file\t" + name)
        jobs.append("file\t" + name + "\tbang")
    jobs.append("# snippets")
    for js in SNIPPETS:
        jobs.append("snippet\t" + js)
        if js in BANG_SNIPPETS:
            jobs.append("snippet\t" + js + "\tbang")
    for js in sorted(BANG_SNIPPETS - set(SNIPPETS)):
        jobs.append("snippet\t" + js)
        jobs.append("snippet\t" + js + "\tbang")
    jobs.append("# bytes in, bytes out")
    for js in BYTES:
        jobs.append("bytes\t" + js)
        jobs.append("bytes\t" + js + "\tbang")
    jobs.append("# jsmin_for_posers, the same minifier as two literal patterns")
    for name in POSERS:
        jobs.append("posers\t" + name)
        jobs.append("posers\t" + name + "\tbang")
    jobs.append("# the rjsmin command")
    for args in CLI:
        jobs.append("\t".join(["cli"] + args))
    jobs.append("# programs")
    jobs.append("bundle\tsite/manifest.txt\tout/site.min.js")
    jobs.append("bundle\tsite/nope.txt\tout/nope.min.js")
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(jobs) + "\n")
    files = ["patterns.txt"] + sorted(FILES)
    with open(os.path.join(DATA, "files.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(files) + "\n")


main()
