"""Reference for mini_transitions. Reads data/ (as mk.py writes it) and
prints the report the Kāra program must print.

Run from this directory: python3 -I -B oracle.py"""

OUT = []
OPS = ["==", "!=", "<", "<=", ">", ">="]
QUEUE_LIMIT = 3
DEPTH_LIMIT = 5


def say(s):
    OUT.append(s)


def is_ident(s):
    return (0 < len(s) <= 32 and "a" <= s[0] <= "z"
            and all(c == "_" or "a" <= c <= "z" or "0" <= c <= "9" for c in s))


def number(s):
    """An i64 written as an optional `-` and 1 to 9 digits, or None."""
    d = s[1:] if s.startswith("-") else s
    if not (0 < len(d) <= 9 and all("0" <= c <= "9" for c in d)):
        return None
    return int(s)


def ancestors(path):
    """`a.b.c` -> [`a`, `a.b`, `a.b.c`]."""
    parts = path.split(".")
    return [".".join(parts[:i]) for i in range(1, len(parts) + 1)]


class Machine:
    def __init__(self, name):
        self.name = name
        self.queued = False
        self.vars = []          # [name, value], declaration order
        self.states = []        # paths, declaration order
        self.final = set()
        self.initial = None
        self.conds = {}         # name -> (var, op, value)
        self.actions = {}       # name -> (op, args)
        self.transitions = []   # dicts
        self.on_enter = {}
        self.on_exit = {}
        self.state = None
        self.busy = False
        self.queue = []
        self.fired = 0
        self.blocked = 0
        self.refused = 0

    def var(self, n):
        for v in self.vars:
            if v[0] == n:
                return v
        return None


def directive(m, w):
    """Applies one directive to machine `m`; raises ValueError."""
    d = w[0]
    if d == "queued":
        if len(w) != 1:
            raise ValueError("usage: queued")
        m.queued = True
    elif d == "var":
        if len(w) != 3:
            raise ValueError("usage: var <name> <value>")
        if not is_ident(w[1]):
            raise ValueError(f"bad var name '{w[1]}'")
        if m.var(w[1]):
            raise ValueError(f"var {w[1]} already defined")
        v = number(w[2])
        if v is None:
            raise ValueError(f"bad value '{w[2]}'")
        m.vars.append([w[1], v])
    elif d == "state":
        if len(w) < 2:
            raise ValueError("usage: state <path> [initial] [final]")
        p = w[1]
        if not all(is_ident(s) for s in p.split(".")):
            raise ValueError(f"bad state name '{p}'")
        if p in m.states:
            raise ValueError(f"state {p} already defined")
        if "." in p:
            parent = p.rsplit(".", 1)[0]
            if parent not in m.states:
                raise ValueError(f"no state '{parent}'")
            if parent in m.final:
                raise ValueError(f"final state {parent} cannot have children")
        initial = final = False
        for f in w[2:]:
            if f == "initial":
                initial = True
            elif f == "final":
                final = True
            else:
                raise ValueError(f"unknown flag '{f}'")
        if initial and m.initial is not None:
            raise ValueError(f"initial state already set to {m.initial}")
        m.states.append(p)
        if initial:
            m.initial = p
        if final:
            m.final.add(p)
    elif d == "cond":
        if len(w) != 5:
            raise ValueError("usage: cond <name> <var> <op> <value>")
        if not is_ident(w[1]):
            raise ValueError(f"bad cond name '{w[1]}'")
        if w[1] in m.conds:
            raise ValueError(f"cond {w[1]} already defined")
        if not m.var(w[2]):
            raise ValueError(f"no var '{w[2]}'")
        if w[3] not in OPS:
            raise ValueError(f"bad operator '{w[3]}'")
        v = number(w[4])
        if v is None:
            raise ValueError(f"bad value '{w[4]}'")
        m.conds[w[1]] = (w[2], w[3], v)
    elif d == "action":
        if len(w) < 3:
            raise ValueError("usage: action <name> <op> ...")
        name, op, args = w[1], w[2], w[3:]
        if not is_ident(name):
            raise ValueError(f"bad action name '{name}'")
        if name in m.actions:
            raise ValueError(f"action {name} already defined")
        if op == "say":
            if not args:
                raise ValueError("usage: action <name> say <words>")
            m.actions[name] = ("say", [" ".join(args)])
        elif op in ("add", "set"):
            if len(args) != 2:
                raise ValueError(f"usage: action <name> {op} <var> <value>")
            if not m.var(args[0]):
                raise ValueError(f"no var '{args[0]}'")
            v = number(args[1])
            if v is None:
                raise ValueError(f"bad value '{args[1]}'")
            m.actions[name] = (op, [args[0], v])
        elif op == "trigger":
            if len(args) not in (1, 2):
                raise ValueError("usage: action <name> trigger [<machine>] <event>")
            target = args[0] if len(args) == 2 else m.name
            m.actions[name] = ("trigger", [target, args[-1]])
        else:
            raise ValueError(f"unknown action '{op}'")
    elif d == "transition":
        if len(w) < 5 or w[3] != "->":
            raise ValueError("usage: transition <trigger> <src> -> <dst> [options]")
        trig, src, dst = w[1], w[2], w[4]
        if not is_ident(trig):
            raise ValueError(f"bad trigger name '{trig}'")
        if trig.startswith("to_"):
            raise ValueError("trigger names starting with to_ are reserved")
        if src != "*" and src not in m.states:
            raise ValueError(f"no state '{src}'")
        if src in m.final:
            raise ValueError(f"final state {src} has no exits")
        if dst != "=" and dst not in m.states:
            raise ValueError(f"no state '{dst}'")
        t = {"trigger": trig, "src": src, "dst": dst}
        for o in w[5:]:
            k, eq, v = o.partition("=")
            if not eq or k not in ("if", "unless", "before", "after"):
                raise ValueError(f"unknown option '{o}'")
            if k in t:
                raise ValueError(f"duplicate option {k}")
            if k in ("if", "unless") and v not in m.conds:
                raise ValueError(f"no cond '{v}'")
            if k in ("before", "after") and v not in m.actions:
                raise ValueError(f"no action '{v}'")
            t[k] = v
        m.transitions.append(t)
    elif d in ("on_enter", "on_exit"):
        if len(w) != 3:
            raise ValueError(f"usage: {d} <state> <action>")
        if w[1] not in m.states:
            raise ValueError(f"no state '{w[1]}'")
        if w[2] not in m.actions:
            raise ValueError(f"no action '{w[2]}'")
        table = m.on_enter if d == "on_enter" else m.on_exit
        table.setdefault(w[1], []).append(w[2])
    else:
        raise ValueError(f"unknown directive '{d}'")


