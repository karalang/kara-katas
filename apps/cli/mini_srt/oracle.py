# Runs data/jobs.tsv through srt 3.5.3 (srt.py and the srt_tools scripts
# next to this file, unchanged) and prints what it did. mini_srt.kara must
# print the same bytes.
#
# A `tool` job runs the srt_tools script itself, with its own argument
# parser, on files in data/, writing to data/out.srt; the job prints what
# the script wrote. The other jobs call the library.
import datetime
import importlib.machinery
import logging
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, HERE)

import srt  # noqa: E402

OUT = []


def emit(s):
    OUT.append(s + "\n")


class Capture(logging.Handler):
    def emit(self, record):
        emit("! %s:%s:%s" % (record.levelname, record.name, record.getMessage()))


root = logging.getLogger()
root.addHandler(Capture())
root.setLevel(logging.INFO)


def raw(text):
    OUT.append(text)
    if text and not text.endswith("\n"):
        OUT.append("\n\\ no newline at end\n")


def unescape(s):
    return s.replace("\\n", "\n")


def err(e):
    return "error: %s: %s" % (type(e).__name__, e)


def read(rel):
    with open(os.path.join(DATA, rel), "rb") as f:
        return f.read().decode("utf-8-sig")


def parse_job(args):
    try:
        for sub in srt.parse(read(args[0]), ignore_errors="ignore" in args[1:]):
            emit(repr(sub))
    except Exception as e:
        emit(err(e))


def compose_job(args):
    opts = dict(a.split("=", 1) for a in args[1:])
    subs = list(srt.parse(read(args[0])))
    if "shift" in opts:
        d = datetime.timedelta(seconds=float(opts["shift"]))
        for s in subs:
            s.start += d
            s.end += d
    raw(srt.compose(
        subs,
        reindex=opts.get("reindex") != "no",
        start_index=int(opts.get("start", "1")),
        strict=opts.get("strict") != "no",
        eol="\r\n" if opts.get("eol") == "crlf" else None,
    ))


def ts_job(args):
    try:
        d = srt.srt_timestamp_to_timedelta(args[0])
        emit("%r %s" % (d, srt.timedelta_to_srt_timestamp(d)))
    except Exception as e:
        emit(err(e))


def legal_job(args):
    emit(repr(srt.make_legal_content(unescape(args[0]) if args else "")))


def tool_job(args):
    name = args[0]
    argv = list(args[1:])
    encoding = "utf-8"
    if "-e" in argv:
        encoding = argv[argv.index("-e") + 1]
    inplace = "-p" in argv
    target = "out.srt"
    if inplace:
        target = argv[argv.index("-i") + 1]
    else:
        argv += ["-o", target]
    path = os.path.join(HERE, "srt_tools", "srt-" + name)
    loader = importlib.machinery.SourceFileLoader("srt_tool_" + name.replace("-", "_"), path)
    mod = loader.load_module()
    sys.argv = ["srt-" + name] + argv
    cwd = os.getcwd()
    os.chdir(DATA)
    try:
        mod.main()
    except Exception as e:
        emit(err(e))
        return
    finally:
        os.chdir(cwd)
    with open(os.path.join(DATA, target), "rb") as f:
        raw(f.read().decode(encoding))
    if not inplace:
        os.remove(os.path.join(DATA, target))


def main():
    with open(os.path.join(DATA, "jobs.tsv"), encoding="utf-8") as f:
        jobs = [line.rstrip("\n").split("\t") for line in f]
    for job in jobs:
        emit("== " + " ".join(job))
        kind, args = job[0], job[1:]
        if kind == "parse":
            parse_job(args)
        elif kind == "compose":
            compose_job(args)
        elif kind == "ts":
            ts_job(args)
        elif kind == "legal":
            legal_job(args)
        else:
            tool_job(args)
    sys.stdout.write("".join(OUT))


main()
