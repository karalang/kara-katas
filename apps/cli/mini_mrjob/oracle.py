"""Reference for mini_mrjob (README.md is the spec). It runs every task in
order on one thread; the program's output must not depend on which worker
ran what or in which order the tasks finished.

Run from this directory, after mk.py: python3 -I -B oracle.py"""
import os
import sys

WORKERS = 4


def is_name(s):
    return 1 <= len(s) <= 32 and "a" <= s[0] <= "z" and all(
        "a" <= c <= "z" or "0" <= c <= "9" or c == "_" for c in s)


def number(s):
    d = s[1:] if s.startswith("-") else s
    if not d or len(d) > 9 or not all("0" <= c <= "9" for c in d):
        return None
    return int(s)


def words_of(line):
    body = line.split("#", 1)[0]
    return body.split()


# Values: ("int", n), ("text", s), ("list", [values]).
RANK = {"int": 0, "text": 1, "list": 2}


def key_of(v):
    if v[0] == "int":
        return (0, v[1])
    if v[0] == "text":
        return (1, v[1].encode("utf-8"))
    return (2, [key_of(x) for x in v[1]])


def json(v):
    if v[0] == "int":
        return str(v[1])
    if v[0] == "text":
        return '"' + v[1].replace("\\", "\\\\").replace('"', '\\"') + '"'
    return "[" + ",".join(json(x) for x in v[1]) + "]"


def kind(v):
    return {"int": "an int", "text": "text", "list": "a list"}[v[0]]


def fnv(s):
    h = 2166136261
    for b in s.encode("utf-8"):
        h ^= b
        h = (h * 16777619) % 4294967296
    return h


def tokens(text):
    out, cur = [], []
    for c in text:
        c = c.lower() if "A" <= c <= "Z" else c
        if "a" <= c <= "z":
            cur.append(c)
        elif cur:
            out.append("".join(cur))
            cur = []
    if cur:
        out.append("".join(cur))
    return out


class Fail(Exception):
    pass


MAPPERS = ["words", "bigrams", "lengths", "index", "pack", "first_letter", "total"]
REDUCERS = ["sum", "max", "count", "collect", "top3"]


def need_line(m, rec):
    if rec[0] != "line":
        raise Fail(f"TypeError: {m} expects a line, got a pair")


def need_pair(m, rec):
    if rec[0] != "pair":
        raise Fail(f"TypeError: {m} expects a pair, got a line")


def map_one(m, rec):
    if m in ("words", "bigrams", "lengths", "index"):
        need_line(m, rec)
        _, path, no, text = rec
        ws = tokens(text)
        if m == "words":
            return [(("text", w), ("int", 1)) for w in ws]
        if m == "bigrams":
            return [(("text", a + " " + b), ("int", 1)) for a, b in zip(ws, ws[1:])]
        if m == "lengths":
            return [(("int", len(w)), ("int", 1)) for w in ws]
        stem = path.rsplit("/", 1)[-1]
        if "." in stem:
            stem = stem[:stem.rindex(".")]
        return [(("text", w), ("text", f"{stem}:{no}")) for w in ws]
    need_pair(m, rec)
    _, k, v = rec
    if m == "pack":
        return [(("text", "all"), ("list", [v, k]))]
    if m == "total":
        return [(("text", "total"), v)]
    if k[0] != "text":
        raise Fail(f"TypeError: first_letter expects a text key, got {kind(k)}")
    return [(("text", k[1][:1]), v)]


def reduce_one(r, vals):
    if r in ("sum", "max"):
        for v in vals:
            if v[0] != "int":
                raise Fail(f"TypeError: {r} expects ints, got {kind(v)}")
        if r == "max":
            return ("int", max(v[1] for v in vals))
        t = 0
        for v in vals:
            t += v[1]
            if not -2**63 <= t < 2**63:
                raise Fail("OverflowError: sum does not fit in 64 bits")
        return ("int", t)
    if r == "count":
        return ("int", len(vals))
    s = sorted(vals, key=key_of)
    if r == "collect":
        out = []
        for v in s:
            if not out or key_of(out[-1]) != key_of(v):
                out.append(v)
        return ("list", out)
    return ("list", list(reversed(s))[:3])


