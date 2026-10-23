"""Replay data/jobs.tsv against the vendored htmlmin 0.1.12.

`minify` runs htmlmin.minify over a page with a set of options, `snippet`
over a short document written in the job, and `chunks` feeds a page to
one Minifier in pieces of a given size before finalize(). `attr_value`,
`ambiguous`, `unescape` and `escape_tag` call the escaping helpers. `cli`
runs the htmlmin command with the given arguments, and `site` is a build
step that minifies the pages a manifest lists into an output tree and
reports the bytes saved. A minified document prints one `|` line per
line; a job that raises prints `error <class>: <message>`.

htmlmin imports the cgi module, which Python 3.13 removed, without using
it, so an empty module stands in for it. Its log messages go to stdout
as `log <level> <message>` lines, where they happen.
"""
import logging
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.modules.setdefault("cgi", type(sys)("cgi"))

logging.basicConfig(stream=sys.stdout, format="  log %(levelname)s %(message)s")

import htmlmin  # noqa: E402
from htmlmin import command, escape  # noqa: E402
from htmlmin.python3html import unescape  # noqa: E402


def out(s):
    print("  " + s)


def unesc(s):
    """Job text uses \\t, \\n, \\\\ and \\uXXXX escapes."""
    res = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            if n == "t":
                res.append("\t")
            elif n == "n":
                res.append("\n")
            elif n == "u":
                res.append(chr(int(s[i + 2:i + 6], 16)))
                i += 4
            else:
                res.append(n)
            i += 2
            continue
        res.append(c)
        i += 1
    return "".join(res)


def options(fields):
    kw = {}
    for f in fields:
        key, _, v = f.partition("=")
        if key == "keep_quotes":
            kw["remove_optional_attribute_quotes"] = False
        elif key == "charrefs":
            kw["convert_charrefs"] = v == "1"
        elif key == "reduce_empty_attributes":
            kw[key] = v == "1"
        elif key == "pre_tags":
            kw[key] = tuple(t for t in v.split(",") if t)
        elif key == "pre_attr":
            kw[key] = v
        else:
            kw[key] = True
    return kw


def show(html):
    for line in html.split("\n"):
        print("  | " + line)


def read_text(name):
    path = os.path.join("data", name)
    if not os.path.exists(path):
        raise OSError("cannot read %s" % name)
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def page(name):
    return read_text("pages/%s.html" % name)


def cmd_minify(f):
    text = page(f[0])
    result = htmlmin.minify(text, **options(f[1:]))
    out("%d -> %d chars" % (len(text), len(result)))
    show(result)


def cmd_snippet(f):
    show(htmlmin.minify(unesc(f[0]), **options(f[1:])))


def cmd_chunks(f):
    text = page(f[0])
    size = int(f[1])
    kw = options(f[2:])
    m = htmlmin.Minifier(**kw)
    m.input(*[text[k:k + size] for k in range(0, len(text), size)])
    result = m.finalize()
    out("same as one call: %s" % (result == htmlmin.minify(text, **kw)))
    show(result)
    # finalize() resets the parser, so the Minifier is ready for the next page
    out("reused: %r" % m.minify("<p>  again  </p>"))


def cmd_attr_value(f):
    v, q = escape.escape_attr_value(unesc(f[0]), double_quote=f[1] == "1")
    out("%r %d" % (v, q))


def cmd_ambiguous(f):
    out("%r" % escape.escape_ambiguous_ampersand(unesc(f[0])))


def cmd_unescape(f):
    out("%r" % unescape(unesc(f[0])))


def cmd_escape_tag(f):
    out("%r" % escape.escape_tag(unesc(f[0])))


def cmd_cli(f):
    saved = sys.argv
    sys.argv = ["htmlmin"] + f
    os.chdir("data")
    try:
        command.main()
    finally:
        os.chdir(HERE)
        sys.argv = saved
    show(read_text(f[-1]))


def cmd_site(f):
    total_in = total_out = 0
    for line in read_text(f[0]).split("\n"):
        if not line or line.startswith("#"):
            continue
        fields = line.split(" ")
        name = fields[0]
        try:
            text = read_text("site/src/" + name)
        except OSError as e:
            out("%s skipped: %s" % (name, e))
            continue
        result = htmlmin.minify(text, **options(fields[1:]))
        dest = os.path.join("data", "site", "out", name)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8", newline="") as fh:
            fh.write(result)
        size_in = len(text.encode("utf-8"))
        size_out = len(read_text("site/out/" + name).encode("utf-8"))
        total_in += size_in
        total_out += size_out
        saved = size_in - size_out
        out("%s %d -> %d bytes, saved %d (%d%%)" % (
            name, size_in, size_out, saved, saved * 100 // size_in))
    if total_in:
        saved = total_in - total_out
        out("total %d -> %d bytes, saved %d (%d%%)" % (
            total_in, total_out, saved, saved * 100 // total_in))


COMMANDS = {
    "minify": cmd_minify, "snippet": cmd_snippet, "chunks": cmd_chunks,
    "attr_value": cmd_attr_value, "ambiguous": cmd_ambiguous,
    "unescape": cmd_unescape, "escape_tag": cmd_escape_tag,
    "cli": cmd_cli, "site": cmd_site,
}


def main():
    with open("data/jobs.tsv", encoding="utf-8") as fh:
        jobs = [ln.rstrip("\n") for ln in fh if ln.strip()]
    for line in jobs:
        if line.startswith("#"):
            print(line)
            continue
        print("> " + line.replace("\t", " "))
        f = line.split("\t")
        try:
            COMMANDS[f[0]](f[1:])
        except Exception as e:  # noqa: BLE001
            print("  error %s: %s" % (type(e).__name__, e))


main()
