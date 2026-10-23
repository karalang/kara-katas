#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored pysubs2 1.9.0, printing what
mini_pysubs2.kara must print.

A job line is: name, files, dirs, then one op per field. Files are
"name=hex" pairs (comma-separated, "-" for none) and dirs a comma-separated
list; both are made in a fresh working directory, which the output calls
/work. An op is words separated by spaces: "h:<hex>" is a UTF-8 string,
"-" is None. After each op its warnings are printed, then the files it
created or changed. An exception prints as "error <Class>: <str(e)>" and
the job goes on.

Two things are made deterministic here rather than in the library: the
format list of a FormatAutodetectionError comes from a set, so it is
printed sorted, and standard input is a terminal, so the command line with
no files prints its help instead of reading a pipe.

Run: python3 -I -B oracle.py > expected.out"""
import contextlib
import io
import os
import re
import shutil
import sys
import tempfile
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import pysubs2  # noqa: E402
from pysubs2 import Alignment, SSAEvent, SSAFile, SSAStyle  # noqa: E402
from pysubs2 import formats, time as ptime  # noqa: E402
from pysubs2.cli import Pysubs2CLI  # noqa: E402
from pysubs2.exceptions import FormatAutodetectionError  # noqa: E402
from pysubs2.formats.microdvd import MicroDVDFormat  # noqa: E402
from pysubs2.formats.subrip import SubripFormat  # noqa: E402
from pysubs2.formats.substation import SubstationFormat, parse_tags, rgba_to_color, color_to_ass_rgba, color_to_ssa_rgb  # noqa: E402
from pysubs2.formats.tmp import TmpFormat  # noqa: E402
from pysubs2.formats.webvtt import WebVTTFormat  # noqa: E402

os.environ["COLUMNS"] = "80"
WORK = None


class Tty(io.StringIO):
    def isatty(self):
        return True


sys.stdin = Tty()

STYLE_FIELDS = ["fontname", "fontsize", "primarycolor", "secondarycolor", "tertiarycolor", "outlinecolor",
                "backcolor", "bold", "italic", "underline", "strikeout", "scalex", "scaley", "spacing", "angle",
                "borderstyle", "outline", "shadow", "alignment", "marginl", "marginr", "marginv", "alphalevel",
                "encoding", "drawing"]


def vis(s):
    out = []
    for c in s:
        n = ord(c)
        if n < 0x20 or n == 0x7F or 0x80 <= n < 0xA0:
            out.append("\\x%02x" % n)
        elif n in (0x2028, 0x2029, 0xFEFF) or 0xD800 <= n < 0xE000:
            out.append("\\u%04x" % n)
        else:
            out.append(c)
    return "".join(out)


def emit(s):
    sys.stdout.write(s.replace(WORK, "/work") + "\n")


def arg(w):
    if w == "-":
        return None
    if w.startswith("h:"):
        return bytes.fromhex(w[2:]).decode("utf-8")
    return w


def shown(w):
    if w.startswith("h:"):
        return repr(bytes.fromhex(w[2:]).decode("utf-8"))
    return w


def num(w):
    return int(w) if re.fullmatch(r"-?\d+", w) else float(w)


def kwargs_of(words):
    kw = {}
    for w in words:
        k, v = w.split("=", 1)
        if k in ("keep_html_tags", "keep_unknown_html_tags", "strict_fps_inference", "apply_styles",
                 "keep_ssa_tags", "write_fps_declaration"):
            kw[k] = v == "1"
        elif k == "fps":
            kw[k] = float(v)
        elif k == "frames":
            kw[k] = int(v)
        elif k == "header_notice":
            kw[k] = arg(v)
        else:
            kw[k] = num(v)
    return kw


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


def describe_style(name, sty):
    emit(f"  style {name!r} {sty!r}")
    fields = [f"{f}={getattr(sty, f)!r}" for f in STYLE_FIELDS]
    for i in range(0, len(fields), 5):
        emit("    " + " ".join(fields[i:i + 5]))


def describe_event(i, ev):
    emit(f"  event {i} {ev!r}")
    emit(f"    start={ev.start!r} end={ev.end!r} layer={ev.layer!r} style={ev.style!r} name={ev.name!r} marked={ev.marked!r}")
    emit(f"    marginl={ev.marginl!r} marginr={ev.marginr!r} marginv={ev.marginv!r} effect={ev.effect!r} type={ev.type!r}")
    emit(f"    text={ev.text!r}")
    emit(f"    plaintext={ev.plaintext!r} duration={ev.duration!r} is_drawing={ev.is_drawing!r} is_text={ev.is_text!r}")


def describe(subs):
    emit("  repr " + repr(subs))
    emit(f"  format {subs.format!r}, fps {subs.fps!r}")
    for k, v in subs.info.items():
        emit(f"  info {k!r}: {v!r}")
    for k, v in subs.aegisub_project.items():
        emit(f"  aegisub {k!r}: {v!r}")
    for name, sty in subs.styles.items():
        describe_style(name, sty)
    for k, v in subs.fonts_opaque.items():
        emit(f"  font {k!r} {v!r}")
    for k, v in subs.graphics_opaque.items():
        emit(f"  graphic {k!r} {v!r}")
    for i, ev in enumerate(subs.events):
        describe_event(i, ev)


def read_text(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8")


def run_op(st, words):
    op = words[0]
    a = [arg(x) for x in words[1:]]
    subs = st["subs"]
    if op == "load":
        path = a[0]
        fmt = a[1] if len(a) > 1 else None
        enc = a[2] if len(a) > 2 and a[2] is not None else "utf-8"
        errors = a[3] if len(a) > 3 else None
        kw = kwargs_of(words[5:])
        st["subs"] = SSAFile.load(path, encoding=enc, format_=fmt, errors=errors, **kw)
    elif op == "string":
        fmt = a[1] if len(a) > 1 else None
        st["subs"] = SSAFile.from_string(read_text(a[0]), fmt)
    elif op == "new":
        st["subs"] = SSAFile()
    elif op == "show":
        describe(subs)
    elif op == "tostr":
        text_block(subs.to_string(a[0], **kwargs_of(words[2:])))
    elif op == "save":
        path = a[0]
        fmt = a[1] if len(a) > 1 else None
        enc = a[2] if len(a) > 2 and a[2] is not None else "utf-8"
        errors = a[3] if len(a) > 3 else None
        subs.save(path, encoding=enc, format_=fmt, errors=errors, **kwargs_of(words[5:]))
    elif op == "shift":
        subs.shift(**kwargs_of(words[1:]))
    elif op == "tf":
        subs.transform_framerate(num(a[0]), num(a[1]))
    elif op == "rename":
        subs.rename_style(a[0], a[1])
    elif op == "import":
        other = SSAFile.load(a[0])
        subs.import_styles(other, overwrite=a[1] == "1")
    elif op == "equals":
        other = SSAFile.load(a[0])
        emit(f"  {subs.equals(other)}")
    elif op == "clean":
        subs.remove_miscellaneous_events()
    elif op == "sort":
        subs.sort()
    elif op == "textevents":
        for ev in subs.get_text_events():
            emit("  " + repr(ev))
    elif op == "get":
        emit("  " + repr(subs[int(a[0])]))
    elif op == "setplain":
        subs[int(a[0])].plaintext = a[1]
    elif op == "setdur":
        subs[int(a[0])].duration = int(a[1])
    elif op == "setcomment":
        subs[int(a[0])].is_comment = a[1] == "1"
    elif op == "del":
        del subs[int(a[0])]
    elif op == "insert":
        subs.insert(int(a[0]), SSAEvent(start=int(a[1]), end=int(a[2]), text=a[3]))
    elif op == "copyev":
        subs.append(subs[int(a[0])].copy())
    elif op == "evequals":
        emit(f"  {subs[int(a[0])].equals(subs[int(a[1])])}")
    elif op == "evcmp":
        x, y = subs[int(a[0])], subs[int(a[1])]
        emit(f"  == {x == y}, != {x != y}, < {x < y}, <= {x <= y}, > {x > y}, >= {x >= y}")
    elif op == "tsparse":
        m = ptime.TIMESTAMP.match(a[0])
        emit("  TIMESTAMP " + (f"{m.groups()!r} {ptime.timestamp_to_ms(m.groups())}" if m else "no match"))
        m = ptime.TIMESTAMP_SHORT.match(a[0])
        emit("  TIMESTAMP_SHORT " + (f"{m.groups()!r} {ptime.timestamp_to_ms(m.groups())}" if m else "no match"))
    elif op == "mt":
        emit(f"  {ptime.make_time(**kwargs_of(words[1:]))}")
    elif op == "mstostr":
        emit("  " + ptime.ms_to_str(num(a[0]), fractions=len(a) > 1))
    elif op == "mstotimes":
        emit(f"  {ptime.ms_to_times(num(a[0]))!r}")
    elif op == "ftoms":
        emit(f"  {ptime.frames_to_ms(int(a[0]), num(a[1]))}")
    elif op == "mstof":
        emit(f"  {ptime.ms_to_frames(int(a[0]), num(a[1]))}")
    elif op == "stamp":
        impl = {"ass": SubstationFormat, "srt": SubripFormat, "vtt": WebVTTFormat, "tmp": TmpFormat}[a[0]]
        emit("  " + impl.ms_to_timestamp(int(a[1])))
    elif op == "color":
        c = rgba_to_color(a[0])
        emit(f"  {c!r} {color_to_ass_rgba(c)} {color_to_ssa_rgb(c)}")
    elif op == "detect":
        text = read_text(a[0])
        try:
            emit("  " + formats.autodetect_format(text[:10000]))
        except FormatAutodetectionError as e:
            if e.formats:
                emit(f"  error FormatAutodetectionError: Multiple suitable formats ({sorted(e.formats)!r})")
            else:
                emit(f"  error FormatAutodetectionError: {e}")
    elif op == "ext":
        emit("  " + formats.get_file_extension(a[0]))
    elif op == "fmtid":
        emit("  " + formats.get_format_identifier(a[0]))
    elif op == "tags":
        styles = subs.styles if subs is not None else None
        for frag, sty in parse_tags(a[0], styles=styles, skip_empty_fragments=len(a) > 1):
            emit(f"  {frag!r} italic={sty.italic} bold={sty.bold} underline={sty.underline} strikeout={sty.strikeout}"
                 f" fontname={sty.fontname!r} drawing={sty.drawing} fontsize={sty.fontsize!r}")
    elif op == "align":
        al = Alignment.from_ssa_alignment(int(a[0]))
        emit(f"  {al!r} {al.to_ssa_alignment()}")
    elif op == "cli":
        out, err = io.StringIO(), io.StringIO()
        code = None
        ret = None
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                try:
                    ret = Pysubs2CLI()(a)
                except SystemExit as e:
                    code = e.code
        finally:
            for line in out.getvalue().splitlines():
                emit("  out|" + vis(line))
            for line in err.getvalue().splitlines():
                emit("  err|" + vis(line))
        if code is not None:
            emit(f"  exit {code}")
        else:
            emit(f"  return {ret}")
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
        st = {"subs": None}
        before = snapshot()
        for op in fields[3:]:
            words = op.split(" ")
            emit("> " + " ".join(shown(x) for x in words))
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                try:
                    run_op(st, words)
                except FormatAutodetectionError as e:
                    if e.formats:
                        emit(f"  error FormatAutodetectionError: Multiple suitable formats ({sorted(e.formats)!r})")
                    else:
                        emit(f"  error FormatAutodetectionError: {vis(str(e))}")
                except Exception as e:  # noqa: BLE001
                    emit(f"  error {type(e).__name__}: {vis(str(e))}")
            for wn in caught:
                emit(f"  warning {wn.category.__name__}: {vis(str(wn.message))}")
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