def grouped(pairs):
    pairs = sorted(pairs, key=lambda p: key_of(p[0]))
    out = []
    for k, v in pairs:
        if out and key_of(out[-1][0]) == key_of(k):
            out[-1][1].append(v)
        else:
            out.append((k, [v]))
    return out


class Totals:
    tasks = 0
    records = 0
    failed = 0
    by_kind = {}


T = Totals()


def task_done(kind_, n_in, ok):
    T.tasks += 1
    T.records += n_in
    T.by_kind[kind_] = T.by_kind.get(kind_, 0) + 1
    if not ok:
        T.failed += 1


def map_task(step, chunk, reduces):
    m, c, _ = step
    try:
        out = []
        for rec in chunk:
            out += map_one(m, rec)
        emitted = len(out)
        if c is not None:
            out = [(k, reduce_one(c, vs)) for k, vs in grouped(out)]
        parts = [[] for _ in range(reduces)]
        for k, v in out:
            parts[fnv(json(k)) % reduces].append((k, v))
    except Fail as e:
        task_done("map", len(chunk), False)
        return None, str(e)
    task_done("map", len(chunk), True)
    return (emitted, parts), None


def reduce_task(step, pairs):
    _, _, r = step
    try:
        out = [(k, reduce_one(r, vs)) for k, vs in grouped(pairs)]
    except Fail as e:
        task_done("reduce", len(pairs), False)
        return None, str(e)
    task_done("reduce", len(pairs), True)
    return out, None


def chunks(recs, n):
    base, extra = divmod(len(recs), n)
    out, at = [], 0
    for i in range(n):
        size = base + (1 if i < extra else 0)
        out.append(recs[at:at + size])
        at += size
    return out


def step_name(step):
    m, c, r = step
    return f"{m}|{c}|{r}" if c is not None else f"{m}|{r}"


