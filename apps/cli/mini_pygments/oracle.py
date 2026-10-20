# Oracle for mini_pygments: runs the jobs, style definitions and the
# docs-site build in data/ through Pygments 2.17.2 itself.
import os
import re

import pygments
from pygments import highlight
from pygments.filters import get_filter_by_name
from pygments.formatters import get_formatter_by_name, HtmlFormatter
from pygments.lexers import (get_lexer_by_name, get_lexer_for_filename,
                             get_lexer_for_mimetype, find_lexer_class_for_filename)
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound, OptionError
from pygments.lexers._mapping import LEXERS

assert pygments.__version__ == "2.17.2"

IMPLEMENTED = ["python", "bash", "ini", "diff", "toml", "nginx", "css", "sql", "docker",
               "go", "rust", "javascript", "systemd", "properties", "xml", "html",
               "pytb", "c", "json", "text"]
IMPL_NAMES = {type(get_lexer_by_name(a)).name for a in IMPLEMENTED}


def opts_of(text):
    # pygmentize's _parse_options for one -O string
    opts = {}
    if not text.strip():
        return opts
    for o_arg in text.split(","):
        o_arg = o_arg.strip()
        try:
            k, v = o_arg.split("=", 1)
        except ValueError:
            opts[o_arg] = True
        else:
            opts[k.strip()] = v.strip()
    return opts


def show(out):
    if isinstance(out, bytes):
        out = out.decode("ascii")
    return out.replace("\x1b", "^[")


def emit(text):
    if not text.endswith("\n"):
        text += "\n<no newline>\n"
    print(text, end="")


def candidates(fn):
    # every lexer in Pygments whose file name patterns match fn
    import fnmatch
    out = set()
    for _mod, name, _a, filenames, _m in LEXERS.values():
        for pat in filenames:
            if fnmatch.fnmatch(os.path.basename(fn), pat):
                out.add(name)
    return out


def catalog():
    print("# lexers")
    for alias in IMPLEMENTED:
        cls = type(get_lexer_by_name(alias))
        print("%s: aliases=%s filenames=%s mimetypes=%s" % (
            cls.name, ",".join(cls.aliases), ",".join(cls.filenames),
            ",".join(cls.mimetypes)))
    print("# find_lexer_class_for_filename")
    for fn in ["x.py", "x.pyw", "SConstruct", "x.sh", ".bashrc", "PKGBUILD", "x.ini", "x.cfg",
               "x.patch", "Pipfile", "x.toml", "nginx.conf", "x.css", "x.sql", "Dockerfile",
               "x.go", "x.rs", "x.js", "x.mjs", "x.service", "x.properties", "x.xml",
               "x.html", "x.xhtml", "x.pytb", "x.c", "x.h", "x.json", "x.txt", "x.unknown",
               "dir/sub/x.rs", "X.PY", "x.tar.gz"]:
        cls = find_lexer_class_for_filename(fn)
        print("%s -> %s" % (fn, cls.aliases[0] if cls else "text"))


def run_job(n, line):
    kind, lexname, lopts, filters, fmt, fopts, src = line.split("|")
    print("== job %d: %s" % (n, " ".join(x for x in line.split("|") if x)))
    code = open(os.path.join("data/src", src), encoding="utf-8", newline="").read()
    try:
        lo = opts_of(lopts)
        if kind == "lex":
            lexer = get_lexer_by_name(lexname, **lo)
        elif kind == "file":
            names = candidates(lexname)
            assert len(names) <= 1 and names <= IMPL_NAMES, (lexname, names)
            lexer = get_lexer_for_filename(lexname, code, **lo)
        else:
            lexer = get_lexer_for_mimetype(lexname, **lo)
        print("lexer: %r" % (lexer,))
        for f in filter(None, filters.split(";")):
            if ":" in f:
                fname, fo = f.split(":", 1)
                lexer.add_filter(fname, **opts_of(fo))
            else:
                lexer.add_filter(f)
        if fmt == "-":
            return
        formatter = get_formatter_by_name(fmt, **opts_of(fopts))
    except (ClassNotFound, OptionError) as err:
        print("Error: %s" % err)
        return
    try:
        out = highlight(code, lexer, formatter)
    except Exception as err:
        print("raised %s: %s" % (type(err).__name__, err))
        return
    emit(show(out))


def run_styles():
    for n, line in enumerate(open("data/styles.txt", encoding="utf-8").read().splitlines(), 1):
        style, arg, fopts = line.split("|")
        print("== style %d: %s" % (n, " ".join(x for x in line.split("|") if x)))
        o = opts_of(fopts)
        o["style"] = style
        try:
            fmter = get_formatter_by_name("html", **o)
        except ClassNotFound as err:
            print(err)
            continue
        print(fmter.get_style_defs(arg or ""))


FENCE = re.compile(r'^```(\w[\w+-]*)?(?:\s*\{([^}]*)\})?\s*$')
ATTR = re.compile(r'(\w+)(?:="([^"]*)")?')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_site():
    os.makedirs("data/site", exist_ok=True)
    pages = sorted(f for f in os.listdir("data/docs") if f.endswith(".md"))
    for page in pages:
        lines = open(os.path.join("data/docs", page), encoding="utf-8").read().split("\n")
        out = ["<!doctype html>", '<link rel="stylesheet" href="pygments.css">']
        para = []
        i = 0

        def flush():
            if para:
                out.append("<p>%s</p>" % esc(" ".join(para)))
                para.clear()
        while i < len(lines):
            line = lines[i]
            m = FENCE.match(line)
            if m:
                flush()
                lang, attrs = m.group(1), m.group(2) or ""
                body = []
                i += 1
                while i < len(lines) and lines[i] != "```":
                    body.append(lines[i])
                    i += 1
                i += 1
                opts = {}
                for am in ATTR.finditer(attrs):
                    k, v = am.group(1), am.group(2)
                    opts[k] = "table" if (k == "linenos" and v is None) else v
                try:
                    lexer = get_lexer_by_name(lang) if lang else TextLexer()
                except ClassNotFound:
                    lexer = TextLexer()
                fmt = HtmlFormatter(**opts)
                out.append("<!-- %s -->" % lexer.name)
                out.append(highlight("\n".join(body) + "\n", lexer, fmt).rstrip("\n"))
                continue
            if line.startswith("# "):
                flush()
                out.append("<h1>%s</h1>" % esc(line[2:]))
            elif line.strip() == "":
                flush()
            else:
                para.append(line.strip())
            i += 1
        flush()
        name = page[:-3] + ".html"
        with open(os.path.join("data/site", name), "w", encoding="utf-8") as f:
            f.write("\n".join(out) + "\n")
    with open("data/site/pygments.css", "w", encoding="utf-8") as f:
        f.write(HtmlFormatter().get_style_defs(".highlight") + "\n")
    for name in sorted(os.listdir("data/site")):
        print("== site/%s" % name)
        emit(open(os.path.join("data/site", name), encoding="utf-8").read())


def main():
    catalog()
    jobs = open("data/jobs.txt", encoding="utf-8").read().splitlines()
    for n, line in enumerate(jobs, 1):
        run_job(n, line)
    run_styles()
    build_site()


main()
