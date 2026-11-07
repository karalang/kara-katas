"""Reference for mini_rq. Reads data/script.txt (as mk.py writes it) and
prints the report the Kāra program must print. The jobs run in order here;
the program runs them on a pool of workers, and its output does not depend
on which worker ran what.

Run from this directory: python3 -I -B oracle.py"""

OUT = []
WORKERS = 3
DEFAULT_TIMEOUT = 180
DEFAULT_TTL = 500
FIB_MAX = 90
PRIMES_MAX = 1000000

FUNCS = {
    "add": "add <a> <b>",
    "fib": "fib <n>",
    "words": "words <word>...",
    "echo": "echo <word>...",
    "flaky": "flaky <n>",
    "slow": "slow <seconds>",
    "primes": "primes <n>",
    "boom": "boom",
}


def say(s):
    OUT.append(s)


class Fail(Exception):
    pass


def is_name(s):
    return (0 < len(s) <= 32 and "a" <= s[0] <= "z"
            and all(c == "_" or "a" <= c <= "z" or "0" <= c <= "9" for c in s))


def number(s):
    """An optional `-` and 1 to 9 digits."""
    d = s[1:] if s.startswith("-") else s
    if not (0 < len(d) <= 9 and all("0" <= c <= "9" for c in d)):
        return None
    return int(s)


def count(s, lo, hi):
    """A number from lo to hi, written without a sign."""
    n = number(s)
    if n is None or s.startswith("-") or not lo <= n <= hi:
        return None
    return n


def args_ok(func, args):
    if func == "add":
        return len(args) == 2 and all(number(a) is not None for a in args)
    if func in ("fib", "flaky", "slow", "primes"):
        return len(args) == 1 and count(args[0], 0, 999999999) is not None
    if func in ("words", "echo"):
        return len(args) >= 1
    return not args  # boom


# ------------------------------------------------------------ what a worker does


def perform(func, args, attempt, timeout):
    """(ok, text)"""
    if func == "add":
        return True, str(int(args[0]) + int(args[1]))
    if func == "fib":
        n = int(args[0])
        if n > FIB_MAX:
            return False, f"ValueError: fib({n}) does not fit in 64 bits"
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return True, str(a)
    if func == "words":
        return True, f"{len(args)} words"
    if func == "echo":
        return True, " ".join(args)
    if func == "flaky":
        k = int(args[0])
        if attempt < k:
            return False, f"FlakyError: attempt {attempt} of {k}"
        return True, f"ok on attempt {attempt}"
    if func == "slow":
        t = int(args[0])
        if t > timeout:
            return False, f"JobTimeoutException: Task exceeded maximum timeout value ({timeout} seconds)"
        return True, f"slept {t}s"
    if func == "primes":
        n = int(args[0])
        if n > PRIMES_MAX:
            return False, f"ValueError: primes below {n} is too many"
        sieve = bytearray([1]) * max(n, 2)
        sieve[0] = sieve[1] = 0
        i = 2
        while i * i < n:
            if sieve[i]:
                for k in range(i * i, n, i):
                    sieve[k] = 0
            i += 1
        return True, f"{sum(sieve[:n])} primes below {n}"
    return False, "ZeroDivisionError: division by zero"


# ------------------------------------------------------------ the queue


class Job:
    def __init__(self, jid, queue, func, args):
        self.id = jid
        self.queue = queue
        self.func = func
        self.args = args
        self.depends = []
        self.retry = 0
        self.retries_left = 0
        self.backoff = []
        self.timeout = DEFAULT_TIMEOUT
        self.ttl = DEFAULT_TTL
        self.status = "queued"
        self.attempt = 1
        self.result = None
        self.error = None
        self.due = 0
        self.expires = 0


