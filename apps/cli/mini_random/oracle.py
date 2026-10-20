# Runs data/jobs.tsv through Python 3.13's own random module and prints
# what expected.out holds.
import io
import math
import random
import sys
import contextlib
from datetime import date, timedelta
from random import Random


def num(t):
    try:
        return int(t)
    except ValueError:
        return float(t)


def is_num(t):
    try:
        num(t)
        return True
    except ValueError:
        return False


def lst(t):
    return t.split(",") if t else []


def rarg(t):
    if t == "-":
        return "None"
    if is_num(t):
        return repr(num(t))
    return repr(lst(t))


def call(name, args):
    return f"{name}({', '.join(rarg(a) for a in args)})"


def err(e):
    return f"{type(e).__name__}: {e}"


def head(r):
    st = r.getstate()
    c = Random()
    c.setstate(st)
    return f"next random() {c.random()!r}"


def line(h, f):
    try:
        return f"{h} = {f()}"
    except Exception as e:
        return f"{h} -> {err(e)}"


def do_seed(r, f):
    kind = f[1]
    val = f[2] if len(f) > 2 else ""
    a = {"int": lambda: int(val), "float": lambda: float(val), "str": lambda: val,
         "bytes": lambda: bytes.fromhex(val), "list": lambda: lst(val)}[kind]()
    if kind == "list":
        a = [int(x) for x in a]
    kw = {}
    vt = ""
    if len(f) > 3:
        kw["version"] = int(f[3])
        vt = f", version={int(f[3])}"
    h = f"seed({a!r}{vt})"
    try:
        r.seed(a, **kw)
    except Exception as e:
        return f"{h} -> {err(e)}"
    return f"{h} -> {head(r)}"


DISTS = {"uniform", "triangular", "normalvariate", "gauss", "lognormvariate", "expovariate",
         "vonmisesvariate", "gammavariate", "betavariate", "paretovariate", "weibullvariate",
         "binomialvariate"}


def state_line(r):
    st = r.getstate()
    return (f"getstate() = version {st[0]}, {len(st[1])} words, index {st[1][-1]}, "
            f"mt[0] {st[1][0]}, mt[623] {st[1][623]}, gauss_next {st[2]!r}")


def setstate_line(r, st, what):
    try:
        r.setstate(st)
    except Exception as e:
        return f"setstate({what}) -> {err(e)}"
    return f"setstate({what}) -> {head(r)}"


def cli(r, argv):
    shown = [repr(a) if (a == "" or " " in a) else a for a in argv]
    h = f"$ python -m random {' '.join(shown)}".strip()
    saved = random._inst
    # main() calls the module functions, which are bound to _inst
    names = ["choice", "randint", "uniform"]
    old = {n: getattr(random, n) for n in names}
    for n in names:
        setattr(random, n, getattr(r, n))
    out, errs = io.StringIO(), io.StringIO()
    argv0 = sys.argv[0]
    sys.argv[0] = "random.py"
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(errs):
            try:
                print(random.main(argv))
                tail = ""
            except SystemExit as e:
                tail = f"[exit {e.code}]" if e.code else ""
            except Exception as e:
                tail = f"Traceback (most recent call last):\n{err(e)}\n[exit 1]"
    finally:
        sys.argv[0] = argv0
        for n in names:
            setattr(random, n, old[n])
    body = out.getvalue() + errs.getvalue()
    if body.endswith("\n"):
        body = body[:-1]
    parts = [h]
    if body or not tail:
        parts.append(body)
    if tail:
        parts.append(tail)
    return "\n".join(parts)


