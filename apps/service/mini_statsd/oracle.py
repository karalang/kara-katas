# Python mirror of mini_statsd: runs data/jobs.txt with a port of statsd
# 0.9.0's packet handling, metric processing, management console and
# graphite text backend, using a virtual clock (startup at T0, flush k at
# T0 + interval*(k+1)) in place of the wall clock.
import math, re, sys

T0 = 1760000000
out = []

# ---- a parser for the subset of JS object literals statsd configs use ----
class P:
    def __init__(self, s):
        self.s = s; self.i = 0
    def ws(self):
        s = self.s
        while self.i < len(s):
            if s[self.i] in " \t\r\n":
                self.i += 1
            elif s.startswith("//", self.i):
                while self.i < len(s) and s[self.i] != "\n":
                    self.i += 1
            elif s.startswith("/*", self.i):
                self.i = s.index("*/", self.i) + 2
            else:
                break
    def value(self):
        self.ws()
        c = self.s[self.i]
        if c == "{":
            self.i += 1
            o = {}
            while True:
                self.ws()
                if self.s[self.i] == ",":
                    self.i += 1; continue
                if self.s[self.i] == "}":
                    self.i += 1; return o
                j = self.i
                while self.s[self.i].isalnum() or self.s[self.i] == "_":
                    self.i += 1
                k = self.s[j:self.i]
                self.ws(); assert self.s[self.i] == ":"; self.i += 1
                o[k] = self.value()
        if c == "[":
            self.i += 1
            a = []
            while True:
                self.ws()
                if self.s[self.i] == ",":
                    self.i += 1; continue
                if self.s[self.i] == "]":
                    self.i += 1; return a
                a.append(self.value())
        if c in "'\"":
            j = self.s.index(c, self.i + 1)
            v = self.s[self.i + 1:j]; self.i = j + 1
            return v
        j = self.i
        while self.i < len(self.s) and (self.s[self.i].isalnum() or self.s[self.i] in ".-+"):
            self.i += 1
        w = self.s[j:self.i]
        if w == "true":
            return True
        if w == "false":
            return False
        return float(w)

# ---- JS numbers and objects ----
def js_num(x):
    if x != x:
        return "NaN"
    if x == math.inf:
        return "Infinity"
    if x == -math.inf:
        return "-Infinity"
    if x == 0:
        return "0"
    if x < 0:
        return "-" + js_num(-x)
    r = repr(x)
    m, _, e = r.partition("e")
    digits = m.replace(".", "")
    point = m.index(".") if "." in m else len(m)
    exp = point + (int(e) if e else 0)
    digits = digits.lstrip("0")
    exp -= len(m.replace(".", "")) - len(m.replace(".", "").lstrip("0"))
    digits = digits.rstrip("0")
    k = len(digits); n = exp
    if k <= n <= 21:
        return digits + "0" * (n - k)
    if 0 < n <= 21:
        return digits[:n] + "." + digits[n:]
    if -6 < n <= 0:
        return "0." + "0" * (-n) + digits
    sign = "+" if n - 1 >= 0 else "-"
    mant = digits[0] + ("." + digits[1:] if k > 1 else "")
    return f"{mant}e{sign}{abs(n - 1)}"

def is_index(k):
    return re.fullmatch(r"0|[1-9][0-9]*", k) is not None and int(k) < 2**32 - 1

class Obj:
    """A JS object's own string keys: array indices ascending, then insertion order."""
    def __init__(self):
        self.d = {}
    def keys(self):
        idx = sorted((k for k in self.d if is_index(k)), key=int)
        return idx + [k for k in self.d if not is_index(k)]
    def __contains__(self, k):
        return k in self.d
    def get(self, k):
        return self.d.get(k)
    def set(self, k, v):
        self.d[k] = v
    def delete(self, k):
        del self.d[k]

def inspect_value(v, indent):
    if isinstance(v, list):
        items = [js_num(x) for x in v]
        return join_braces(items, "[", "]", indent)
    return js_num(v)

def inspect_obj(o):
    items = []
    for k in o.keys():
        name = k if re.fullmatch(r"[a-zA-Z_][a-zA-Z_0-9]*", k) else "'" + k + "'"
        items.append(f"{name}: {inspect_value(o.get(k), 2)}")
    if not items:
        return "{}"
    return join_braces(items, "{", "}", 0)

def join_braces(items, open_, close, indent):
    if not items:
        return open_ + close
    start = len(items) + indent + len(open_) + 10
    total = len(items) + start + sum(len(x) for x in items)
    if total <= 80 and not any("\n" in x for x in items):
        return f"{open_} {', '.join(items)} {close}"
    pad = "\n" + " " * indent
    return f"{open_}{pad}  " + f",{pad}  ".join(items) + f"{pad}{close}"

