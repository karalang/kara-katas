#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored webvtt-py 0.5.1, printing what
mini_webvtt.kara must print.

A job line is: name, files, dirs, then one op per field. Files are
"name=hex" pairs (comma-separated, "-" for none) and dirs a comma-separated
list; both are made in a fresh working directory, which the output calls
/work. An op is words separated by spaces: "h:<hex>" is a UTF-8 string,
"-" is None. After each op the files it created or changed are printed.
An exception prints as "error <Class>: <str(e)>" and the job goes on.
Run: python3 -I -B oracle.py > expected.out"""
import contextlib
import io
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import webvtt  # noqa: E402
from webvtt import cli  # noqa: E402
from webvtt.models import Caption, Style, Timestamp  # noqa: E402

os.environ["COLUMNS"] = "80"
sys.argv[0] = "webvtt"
WORK = None


def vis(s):
    out = []
    for c in s:
        n = ord(c)
        if n < 0x20 or n == 0x7F or 0x80 <= n < 0xA0:
            out.append("\\x%02x" % n)
        elif n in (0x2028, 0x2029, 0xFEFF):
            out.append("\\u%04x" % n)
        else:
            out.append(c)
    return "".join(out)


def emit(s):
    sys.stdout.write(s.replace(WORK, "/work") + "\n")


def lrepr(xs):
    return "[" + ", ".join(repr(x) for x in xs) + "]"


def arg(w):
    if w == "-":
        return None
    if w.startswith("h:"):
        return bytes.fromhex(w[2:]).decode("utf-8")
    if w.startswith("/work"):
        return WORK + w[5:]
    return w


def shown(w):
    if w.startswith("h:"):
        return repr(bytes.fromhex(w[2:]).decode("utf-8"))
    return w


def text_block(s):
    for line in s.split("\n"):
        emit("  |" + vis(line))


def file_block(data):
    try:
        text = data.decode("utf-8")
        ok = "\x00" not in text
    except UnicodeDecodeError:
        ok = False
    if ok:
        for line in text.split("\n"):
            emit("    |" + vis(line))
    else:
        for i in range(0, len(data), 32):
            emit("    " + data[i:i + 32].hex())


def snapshot():
    snap = {}
    for root, _dirs, files in os.walk(WORK):
        for f in files:
            p = os.path.join(root, f)
            with open(p, "rb") as fh:
                snap[os.path.relpath(p, WORK)] = fh.read()
    return snap


def describe(w):
    emit("  repr " + repr(w))
    emit(f"  captions {len(w)}, styles {len(w.styles)}, total_length {w.total_length}")
    emit("  header_comments " + lrepr(w.header_comments))
    emit("  footer_comments " + lrepr(w.footer_comments))
    for i, s in enumerate(w.styles):
        emit(f"  style {i} {s.text!r} comments {lrepr(s.comments)}")
    for i, c in enumerate(w.captions):
        emit(f"  caption {i} {c!r}")
        emit("    str " + vis(str(c)))
        emit(f"    seconds {c.start_in_seconds} {c.end_in_seconds}, identifier {c.identifier!r}, voice {c.voice!r}")
        emit("    lines " + lrepr(c.lines))
        emit("    comments " + lrepr(c.comments))


def run_op(st, words):
    op = words[0]
    a = [arg(x) for x in words[1:]]
    w = st["w"]
    if op in ("read", "srt", "sbv"):
        kw = {"encoding": a[1]} if len(a) > 1 else {}
        f = {"read": webvtt.read, "srt": webvtt.from_srt, "sbv": webvtt.from_sbv}[op]
        st["w"] = f(a[0], **kw)
    elif op == "buffer":
        with open(a[0], "rb") as fh:
            data = fh.read()
        st["w"] = webvtt.from_buffer(io.BytesIO(data), format=a[1])
    elif op == "string":
        with open(a[0], "rb") as fh:
            data = fh.read()
        st["w"] = webvtt.from_string(data.decode("utf-8"))
    elif op == "new":
        st["w"] = webvtt.WebVTT()
    elif op == "show":
        describe(w)
    elif op == "content":
        text_block(w.content)
    elif op == "write":
        f = io.StringIO()
        w.write(f, format=a[0])
        text_block(f.getvalue())
    elif op == "slice":
        for c in w.iter_slice(a[0], a[1]):
            emit("  " + vis(str(c)))
    elif op == "segment":
        webvtt.segment(a[0], a[1], int(a[2]), int(a[3]))
    elif op == "save":
        kw = {}
        if len(a) > 1 and a[1] is not None:
            kw["encoding"] = a[1]
        if len(a) > 2 and a[2] is not None:
            kw["add_bom"] = a[2] == "1"
        w.save(a[0], **kw)
        emit("  file " + repr(w.file))
    elif op == "savesrt":
        kw = {}
        if len(a) > 1 and a[1] is not None:
            kw["encoding"] = a[1]
        w.save_as_srt(a[0], **kw)
        emit("  file " + repr(w.file))
    elif op == "cap":
        w.captions.append(Caption(a[0], a[1], a[2], a[3]))
    elif op == "settext":
        w.captions[int(a[0])].text = a[1]
    elif op == "setstart":
        w.captions[int(a[0])].start = a[1]
    elif op == "setend":
        w.captions[int(a[0])].end = a[1]
    elif op == "style":
        w.styles.append(Style(a[0]))
    elif op == "hdr":
        w.header_comments.append(a[0])
    elif op == "ftr":
        w.footer_comments.append(a[0])
    elif op == "capcomment":
        w.captions[int(a[0])].comments.append(a[1])
    elif op == "stylecomment":
        w.styles[int(a[0])].comments.append(a[1])
    elif op == "del":
        del w.captions[int(a[0])]
    elif op == "get":
        emit("  " + repr(w[int(a[0])]))
    elif op == "eq":
        emit(f"  {w.captions[int(a[0])] == w.captions[int(a[1])]}")
    elif op == "ts":
        t = Timestamp.from_string(a[0])
        emit(f"  {t} {t!r} {t.in_seconds()} {t.to_tuple()}")
    elif op == "cmp":
        x = Timestamp.from_string(a[0])
        y = Timestamp.from_string(a[1])
        emit(f"  == {x == y}, != {x != y}, < {x < y}, <= {x <= y}, > {x > y}, >= {x >= y}")
    elif op == "cli":
        out, err = io.StringIO(), io.StringIO()
        code = None
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                try:
                    cli.main(a)
                except SystemExit as e:
                    code = e.code
        finally:
            for line in out.getvalue().splitlines():
                emit("  out|" + line)
            for line in err.getvalue().splitlines():
                emit("  err|" + line)
        if code is not None:
            emit(f"  exit {code}")
    else:
        raise SystemExit("bad op " + op)


def run_job(fields):
    global WORK
    name, files, dirs = fields[0], fields[1], fields[2]
    tmp = tempfile.mkdtemp()
    os.chdir(tmp)
    WORK = os.getcwd()
    try:
        if dirs != "-":
            for d in dirs.split(","):
                os.makedirs(d)
        if files != "-":
            for pair in files.split(","):
                fname, hx = pair.split("=")
                with open(fname, "wb") as fh:
                    fh.write(bytes.fromhex(hx))
        emit("== " + name)
        st = {"w": None}
        before = snapshot()
        for op in fields[3:]:
            words = op.split(" ")
            emit("> " + " ".join(shown(x) for x in words))
            try:
                run_op(st, words)
            except Exception as e:  # noqa: BLE001
                emit(f"  error {type(e).__name__}: {vis(str(e))}")
            after = snapshot()
            for p in sorted(after):
                if before.get(p) != after[p]:
                    emit(f"  wrote {p} ({len(after[p])} bytes)")
                    file_block(after[p])
            before = after
        emit("")
    finally:
        os.chdir(HERE)
        shutil.rmtree(tmp)


def main():
    with open(os.path.join(HERE, "data", "jobs.tsv"), encoding="utf-8") as fh:
        for line in fh.read().split("\n"):
            if line:
                run_job(line.split("\t"))


main()
