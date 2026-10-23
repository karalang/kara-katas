#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored intelhex 2.3.0 and its
scripts, printing what mini_intelhex.kara must print. Each job prints a
header line, "== <kind> <fields>", then its results; an exception prints as
"<ClassName>: <str(e)>". Run: python3 -I -B oracle.py > expected.out"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.path.insert(0, os.path.join(HERE, "vendor", "scripts"))
import intelhex  # noqa: E402
from intelhex import IntelHex, IntelHex16bit, Record  # noqa: E402
import hexinfo  # noqa: E402
import hexmerge  # noqa: E402

with open(os.path.join(HERE, "data", "jobs.tsv"), encoding="utf-8") as fh:
    JOBS = [ln.split("\t") for ln in fh.read().split("\n") if ln]
os.chdir(os.path.join(HERE, "data", "files"))


def err(e):
    msg = str(e)
    print("%s: %s" % (type(e).__name__, msg) if msg else type(e).__name__)


def opt(s, conv=lambda x: int(x, 0)):
    return None if s == "-" else conv(s)


def addr(a):
    return "None" if a is None else "0x%X" % a


def segs(ss):
    return "[" + ", ".join("0x%X..0x%X" % (a, b) for a, b in ss) + "]"


def show_text(s):
    sys.stdout.write(s.replace("\r", "\\r"))


def capture(fn, *args):
    """Runs fn with stdout and stderr captured; returns (result, out, err)."""
    out, er = io.StringIO(), io.StringIO()
    old = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out, er
    try:
        r = fn(*args)
    except Exception as e:  # printed by the caller after the output
        r = e
    finally:
        sys.stdout, sys.stderr = old
    return r, out.getvalue(), er.getvalue()


def show_dump(ih, width=16, withpadding=False):
    sio = io.StringIO()
    try:
        ih.dump(sio, width, withpadding)
    except Exception as e:
        err(e)
        return
    sys.stdout.write(sio.getvalue())


def show_hex(ih, write_start_addr=True, eolstyle="native", byte_count=16):
    sio = io.StringIO()
    try:
        ih.write_hex_file(sio, write_start_addr, eolstyle, byte_count)
    except Exception as e:
        err(e)
        return
    show_text(sio.getvalue())


def summary(ih):
    print("len %d min %s max %s start %r padding 0x%X" % (
        len(ih), addr(ih.minaddr()), addr(ih.maxaddr()), ih.start_addr, ih.padding))
    print("segments", segs(ih.segments()))
    if len(ih) and ih.maxaddr() - ih.minaddr() <= 0x1000:
        show_dump(ih)
    else:
        print("dump skipped")
    show_hex(ih)


def load(f):
    try:
        return IntelHex(f)
    except Exception as e:
        err(e)
        return None


def run_edit(f, ops):
    ih = IntelHex() if f == "-" else IntelHex(f)
    for n, op in enumerate(ops.split(";")):
        p = op.split(":")
        try:
            k = p[0]
            if k == "set":
                ih[int(p[1], 0)] = int(p[2], 0)
            elif k == "del":
                del ih[int(p[1], 0)]
            elif k == "setsl":
                vals = [int(x, 0) for x in p[4].split(",")]
                ih[opt(p[1]):opt(p[2]):opt(p[3])] = vals
            elif k == "delsl":
                del ih[opt(p[1]):opt(p[2]):opt(p[3])]
            elif k == "puts":
                ih.puts(int(p[1], 0), bytes.fromhex(p[2]))
            elif k == "putsz":
                ih.putsz(int(p[1], 0), bytes.fromhex(p[2]))
            elif k == "pad":
                ih.padding = int(p[1], 0)
            elif k == "dict":
                d = {}
                for kv in p[1].split(","):
                    a, v = kv.split("=")
                    d[int(a, 0)] = int(v, 0)
                ih.fromdict(d)
            elif k == "start":
                d = {}
                for kv in p[1].split(","):
                    a, v = kv.split("=")
                    d[a] = int(v, 0)
                ih.fromdict({"start_addr": d})
            elif k == "frombin":
                ih.loadbin(p[1], int(p[2], 0))
            elif k == "copy":
                ih = IntelHex(ih)
            elif k == "bin":
                print("bin", ih.tobinstr(int(p[1], 0), int(p[2], 0)).hex())
            elif k == "dumppad":
                show_dump(ih, 16, True)
            else:
                raise SystemExit("bad op " + op)
        except Exception as e:
            sys.stdout.write("op %d: " % (n + 1))
            err(e)
            break
    summary(ih)