# ---- the daemon ----
def js_number(s):
    """JS Number(string)."""
    t = s.strip(" \t\n\r\v\f")
    if t == "":
        return 0.0
    if re.fullmatch(r"0[xX][0-9a-fA-F]+", t):
        return float(int(t[2:], 16))
    if re.fullmatch(r"0[oO][0-7]+", t):
        return float(int(t[2:], 8))
    if re.fullmatch(r"0[bB][01]+", t):
        return float(int(t[2:], 2))
    if re.fullmatch(r"[+-]?Infinity", t):
        return -math.inf if t[0] == "-" else math.inf
    if re.fullmatch(r"[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?", t):
        return float(t)
    return math.nan

def is_number(s):
    return s is not None and s != "" and js_number(s) == js_number(s)

def valid_rate(s):
    return len(s) > 1 and s[0] == "@" and is_number(s[1:]) and s[1] != "-"

def valid_packet(f):
    if len(f) < 2:
        return False
    if len(f) > 2 and not valid_rate(f[2]):
        return False
    if f[1] == "s":
        return True
    if f[1] == "g":
        return is_number(f[0])
    if f[1] == "ms":
        return is_number(f[0]) and js_number(f[0]) >= 0
    return is_number(f[0])

def sanitize(k):
    k = re.sub(r"\s+", "_", k)
    k = k.replace("/", "-")
    return re.sub(r"[^a-zA-Z_\-0-9.;=]", "", k)

def js_round(x):
    return math.floor(x + 0.5)

def clean_pct(p):
    s = js_num(p)
    return s.replace(".", "_", 1).replace("-", "top", 1)