def run_op(r, saved, f):
    o, a = f[0], f[1:]
    if o == "seed":
        return do_seed(r, f)
    if o == "random":
        n = int(a[0])
        return f"random() x{n} = {[r.random() for _ in range(n)]!r}"
    if o == "getrandbits":
        k = int(a[0])
        return line(f"getrandbits({k})", lambda: r.getrandbits(k)).replace(" = ", " = ", 1)
    if o == "randbytes":
        n = int(a[0])
        return line(f"randbytes({n})", lambda: repr(r.randbytes(n)))
    if o == "randrange":
        args = [None if x == "-" else num(x) for x in a]
        return line(call(o, a), lambda: r.randrange(*args))
    if o == "randint":
        return line(call(o, a), lambda: r.randint(num(a[0]), num(a[1])))
    if o == "choice":
        return line(call(o, a), lambda: repr(r.choice(lst(a[0]))))
    if o == "shuffle":
        v = lst(a[0])
        r.shuffle(v)
        return f"shuffle({lst(a[0])!r}) -> {v!r}"
    if o == "sample":
        k = int(a[1])
        if a[0].startswith("range:"):
            n = int(a[0][6:])
            return line(f"sample(range(0, {n}), {k})", lambda: r.sample(range(n), k))
        h = f"sample({lst(a[0])!r}, {k}"
        kw = {}
        if len(a) > 2:
            kw["counts"] = [int(x) for x in lst(a[2])]
            h += f", counts={kw['counts']!r}"
        h += ")"
        return line(h, lambda: r.sample(lst(a[0]), k, **kw))
    if o == "choices":
        kw = {"k": int(a[3])}
        h = f"choices({lst(a[0])!r}"
        if a[1] != "-":
            kw["weights"] = [num(x) for x in lst(a[1])]
            h += f", weights={kw['weights']!r}"
        if a[2] != "-":
            kw["cum_weights"] = [num(x) for x in lst(a[2])]
            h += f", cum_weights={kw['cum_weights']!r}"
        h += f", k={kw['k']})"
        return line(h, lambda: r.choices(lst(a[0]), **kw))
    if o == "state":
        return state_line(r)
    if o == "save":
        saved[0] = r.getstate()
        return "state = getstate()"
    if o == "restore":
        return setstate_line(r, saved[0], "state")
    if o == "badstate":
        what, val = a[0], int(a[1])
        v, words, g = saved[0]
        words = list(words)
        if what == "index":
            words[-1] = val
            d = f"state with index {val}"
        elif what == "version":
            v = val
            d = f"state with version {val}"
        elif what == "size":
            words.pop()
            d = f"state with {len(words)} words"
        else:
            g = float(val)
            d = f"state with gauss_next {g!r}"
        return setstate_line(r, (v, tuple(words), g), d)
    if o == "cli":
        return cli(r, a)
    if o in DISTS:
        n = int(a[0])
        args = [None if x == "-" else num(x) for x in a[1:]]
        h = call(o, a[1:])
        vals = []
        try:
            for _ in range(n):
                vals.append(getattr(r, o)(*args))
        except Exception as e:
            return f"{h} -> {err(e)}"
        return f"{h} x{n} = [{', '.join(repr(v) for v in vals)}]"
    raise SystemExit(f"unknown op {o}")


# ------------------------------------------------------------ programs

def read(path):
    with open("data/" + path) as f:
        return f.read()


def conf(path):
    out = {}
    eps = []
    for ln in read(path).splitlines():
        ln = ln.split("#")[0].strip()
        if not ln:
            continue
        if ln.startswith("endpoint "):
            eps.append(ln.split()[1:])
        else:
            k, _, v = ln.partition("=")
            out[k.strip()] = v.strip()
    return out, eps


def rank(xs, q):
    # nearest-rank percentile of sorted data
    k = math.ceil(q * len(xs))
    return xs[max(k, 1) - 1]