def parse_machines(text):
    machines, errors = [], []
    cur = None

    def close():
        if cur is not None:
            if cur.initial is None:
                errors.append(f"machines.conf: machine {cur.name} has no initial state")
            else:
                cur.state = cur.initial
                machines.append(cur)

    for no, raw in enumerate(text.split("\n"), 1):
        w = raw.split("#", 1)[0].split()
        if not w:
            continue
        if w[0] == "machine":
            close()
            cur = None
            if len(w) != 2:
                errors.append(f"machines.conf:{no}: usage: machine <name>")
            elif not is_ident(w[1]):
                errors.append(f"machines.conf:{no}: bad machine name '{w[1]}'")
            elif any(m.name == w[1] for m in machines):
                errors.append(f"machines.conf:{no}: machine {w[1]} already defined")
            else:
                cur = Machine(w[1])
            continue
        if cur is None:
            errors.append(f"machines.conf:{no}: no machine to add to")
            continue
        try:
            directive(cur, w)
        except ValueError as e:
            errors.append(f"machines.conf:{no}: {e}")
    close()
    return machines, errors


# ------------------------------------------------------------ running


class Bus:
    def __init__(self, machines):
        self.machines = machines

    def get(self, name):
        for m in self.machines:
            if m.name == name:
                return m
        return None

    def holds(self, m, cname):
        var, op, v = m.conds[cname]
        x = m.var(var)[1]
        return {"==": x == v, "!=": x != v, "<": x < v, "<=": x <= v,
                ">": x > v, ">=": x >= v}[op]

    def act(self, m, aname, depth):
        ind = "  " * (depth + 1)
        op, args = m.actions[aname]
        if op == "say":
            say(f"{ind}{m.name} says: {args[0]}")
        elif op == "add":
            m.var(args[0])[1] += args[1]
        elif op == "set":
            m.var(args[0])[1] = args[1]
        else:
            target, ev = args
            say(f"{ind}-> {target} {ev}")
            t = self.get(target)
            if t is None:
                say(f"{ind}no machine '{target}'")
            else:
                self.trigger(t, ev, depth + 1)

    def trigger(self, m, ev, depth):
        ind = "  " * (depth + 1)
        if depth > DEPTH_LIMIT:
            say(f"{ind}{m.name}: too deep, {ev} dropped")
            return
        if not m.queued:
            self.process(m, ev, depth)
            return
        if m.busy:
            m.queue.append(ev)
            say(f"{ind}queued {m.name} {ev}")
            return
        m.busy = True
        self.process(m, ev, depth)
        ran = 0
        while m.queue:
            if ran == QUEUE_LIMIT:
                say(f"{ind}{m.name}: queue limit, dropped {len(m.queue)}")
                m.queue.clear()
                break
            ran += 1
            e = m.queue.pop(0)
            say(f"{ind}run queued {m.name} {e}")
            self.process(m, e, depth)
        m.busy = False

    def process(self, m, trig, depth):
        ind = "  " * (depth + 1)
        cur = m.state
        if trig.startswith("to_"):
            dst = trig[3:]
            if dst not in m.states:
                say(f"{ind}{m.name}: no state '{dst}'")
                m.refused += 1
                return
            if cur in m.final:
                say(f"{ind}{m.name}: can't {trig} from {cur}")
                m.refused += 1
                return
            self.fire(m, {"trigger": trig, "src": cur, "dst": dst}, depth)
            return
        cands = []
        for level in reversed(ancestors(cur)):
            cands += [t for t in m.transitions if t["trigger"] == trig and t["src"] == level]
        if cur not in m.final:
            cands += [t for t in m.transitions if t["trigger"] == trig and t["src"] == "*"]
        if not cands:
            say(f"{ind}{m.name}: can't {trig} from {cur}")
            m.refused += 1
            return
        for t in cands:
            if "if" in t and not self.holds(m, t["if"]):
                continue
            if "unless" in t and self.holds(m, t["unless"]):
                continue
            self.fire(m, t, depth)
            return
        say(f"{ind}{m.name}: {trig} blocked in {cur}")
        m.blocked += 1

    def fire(self, m, t, depth):
        ind = "  " * (depth + 1)
        cur = m.state
        m.fired += 1
        if "before" in t:
            self.act(m, t["before"], depth)
        if t["dst"] == "=":
            say(f"{ind}{m.name}: {cur} -> {cur} (internal)")
        else:
            dst = t["dst"]
            a, b = ancestors(cur), ancestors(dst)
            k = 0
            while k < len(a) and k < len(b) and a[k] == b[k]:
                k += 1
            if k == len(b):
                k -= 1
            for s in reversed(a[k:]):
                say(f"{ind}exit {s}")
                for x in m.on_exit.get(s, []):
                    self.act(m, x, depth)
            m.state = dst
            say(f"{ind}{m.name}: {cur} -> {dst}")
            for s in b[k:]:
                say(f"{ind}enter {s}")
                for x in m.on_enter.get(s, []):
                    self.act(m, x, depth)
        if "after" in t:
            self.act(m, t["after"], depth)


