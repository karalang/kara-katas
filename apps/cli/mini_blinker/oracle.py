"""Reference for mini_blinker. Reads data/ (as mk.py writes it), writes
data/out/, and prints the report the Kāra program must print.

Run from this directory: python3 -I -B oracle.py"""
import os
import shutil

OUT = []
KINDS = ["inventory", "mailer", "audit", "fraud", "loyalty"]
SETTINGS = {"inventory": ["low"], "mailer": ["from"], "audit": ["file"],
            "fraud": ["limit"], "loyalty": ["rate"]}


def say(s):
    OUT.append(s)


def is_ident(s):
    return (0 < len(s) <= 32 and "a" <= s[0] <= "z"
            and all(c == "_" or "a" <= c <= "z" or "0" <= c <= "9" for c in s))


def is_word(s):
    return 0 < len(s) <= 40 and all(c in "-_." or "a" <= c <= "z" or "0" <= c <= "9" for c in s)


def digits(s):
    return 0 < len(s) <= 9 and all("0" <= c <= "9" for c in s)


def money(s):
    """Cents, or None. `12`, `12.5` and `12.50` are all fine."""
    whole, _, frac = s.partition(".")
    if not digits(whole) or len(frac) > 2 or ("." in s and not digits(frac)):
        return None
    return int(whole) * 100 + (int(frac.ljust(2, "0")) if frac else 0)


def show_money(c):
    return f"{c // 100}.{c % 100:02d}"


def words(line):
    return line.split("#", 1)[0].split()


# ------------------------------------------------------------ inputs


def parse_wiring(text):
    signals, plugins, conns, errors = [], [], [], []
    for no, raw in enumerate(text.split("\n"), 1):
        w = words(raw)
        if not w:
            continue
        try:
            if w[0] == "signal":
                if len(w) != 2:
                    raise ValueError("usage: signal <name>")
                if not is_ident(w[1]):
                    raise ValueError(f"bad signal name '{w[1]}'")
                if w[1] in signals:
                    raise ValueError(f"signal {w[1]} already defined")
                signals.append(w[1])
            elif w[0] == "plugin":
                if len(w) < 3:
                    raise ValueError("usage: plugin <name> <kind> [key=value...]")
                name, kind = w[1], w[2]
                if not is_ident(name):
                    raise ValueError(f"bad plugin name '{name}'")
                if name == "metrics":
                    raise ValueError("plugin name 'metrics' is reserved")
                if any(p["name"] == name for p in plugins):
                    raise ValueError(f"plugin {name} already defined")
                if kind not in KINDS:
                    raise ValueError(f"unknown kind '{kind}'")
                opts = {}
                for o in w[3:]:
                    k, eq, v = o.partition("=")
                    if not eq:
                        raise ValueError(f"expected key=value, found '{o}'")
                    if k not in SETTINGS[kind]:
                        raise ValueError(f"unknown setting {k} for {kind}")
                    if k in opts:
                        raise ValueError(f"duplicate setting {k}")
                    if k == "low" and v not in signals:
                        raise ValueError(f"no signal '{v}'")
                    if k == "from" and not (is_word(v.replace("@", "")) and v.count("@") == 1):
                        raise ValueError(f"bad value for from: '{v}'")
                    if k == "file" and not is_word(v):
                        raise ValueError(f"bad value for file: '{v}'")
                    if k == "limit" and money(v) is None:
                        raise ValueError(f"bad value for limit: '{v}'")
                    if k == "rate" and (not digits(v) or int(v) == 0):
                        raise ValueError(f"bad value for rate: '{v}'")
                    opts[k] = v
                need = SETTINGS[kind][0]
                if need not in opts:
                    raise ValueError(f"{kind} needs {need}=<value>")
                plugins.append({"name": name, "kind": kind, "opts": opts})
            elif w[0] == "connect":
                if len(w) < 3:
                    raise ValueError("usage: connect <receiver> <signal|*> [sender=<name>] [weak]")
                r, s = w[1], w[2]
                if r != "metrics" and not any(p["name"] == r for p in plugins):
                    raise ValueError(f"no receiver '{r}'")
                if s != "*" and s not in signals:
                    raise ValueError(f"no signal '{s}'")
                weak = False
                sender = None
                for o in w[3:]:
                    if o == "weak":
                        if r == "metrics":
                            raise ValueError("metrics cannot be connected weakly")
                        weak = True
                    elif o.startswith("sender=") and is_word(o[7:]):
                        sender = o[7:]
                    else:
                        raise ValueError(f"unknown option '{o}'")
                targets = list(signals) if s == "*" else [s]
                for t in targets:
                    if any(c["recv"] == r and c["signal"] == t for c in conns):
                        raise ValueError(f"{r} already connected to {t}")
                for t in targets:
                    conns.append({"recv": r, "signal": t, "weak": weak, "sender": sender})
            else:
                raise ValueError(f"unknown directive '{w[0]}'")
        except ValueError as e:
            errors.append(f"wiring.conf:{no}: {e}")
    return signals, plugins, conns, errors