def main():
    for job in JOBS:
        kind = job[0]
        if kind == "file":
            print("== file %s %d bytes" % (job[1], len(job[2]) // 2))
            continue
        print("== " + " ".join(job).replace("\x1f", " | "))
        a = job[1:]
        if kind == "load":
            ih = load(a[0])
            if ih is not None:
                print("len %d min %s max %s start %r" % (
                    len(ih), addr(ih.minaddr()), addr(ih.maxaddr()), ih.start_addr))
                print("segments", segs(ih.segments()))
        elif kind == "todict":
            print(IntelHex(a[0]).todict())
        elif kind == "dump":
            ih = IntelHex(a[0])
            if a[3] != "-" or a[4] != "-":
                ih = ih[opt(a[3]):opt(a[4])]
            show_dump(ih, int(a[1]), a[2] == "1")
        elif kind == "hex":
            show_hex(IntelHex(a[0]), a[2] == "1", a[3], int(a[1]))
        elif kind == "bin":
            ih = IntelHex(a[0])
            if a[4] != "-":
                ih.padding = int(a[4], 0)
            try:
                print(ih.tobinstr(opt(a[1]), opt(a[2]), size=opt(a[3])).hex())
            except Exception as e:
                err(e)
        elif kind == "get":
            ih = IntelHex(a[0])
            for x in a[1].split(","):
                try:
                    print("%s -> %d" % (x, ih[int(x, 0)]))
                except Exception as e:
                    sys.stdout.write("%s -> " % x)
                    err(e)
        elif kind == "gets":
            try:
                print(IntelHex(a[0]).gets(int(a[1], 0), int(a[2])).hex())
            except Exception as e:
                err(e)
        elif kind == "getsz":
            try:
                print(IntelHex(a[0]).getsz(int(a[1], 0)).hex())
            except Exception as e:
                err(e)
        elif kind == "find":
            sub = b"" if a[1] == "-" else bytes.fromhex(a[1])
            print(IntelHex(a[0]).find(sub, opt(a[2]), opt(a[3])))
        elif kind == "seg":
            print(segs(IntelHex(a[0]).segments(int(a[1]))))
        elif kind == "edit":
            run_edit(a[0], a[1])
        elif kind == "merge":
            x = IntelHex(a[0])
            y = x if a[1] == "self" else IntelHex(a[1])
            try:
                x.merge(y, a[2])
            except Exception as e:
                err(e)
            summary(x)
        elif kind == "h16":
            ih = IntelHex16bit(a[0])
            print("min %d max %d padding 0x%X" % (ih.minaddr(), ih.maxaddr(), ih.padding))
            try:
                words = ih.tobinarray(opt(a[1]), opt(a[2]), opt(a[3]))
                print("words", " ".join("%04X" % w for w in words))
            except Exception as e:
                err(e)
            if a[4] != "-":
                for x in a[4].split(","):
                    try:
                        print("%s -> 0x%X" % (x, ih[int(x, 0)]))
                    except Exception as e:
                        sys.stdout.write("%s -> " % x)
                        err(e)
        elif kind == "record":
            try:
                if a[0] == "data":
                    bs = [int(v) for v in a[2].split(",")] if a[2] else []
                    print(Record.data(int(a[1], 0), bs))
                elif a[0] == "eof":
                    print(Record.eof())
                elif a[0] == "esa":
                    print(Record.extended_segment_address(int(a[1], 0)))
                elif a[0] == "ssa":
                    print(Record.start_segment_address(int(a[1], 0), int(a[2], 0)))
                elif a[0] == "ela":
                    print(Record.extended_linear_address(int(a[1], 0)))
                elif a[0] == "sla":
                    print(Record.start_linear_address(int(a[1], 0)))
            except Exception as e:
                err(e)
        elif kind == "info":
            def summarize_all(names):
                for n in names:
                    hexinfo.summarize_yaml(n)
            r, out, _ = capture(summarize_all, a[0].split(","))
            sys.stdout.write(out)
            if isinstance(r, Exception):
                err(r)
        elif kind == "diff":
            sio = io.StringIO()
            intelhex.diff_dumps(IntelHex(a[0]), IntelHex(a[1]), sio, a[0], a[1])
            sys.stdout.write(sio.getvalue())
        elif kind == "hex2bin":
            fout = io.BytesIO()
            r, out, _ = capture(intelhex.hex2bin, a[0], fout, opt(a[1]), opt(a[2]),
                                opt(a[3]), opt(a[4]))
            sys.stdout.write(out)
            print("rc %d bin %s" % (r, fout.getvalue().hex()))
        elif kind == "bin2hex":
            fout = io.StringIO()
            r, out, _ = capture(intelhex.bin2hex, a[0], fout, int(a[1]))
            sys.stdout.write(out)
            print("rc %d" % r)
            show_text(fout.getvalue())
        elif kind == "hexmerge":
            args = [] if a[0] == "-" else a[0].split("\x1f")
            r, out, er = capture(hexmerge.main, args)
            if isinstance(r, Exception):
                sys.stdout.write(out)
                err(r)
            else:
                print("rc %d" % r)
                sys.stdout.write(out)
                if er:
                    print("-- stderr")
                    sys.stdout.write(er)
        else:
            raise SystemExit("bad job " + kind)


main()