class Daemon:
    def __init__(self, cfg):
        self.cfg = cfg
        self.interval = cfg.get("flushInterval", 10000) / 1000
        self.ttl_max = cfg.get("gaugesMaxTTL", 1)
        if not (isinstance(self.ttl_max, float) and self.ttl_max == int(self.ttl_max) and self.ttl_max > 1):
            self.ttl_max = 1
        idle = cfg.get("deleteIdleStats", False)
        self.del_counters = cfg.get("deleteCounters", idle)
        self.del_timers = cfg.get("deleteTimers", idle)
        self.del_sets = cfg.get("deleteSets", idle)
        self.del_gauges = cfg.get("deleteGauges", idle)
        self.sanitize = cfg.get("keyNameSanitize", True)
        ps = cfg.get("prefixStats", "statsd")
        self.ps = ps
        self.bad, self.packets, self.metrics = ps + ".bad_lines_seen", ps + ".packets_received", ps + ".metrics_received"
        self.lag = ps + ".timestamp_lag"
        self.counters = Obj(); self.timers = Obj(); self.tcount = Obj(); self.gauges = Obj()
        self.ttl = Obj(); self.sets = Obj()
        for k in (self.bad, self.packets, self.metrics):
            self.counters.set(k, 0.0)
        p = cfg.get("percentThreshold", 90.0)
        self.pcts = p if isinstance(p, list) else [p]
        self.hist = cfg.get("histogram", [])
        self.calc = cfg.get("calculatedTimerMetrics", [])
        self.health = "up"
        g = cfg.get("graphite", {})
        self.legacy = g.get("legacyNamespace", True)
        gp = g.get("globalPrefix", "stats")
        self.suffix = "." + g["globalSuffix"] if "globalSuffix" in g else ""
        self.flush_counts = cfg.get("flush_counts", True)
        if self.legacy:
            self.ns = {"g": ["stats"], "c": ["stats"], "t": ["stats", "timers"], "ga": ["stats", "gauges"], "s": ["stats", "sets"]}
        else:
            base = [gp] if gp != "" else []
            self.ns = {"g": base}
            for n, key, d in (("c", "prefixCounter", "counters"), ("t", "prefixTimer", "timers"),
                              ("ga", "prefixGauge", "gauges"), ("s", "prefixSet", "sets")):
                pre = g.get(key, d)
                self.ns[n] = base + ([pre] if pre != "" else [])
        self.k = 0
        self.last_flush = T0
        self.last_len = 0
        self.flush()  # the silent first flush

    def bump(self, key):
        v = self.counters.get(key)
        self.counters.set(key, math.nan if v is None else v + 1)

    def packet(self, data):
        self.bump(self.packets)
        for line in data.split("\n"):
            if line == "":
                continue
            self.bump(self.metrics)
            parts = line.split("|#")
            tags = parts[1].split(",") if len(parts) > 1 and parts[1] != "" else []
            bits = parts[0].split(":")
            key = bits.pop(0)
            if tags:
                key += ";" + ";".join(t.replace(";", "_", 1).replace(":", "=", 1) for t in tags)
            if self.sanitize:
                key = sanitize(key)
            if not bits:
                bits = ["1"]
            for b in bits:
                f = b.split("|")
                if not valid_packet(f):
                    self.bump(self.bad)
                    continue
                rate = 1.0
                if len(f) > 2 and f[2] != "":
                    rate = js_number(re.match(r"@([\d.]+)", f[2]).group(1))
                t = f[1].strip()
                inv = 1 / rate if rate != 0 else math.inf
                if t == "ms":
                    if self.timers.get(key) is None:
                        self.timers.set(key, []); self.tcount.set(key, 0.0)
                    self.timers.get(key).append(js_number(f[0]))
                    self.tcount.set(key, self.tcount.get(key) + inv)
                elif t == "g":
                    if self.del_gauges:
                        self.ttl.set(key, self.ttl_max)
                    cur = self.gauges.get(key)
                    if cur and cur == cur and f[0][:1] in ("+", "-"):
                        self.gauges.set(key, cur + js_number(f[0]))
                    else:
                        self.gauges.set(key, js_number(f[0]))
                elif t == "s":
                    if self.sets.get(key) is None:
                        self.sets.set(key, Obj())
                    self.sets.get(key).set(f[0] or "0", True)
                else:
                    cur = self.counters.get(key)
                    if cur is None or cur != cur:
                        cur = 0.0  # JS: `if (!counters[key]) counters[key] = 0`
                    v = js_number(f[0]) if f[0] != "" else 1.0
                    self.counters.set(key, cur + v * inv)

    def timer_data(self, key):
        vals = sorted(self.timers.get(key))
        d = []
        if not vals:
            d = [("count_ps", 0.0), ("count", 0.0)]
        else:
            n = len(vals)
            cum = [vals[0]]; cumsq = [vals[0] * vals[0]]
            for i in range(1, n):
                cum.append(vals[i] + cum[i - 1]); cumsq.append(vals[i] * vals[i] + cumsq[i - 1])
            s = vals[0]; sq = vals[0] * vals[0]; mean = vals[0]; bound = vals[-1]
            for p in self.pcts:
                num = n
                if n > 1:
                    num = js_round(abs(p) / 100 * n)
                    if num == 0:
                        continue
                    if p > 0:
                        bound = vals[num - 1]; s = cum[num - 1]; sq = cumsq[num - 1]
                    else:
                        bound = vals[n - num]
                        s = cum[n - 1] - cum[n - num - 1]; sq = cumsq[n - 1] - cumsq[n - num - 1]
                    mean = s / num
                c = clean_pct(p)
                d += [("count_" + c, float(num)), ("mean_" + c, mean),
                      (("upper_" if p > 0 else "lower_") + c, bound), ("sum_" + c, s), ("sum_squares_" + c, sq)]
            s = cum[-1]; sq = cumsq[-1]; mean = s / n
            diffs = 0.0
            for v in vals:
                diffs += (v - mean) * (v - mean)
            mid = n // 2
            med = vals[mid] if n % 2 else (vals[mid - 1] + vals[mid]) / 2
            tc = self.tcount.get(key)
            d += [("std", math.sqrt(diffs / n)), ("upper", vals[-1]), ("lower", vals[0]), ("count", tc),
                  ("count_ps", tc / self.interval), ("sum", s), ("sum_squares", sq), ("mean", mean), ("median", med)]
            bins = []
            for h in self.hist:
                if h["metric"] in key:
                    bins = h["bins"]; break
            i = 0
            for b in bins:
                freq = 0
                while i < n and (b == "inf" or vals[i] < b):
                    freq += 1; i += 1
                d.append(("histogram.bin_" + (b if b == "inf" else js_num(b)).replace(".", "_", 1), float(freq)))
        if self.calc:
            d = [(k, v) for k, v in d if re.sub(r"_(top)?\d+$", "_percent", k) in self.calc]
        return d

    def fmt(self, ns, key, *extra):
        parts = key.split(";")
        name = parts[0] if self.sanitize else sanitize(parts[0])
        tags = ";" + ";".join(parts[1:]) if len(parts) > 1 else ""
        return ".".join(self.ns[ns] + [name] + list(extra)) + self.suffix + tags

    def flush(self):
        ts = T0 + int(self.interval) * (self.k + 1)
        if self.k > 0:
            self.gauges.set(self.lag, 0.0)
        lines = []
        def add(k, v):
            lines.append(f"{k} {v if isinstance(v, str) else js_num(v)} {ts}")
        num = 0
        for k in self.counters.keys():
            v = self.counters.get(k)
            r = v / self.interval
            if self.legacy:
                add(self.fmt("c", k), r)
                if self.flush_counts:
                    add(".".join(["stats_counts", k]) + self.suffix, v)
            else:
                add(self.fmt("c", k, "rate"), r)
                if self.flush_counts:
                    add(self.fmt("c", k, "count"), v)
            num += 1
        for k in self.timers.keys():
            for name, v in self.timer_data(k):
                add(self.fmt("t", k, *name.split(".")), v)
            num += 1
        for k in self.gauges.keys():
            add(self.fmt("ga", k), self.gauges.get(k)); num += 1
        for k in self.sets.keys():
            add(self.fmt("s", k, "count"), float(len(self.sets.get(k).keys()))); num += 1
        ns = ".".join(self.ns["g"] + [self.ps])
        if self.legacy:
            add(self.ps + ".numStats" + self.suffix, float(num))
            add("stats." + self.ps + ".graphiteStats.calculationtime" + self.suffix, 0.0)
            add("stats." + self.ps + ".processing_time" + self.suffix, 0.0)
        else:
            add(self.fmt("g", self.ps, "numStats"), float(num))
            add(self.fmt("g", self.ps, "graphiteStats", "calculationtime"), 0.0)
            add(self.fmt("g", self.ps, "processing_time"), 0.0)
        add(ns + ".graphiteStats.last_exception" + self.suffix, 0.0)
        add(ns + ".graphiteStats.last_flush" + self.suffix, float(self.last_flush))
        add(ns + ".graphiteStats.flush_time" + self.suffix, 0.0)
        add(ns + ".graphiteStats.flush_length" + self.suffix, float(self.last_len))
        text = "\n".join(lines) + "\n"
        self.last_len = len(text); self.last_flush = ts; self.k += 1
        # reset for the next interval
        for k in self.counters.keys():
            if self.del_counters and not any(s in k for s in ("packets_received", "metrics_received", "bad_lines_seen")):
                self.counters.delete(k)
            else:
                self.counters.set(k, 0.0)
        for k in self.timers.keys():
            if self.del_timers:
                self.timers.delete(k); self.tcount.delete(k)
            else:
                self.timers.set(k, []); self.tcount.set(k, 0.0)
        for k in self.sets.keys():
            if self.del_sets:
                self.sets.delete(k)
            else:
                self.sets.set(k, Obj())
        if self.del_gauges:
            for k in self.ttl.keys():
                self.ttl.set(k, self.ttl.get(k) - 1)
                if self.ttl.get(k) < 1:
                    if k in self.gauges:
                        self.gauges.delete(k)
                    self.ttl.delete(k)
        return text

    def delete_stats(self, o, names):
        r = ""
        for b in names:
            found = []
            if b in o:
                found.append(b)
            if b.endswith(".*"):
                folder = b[:-1]
                found += [k for k in o.keys() if k.startswith(folder)]
            if not found:
                r += f"metric {b} not found\n"
            for k in found:
                if k in o:
                    o.delete(k)
                r += f"deleted: {k}\n"
        return r + "END\n\n"

    def admin(self, line):
        parts = line.strip().split(" ")
        cmd, args = parts[0], parts[1:]
        if cmd == "help":
            return "Commands: stats, counters, timers, gauges, delcounters, deltimers, delgauges, health, config, quit\n\n"
        if cmd == "health":
            if args:
                a = args[0].lower()
                if a in ("up", "down"):
                    self.health = a
            return f"health: {self.health}\n"
        if cmd in ("counters", "gauges"):
            return inspect_obj(self.counters if cmd == "counters" else self.gauges) + "\nEND\n\n"
        if cmd == "timers":
            return inspect_obj(self.timers) + "\nEND\n\n"
        if cmd == "delcounters":
            return self.delete_stats(self.counters, args)
        if cmd == "deltimers":
            return self.delete_stats(self.timers, args)
        if cmd == "delgauges":
            return self.delete_stats(self.gauges, args)
        if cmd == "quit":
            return None
        return "ERROR\n"

d = None
for line in open("data/jobs.txt").read().split("\n"):
    if line == "" or line.startswith("#"):
        continue
    out.append(f"$ {line}\n")
    cmd, _, arg = line.partition(" ")
    if cmd == "config":
        d = Daemon(P(open("data/" + arg).read()).value())
    elif cmd == "send":
        d.packet(arg.replace("\\n", "\n"))
    elif cmd == "admin":
        r = d.admin(arg)
        out.append("(connection closed)\n" if r is None else r)
    elif cmd == "flush":
        out.append(d.flush())
    out.append("\n")
sys.stdout.write("".join(out))
