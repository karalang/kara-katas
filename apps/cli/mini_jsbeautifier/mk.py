"""Writes data/jobs.txt: the beautify() calls jsbeautifier's own test suite
makes (vendor/jsbeautifier/tests/generated/tests.py), recorded with their
options, one in seven of them plus the first call of every distinct set of
options, and a few hand-written programs.

Run from this directory: python3 -s -P -B mk.py"""
import os
import sys
import types
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

# The unpackers (eval-packed and obfuscated scripts) are not vendored; every
# call passes its source through unchanged, as unpack() does when no
# unpacker detects the input.
stub = types.ModuleType("jsbeautifier.unpackers")


class UnpackingError(Exception):
    pass


stub.UnpackingError = UnpackingError
stub.run = lambda source, evalcode=False: source
sys.modules["jsbeautifier.unpackers"] = stub

import jsbeautifier  # noqa: E402

FIELDS = [
    "disabled", "eol", "end_with_newline", "indent_size", "indent_char", "indent_level",
    "preserve_newlines", "max_preserve_newlines", "indent_with_tabs", "wrap_line_length",
    "max_char", "indent_empty_lines", "templating", "brace_style", "unindent_chained_methods",
    "break_chained_methods", "space_in_paren", "space_in_empty_paren", "jslint_happy",
    "space_after_anon_function", "space_after_named_function", "keep_array_indentation",
    "space_before_conditional", "unescape_strings", "e4x", "comma_first", "operator_position",
]


# Code points written as \u{hex}: the ASCII controls and the Unicode
# separators, format characters and non-characters the jobs hold (the same
# rule as shown_escaped() in the port).
def shown_escaped(ch):
    n = ord(ch)
    return (n < 0x20 or n == 0x7F or 0x80 <= n < 0xA0 or n == 0xA0 or n == 0xAD or n == 0x1680 or n == 0x180E
            or 0x2000 <= n <= 0x200F or 0x2028 <= n <= 0x202F or 0x205F <= n <= 0x206F or n == 0x3000
            or n == 0xFEFF or 0xFFF0 <= n <= 0xFFFF or 0xD800 <= n <= 0xF8FF or n >= 0xE0000)


def esc(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == "\\":
            out.append("\\\\")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif shown_escaped(ch):
            out.append("\\u{%x}" % o)
        else:
            out.append(ch)
    return "".join(out)


def value(v):
    if isinstance(v, bool):
        return "b " + ("1" if v else "0")
    if isinstance(v, int):
        return "i %d" % v
    if isinstance(v, str):
        return "s " + esc(v)
    if isinstance(v, (list, tuple)):
        return "l " + esc(",".join(v))
    return None


def options_lines(opts):
    lines = []
    if opts is None:
        return lines
    if isinstance(opts, tuple):
        opts = dict(opts)
    if isinstance(opts, dict):
        items = list(opts.items())
    else:
        d = vars(opts)
        items = [(k, d[k]) for k in d if k in FIELDS or "-" in k or k == "js"]
    for k, v in items:
        if k == "js":
            if isinstance(v, dict):
                for ck, cv in v.items():
                    val = value(cv)
                    if val is not None:
                        lines.append("o js." + ck + " " + val)
            continue
        if k not in FIELDS and "-" not in k:
            continue
        val = value(v)
        if val is not None:
            lines.append("o " + k + " " + val)
    return lines


calls = []
orig = jsbeautifier.beautify


def record(src, opts=None):
    calls.append(("\n".join(options_lines(opts)), src or ""))
    return orig(src, opts)


jsbeautifier.beautify = record
from jsbeautifier.tests.generated import tests  # noqa: E402

suite = unittest.TestLoader().loadTestsFromModule(tests)
result = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, "w")).run(suite)
for t, e in result.failures + result.errors:
    print(t, e[-1500:])
if result.failures or result.errors:
    sys.exit("the upstream suite failed under the recorder")
jsbeautifier.beautify = orig

seen = set()
distinct = []
for c in calls:
    if c not in seen:
        seen.add(c)
        distinct.append(c)