def parse_stock(text):
    stock, errors = [], []
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines or lines[0] != "sku,qty,reorder":
        return [], ["stock.csv:1: bad header"]
    for no, line in enumerate(lines[1:], 2):
        f = line.split(",")
        if len(f) != 3:
            errors.append(f"stock.csv:{no}: expected 3 fields")
        elif not is_word(f[0]):
            errors.append(f"stock.csv:{no}: bad sku '{f[0]}'")
        elif any(s[0] == f[0] for s in stock):
            errors.append(f"stock.csv:{no}: duplicate sku {f[0]}")
        elif not digits(f[1]):
            errors.append(f"stock.csv:{no}: bad qty '{f[1]}'")
        elif not digits(f[2]):
            errors.append(f"stock.csv:{no}: bad reorder level '{f[2]}'")
        else:
            stock.append([f[0], int(f[1]), int(f[2])])
    return stock, errors


def is_time(t):
    if len(t) != 8 or t[2] != ":" or t[5] != ":":
        return False
    h, m, s = t[0:2], t[3:5], t[6:8]
    return all(digits(x) for x in (h, m, s)) and int(h) < 24 and int(m) < 60 and int(s) < 60


def parse_events(text):
    evs = []
    for no, raw in enumerate(text.split("\n"), 1):
        line = raw.strip()
        if line == "" or line.startswith("#"):
            continue
        w = line.split()
        ev = {"no": no, "line": line, "at": w[0], "cmd": None, "err": None}
        if not is_time(w[0]):
            ev["err"] = f"bad time '{w[0]}'"
        elif len(w) >= 2 and w[1] == "@":
            if len(w) < 3:
                ev["err"] = "missing command"
            else:
                ev["cmd"] = w[2:]
        elif len(w) < 3:
            ev["err"] = "missing signal"
        else:
            ev["sender"] = w[1]
            ev["signal"] = w[2]
            fields = []
            for f in w[3:]:
                k, eq, v = f.partition("=")
                if not eq or k == "":
                    ev["err"] = f"bad field '{f}'"
                    break
                fields.append((k, v))
            ev["fields"] = fields
        evs.append(ev)
    return evs


# ------------------------------------------------------------ plugins


def field(d, k):
    for kk, v in d["fields"]:
        if kk == k:
            return v
    raise ValueError(f"missing field '{k}'")


def fields_text(fields):
    return " ".join(f"{k}={v}" for k, v in fields)


