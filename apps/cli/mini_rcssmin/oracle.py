"""Replay data/jobs.tsv against the vendored rcssmin 1.1.2.

`file` minifies one of the style sheets under data/ and `snippet` a short
one written in the job, each with `bang` for keep_bang_comments=True.
`bytes` passes the snippet as bytes (Latin-1, as the library decodes
them) and prints the bytes it returns. `cli` runs the module as
`python rcssmin.py <args> < <file>`, and `bundle` is a build step that
minifies the sheets a manifest lists into one file and reports the bytes
saved. A minified sheet prints as its repr; a job that raises prints
`error <class>: <message>`.

The library's pure-Python minifier is used throughout
(`_make_cssmin(python_only=True)`); its C extension is not built.
"""
import io
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "vendor"))

import rcssmin  # noqa: E402

cssmin = rcssmin._make_cssmin(python_only=True)


def out(s):
    print("  " + s)


def unesc(s):
    """Job text uses \\t, \\n, \\r, \\f, \\\\ and \\uXXXX escapes."""
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
            elif n == "r":
                res.append("\r")
            elif n == "f":
                res.append("\f")
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


def read_text(name):
    path = os.path.join("data", name)
    if not os.path.exists(path):
        raise OSError("cannot read %s" % name)
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def cmd_file(f):
    text = read_text(f[0])
    res = cssmin(text, keep_bang_comments=f[1:] == ["bang"])
    out("%d -> %d chars" % (len(text), len(res)))
    out(repr(res))


def cmd_snippet(f):
    out(repr(cssmin(unesc(f[0]), keep_bang_comments=f[1:] == ["bang"])))


def cmd_bytes(f):
    data = unesc(f[0]).encode("latin-1")
    out(repr(cssmin(data, keep_bang_comments=f[1:] == ["bang"])))


def cmd_cli(f):
    """`python rcssmin.py <args> < <file>`: the last field is the file."""
    saved = sys.argv, sys.stdin, sys.stdout
    path = os.path.join("data", f[-1])
    buf = io.StringIO()
    with open(path, encoding="utf-8") as stdin:
        sys.argv = ["rcssmin.py"] + f[:-1]
        sys.stdin = stdin
        sys.stdout = buf
        try:
            runpy.run_path(os.path.join(HERE, "vendor", "rcssmin.py"),
                           run_name="__main__")
        finally:
            sys.argv, sys.stdin, sys.stdout = saved
    out(repr(buf.getvalue()))


def cmd_bundle(f):
    parts = []
    total_in = 0
    for line in read_text(f[0]).split("\n"):
        if not line or line.startswith("#"):
            continue
        fields = line.split(" ")
        name = fields[0]
        try:
            text = read_text("site/css/" + name)
        except OSError as e:
            out("%s skipped: %s" % (name, e))
            continue
        res = cssmin(text, keep_bang_comments="bang" in fields[1:])
        size_in = len(text.encode("utf-8"))
        total_in += size_in
        out("%s %d -> %d bytes" % (name, size_in, len(res.encode("utf-8"))))
        parts.append(res)
    dest = os.path.join("data", f[1])
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(parts) + "\n")
    bundle = read_text(f[1])
    size_out = len(bundle.encode("utf-8"))
    saved = total_in - size_out
    out("%s %d -> %d bytes, saved %d (%d%%)" % (
        f[1], total_in, size_out, saved, saved * 100 // total_in))
    for line in bundle.split("\n"):
        print("  | " + line)


COMMANDS = {
    "file": cmd_file, "snippet": cmd_snippet, "bytes": cmd_bytes,
    "cli": cmd_cli, "bundle": cmd_bundle,
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