def loadgen(path):
    c, eps = conf(path)
    r = Random(c["seed"])
    rate = float(c["rate"])
    n = int(c["requests"])
    er = float(c["error_rate"])
    names = [f"{e[0]} {e[1]}" for e in eps]
    weights = [int(e[2]) for e in eps]
    params = {f"{e[0]} {e[1]}": (float(e[3]), float(e[4])) for e in eps}
    t = 0.0
    lat = {nm: [] for nm in names}
    errs = {nm: 0 for nm in names}
    print(f"{path}: {n} requests at {rate} rps, seed {c['seed']!r}")
    for i in range(n):
        t += r.expovariate(rate)
        ep = r.choices(names, weights)[0]
        mu, sigma = params[ep]
        ms = r.lognormvariate(mu, sigma)
        fail = r.random() < er
        status = 503 if fail else 200
        lat[ep].append(ms)
        if fail:
            errs[ep] += 1
        if i < 6:
            print(f"  t={t:7.3f}s  {ep:<22} {ms:7.1f}ms  {status}")
    print(f"  {'endpoint':<22} {'count':>5} {'errors':>6} {'mean':>8} {'p50':>8} {'p95':>8} {'p99':>8} {'max':>8}")
    for nm in names:
        xs = sorted(lat[nm])
        if not xs:
            print(f"  {nm:<22} {0:>5}")
            continue
        mean = sum(xs) / len(xs)
        print(f"  {nm:<22} {len(xs):>5} {errs[nm]:>6} {mean:8.1f} {rank(xs, 0.5):8.1f} "
              f"{rank(xs, 0.95):8.1f} {rank(xs, 0.99):8.1f} {xs[-1]:8.1f}")
    print(f"  ran {t:.2f}s, {n / t:.2f} requests/s, {sum(errs.values())} errors")


def abtest(conf_path, users_path):
    users = read(users_path).split()
    exps = []
    for ln in read(conf_path).splitlines():
        if ln.startswith("#") or not ln.strip():
            continue
        name, roll, vs, ws = ln.split()
        exps.append((name, float(roll), vs.split(","), [int(w) for w in ws.split(",")]))
    got = {}
    for name, roll, vs, ws in exps:
        counts = {v: 0 for v in vs + ["off"]}
        firsts = []
        for u in users:
            rr = Random(f"{name}:{u}")
            if rr.random() < roll:
                v = rr.choices(vs, ws)[0]
            else:
                v = "off"
            counts[v] += 1
            got[(name, u)] = v
            if len(firsts) < 6:
                firsts.append(f"{u}={v}")
        shares = ", ".join(f"{v} {counts[v]} ({counts[v] / len(users):.1%})" for v in vs + ["off"])
        print(f"{name}: rollout {roll:.0%} of {len(users)} users: {shares}")
        print(f"  {' '.join(firsts)}")
    both = [u for u in users if got[("new-checkout", u)] == "treatment" and got[("dark-mode", u)] == "on"]
    print(f"in new-checkout treatment and dark-mode: {len(both)} {both}")
    again = Random(f"pricing-page:{users[3]}")
    v = again.choices(["A", "B", "C"], [34, 33, 33])[0] if again.random() < 1.0 else "off"
    print(f"{users[3]} again: {v} (sticky: {v == got[('pricing-page', users[3])]})")


def backoff(path):
    c, _ = conf(path)
    r = Random(int(c["seed"]))
    base, cap = float(c["base"]), float(c["cap"])
    attempts, clients = int(c["attempts"]), int(c["clients"])
    print(f"base {base}s, cap {cap}s, {attempts} attempts, {clients} clients")
    print("  attempt   no jitter  " + "  ".join(f"full#{k}" for k in range(clients)))
    full = [[r.uniform(0, min(cap, base * 2 ** a)) for a in range(attempts)] for _ in range(clients)]
    for a in range(attempts):
        row = "  ".join(f"{full[k][a]:6.3f}" for k in range(clients))
        print(f"  {a:>7}   {min(cap, base * 2 ** a):9.3f}  {row}")
    eq = []
    for k in range(clients):
        s = []
        for a in range(attempts):
            temp = min(cap, base * 2 ** a)
            s.append(temp / 2 + r.uniform(0, temp / 2))
        eq.append(s)
    dec = []
    for k in range(clients):
        s, sleep = [], base
        for a in range(attempts):
            sleep = min(cap, r.uniform(base, sleep * 3))
            s.append(sleep)
        dec.append(s)
    for label, sched in [("full jitter", full), ("equal jitter", eq), ("decorrelated", dec)]:
        totals = ", ".join(f"{sum(s):.3f}" for s in sched)
        print(f"  {label:<13} totals {totals}  last {', '.join(f'{s[-1]:.3f}' for s in sched)}")
    nojit = sum(min(cap, base * 2 ** a) for a in range(attempts))
    print(f"  no jitter total {nojit:.3f}: every client retries at the same instants")


