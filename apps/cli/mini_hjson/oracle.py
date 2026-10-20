# Runs data/jobs.tsv through hjson-py 3.1.0 (the hjson/ package next to
# this file, unchanged) and prints what it did. mini_hjson.kara must print
# the same bytes.
#
# An `hjson` job runs the package's own command-line tool, hjson/tool.py,
# with those arguments in data/, and prints what it wrote to stdout, each
# stderr line after "stderr: ", and the SystemExit it raised. A `dumps`
# job loads a file with use_decimal=True and prints hjson.dumps or
# hjson.dumpsJSON with the options named. A `roundtrip` job checks that
# dumps(loads(dumps(x))) and dumpsJSON(loads(dumpsJSON(x))) give the same
# text again.
import io
import os
import sys

if os.environ.get("PYTHONUTF8") != "1":
    os.environ["PYTHONUTF8"] = "1"
    os.execv(sys.executable, [sys.executable] + sys.argv)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, HERE)

import hjson  # noqa: E402
import hjson.tool  # noqa: E402

OUT = []


def emit(s):
    OUT.append(s + "\n")


class Keep(io.StringIO):
    def close(self):
        pass


def crash(e):
    return "crash: %s: %s" % (type(e).__name__, e)


def tool_job(args):
    out, err = Keep(), Keep()
    real = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out, err
    sys.argv = ["hjson"] + args
    status = None
    try:
        hjson.tool.main()
    except SystemExit as e:
        status = "exit: %s" % (e.code,)
    except Exception as e:
        status = crash(e)
    finally:
        sys.stdout, sys.stderr = real
    OUT.append(out.getvalue())
    for line in err.getvalue().split("\n")[:-1]:
        emit("stderr: " + line)
    if status is not None:
        emit(status)


def load(rel):
    with open(os.path.join(DATA, rel), "r") as f:
        return hjson.loads(f.read(), use_decimal=True)


def encode(obj, opts):
    kw = {"ensure_ascii": "ensure_ascii" in opts, "sort_keys": "sort_keys" in opts}
    for o in opts:
        if o.startswith("indent="):
            kw["indent"] = int(o.split("=")[1])
    if "json" in opts:
        return hjson.dumpsJSON(obj, **kw)
    return hjson.dumps(obj, **kw)


def dumps_job(args):
    try:
        emit(encode(load(args[0]), args[1:]))
    except Exception as e:
        emit(crash(e))


def roundtrip_job(args):
    try:
        obj = load(args[0])
    except Exception as e:
        emit(crash(e))
        return
    h1 = hjson.dumps(obj)
    h2 = hjson.dumps(hjson.loads(h1, use_decimal=True))
    emit("hjson: " + ("stable" if h1 == h2 else "changed"))
    if h1 != h2:
        emit(h2)
    j1 = hjson.dumpsJSON(obj)
    j2 = hjson.dumpsJSON(hjson.loads(j1, use_decimal=True))
    emit("json: " + ("stable" if j1 == j2 else "changed"))
    emit(j1)


def main():
    with open(os.path.join(DATA, "jobs.tsv"), encoding="utf-8") as f:
        jobs = [line.rstrip("\n").split("\t") for line in f]
    os.chdir(DATA)
    for job in jobs:
        emit("== " + " ".join(job))
        kind, args = job[0], job[1:]
        if kind == "hjson":
            tool_job(args)
        elif kind == "dumps":
            dumps_job(args)
        else:
            roundtrip_job(args)
    sys.stdout.write("".join(OUT))


main()
