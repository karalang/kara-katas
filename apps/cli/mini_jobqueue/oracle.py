"""Reference implementation of mini_jobqueue (README.md is the spec).

Run from this directory after mk.py: python3 -I -B oracle.py"""
import os
import re

NAME = re.compile(r"[a-z0-9_]+\Z")
KEY = re.compile(r"[a-z_]+\Z")
DIGITS = re.compile(r"[0-9]{1,7}\Z")
DUR = re.compile(r"([0-9]{1,7})([smh]?)\Z")
TIME = re.compile(r"([0-9]{2}):([0-9]{2}):([0-9]{2})\Z")
STATES = ["executing", "available", "scheduled", "retryable", "completed", "discarded", "cancelled"]
FINAL = ("completed", "discarded", "cancelled")
LOG = "data/out/queue.log"


def fmt(t):
    return f"{t // 3600:02}:{t // 60 % 60:02}:{t % 60:02}"


def small(s, lo, hi):
    if not DIGITS.match(s):
        return None
    v = int(s)
    return v if lo <= v <= hi else None


def dur(s, lo):
    m = DUR.match(s)
    if not m:
        return None
    v = int(m.group(1)) * {"": 1, "s": 1, "m": 60, "h": 3600}[m.group(2)]
    return v if v >= lo else None


def attempt_list(s):
    if s == "none":
        return []
    out = []
    for p in s.split(","):
        a = small(p, 1, 25)
        if a is None:
            return None
        out.append(a)
    return out


def show_list(xs):
    if xs is None:
        return "-"
    if not xs:
        return "none"
    return ",".join(str(x) for x in xs)


def read_list(s):
    if s == "-":
        return None
    return attempt_list(s)


def fnv(s):
    h = 2166136261
    for b in s.encode():
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h


def lines_of(text):
    for i, raw in enumerate(text.split("\n")):
        line = raw.split("#", 1)[0].strip()
        if line:
            yield i + 1, line


class Err(Exception):
    pass


def parse_queues(text):
    queues, errors = {}, []
    for no, line in lines_of(text):
        try:
            t = line.split()
            if t[0] != "queue":
                raise Err(f"unknown directive '{t[0]}'")
            if len(t) < 2:
                raise Err("queue needs a name")
            name = t[1]
            if not NAME.match(name):
                raise Err(f"bad name '{name}'")
            limit, paused = None, False
            for f in t[2:]:
                if f.startswith("limit="):
                    limit = small(f[6:], 1, 100)
                    if limit is None:
                        raise Err(f"bad limit '{f[6:]}'")
                elif f == "paused":
                    paused = True
                else:
                    raise Err(f"unknown field '{f}'")
            if limit is None:
                raise Err(f"queue '{name}' needs limit")
            if name in queues:
                raise Err(f"duplicate queue '{name}'")
            queues[name] = (limit, paused)
        except Err as e:
            errors.append(f"error: queues.conf:{no}: {e}")
    return queues, errors


def parse_workers(text):
    workers, errors = {}, []
    for no, line in lines_of(text):
        try:
            t = line.split()
            if t[0] != "worker":
                raise Err(f"unknown directive '{t[0]}'")
            if len(t) < 2:
                raise Err("worker needs a kind")
            kind = t[1]
            if not NAME.match(kind):
                raise Err(f"bad name '{kind}'")
            w = {"duration": None, "timeout": None, "attempts": 5, "fail": [], "cancel_on": None, "error": "failed"}
            i = 2
            while i < len(t):
                f = t[i]
                k, _, v = f.partition("=")
                if k in ("duration", "timeout") and "=" in f:
                    d = dur(v, 1)
                    if d is None:
                        raise Err(f"bad duration '{v}'")
                    w[k] = d
                elif k == "attempts" and "=" in f:
                    a = small(v, 1, 25)
                    if a is None:
                        raise Err(f"bad attempts '{v}'")
                    w["attempts"] = a
                elif k == "fail" and "=" in f:
                    xs = attempt_list(v)
                    if xs is None:
                        raise Err(f"bad attempt list '{v}'")
                    w["fail"] = xs
                elif k == "cancel_on" and "=" in f:
                    a = small(v, 1, 25)
                    if a is None:
                        raise Err(f"bad attempt '{v}'")
                    w["cancel_on"] = a
                elif k == "error" and "=" in f:
                    msg = " ".join([v] + t[i + 1:]).strip()
                    if not msg:
                        raise Err("bad error")
                    w["error"] = msg
                    break
                else:
                    raise Err(f"unknown field '{f}'")
                i += 1
            if w["duration"] is None:
                raise Err(f"worker '{kind}' needs duration")
            if kind in workers:
                raise Err(f"duplicate worker '{kind}'")
            workers[kind] = w
        except Err as e:
            errors.append(f"error: workers.conf:{no}: {e}")
    return workers, errors


