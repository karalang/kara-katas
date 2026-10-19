# Runs data/jobs.jsonl through idna 3.20 (the files in idna/, unchanged)
# and prints what each operation returns. Run mk.py first.
import contextlib
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import idna  # noqa: E402
import idna.codec  # noqa: E402
from idna.cli import main as cli_main  # noqa: E402


def err(e):
    if isinstance(e, idna.IDNAError):
        pos = "" if e.position is None else f" at {e.position}"
        return f"{type(e).__name__} {e.code}{pos}: {e}"
    return f"{type(e).__name__}: {e}"


def flags(op, names):
    on = [n for n in names if op.get(n)]
    return (" " + ",".join(on)) if on else ""


def host(h):
    # requests' PreparedRequest.prepare_url, for the host.
    if not h.isascii():
        try:
            return idna.encode(h, uts46=True).decode("utf-8")
        except idna.IDNAError:
            raise ValueError("URL has an invalid label.")
    elif h.startswith(("*", ".")):
        raise ValueError("URL has an invalid label.")
    return h


def run(op):
    kind = op["op"]
    s = op.get("s")
    if kind == "encode":
        print(f"-- encode{flags(op, ['strict', 'uts46', 'std3'])} {s!r}")
        f = lambda: idna.encode(s, strict=op.get("strict", False), uts46=op.get("uts46", False),  # noqa: E731
                                std3_rules=op.get("std3", False))
    elif kind == "decode":
        print(f"-- decode{flags(op, ['strict', 'uts46', 'std3', 'display'])} {s!r}")
        f = lambda: idna.decode(s, strict=op.get("strict", False), uts46=op.get("uts46", False),  # noqa: E731
                                std3_rules=op.get("std3", False), display=op.get("display", False))
    elif kind == "remap":
        print(f"-- remap{flags(op, ['std3'])} {s!r}")
        f = lambda: idna.uts46_remap(s, std3_rules=op["std3"])  # noqa: E731
    elif kind == "alabel":
        print(f"-- alabel {s!r}")
        f = lambda: idna.alabel(s)  # noqa: E731
    elif kind == "ulabel":
        print(f"-- ulabel {s!r}")
        f = lambda: idna.ulabel(s)  # noqa: E731
    elif kind == "check_label":
        print(f"-- check_label {s!r}")
        f = lambda: idna.check_label(s)  # noqa: E731
    elif kind == "bidi":
        print(f"-- check_bidi{flags(op, ['ltr'])} {s!r}")
        f = lambda: idna.check_bidi(s, check_ltr=op["ltr"])  # noqa: E731
    elif kind == "host":
        print(f"-- host {s!r}")
        f = lambda: host(s)  # noqa: E731
    elif kind == "codec_encode":
        print(f"-- codec encode {s!r}")
        f = lambda: s.encode("idna2008")  # noqa: E731
    elif kind == "codec_decode":
        print(f"-- codec decode {s!r}")
        f = lambda: s.encode("utf-8").decode("idna2008")  # noqa: E731
    elif kind in ("inc_encode", "inc_decode"):
        chunks = op["chunks"]
        print(f"-- {kind} " + " | ".join(repr(c) for c in chunks))
        if kind == "inc_encode":
            coder = idna.codec.IncrementalEncoder()
        else:
            coder = idna.codec.IncrementalDecoder()
        for i, c in enumerate(chunks):
            last = i == len(chunks) - 1
            try:
                out = coder.encode(c, final=last) if kind == "inc_encode" else coder.decode(c.encode("utf-8"), final=last)
            except (idna.IDNAError, UnicodeError) as e:
                print("error: " + err(e))
                return
            print(f"   {out!r}")
        return
    else:
        print("-- cli " + " ".join(repr(a) for a in op["args"]) + ("" if "stdin" not in op else " < stdin"))
        out, errs = io.StringIO(), io.StringIO()
        stdin = sys.stdin
        sys.stdin = io.StringIO("".join(line + "\n" for line in op.get("stdin", [])))
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(errs):
                try:
                    code = cli_main(op["args"])
                except SystemExit as e:
                    code = e.code
        finally:
            sys.stdin = stdin
        for line in out.getvalue().splitlines():
            print("   out: " + line)
        for line in errs.getvalue().splitlines():
            print("   err: " + line)
        print(f"   exit {code}")
        return
    try:
        r = f()
        print("   ok" if r is None or r is True else f"   {r!r}")
    except (idna.IDNAError, UnicodeError, ValueError) as e:
        print("error: " + err(e))


with open("data/jobs.jsonl") as fh:
    for line in fh:
        job = json.loads(line)
        print(f"== {job['name']}")
        for op in job["ops"]:
            run(op)