class Inventory:
    def __init__(self, opts, stock, bus):
        self.stock = {s[0]: [s[1], s[2]] for s in stock}
        self.low = bus.signals[opts["low"]]
        self.bus = bus
        self.flagged = set()
        self.reserved = 0
        self.released = 0

    def receive(self, d):
        if d["signal"] not in ("order_placed", "order_cancelled"):
            return None
        sku = field(d, "sku")
        q = field(d, "qty")
        if not digits(q) or int(q) == 0:
            raise ValueError(f"bad qty '{q}'")
        q = int(q)
        if sku not in self.stock:
            raise ValueError(f"unknown sku '{sku}'")
        have, level = self.stock[sku]
        if d["signal"] == "order_cancelled":
            self.stock[sku][0] = have + q
            self.released += 1
            if have + q > level:
                self.flagged.discard(sku)
            return f"released {q} {sku}, {have + q} left"
        if q > have:
            raise ValueError(f"out of stock: {sku} has {have}, wants {q}")
        left = have - q
        self.stock[sku][0] = left
        self.reserved += 1
        if left <= level and sku not in self.flagged:
            self.flagged.add(sku)
            self.bus.send(self.low, "inventory", d["at"], [("sku", sku), ("left", str(left))], d["depth"] + 1)
        return f"reserved {q} {sku}, {left} left"

    def summary(self):
        return f"{self.reserved} orders reserved, {self.released} released"


class Mailer:
    def __init__(self, opts):
        self.sender = opts.get("from", "shop@example.test")
        self.n = 0
        self.fh = open("data/out/outbox.txt", "w", encoding="utf-8", newline="")

    def mail(self, to, subject):
        self.n += 1
        self.fh.write(f"#{self.n} from {self.sender} to {to}: {subject}\n")
        return f"mail #{self.n} to {to}"

    def receive(self, d):
        s = d["signal"]
        if s in ("order_placed", "order_shipped"):
            order = field(d, "order")
            cust = field(d, "customer")
            what = "received" if s == "order_placed" else "shipped"
            return self.mail(cust, f"order {order} {what}")
        if s == "stock_low":
            return self.mail("buyer", f"restock {field(d, 'sku')}, {field(d, 'left')} left")
        return None

    def summary(self):
        return f"{self.n} mails"


class Audit:
    def __init__(self, opts):
        self.file = opts["file"]
        self.n = 0
        self.fh = open(f"data/out/{self.file}", "w", encoding="utf-8", newline="")

    def receive(self, d):
        self.n += 1
        self.fh.write(f"{d['at']} {d['signal']} {d['sender']} {fields_text(d['fields'])}\n")
        return None

    def summary(self):
        return f"{self.n} lines in {self.file}"


class Fraud:
    def __init__(self, opts):
        self.limit = money(opts["limit"])
        self.refused = 0

    def receive(self, d):
        if d["signal"] != "payment_received":
            return None
        order = field(d, "order")
        a = field(d, "amount")
        c = money(a)
        if c is None:
            raise ValueError(f"bad amount '{a}'")
        if c > self.limit:
            self.refused += 1
            raise ValueError(f"payment of {show_money(c)} for order {order} is over the limit of {show_money(self.limit)}")
        return None

    def summary(self):
        return f"{self.refused} payments refused"


class Loyalty:
    def __init__(self, opts):
        self.rate = int(opts["rate"])
        self.points = {}

    def receive(self, d):
        if d["signal"] != "order_placed":
            return None
        cust = field(d, "customer")
        t = field(d, "total")
        c = money(t)
        if c is None:
            raise ValueError(f"bad total '{t}'")
        p = c // (self.rate * 100)
        self.points[cust] = self.points.get(cust, 0) + p
        return f"{cust} +{p} points, {self.points[cust]} in all"

    def summary(self):
        return ", ".join(f"{k} {v}" for k, v in sorted(self.points.items())) or "no points"


class Sub:
    def __init__(self, name, handler):
        self.name = name
        self.handler = handler
        self.busy = False
        self.delivered = 0


class Signal:
    def __init__(self, name):
        self.name = name
        self.receivers = []
        self.muted = False