def reservoir(path):
    lines = read(path).splitlines()
    r = Random(2024)
    k = 8
    res = []
    for i, ln in enumerate(lines):
        if i < k:
            res.append((i + 1, ln))
        else:
            j = r.randrange(i + 1)
            if j < k:
                res[j] = (i + 1, ln)
    print(f"{path}: {len(lines)} lines, a reservoir of {k}")
    for no, ln in sorted(res):
        print(f"  {no:>4}  {ln}")
    errors = [ln for ln in lines if " ERROR " in ln]
    print(f"{len(errors)} ERROR lines, three for the incident review:")
    for ln in r.sample(errors, 3):
        print(f"  {ln}")
    levels = ["DEBUG", "INFO", "WARN", "ERROR"]
    counts = [sum(1 for ln in lines if f" {lv} " in ln or f" {lv}  " in ln) for lv in levels]
    print(f"level counts {dict(zip(levels, counts))}")
    print(f"levels drawn by weight: {r.choices(levels, counts, k=10)}")
    order = list(range(1, 11))
    r.shuffle(order)
    print(f"replay order for lines 1-10: {order}")


def montecarlo(path):
    rows = [ln.split(",") for ln in read(path).splitlines()[1:]]
    r = Random("roadmap-q3")
    trials = 2000
    deadline = 40
    tri, pert = [], []
    for _ in range(trials):
        for model, out in (("tri", tri), ("pert", pert)):
            tracks = {"A": 0.0, "B": 0.0, "final": 0.0}
            for name, track, o, m, p in rows:
                o, m, p = float(o), float(m), float(p)
                if model == "tri":
                    d = r.triangular(o, p, m)
                else:
                    a = 1 + 4 * (m - o) / (p - o)
                    b = 1 + 4 * (p - m) / (p - o)
                    d = o + (p - o) * r.betavariate(a, b)
                tracks[track] += d
            out.append(max(tracks["A"], tracks["B"]) + tracks["final"])
    print(f"{path}: {len(rows)} tasks, {trials} trials, deadline {deadline} days")
    for label, xs in (("triangular", tri), ("PERT", pert)):
        s = sorted(xs)
        mean = sum(s) / len(s)
        within = sum(1 for x in s if x <= deadline) / len(s)
        print(f"  {label:<10} mean {mean:6.2f}  P50 {rank(s, 0.5):6.2f}  P80 {rank(s, 0.8):6.2f}  "
              f"P95 {rank(s, 0.95):6.2f}  on time {within:.1%}")
    lo, hi = math.floor(min(tri)), math.ceil(max(tri))
    width = (hi - lo) / 10
    print(f"  triangular totals, {lo} to {hi} days:")
    for b in range(10):
        a0 = lo + b * width
        a1 = a0 + width
        n = sum(1 for x in tri if a0 <= x < a1 or (b == 9 and x == a1))
        print(f"  {a0:5.1f}-{a1:5.1f} {'#' * (n // 10)} {n}")


def draw(players_path, office_path):
    players = [ln.split("|") for ln in read(players_path).splitlines()]
    r = Random("spring-cup-2026")
    order = list(range(len(players)))
    r.shuffle(order)
    for g in range(4):
        names = [players[i][0] for i in order[g * 4:(g + 1) * 4]]
        print(f"group {'ABCD'[g]}: {', '.join(names)}")
    clash = 0
    for g in range(4):
        clubs = [players[i][1] for i in order[g * 4:(g + 1) * 4]]
        clash += len(clubs) - len(set(clubs))
    print(f"groups with two players from one club: {clash}")
    seeds = r.sample(range(len(players)), 4)
    print(f"seeded: {', '.join(players[i][0] for i in seeds)}")
    office = [ln.split("|") for ln in read(office_path).splitlines()]
    rr = Random(2026)
    tries = 0
    while True:
        tries += 1
        gift = list(range(len(office)))
        rr.shuffle(gift)
        if all(gift[i] != i and office[gift[i]][1] != office[i][1] for i in range(len(office))):
            break
    print(f"Secret Santa after {tries} shuffles (nobody draws themselves or their own team):")
    for i in range(len(office)):
        print(f"  {office[i][0]:<6} -> {office[gift[i]][0]}")