class Rq:
    def __init__(self):
        self.queues = []          # names, priority order
        self.items = {}           # queue -> [job id]
        self.jobs = []            # creation order
        self.by_id = {}
        self.scheduled = []       # [(due, seq, id)]
        self.seq = 0
        self.clock = 0
        self.runs = 0
        self.failures = 0
        self.by_func = {}

    def job(self, jid):
        if jid not in self.by_id:
            raise Fail(f"no job '{jid}'")
        return self.by_id[jid]

    def deps_done(self, j):
        return all(self.by_id[d].status in ("finished", "expired") for d in j.depends)

    def schedule(self, j, due):
        j.status = "scheduled"
        j.due = due
        self.scheduled.append((due, self.seq, j.id))
        self.seq += 1

    def unschedule(self, j):
        self.scheduled = [s for s in self.scheduled if s[2] != j.id]

    # -------------------------------------------------- script commands

    def queue(self, w):
        if len(w) != 2:
            raise Fail("usage: queue <name>")
        if not is_name(w[1]):
            raise Fail(f"bad queue name '{w[1]}'")
        if w[1] in self.items:
            raise Fail(f"queue {w[1]} already exists")
        self.queues.append(w[1])
        self.items[w[1]] = []

    def build(self, w, scheduled):
        """A job from `<queue> <id> <func> [args] [options]`."""
        if len(w) < 3:
            raise Fail("usage: enqueue <queue> <id> <func> [args] [options]")
        q, jid, func = w[0], w[1], w[2]
        if q not in self.items:
            raise Fail(f"no queue '{q}'")
        if not is_name(jid):
            raise Fail(f"bad job id '{jid}'")
        if jid in self.by_id:
            raise Fail(f"job {jid} already exists")
        if func not in FUNCS:
            raise Fail(f"unknown function '{func}'")
        args, opts, front = [], {}, False
        for t in w[3:]:
            if t == "at_front":
                front = True
            elif "=" in t:
                k, _, v = t.partition("=")
                if k not in ("depends_on", "retry", "backoff", "timeout", "ttl"):
                    raise Fail(f"unknown option '{k}'")
                if k in opts:
                    raise Fail(f"duplicate option {k}")
                opts[k] = v
            else:
                args.append(t)
        if not args_ok(func, args):
            raise Fail(f"bad arguments for {func}: {FUNCS[func]}")
        j = Job(jid, q, func, args)
        if "retry" in opts:
            n = count(opts["retry"], 0, 9)
            if n is None:
                raise Fail(f"bad retry '{opts['retry']}'")
            j.retry = j.retries_left = n
        if "backoff" in opts:
            parts = opts["backoff"].split(",")
            ns = [count(p, 1, 9999) for p in parts]
            if None in ns:
                raise Fail(f"bad backoff '{opts['backoff']}'")
            if "retry" not in opts:
                raise Fail("backoff needs retry")
            j.backoff = ns
        for k in ("timeout", "ttl"):
            if k in opts:
                n = count(opts[k], 1, 9999)
                if n is None:
                    raise Fail(f"bad {k} '{opts[k]}'")
                setattr(j, k, n)
        if "depends_on" in opts:
            if scheduled:
                raise Fail("depends_on is not allowed with enqueue_in")
            for d in opts["depends_on"].split(","):
                if d not in self.by_id:
                    raise Fail(f"no job '{d}'")
                if d in j.depends:
                    raise Fail(f"duplicate dependency {d}")
                j.depends.append(d)
        return j, front

    def add(self, j):
        self.jobs.append(j)
        self.by_id[j.id] = j

    def enqueue(self, w):
        j, front = self.build(w[1:], False)
        self.add(j)
        if not self.deps_done(j):
            j.status = "deferred"
            waiting = [d for d in j.depends if self.by_id[d].status not in ("finished", "expired")]
            say(f"  {j.id}: deferred on {j.queue} until {', '.join(waiting)} finish")
            return
        if front:
            self.items[j.queue].insert(0, j.id)
        else:
            self.items[j.queue].append(j.id)
        say(f"  {j.id}: queued on {j.queue}" + (" at the front" if front else ""))

    def enqueue_in(self, w):
        if len(w) < 2:
            raise Fail("usage: enqueue_in <seconds> <queue> <id> <func> [args] [options]")
        delay = count(w[1], 1, 99999)
        if delay is None:
            raise Fail(f"bad delay '{w[1]}'")
        j, _ = self.build(w[2:], True)
        self.add(j)
        self.schedule(j, self.clock + delay)
        say(f"  {j.id}: scheduled on {j.queue} for {j.due}")

    def cancel(self, w):
        if len(w) != 2:
            raise Fail("usage: cancel <id>")
        j = self.job(w[1])
        if j.status not in ("queued", "scheduled", "deferred"):
            raise Fail(f"job {j.id} is {j.status}")
        if j.status == "queued":
            self.items[j.queue].remove(j.id)
        if j.status == "scheduled":
            self.unschedule(j)
        j.status = "canceled"
        say(f"  canceled {j.id}")

    def requeue(self, w):
        if len(w) != 2:
            raise Fail("usage: requeue <id>")
        j = self.job(w[1])
        if j.status != "failed":
            raise Fail(f"job {j.id} is not failed")
        j.status = "queued"
        j.attempt += 1
        j.error = None
        self.items[j.queue].append(j.id)
        say(f"  requeued {j.id} on {j.queue}")

    def tick(self, w):
        if len(w) != 2:
            raise Fail("usage: tick <seconds>")
        n = count(w[1], 1, 99999)
        if n is None:
            raise Fail(f"bad seconds '{w[1]}'")
        self.clock += n
        say(f"  clock {self.clock}")
        due = sorted(s for s in self.scheduled if s[0] <= self.clock)
        self.scheduled = [s for s in self.scheduled if s[0] > self.clock]
        for _, _, jid in due:
            j = self.by_id[jid]
            j.status = "queued"
            self.items[j.queue].append(j.id)
            say(f"  {j.id}: due, queued on {j.queue}")
        for j in self.jobs:
            if j.status == "finished" and j.expires <= self.clock:
                j.status = "expired"
                j.result = None
                say(f"  {j.id}: result expired")

    def work(self, w):
        if len(w) != 1:
            raise Fail("usage: work")
        rounds = 0
        while any(self.items[q] for q in self.queues):
            rounds += 1
            batch = []
            for q in self.queues:
                batch += self.items[q]
                self.items[q] = []
            say(f"  round {rounds}: {', '.join(batch)}")
            for jid in batch:
                j = self.by_id[jid]
                ok, text = perform(j.func, j.args, j.attempt, j.timeout)
                self.runs += 1
                self.by_func[j.func] = self.by_func.get(j.func, 0) + 1
                if ok:
                    j.status = "finished"
                    j.result = text
                    j.expires = self.clock + j.ttl
                    say(f"  {jid}: finished -> {text}")
                    continue
                self.failures += 1
                if j.retries_left > 0:
                    j.retries_left -= 1
                    n = j.retry - j.retries_left
                    j.attempt += 1
                    if j.backoff:
                        delay = j.backoff[min(n, len(j.backoff)) - 1]
                        self.schedule(j, self.clock + delay)
                        say(f"  {jid}: failed ({text}), retry {n} of {j.retry} in {delay}s")
                    else:
                        j.status = "queued"
                        self.items[j.queue].append(jid)
                        say(f"  {jid}: failed ({text}), retry {n} of {j.retry} now")
                else:
                    j.status = "failed"
                    j.error = text
                    say(f"  {jid}: failed ({text})")
            for j in self.jobs:
                if j.status == "deferred" and self.deps_done(j):
                    j.status = "queued"
                    self.items[j.queue].append(j.id)
                    say(f"  {j.id}: dependencies met, queued on {j.queue}")
        if rounds == 0:
            say("  nothing to do")
        else:
            say(f"  idle after {rounds} round" + ("" if rounds == 1 else "s"))

    # -------------------------------------------------- inspection

    def inspect(self, w):
        if not w:
            raise Fail("missing command")
        if w[0] == "status":
            if len(w) != 1:
                raise Fail("usage: @ status")
            say(f"  clock {self.clock}")
            for q in self.queues:
                say(f"  {q}: {', '.join(self.items[q]) or 'empty'}")
        elif w[0] == "registries":
            if len(w) != 1:
                raise Fail("usage: @ registries")
            self.registries()
        elif w[0] == "job":
            if len(w) != 2:
                raise Fail("usage: @ job <id>")
            j = self.job(w[1])
            s = f"  {j.id}: {j.status} on {j.queue}, {j.func}({', '.join(j.args)}), attempt {j.attempt}"
            if j.retry:
                s += f", {j.retries_left} of {j.retry} retries left"
            if j.status == "finished":
                s += f", result {j.result}, expires at {j.expires}"
            elif j.status == "failed":
                s += f", error {j.error}"
            elif j.status == "scheduled":
                s += f", due at {j.due}"
            elif j.status == "deferred":
                waiting = [d for d in j.depends if self.by_id[d].status not in ("finished", "expired")]
                s += f", waiting on {', '.join(waiting)}"
            say(s)
        else:
            raise Fail(f"unknown command '@ {w[0]}'")

    def registries(self):
        for name in ("deferred", "scheduled", "finished", "failed", "canceled", "expired"):
            ids = sorted(j.id for j in self.jobs if j.status == name)
            if name == "scheduled":
                ids = [f"{i}@{self.by_id[i].due}" for i in ids]
            say(f"  {name}: {', '.join(ids) or 'none'}")