class Bus:
    def __init__(self):
        self.signals = {}
        self.order = []
        self.held = {}
        self.next_id = 0

    def alive(self, name):
        if name in self.held:
            return self.held[name]
        for s in self.order:
            for c in self.signals[s].receivers:
                if c["name"] == name and c["kind"] == "strong":
                    return c["sub"]
        return None

    def connect(self, sig, conn):
        self.next_id += 1
        conn["id"] = self.next_id
        sig.receivers.append(conn)
        return self.next_id

    def send(self, sig, sender, at, fields, depth):
        ind = "  " * (depth + 1)
        if depth > 0:
            say("  " * depth + f">> {sig.name} from {sender}: {fields_text(fields)}")
        if sig.muted:
            say(ind + "(muted)")
            return
        d = {"signal": sig.name, "sender": sender, "at": at, "fields": fields, "depth": depth}
        dead = []
        for conn in list(sig.receivers):
            if conn["sender"] is not None and conn["sender"] != sender:
                continue
            try:
                if conn["kind"] == "func":
                    r = conn["f"](d)
                else:
                    sub = conn["sub"] if conn["kind"] == "strong" else self.alive(conn["name"])
                    if sub is None:
                        dead.append(conn["id"])
                        say(f"{ind}pruned {conn['name']}")
                        continue
                    if sub.busy:
                        raise ValueError("re-entrant delivery skipped")
                    sub.busy = True
                    try:
                        r = sub.handler.receive(d)
                    finally:
                        sub.busy = False
                        sub.delivered += 1
                if r is not None:
                    say(f"{ind}{conn['name']}: {r}")
            except ValueError as e:
                say(f"{ind}{conn['name']} failed: {e}")
        sig.receivers = [c for c in sig.receivers if c["id"] not in dead]


def main():
    if os.path.exists("data/out"):
        shutil.rmtree("data/out")
    os.makedirs("data/out")
    with open("data/wiring.conf", encoding="utf-8", newline="") as fh:
        signals, plugins, conns, werr = parse_wiring(fh.read())
    with open("data/stock.csv", encoding="utf-8", newline="") as fh:
        stock, serr = parse_stock(fh.read())
    with open("data/events.log", encoding="utf-8", newline="") as fh:
        evs = parse_events(fh.read())
    say("== load")
    say(f"wiring.conf: {len(signals)} signals, {len(plugins)} plugins, {len(conns)} connections")
    for e in werr:
        say(e)
    say(f"stock.csv: {len(stock)} items")
    for e in serr:
        say(e)
    say(f"events.log: {len(evs)} lines")

    bus = Bus()
    for s in signals:
        bus.signals[s] = Signal(s)
        bus.order.append(s)
    for p in plugins:
        k = p["kind"]
        if k == "inventory":
            h = Inventory(p["opts"], stock, bus)
        elif k == "mailer":
            h = Mailer(p["opts"])
        elif k == "audit":
            h = Audit(p["opts"])
        elif k == "fraud":
            h = Fraud(p["opts"])
        else:
            h = Loyalty(p["opts"])
        bus.held[p["name"]] = Sub(p["name"], h)
    counts = {s: 0 for s in signals}

    def metrics(d):
        counts[d["signal"]] += 1
        return None

    for c in conns:
        sig = bus.signals[c["signal"]]
        if c["recv"] == "metrics":
            bus.connect(sig, {"name": "metrics", "kind": "func", "f": metrics, "sender": c["sender"]})
        else:
            kind = "weak" if c["weak"] else "strong"
            conn = {"name": c["recv"], "kind": kind, "sender": c["sender"]}
            if kind == "strong":
                conn["sub"] = bus.held[c["recv"]]
            bus.connect(sig, conn)

    say("== events")
    guards = []
    for ev in evs:
        say(f"> {ev['line']}")
        if ev["err"]:
            say(f"  error: events.log:{ev['no']}: {ev['err']}")
            continue
        try:
            if ev["cmd"] is not None:
                command(bus, guards, ev["cmd"])
                continue
            if ev["signal"] not in bus.signals:
                raise ValueError(f"no signal '{ev['signal']}'")
            sig = bus.signals[ev["signal"]]
            bus.send(sig, ev["sender"], ev["at"], ev["fields"], 0)
            keep = []
            for g in guards:
                if g["signal"] is sig:
                    g["left"] -= 1
                    if g["left"] == 0:
                        sig.receivers = [c for c in sig.receivers if c["id"] != g["id"]]
                        say(f"  trace on {sig.name} ended")
                        continue
                keep.append(g)
            guards[:] = keep
        except ValueError as e:
            say(f"  error: events.log:{ev['no']}: {e}")

    say("== end")
    for p in plugins:
        sub = bus.alive(p["name"])
        if sub is None:
            say(f"  {p['name']}: gone")
        else:
            say(f"  {p['name']}: {sub.delivered} delivered; {sub.handler.summary()}")
    inv = [bus.alive(p["name"]) for p in plugins if p["kind"] == "inventory"]
    if inv and inv[0] is not None:
        for sku, (q, level) in inv[0].handler.stock.items():
            say(f"  stock {sku}: {q} (reorder at {level})")
    for s in signals:
        say(f"  sent {s}: {counts[s]}")
    # Closing every plugin's files.
    for p in plugins:
        sub = bus.alive(p["name"])
        if sub is not None and hasattr(sub.handler, "fh"):
            sub.handler.fh.close()
    say("== files")
    for n in sorted(os.listdir("data/out")):
        with open(f"data/out/{n}", encoding="utf-8", newline="") as fh:
            text = fh.read()
        say(f"  {n}: {text.count(chr(10))} lines")
    print("\n".join(OUT))