def show_vars(m):
    return " ".join(f"{n}={v}" for n, v in m.vars)


def command(bus, w):
    usage = {"state": "<machine>", "set": "<machine> <var> <value>", "triggers": "<machine>"}
    cmd, args = w[0], w[1:]
    if cmd not in usage:
        raise ValueError(f"unknown command '{cmd}'")
    if len(args) != len(usage[cmd].split()):
        raise ValueError(f"usage: @ {cmd} {usage[cmd]}")
    m = bus.get(args[0])
    if m is None:
        raise ValueError(f"no machine '{args[0]}'")
    if cmd == "state":
        vs = show_vars(m)
        say(f"  {m.name}: {m.state}" + (f" ({vs})" if vs else ""))
    elif cmd == "set":
        v = m.var(args[1])
        if v is None:
            raise ValueError(f"no var '{args[1]}'")
        x = number(args[2])
        if x is None:
            raise ValueError(f"bad value '{args[2]}'")
        v[1] = x
        say(f"  set {m.name}.{args[1]} = {x}")
    else:
        levels = ancestors(m.state)
        names = sorted({t["trigger"] for t in m.transitions
                        if t["src"] in levels or (t["src"] == "*" and m.state not in m.final)})
        say(f"  {m.name} in {m.state}: {', '.join(names) if names else 'none'}")


def main():
    with open("data/machines.conf", encoding="utf-8", newline="") as fh:
        machines, errors = parse_machines(fh.read())
    with open("data/events.log", encoding="utf-8", newline="") as fh:
        lines = [(no, l.strip()) for no, l in enumerate(fh.read().split("\n"), 1)]
    lines = [(no, l) for no, l in lines if l and not l.startswith("#")]
    say("== load")
    say(f"machines.conf: {len(machines)} machines")
    for e in errors:
        say(e)
    for m in machines:
        q = ", queued" if m.queued else ""
        say(f"  {m.name}: {len(m.states)} states, {len(m.transitions)} transitions, "
            f"starts in {m.initial}{q}")
    say(f"events.log: {len(lines)} lines")
    bus = Bus(machines)
    say("== events")
    for no, line in lines:
        say(f"> {line}")
        w = line.split()
        try:
            if w[0] == "@":
                if len(w) < 2:
                    raise ValueError("missing command")
                command(bus, w[1:])
                continue
            if len(w) != 2:
                raise ValueError("usage: <machine> <trigger>")
            m = bus.get(w[0])
            if m is None:
                raise ValueError(f"no machine '{w[0]}'")
            bus.trigger(m, w[1], 0)
        except ValueError as e:
            say(f"  error: events.log:{no}: {e}")
    say("== end")
    for m in machines:
        vs = show_vars(m)
        say(f"  {m.name}: {m.state} after {m.fired} transitions, {m.blocked} blocked, "
            f"{m.refused} refused" + (f"; {vs}" if vs else ""))
    print("\n".join(OUT))


main()