def main():
    with open("data/script.txt", encoding="utf-8", newline="") as fh:
        lines = [(no, l.split("#", 1)[0].strip()) for no, l in enumerate(fh.read().split("\n"), 1)]
    rq = Rq()
    say(f"== script ({WORKERS} workers)")
    for no, line in lines:
        if not line:
            continue
        w = line.split()
        say(f"> {' '.join(w)}")
        try:
            if w[0] == "@":
                rq.inspect(w[1:])
            elif w[0] == "queue":
                rq.queue(w)
            elif w[0] == "enqueue":
                rq.enqueue(w)
            elif w[0] == "enqueue_in":
                rq.enqueue_in(w)
            elif w[0] == "cancel":
                rq.cancel(w)
            elif w[0] == "requeue":
                rq.requeue(w)
            elif w[0] == "tick":
                rq.tick(w)
            elif w[0] == "work":
                rq.work(w)
            else:
                raise Fail(f"unknown command '{w[0]}'")
        except Fail as e:
            say(f"  error: script.txt:{no}: {e}")
    say("== end")
    say(f"  clock {rq.clock}")
    rq.registries()
    say(f"  {WORKERS} workers: {rq.runs} runs, {rq.failures} failed")
    say("  by function: " + ", ".join(f"{f} {n}" for f, n in sorted(rq.by_func.items())))
    print("\n".join(OUT))


main()