# A source the port cannot hold: a lone surrogate.
def holdable(s):
    return not any(0xD800 <= ord(ch) <= 0xDFFF for ch in s)


chosen = []
option_sets = set()
for i, (o, s) in enumerate(distinct):
    if not holdable(s):
        continue
    if i % 7 == 0 or o not in option_sets:
        chosen.append((o, s))
    option_sets.add(o)

# Hand-written programs, each under a few option sets.
PROGRAMS = [
    # A minified module the way a bundler emits it.
    '!function(e,t){"object"==typeof exports&&"undefined"!=typeof module?module.exports=t():"function"=='
    'typeof define&&define.amd?define(t):(e=e||self).Cart=t()}(this,function(){"use strict";var e=functi'
    'on(e,t){return e.qty*e.price+(t||0)};function t(t,n){var r=0;for(var o=0;o<t.length;o++)r+=e(t[o]);'
    'return n?Math.round(r*(1+n.rate)*100)/100:r}return{total:t,line:e,version:"1.4.2"}});',
    # An event handler with a template literal, a regexp and an arrow chain.
    'document.querySelectorAll(".row").forEach(r=>{r.addEventListener("click",async ev=>{const id=r.datas'
    'et.id;if(!/^[a-z0-9-]{8,}$/i.test(id))return;const res=await fetch(`/api/items/${id}?expand=owner`,'
    '{headers:{Accept:"application/json"}});if(res.ok){const {name,owner:{email}}=await res.json();r.quer'
    'ySelector(".name").textContent=name;console.log(`${name} <${email}>`)}else{throw new Error("HTTP "+r'
    'es.status)}})});',
    # A class with getters, a generator, a switch and a labelled loop.
    'class Queue extends Base{constructor(n){super();this.items=[];this.limit=n}get size(){return this.it'
    'ems.length}*drain(){while(this.items.length)yield this.items.shift()}push(x){switch(typeof x){case"n'
    'umber":x={v:x};break;case"string":x={v:x,s:true};default:if(x==null)throw new TypeError("no item")}o'
    'uter:for(let i=0;i<this.items.length;i++){for(const k in x){if(this.items[i][k]===x[k])continue oute'
    'r}}this.items.length<this.limit?this.items.push(x):this.items.splice(0,1,x);return this}}',
    # Comments of each kind, a directive and a preserved block.
    '/* config loader */\n// read once\nvar cfg = {   a:1,\n\n\n  b : [1,2,\n3],   c: { d: null } } ; /*'
    ' beautify preserve:start */\nvar   keep   =   { x:1 };\n/* beautify preserve:end */\nfunction load(  )'
    ' {   /**\n   * Loads it.\n   * @returns {object}\n   */\n  return cfg   }',
]
PROGRAM_OPTIONS = [
    [],
    ["o indent_size i 2", "o brace_style s expand"],
    ["o indent_with_tabs b 1", "o space_in_paren b 1", "o jslint_happy b 1"],
    ["o wrap_line_length i 60", "o break_chained_methods b 1", "o comma_first b 1",
     "o operator_position s after-newline"],
    ["o brace_style s collapse,preserve-inline", "o preserve_newlines b 0", "o end_with_newline b 1",
     "o eol s \\\\r\\\\n"],
]
for p in PROGRAMS:
    for o in PROGRAM_OPTIONS:
        chosen.append(("\n".join(o), p))

sets = []
set_ids = {}
for o, s in chosen:
    if o not in set_ids:
        set_ids[o] = len(sets) + 1
        sets.append(o)

os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
with open(os.path.join(HERE, "data", "jobs.txt"), "w", encoding="utf-8", newline="\n") as f:
    for n, o in enumerate(sets):
        f.write("set %d\n" % (n + 1))
        if o:
            f.write(o + "\n")
    for n, (o, s) in enumerate(chosen):
        f.write("job %d %d\n" % (n + 1, set_ids[o]))
        f.write("in " + esc(s) + "\n")
print("%d calls, %d distinct, %d option sets, %d jobs" % (len(calls), len(distinct), len(sets), len(chosen)))