def parse_events(text):
    evs = []
    for no, line in lines_of(text):
        t = line.split()
        m = TIME.match(t[0])
        if not m or int(m.group(2)) >= 60 or int(m.group(3)) >= 60:
            evs.append((no, line, None, f"bad time '{t[0]}'", []))
        elif len(t) == 1:
            evs.append((no, line, None, "missing command", []))
        else:
            at = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            evs.append((no, line, at, None, t[1:]))
    return evs


class Job:
    def __init__(self, id, queue, kind, prio, max, due, at, fail, args):
        self.id, self.queue, self.kind, self.prio, self.max = id, queue, kind, prio, max
        self.due, self.inserted, self.fail, self.args = due, at, fail, args
        self.state = "scheduled" if due > at else "available"
        self.attempt, self.end, self.finished, self.error = 0, -1, -1, ""

    def snap(self):
        args = " ".join(f"{k}={v}" for k, v in self.args)
        return (f"{self.id} {self.queue} {self.kind} {self.state} {self.attempt} {self.max} {self.prio} "
                f"{self.due} {self.end} {self.finished} {self.inserted} {show_list(self.fail)} [{args}] {self.error}")


class Engine:
    def __init__(self, queues, workers):
        self.conf, self.workers = queues, workers
        self.reset()
        self.now, self.down, self.out = 0, False, []

    def reset(self):
        self.queues = {q: [lim, p] for q, (lim, p) in self.conf.items()}
        self.jobs, self.log, self.next_id = {}, [], 1

    # ---- records
    def apply(self, rec):
        t = rec.split(" ")
        k = t[0]
        if k == "insert":
            args = [tuple(a.split("=", 1)) for a in t[9:]]
            j = Job(int(t[1]), t[2], t[3], int(t[4]), int(t[5]), int(t[6]), int(t[7]), read_list(t[8]), args)
            self.jobs[j.id] = j
            self.next_id = max(self.next_id, j.id + 1)
        elif k == "ids":
            self.next_id = max(self.next_id, int(t[1]))
        elif k in ("pause", "resume"):
            self.queues[t[1]][1] = k == "pause"
        elif k == "scale":
            self.queues[t[1]][0] = int(t[2])
        else:
            j = self.jobs[int(t[1])]
            at = int(t[2])
            rest = " ".join(t[4:])
            if k == "start":
                j.state, j.attempt, j.end = "executing", j.attempt + 1, int(t[3])
            elif k == "complete":
                j.state, j.finished = "completed", at
            elif k == "retry":
                j.state, j.due, j.error = "retryable", int(t[3]), rest
            elif k in ("discard", "cancel"):
                j.state = "discarded" if k == "discard" else "cancelled"
                j.finished, j.error = at, " ".join(t[3:])
            elif k == "requeue":
                j.state, j.due, j.max, j.finished = "available", at, int(t[3]), -1
            elif k == "rescue":
                j.state, j.due = "available", at

    def emit(self, rec):
        self.log.append(rec)
        self.apply(rec)

    def text(self):
        return "".join(r + "\n" for r in self.log)

    def write(self):
        with open(LOG, "w", encoding="utf-8", newline="") as fh:
            fh.write(self.text())

    # ---- engine
    def say(self, s):
        self.out.append(f"{fmt(self.now)} {s}")

    def next_time(self):
        ts = [j.end for j in self.jobs.values() if j.state == "executing"]
        ts += [j.due for j in self.jobs.values() if j.state in ("scheduled", "retryable")]
        return min(ts) if ts else None

    def advance(self, t):
        if not self.down:
            while True:
                n = self.next_time()
                if n is None or n > t:
                    break
                self.now = n
                self.step()
        self.now = t

    def promote(self):
        for j in self.jobs.values():
            if j.state in ("scheduled", "retryable") and j.due <= self.now:
                j.state = "available"

    def step(self):
        for id in sorted(self.jobs):
            j = self.jobs[id]
            if j.state == "executing" and j.end == self.now:
                self.finish(j)
        self.promote()
        for q in sorted(self.queues):
            limit, paused = self.queues[q]
            if paused:
                continue
            running = sum(1 for j in self.jobs.values() if j.queue == q and j.state == "executing")
            avail = sorted((j for j in self.jobs.values() if j.queue == q and j.state == "available"),
                           key=lambda j: (j.prio, j.due, j.id))
            for j in avail:
                if running >= limit:
                    break
                self.start(j)
                running += 1

    def length(self, w):
        if w["timeout"] is not None and w["duration"] > w["timeout"]:
            return w["timeout"]
        return w["duration"]

    def start(self, j):
        w = self.workers[j.kind]
        self.emit(f"start {j.id} {self.now} {self.now + self.length(w)}")
        self.say(f"start #{j.id} {j.kind} on {j.queue} (attempt {j.attempt})")

    def finish(self, j):
        w = self.workers[j.kind]
        a = j.attempt
        fails = j.fail if j.fail is not None else w["fail"]
        if w["timeout"] is not None and w["duration"] > w["timeout"]:
            self.fail(j, f"timeout after {w['timeout']}s")
        elif w["cancel_on"] == a:
            self.emit(f"cancel {j.id} {self.now} cancelled by worker")
            self.say(f"cancel #{j.id} {j.kind} attempt {a}: cancelled by worker")
        elif a in fails:
            self.fail(j, w["error"])
        else:
            self.emit(f"complete {j.id} {self.now}")
            self.say(f"done #{j.id} {j.kind} (attempt {a})")

    def fail(self, j, err):
        a = j.attempt
        if a >= j.max:
            self.emit(f"discard {j.id} {self.now} {err}")
            self.say(f"fail #{j.id} {j.kind} attempt {a}: {err}; discarded")
        else:
            c = a - 1
            due = self.now + c ** 4 + 15 + (fnv(f"{j.id}-{a}") % 10) * (c + 1)
            self.emit(f"retry {j.id} {self.now} {due} {err}")
            self.say(f"fail #{j.id} {j.kind} attempt {a}: {err}; retry at {fmt(due)}")

    def snapshot(self):
        out = [f"next {self.next_id}"]
        out += [f"queue {q} {l} {p}" for q, (l, p) in sorted(self.queues.items())]
        out += [self.jobs[i].snap() for i in sorted(self.jobs)]
        return out

    # ---- commands
    def queue(self, q):
        if q not in self.queues:
            raise Err(f"unknown queue '{q}'")
        return self.queues[q]

    def job(self, s):
        id = small(s, 1, 9999999)
        if id is None:
            raise Err(f"bad job id '{s}'")
        if id not in self.jobs:
            raise Err(f"no job {id}")
        return self.jobs[id]

    def command(self, t):
        cmd, a = t[0], t[1:]
        known = ("enqueue", "pause", "resume", "scale", "cancel", "retry", "crash", "recover",
                 "prune", "stats", "jobs", "drain")
        if cmd not in known:
            raise Err(f"unknown command '{cmd}'")
        if self.down and cmd != "recover":
            raise Err("queue is down")
        getattr(self, "c_" + cmd)(a)

    def usage(self, a, n, u):
        if len(a) != n:
            raise Err(f"usage: {u}")

    def c_enqueue(self, a):
        if len(a) < 2:
            raise Err("usage: enqueue QUEUE KIND [OPTIONS]")
        q, kind = a[0], a[1]
        self.queue(q)
        if kind not in self.workers:
            raise Err(f"unknown kind '{kind}'")
        w = self.workers[kind]
        prio, delay, mx, uniq, fail, args = 0, 0, w["attempts"], None, None, {}
        for f in a[2:]:
            if "=" not in f:
                raise Err(f"bad argument '{f}'")
            k, v = f.split("=", 1)
            if k == "priority":
                prio = small(v, 0, 9)
                if prio is None:
                    raise Err(f"bad priority '{v}'")
            elif k in ("in", "unique"):
                d = dur(v, 0 if k == "in" else 1)
                if d is None:
                    raise Err(f"bad duration '{v}'")
                if k == "in":
                    delay = d
                else:
                    uniq = d
            elif k == "max_attempts":
                mx = small(v, 1, 25)
                if mx is None:
                    raise Err(f"bad max_attempts '{v}'")
            elif k == "fail":
                fail = attempt_list(v)
                if fail is None:
                    raise Err(f"bad attempt list '{v}'")
            else:
                if not KEY.match(k) or not v:
                    raise Err(f"bad argument '{f}'")
                if k in args:
                    raise Err(f"duplicate argument '{k}'")
                args[k] = v
        args = sorted(args.items())
        if uniq is not None:
            for id in sorted(self.jobs):
                j = self.jobs[id]
                if (j.queue == q and j.kind == kind and j.args == args and j.inserted >= self.now - uniq
                        and j.state not in ("cancelled", "discarded")):
                    self.out.append(f"duplicate of #{id}")
                    return
        id = self.next_id
        due = self.now + delay
        rest = "".join(f" {k}={v}" for k, v in args)
        self.emit(f"insert {id} {q} {kind} {prio} {mx} {due} {self.now} {show_list(fail)}{rest}")
        if delay > 0:
            self.out.append(f"scheduled #{id} {kind} on {q} at {fmt(due)}")
        else:
            self.out.append(f"enqueued #{id} {kind} on {q}")

    def c_pause(self, a):
        self.usage(a, 1, "pause QUEUE")
        if self.queue(a[0])[1]:
            raise Err(f"queue '{a[0]}' is already paused")
        self.emit(f"pause {a[0]}")
        self.out.append(f"paused {a[0]}")

    def c_resume(self, a):
        self.usage(a, 1, "resume QUEUE")
        if not self.queue(a[0])[1]:
            raise Err(f"queue '{a[0]}' is not paused")
        self.emit(f"resume {a[0]}")
        self.out.append(f"resumed {a[0]}")

    def c_scale(self, a):
        self.usage(a, 2, "scale QUEUE N")
        old = self.queue(a[0])[0]
        n = small(a[1], 1, 100)
        if n is None:
            raise Err(f"bad limit '{a[1]}'")
        self.emit(f"scale {a[0]} {n}")
        self.out.append(f"scaled {a[0]} {old} -> {n}")

    def c_cancel(self, a):
        self.usage(a, 1, "cancel ID")
        j = self.job(a[0])
        if j.state in FINAL:
            raise Err(f"job {j.id} is {j.state}")
        was = j.state
        self.emit(f"cancel {j.id} {self.now} cancelled by user")
        self.out.append(f"cancelled #{j.id} {j.kind} (was {was})")

    def c_retry(self, a):
        self.usage(a, 1, "retry ID")
        j = self.job(a[0])
        if j.state not in ("discarded", "cancelled"):
            raise Err(f"job {j.id} is {j.state}, not discarded or cancelled")
        mx = j.max if j.attempt < j.max else j.attempt + 1
        self.emit(f"requeue {j.id} {self.now} {mx}")
        self.out.append(f"retrying #{j.id} {j.kind} (attempt {j.attempt + 1} of {mx})")

    def c_crash(self, a):
        if a not in ([], ["torn"]):
            raise Err("usage: crash [torn]")
        self.write()
        data = self.text().encode()
        if a:
            last = len(self.log[-1]) + 1 if self.log else 0
            cut = len(data) - (last + 1) // 2
            with open(LOG, "wb") as fh:
                fh.write(data[:cut])
            self.out.append(f"crashed mid-write (log cut from {len(data)} to {cut} bytes)")
        else:
            self.out.append(f"crashed (log {len(data)} bytes)")
        self.reset()
        self.down = True

    def c_recover(self, a):
        self.usage(a, 0, "recover")
        if not self.down:
            raise Err("queue is not down")
        self.down = False
        self.reset()
        with open(LOG, encoding="utf-8", newline="") as fh:
            parts = fh.read().split("\n")
        torn = parts.pop()
        for r in parts:
            self.log.append(r)
            self.apply(r)
        msg = f"recovered {len(parts)} records"
        if torn:
            msg += f", dropped a torn record of {len(torn.encode())} bytes"
        self.out.append(msg)
        for id in sorted(self.jobs):
            j = self.jobs[id]
            if j.state != "executing":
                continue
            if j.attempt >= j.max:
                self.emit(f"discard {id} {self.now} rescued after crash")
                self.out.append(f"discarded #{id} {j.kind} (rescued after crash)")
            else:
                self.emit(f"rescue {id} {self.now}")
                self.out.append(f"rescued #{id} {j.kind} (attempt {j.attempt} of {j.max})")

    def c_prune(self, a):
        self.usage(a, 1, "prune AGE")
        age = dur(a[0], 0)
        if age is None:
            raise Err(f"bad duration '{a[0]}'")
        gone = {i for i, j in self.jobs.items() if j.state in FINAL and j.finished <= self.now - age}
        before = len(self.text().encode())
        for i in gone:
            del self.jobs[i]
        keep = [f"ids {self.next_id}"]
        for r in self.log:
            t = r.split(" ")
            if t[0] == "ids":
                continue
            if t[0] not in ("pause", "resume", "scale") and int(t[1]) in gone:
                continue
            keep.append(r)
        self.log = keep
        self.out.append(f"pruned {len(gone)} jobs, log {before} -> {len(self.text().encode())} bytes")

    def stats(self):
        for q in sorted(self.queues):
            limit, paused = self.queues[q]
            n = {s: 0 for s in STATES}
            for j in self.jobs.values():
                if j.queue == q:
                    n[j.state] += 1
            body = ", ".join(f"{s} {n[s]}" for s in STATES)
            self.out.append(f"{q} limit={limit}{' paused' if paused else ''}: {body}")

    def c_stats(self, a):
        self.usage(a, 0, "stats")
        self.stats()

    def c_jobs(self, a):
        self.usage(a, 1, "jobs STATE")
        s = a[0]
        if s != "all" and s not in STATES:
            raise Err(f"bad state '{s}'")
        n = 0
        for i in sorted(self.jobs):
            j = self.jobs[i]
            if s != "all" and j.state != s:
                continue
            line = f"#{j.id} {j.state} {j.kind} {j.queue} {j.attempt}/{j.max}"
            if j.state in ("scheduled", "retryable"):
                line += f" next={fmt(j.due)}"
            for k, v in j.args:
                line += f" {k}={v}"
            if j.error:
                line += f" ({j.error})"
            self.out.append(line)
            n += 1
        if n == 0:
            self.out.append("no jobs")

    def c_drain(self, a):
        self.usage(a, 0, "drain")
        while True:
            n = self.next_time()
            if n is None:
                break
            self.now = n
            self.step()
        self.out.append(f"drained at {fmt(self.now)}")