class Mr:
    def __init__(self):
        self.inputs = {}
        self.jobs = {}
        self.runs = {}

    def command(self, w):
        cmd = w[0]
        if cmd == "input":
            if len(w) < 3:
                raise Fail("usage: input <name> <path>...")
            name = w[1]
            if not is_name(name):
                raise Fail(f"bad name '{name}'")
            if name in self.inputs:
                raise Fail(f"input {name} already exists")
            recs = []
            for path in w[2:]:
                try:
                    with open(os.path.join("data", path), encoding="utf-8", newline="") as fh:
                        text = fh.read()
                except OSError:
                    raise Fail(f"cannot read {path}")
                lines = text.split("\n")
                if lines and lines[-1] == "":
                    lines.pop()
                for i, line in enumerate(lines):
                    recs.append(("line", path, i + 1, line))
            self.inputs[name] = recs
            files = len(w) - 2
            print(f"  {name}: {files} file{'' if files == 1 else 's'}, {len(recs)} lines")
        elif cmd == "job":
            if len(w) < 3:
                raise Fail("usage: job <name> <step>...")
            name = w[1]
            if not is_name(name):
                raise Fail(f"bad name '{name}'")
            if name in self.jobs:
                raise Fail(f"job {name} already exists")
            steps = []
            for s in w[2:]:
                parts = s.split("|")
                if len(parts) not in (2, 3):
                    raise Fail(f"bad step '{s}': want mapper|reducer or mapper|combiner|reducer")
                if parts[0] not in MAPPERS:
                    raise Fail(f"unknown mapper '{parts[0]}'")
                comb = None
                if len(parts) == 3:
                    comb = parts[1]
                    if comb not in ("sum", "max"):
                        raise Fail(f"bad combiner '{comb}': only sum and max can combine")
                if parts[-1] not in REDUCERS:
                    raise Fail(f"unknown reducer '{parts[-1]}'")
                steps.append((parts[0], comb, parts[-1]))
            self.jobs[name] = steps
            self.runs[name] = 0
            print(f"  {name}: {len(steps)} step{'' if len(steps) == 1 else 's'}")
        elif cmd == "run":
            if len(w) < 3:
                raise Fail("usage: run <job> <input> [maps=<n>] [reduces=<n>] [show=<n>]")
            job, inp = w[1], w[2]
            if job not in self.jobs:
                raise Fail(f"no job '{job}'")
            if inp not in self.inputs:
                raise Fail(f"no input '{inp}'")
            opts = {}
            for o in w[3:]:
                k, eq, v = o.partition("=")
                if not eq or k not in ("maps", "reduces", "show"):
                    raise Fail(f"unknown option '{o}'")
                if k in opts:
                    raise Fail(f"option {k} given twice")
                n = number(v)
                lo, hi = (0, 1000) if k == "show" else (1, 64)
                if n is None or not lo <= n <= hi:
                    raise Fail(f"bad value for {k}: '{v}'")
                opts[k] = n
            self.run(job, inp, opts.get("maps", 4), opts.get("reduces", 3), opts.get("show", 10))
        elif cmd == "jobs":
            if len(w) != 1:
                raise Fail("usage: jobs")
            for name in sorted(self.jobs):
                runs = self.runs[name]
                steps = " ".join(step_name(s) for s in self.jobs[name])
                print(f"  {name}: {steps} ({runs} run{'' if runs == 1 else 's'})")
        else:
            raise Fail(f"unknown command '{cmd}'")

    def run(self, job, inp, maps, reduces, show):
        self.runs[job] += 1
        print(f"  run {job} on {inp} (maps {maps}, reduces {reduces})")
        recs = self.inputs[inp]
        for si, step in enumerate(self.jobs[job]):
            head = f"  step {si + 1} {step_name(step)}"
            results = [map_task(step, ch, reduces) for ch in chunks(recs, maps)]
            bad = [(i, e) for i, (_, e) in enumerate(results) if e is not None]
            if bad:
                print(f"{head}: failed in map task {bad[0][0]}: {bad[0][1]}")
                return
            emitted = sum(r[0] for r, _ in results)
            combined = sum(len(p) for r, _ in results for p in r[1])
            ins = [[kv for r, _ in results for kv in r[1][p]] for p in range(reduces)]
            reds = [reduce_task(step, ins[p]) for p in range(reduces)]
            bad = [(i, e) for i, (_, e) in enumerate(reds) if e is not None]
            if bad:
                print(f"{head}: failed in reduce task {bad[0][0]}: {bad[0][1]}")
                return
            out = [kv for r, _ in reds for kv in r]
            comb = f", {combined} combined" if step[1] is not None else ""
            sizes = ", ".join(str(len(p)) for p in ins)
            print(f"{head}: map {len(recs)} in, {emitted} out{comb}; "
                  f"reduce [{sizes}] in, {len(out)} out")
            recs = [("pair", k, v) for k, v in out]
        print(f"  output: {len(recs)} record{'' if len(recs) == 1 else 's'}")
        for _, k, v in recs[:show]:
            print(f"    {json(k)}\t{json(v)}")
        if len(recs) > show:
            print(f"    ... {len(recs) - show} more")


def main():
    with open(os.path.join("data", "script.txt"), encoding="utf-8", newline="") as fh:
        text = fh.read()
    mr = Mr()
    print(f"== script ({WORKERS} workers)")
    for i, line in enumerate(text.split("\n")):
        w = words_of(line)
        if not w:
            continue
        print("> " + " ".join(w))
        try:
            mr.command(w)
        except Fail as e:
            print(f"  error: script.txt:{i + 1}: {e}")
    print("== end")
    print(f"  {len(mr.inputs)} inputs, {len(mr.jobs)} jobs")
    kinds = ", ".join(f"{k} {n}" for k, n in sorted(T.by_kind.items())) or "none"
    print(f"  {WORKERS} workers: {T.tasks} tasks, {T.records} records in, {T.failed} failed")
    print(f"  by kind: {kinds}")


main()