def command(bus, guards, w):
    cmd, args = w[0], w[1:]
    usage = {"status": "", "mute": "<signal>", "unmute": "<signal>", "drop": "<plugin>",
             "disconnect": "<receiver> <signal>", "temp": "<signal> <count>"}
    if cmd not in usage:
        raise ValueError(f"unknown command '{cmd}'")
    if len(args) != len(usage[cmd].split()):
        raise ValueError(f"usage: @ {cmd} {usage[cmd]}".rstrip())

    def sig(name):
        if name not in bus.signals:
            raise ValueError(f"no signal '{name}'")
        return bus.signals[name]

    if cmd == "status":
        for s in bus.order:
            g = bus.signals[s]
            parts = []
            for c in g.receivers:
                t = c["name"]
                if c["kind"] == "weak":
                    t += " (weak)"
                if c["sender"]:
                    t += f" (from {c['sender']})"
                parts.append(t)
            m = " [muted]" if g.muted else ""
            say(f"  {s}{m}: {', '.join(parts) if parts else 'none'}")
    elif cmd in ("mute", "unmute"):
        sig(args[0]).muted = cmd == "mute"
        say(f"  {cmd}d {args[0]}")
    elif cmd == "drop":
        if args[0] not in bus.held:
            raise ValueError(f"{args[0]} is not held")
        del bus.held[args[0]]
        say(f"  dropped {args[0]}")
    elif cmd == "disconnect":
        g = sig(args[1])
        for c in g.receivers:
            if c["name"] == args[0]:
                g.receivers = [x for x in g.receivers if x["id"] != c["id"]]
                say(f"  disconnected {args[0]} from {args[1]}")
                return
        raise ValueError(f"{args[0]} is not connected to {args[1]}")
    else:
        g = sig(args[0])
        if not digits(args[1]) or int(args[1]) == 0 or int(args[1]) > 99:
            raise ValueError(f"bad count '{args[1]}'")
        seen = [0]

        def trace(d):
            seen[0] += 1
            return f"trace #{seen[0]}: {fields_text(d['fields'])}"

        cid = bus.connect(g, {"name": "trace", "kind": "func", "f": trace, "sender": None})
        guards.append({"signal": g, "id": cid, "left": int(args[1])})
        say(f"  trace on {args[0]} for {args[1]} sends")


main()