def read(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return fh.read()


def main():
    os.makedirs("data/out", exist_ok=True)
    queues, qerr = parse_queues(read("data/queues.conf"))
    workers, werr = parse_workers(read("data/workers.conf"))
    evs = parse_events(read("data/events.txt"))
    e = Engine(queues, workers)
    out = e.out
    out.append("== load")
    out.append(f"queues.conf: {len(queues)} queues")
    out += qerr
    out.append(f"workers.conf: {len(workers)} workers")
    out += werr
    out.append(f"events.txt: {len(evs)} events")
    out.append("== events")
    e.write()
    for no, line, at, err, toks in evs:
        if err is None and at < e.now:
            err = "time goes back"
        if err is None:
            e.advance(at)
        out.append(f"> {line}")
        if err is None:
            try:
                e.command(toks)
            except Err as x:
                err = str(x)
        if err is not None:
            out.append(f"error: events.txt:{no}: {err}")
        if not e.down:
            e.step()
            e.write()
    out.append("== end")
    if e.down:
        out.append("queue is down")
    else:
        e.stats()
    back = read(LOG)
    recs = [r for r in back.split("\n") if r]
    out.append("== log")
    out.append(f"{LOG}: {len(recs)} records, {len(back.encode())} bytes")
    per = {}
    for r in recs:
        k = r.split(" ")[0]
        per[k] = per.get(k, 0) + 1
    out.append(", ".join(f"{k} {v}" for k, v in sorted(per.items())))
    if e.down:
        out.append("replay: skipped, queue is down")
    else:
        r = Engine(queues, workers)
        for rec in recs:
            r.apply(rec)
        r.now = e.now
        r.promote()
        mine, theirs = e.snapshot(), r.snapshot()
        if mine == theirs:
            out.append(f"replay: {len(r.jobs)} jobs, matches memory")
        else:
            i = 0
            while i < len(mine) and i < len(theirs) and mine[i] == theirs[i]:
                i += 1
            out.append(f"replay differs at entry {i + 1}")
    print("\n".join(out))


main()