def synth(path):
    lists = {}
    for ln in read(path).splitlines():
        k, _, v = ln.partition(": ")
        lists[k] = v.split()
    cities = [c.split(":")[0] for c in lists["city"]]
    cweights = [int(c.split(":")[1]) for c in lists["city"]]
    r = Random(31337)
    print("user_id,name,age,height_cm,city,signup,plan,logins,token,tags")
    ages = []
    plans = {"free": 0, "pro": 0, "team": 0}
    for _ in range(15):
        uid = f"{r.getrandbits(48):012x}"
        name = f"{r.choice(lists['first'])} {r.choice(lists['last'])}"
        age = r.randint(18, 80)
        h = r.gauss(170, 9)
        city = r.choices(cities, cweights)[0]
        signup = date(2025, 1, 1) + timedelta(days=r.randrange(365))
        plan = r.choices(["free", "pro", "team"], cum_weights=[70, 92, 100])[0]
        logins = r.binomialvariate(30, 0.35)
        token = r.randbytes(6).hex()
        tags = "|".join(r.sample(lists["tag"], k=r.randint(0, 3)))
        ages.append(age)
        plans[plan] += 1
        print(f"{uid},{name},{age},{h:.1f},{city},{signup.isoformat()},{plan},{logins},{token},{tags}")
    print(f"mean age {sum(ages) / len(ages):.2f}, plans {plans}")


def sensor(path):
    c, _ = conf(path)
    r = Random(c["seed"].encode())
    hours = int(c["hours"])
    base, swing = float(c["base_temp"]), float(c["swing"])
    print(f"station {c['seed']}, {hours} hourly readings")
    temps, winds, rain, dirs = [], [], 0.0, []
    lost = 0
    for h in range(hours):
        t = base + swing * math.sin(2 * math.pi * (h - 9) / 24) + r.normalvariate(0, 0.8)
        w = r.weibullvariate(float(c["wind_scale"]), float(c["wind_shape"]))
        d = math.degrees(r.vonmisesvariate(math.radians(float(c["wind_dir"])), float(c["wind_kappa"])))
        mm = r.gammavariate(0.6, 2.0) if r.random() < float(c["rain_chance"]) else 0.0
        if r.random() < float(c["loss"]):
            lost += 1
            print(f"  {h:02d}:00  --")
            continue
        temps.append(t)
        winds.append(w)
        dirs.append(d)
        rain += mm
        print(f"  {h:02d}:00  {t:5.1f}C  wind {w:4.1f} m/s from {d:5.1f}  rain {mm:4.1f} mm")
    sectors = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    count = [0] * 8
    for d in dirs:
        count[int(((d + 22.5) % 360) // 45)] += 1
    best = max(range(8), key=lambda i: count[i])
    print(f"  min {min(temps):.1f}C max {max(temps):.1f}C, mean wind {sum(winds) / len(winds):.2f} m/s, "
          f"rain {rain:.1f} mm, prevailing {sectors[best]}, {lost} readings lost")
    sizes = [r.paretovariate(1.5) * 10.0 for _ in range(8)]
    print(f"  upload sizes (KB): {', '.join(f'{s:.1f}' for s in sizes)}")
    drift = [r.lognormvariate(0.0, 0.05) for _ in range(4)]
    print(f"  clock drift factors: {', '.join(f'{x:.4f}' for x in drift)}")


PROGRAMS = {"loadgen": loadgen, "abtest": abtest, "backoff": backoff, "reservoir": reservoir,
            "montecarlo": montecarlo, "draw": draw, "synth": synth, "sensor": sensor}


def main():
    r = Random(0)
    saved = [None]
    for ln in read("jobs.tsv").splitlines():
        if not ln or ln.startswith("#"):
            continue
        f = ln.split("\t")
        if f[0] == "job":
            print()
            print(f"== {f[1]}")
            r = Random(0)
            saved = [None]
            continue
        if f[0] == "program":
            PROGRAMS[f[1]](*f[2:])
            continue
        print(run_op(r, saved, f))


main()
