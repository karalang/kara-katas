# The oracle for mini_logging: the same service script run through
# Python 3.13's real logging, logging.config.dictConfig and
# logging.handlers. Run from this directory after mk.py writes data/.
#
# The clock is a fake one the script advances with `tick`, so every
# timestamp is reproducible; times are shown in UTC. What the
# service writes to stderr is shown on stdout with a "stderr| " tag.
import calendar
import json
import logging
import logging.config
import logging.handlers
import os
import sys
import time

START = calendar.timegm((2026, 10, 15, 8, 0, 0, 0, 0, 0)) * 10**9
CLOCK = [START]
time.time_ns = lambda: CLOCK[0]
logging._startTime = START
logging.Formatter.converter = time.gmtime


class Tagged:
    """stderr, shown on stdout with each line tagged."""

    def __init__(self):
        self.bol = True

    def write(self, s):
        out = []
        for ch in s:
            if self.bol:
                out.append("stderr| ")
            out.append(ch)
            self.bol = ch == "\n"
        sys.stdout.write("".join(out))
        return len(s)

    def flush(self):
        sys.stdout.flush()


STDERR = Tagged()
sys.stderr = STDERR


def level_of(s):
    if s.isdigit():
        return int(s)
    return logging.getLevelNamesMapping()[s]


def show_error(e):
    print(f"  {type(e).__name__}: {e}")
    e = e.__cause__
    while e is not None:
        print(f"    from {type(e).__name__}: {e}")
        e = e.__cause__


def describe(h):
    name = h.name or "-"
    kind = type(h).__name__
    if isinstance(h, logging.FileHandler):
        detail = os.path.relpath(h.baseFilename)
    elif isinstance(h, logging.handlers.MemoryHandler):
        t = h.target.name if h.target is not None else "none"
        detail = f"{len(h.buffer)}/{h.capacity} to {t}"
    elif isinstance(h, logging.StreamHandler):
        detail = "stderr" if h.stream is STDERR else "stdout"
    else:
        detail = ""
    s = f"{name} ({kind}"
    if detail:
        s += f" {detail}"
    if h.level:
        s += f" at {logging.getLevelName(h.level)}"
    if h._closed:
        s += ", closed"
    return s + ")"


def show_logger(name, lg):
    if isinstance(lg, logging.PlaceHolder):
        print(f"  {name}: placeholder")
        return
    parts = [f"level {logging.getLevelName(lg.level)}"]
    if lg.level == 0:
        parts[0] += f" (effective {logging.getLevelName(lg.getEffectiveLevel())})"
    if not lg.propagate:
        parts.append("no propagate")
    if lg.disabled:
        parts.append("disabled")
    if lg.handlers:
        parts.append("handlers " + ", ".join(describe(h) for h in lg.handlers))
    if lg.filters:
        parts.append("filters " + ", ".join(repr(f.name) for f in lg.filters))
    print(f"  {name}: " + "; ".join(parts))


def tree():
    show_logger("root", logging.root)
    d = logging.root.manager.loggerDict
    for name in sorted(d):
        show_logger(name, d[name])


def run_line(line):
    if line.startswith("tick "):
        CLOCK[0] += int(line[5:]) * 10**6
        return
    print(f"> {line}")
    head, *fields = line.split(" | ")
    cmd, _, arg = head.partition(" ")
    if cmd == "log":
        level = level_of(fields[0])
        msg = fields[1]
        args = []
        extra = {}
        for f in fields[2:]:
            kind, v = f[0], f[2:]
            if kind == "s":
                args.append(v)
            elif kind == "i":
                args.append(int(v))
            elif kind == "f":
                args.append(float(v))
            else:
                k, _, val = v.partition("=")
                extra[k] = val
        try:
            logging.getLogger(arg).log(level, msg, *args, extra=extra or None)
        except Exception as e:
            show_error(e)
    elif cmd == "basic":
        kw = {}
        for f in fields:
            k, _, v = f.partition("=")
            if k == "force":
                kw["force"] = True
            elif k == "level":
                kw["level"] = v
            elif k == "stream":
                kw["stream"] = sys.stdout if v == "stdout" else STDERR
            else:
                kw[k] = v
        logging.basicConfig(**kw)
    elif cmd == "getlogger":
        logging.getLogger(arg)
    elif cmd == "config":
        with open(fields[0]) as f:
            cfg = json.load(f)
        try:
            logging.config.dictConfig(cfg)
        except Exception as e:
            show_error(e)
    elif cmd == "tree":
        tree()
    elif cmd == "enabled":
        lg = logging.getLogger(arg)
        names = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        print(f"  {arg}: " + " ".join(f"{n}={'yes' if lg.isEnabledFor(level_of(n)) else 'no'}" for n in names))
    elif cmd == "level":
        logging.getLogger(arg).setLevel(level_of(fields[0]))
    elif cmd == "disable":
        logging.disable(level_of(fields[0]))
    elif cmd == "addlevel":
        logging.addLevelName(int(fields[0]), fields[1])
    elif cmd == "shutdown":
        logging.shutdown()
    elif cmd == "files":
        for name in sorted(os.listdir("data/logs")):
            with open(f"data/logs/{name}", "rb") as f:
                data = f.read()
            print(f"  {name}: {len(data)} bytes")
            for l in data.decode("utf-8").splitlines():
                print(f"    {l}")


def main():
    with open("data/run.txt") as f:
        for line in f.read().splitlines():
            if line and not line.startswith("#"):
                run_line(line)


main()
