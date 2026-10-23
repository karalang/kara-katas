#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored latexcodec 3.0.1, printing
what mini_latexcodec.kara must print.

A job line is: name, files, then one op per field. Files are "name=hex"
pairs (comma-separated, "-" for none), made in a fresh working directory.
An op is words separated by spaces: "h:<hex>" is a UTF-8 string, "x:<hex>"
is bytes, and a chunk of an incremental op is "n:<hex>", "f:<hex>" (final)
or "r" (reset). After each op, the files it created or changed are printed.
An exception prints as "error <Class>: <str(e)>"; an incremental op stops
at its first error, and the job goes on.

Strings print as ascii() does, so every character is visible.

Run: python3 -I -B oracle.py > expected.out"""
import codecs
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import latexcodec  # noqa: E402,F401
from latexcodec import codec as lcodec, lexer as llexer  # noqa: E402

OUT = []


def emit(s):
    OUT.append(s)


def vis(s):
    return ascii(s)[1:-1]


def shown(w):
    if w.startswith("h:"):
        return ascii(bytes.fromhex(w[2:]).decode("utf-8"))
    if w.startswith("x:"):
        return repr(bytes.fromhex(w[2:]))
    return w


def result(r):
    return repr(r) if isinstance(r, bytes) else ascii(r)


def err(e):
    emit(f"  error {type(e).__name__}: {vis(str(e))}")


def tok(t):
    return f"{t.name}:{ascii(t.text)}"


def toks(ts):
    return " ".join(tok(t) for t in ts) if ts else "(none)"


def snapshot():
    snap = {}
    for name in sorted(os.listdir(".")):
        with open(name, "rb") as fh:
            snap[name] = fh.read()
    return snap


def show_file(name, data):
    emit(f"  wrote {name} ({len(data)} bytes)")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        for i in range(0, len(data), 32):
            emit("    #" + data[i:i + 32].hex())
        return
    lines = text.split("\n")
    last = lines.pop()
    for ln in lines:
        emit("    |" + vis(ln))
    if last:
        emit("    |" + vis(last))
        emit("    (no newline at end)")


def text_arg(w):
    return bytes.fromhex(w[2:]).decode("utf-8")


def bytes_arg(w):
    return bytes.fromhex(w[2:])


def chunk_input(codec_name, w):
    # ulatex takes str chunks, every other codec bytes
    data = bytes.fromhex(w[2:])
    if codec_name.lower().startswith("ulatex"):
        return data.decode("utf-8")
    return data


def run_table():
    t = lcodec._LATEX_UNICODE_TABLE
    emit(f"  unicode_map {len(t.unicode_map)} entries, max_length {t.max_length}, latex_map {len(t.latex_map)} entries")
    for k, v in t.unicode_map.items():
        emit(f"  dec {toks(k)} -> {ascii(v)}")
    for k, (latex, ts) in t.latex_map.items():
        emit(f"  enc {ascii(k)} -> {ascii(latex)} [{toks(ts)}]")


def run_op(words):
    op = words[0]
    a = words[1:]
    if op == "table":
        run_table()
    elif op == "enc":
        emit("  -> " + result(codecs.encode(text_arg(a[2]), a[0], a[1])))
    elif op == "dec":
        data = text_arg(a[2]) if a[2].startswith("h:") else bytes_arg(a[2])
        emit("  -> " + result(codecs.decode(data, a[0], a[1])))
    elif op == "strenc":
        emit("  -> " + result(text_arg(a[2]).encode(a[0], a[1])))
    elif op == "bdec":
        emit("  -> " + result(bytes_arg(a[2]).decode(a[0], a[1])))
    elif op == "ienc":
        enc = codecs.getincrementalencoder(a[0])(a[1])
        for i, w in enumerate(a[2:]):
            if w == "r":
                enc.reset()
                emit(f"  [{i}] reset")
                continue
            try:
                r = enc.encode(text_arg(w), final=w.startswith("f:"))
            except Exception as e:
                err(e)
                return
            emit(f"  [{i}] -> {result(r)}")
    elif op == "idec":
        dec = codecs.getincrementaldecoder(a[0])(a[1])
        for i, w in enumerate(a[2:]):
            if w == "r":
                dec.reset()
                emit(f"  [{i}] reset")
                continue
            try:
                r = dec.decode(chunk_input(a[0], w), final=w.startswith("f:"))
            except Exception as e:
                err(e)
                return
            emit(f"  [{i}] -> {result(r)}")
    elif op == "lex":
        lx = llexer.LatexIncrementalDecoder(a[0])
        ts = []
        try:
            for t in lx.get_tokens(bytes_arg(a[1]).decode("ascii"), final=True):
                ts.append(t)
        except Exception as e:
            for t in ts:
                emit("  " + tok(t))
            err(e)
            return
        for t in ts:
            emit("  " + tok(t))
        emit(f"  state {lx.state} inline_math {lx.inline_math}")
    elif op == "ilex":
        lx = llexer.LatexIncrementalDecoder(a[0])
        for i, w in enumerate(a[1:]):
            ts = list(lx.get_tokens(bytes_arg(w).decode("ascii"), final=w.startswith("f:")))
            raw, st = lx.getstate()
            emit(f"  [{i}] {toks(ts)}")
            emit(f"      state {raw.name}:{ascii(raw.text)} {st}")
    elif op == "plain":
        lx = llexer.LatexIncrementalDecoder(a[0])
        emit("  -> " + result(lx.decode(bytes_arg(a[1]), final=True)))
    elif op == "read":
        with codecs.open(a[0], "r", a[1], a[2]) as fh:
            emit("  -> " + result(fh.read()))
    elif op == "write":
        with codecs.open(a[0], "w", a[1], a[2]) as fh:
            fh.write(text_arg(a[3]))
    elif op == "convert":
        with open(a[0], "rb") as fh:
            data = fh.read()
        text = data.decode(a[2], a[4])
        out = text.encode(a[3], a[4])
        with open(a[1], "wb") as fh:
            fh.write(out)
    else:
        raise SystemExit("unknown op " + op)


def run_job(line):
    fields = line.rstrip("\n").split("\t")
    name, files, ops = fields[0], fields[1], fields[2:]
    emit(f"== {name}")
    work = tempfile.mkdtemp(prefix="latexcodec-")
    old = os.getcwd()
    os.chdir(work)
    try:
        if files != "-":
            for item in files.split(","):
                k, v = item.split("=")
                with open(k, "wb") as fh:
                    fh.write(bytes.fromhex(v))
        for o in ops:
            words = o.split(" ")
            emit("> " + " ".join(shown(w) for w in words))
            before = snapshot()
            try:
                run_op(words)
            except Exception as e:
                err(e)
            after = snapshot()
            for k in sorted(after):
                if before.get(k) != after[k]:
                    show_file(k, after[k])
    finally:
        os.chdir(old)
        shutil.rmtree(work)


def main():
    with open(os.path.join(HERE, "data", "jobs.tsv"), encoding="utf-8") as fh:
        for line in fh:
            run_job(line)
    sys.stdout.write("\n".join(OUT) + "\n")


main()
