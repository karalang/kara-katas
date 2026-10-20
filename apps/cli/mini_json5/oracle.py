# Runs data/jobs.tsv through json5 0.17.3 itself (the copy in json5/,
# unchanged) and prints what mini_json5 prints; expected.out is its
# output. Run mk.py first. A lone surrogate prints as \udXXX, the way
# Python's backslashreplace writes it.
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import json5  # noqa: E402
from json5 import tool  # noqa: E402
from json5.host import Host  # noqa: E402

DATA = os.path.join(HERE, "data")
STYLES = {q.value: q for q in json5.QuoteStyle}


def out(s):
    sys.stdout.buffer.write(s.encode("utf-8", "backslashreplace") + b"\n")


def read(rel):
    with open(os.path.join(DATA, rel), "rb") as f:
        return f.read()


def load_opts(fields):
    kw = {}
    for f in fields:
        k, _, v = f.partition("=")
        if k == "strict":
            kw["strict"] = v == "1"
        elif k == "trailing":
            kw["consume_trailing"] = v == "1"
        elif k == "dups":
            kw["allow_duplicate_keys"] = v == "1"
    return kw


def dump_opts(fields):
    kw = {}
    for f in fields:
        k, _, v = f.partition("=")
        if k == "indent":
            if v == "tab":
                kw["indent"] = "\t"
            elif v.startswith("s:"):
                kw["indent"] = v[2:]
            else:
                kw["indent"] = int(v)
        elif k == "compact":
            kw["separators"] = (",", ":")
        elif k == "quote_style":
            kw["quote_style"] = STYLES[v]
        else:
            kw[k] = v == "1"
    return kw


# An error message can quote a raw newline or carriage return; it is
# printed with those two escaped, so it stays on one line.
def err(e):
    msg = str(e).replace("\r", "\\r").replace("\n", "\\n")
    return "%s: %s" % (type(e).__name__, msg)


def show(text):
    for line in text.split("\n"):
        out("  |" + line)


def parse_stream(s):
    start = 0
    while True:
        v, e, pos = json5.parse(s, start=start, consume_trailing=False)
        if e is not None:
            out("  error at %d: %s" % (pos, e))
            return
        out("  %d..%d: %r" % (start, pos, v))
        start = pos
        if start == len(s) or s[start:].isspace():
            return


class FakeHost(Host):
    def __init__(self):
        super().__init__()
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()


def run_tool(args):
    host = FakeHost()
    try:
        code = tool.main(args, host=host)
    except SystemExit as e:
        code = e.code
    except Exception as e:  # noqa: BLE001
        code = err(e)
    for name, stream in (("stdout", host.stdout), ("stderr", host.stderr)):
        text = stream.getvalue()
        if text:
            if text.endswith("\n"):
                text = text[:-1]
            for line in text.split("\n"):
                out("  %s|%s" % (name, line))
    out("  -> %s" % (code,))


def run(f):
    if f[0] == "cases":
        for line in read("cases.tsv").decode("utf-8").split("\n")[:-1]:
            opts, _, doc = line.partition("\t")
            try:
                r = repr(json5.loads(doc, **load_opts(opts.split(",") if opts else [])))
            except Exception as e:  # noqa: BLE001
                r = err(e)
            out("  %s %s -> %s" % (opts or "-", doc, r))
        return
    if f[0] == "tool":
        run_tool(f[1:])
        return
    raw = read(f[1])
    try:
        if f[0] == "parse":
            parse_stream(raw.decode("utf-8"))
            return
        value = json5.loads(raw, **load_opts(f[2:]))
        if f[0] == "load":
            out("  " + repr(value))
        elif f[0] == "dump":
            show(json5.dumps(value, **dump_opts(f[2:])))
        elif f[0] == "roundtrip":
            a = json5.dumps(value)
            b = json5.dumps(json5.loads(a))
            c = json5.dumps(value, indent=2, quote_keys=True, sort_keys=True,
                            ensure_ascii=False, quote_style=json5.QuoteStyle.PREFER_SINGLE)
            d = json5.dumps(json5.loads(c), indent=2, quote_keys=True, sort_keys=True,
                            ensure_ascii=False, quote_style=json5.QuoteStyle.PREFER_SINGLE)
            out("  compact %d chars, same again %s; pretty %d chars, same again %s"
                % (len(a), a == b, len(c), c == d))
    except Exception as e:  # noqa: BLE001
        out("  " + err(e))


def main():
    os.chdir(HERE)
    for job in read("jobs.tsv").decode("utf-8").split("\n")[:-1]:
        f = job.split("\t")
        out("== " + " | ".join(f))
        run(f)


main()
