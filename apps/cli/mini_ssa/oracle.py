"""The Python mirror of mini_ssa: the same optimizer middle end, written
first, whose transcript is expected.out. It reads a three-address IR,
builds the CFG, computes dominators (Cooper, Harvey and Kennedy),
dominance frontiers, natural loops and liveness, puts the program in SSA
form (Cytron et al., semi-pruned as Briggs et al. describe), runs sparse
conditional constant propagation (Wegman and Zadeck), copy propagation,
dead code elimination and CFG cleanup, and leaves SSA with critical-edge
splitting and sequentialized parallel copies. An interpreter runs every
stage, so each job shows that the optimized program computes the same.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os
import sys

BINOPS = ["==", "!=", "<=", ">=", "<<", ">>", "+", "-", "*", "/", "%", "<", ">", "&", "|", "^"]
STEP_LIMIT = 200000
DEPTH_LIMIT = 200


def wrap(v):
    """32-bit two's complement, as the IR's integers are."""
    v &= 0xFFFFFFFF
    return v - (1 << 32) if v & 0x80000000 else v


def tdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def fold(op, a, b):
    """The value of a op b, or None when it traps (division by zero)."""
    if op == "+":
        return wrap(a + b)
    if op == "-":
        return wrap(a - b)
    if op == "*":
        return wrap(a * b)
    if op == "/":
        if b == 0:
            return None
        return wrap(tdiv(a, b))
    if op == "%":
        if b == 0:
            return None
        return wrap(a - b * tdiv(a, b))
    if op == "&":
        return wrap(a & b)
    if op == "|":
        return wrap(a | b)
    if op == "^":
        return wrap(a ^ b)
    if op == "<<":
        return wrap(a << (b & 31))
    if op == ">>":
        return wrap(a >> (b & 31))
    cmp = {"==": a == b, "!=": a != b, "<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}
    return 1 if cmp[op] else 0


# ------------------------------------------------------------------ IR


class Opd:
    """An operand: a variable, a constant, or undef (which reads as 0)."""
    __slots__ = ("kind", "name", "val")

    def __init__(self, kind, name="", val=0):
        self.kind, self.name, self.val = kind, name, val

    def show(self):
        if self.kind == "var":
            return self.name
        if self.kind == "const":
            return str(self.val)
        return "undef"

    def same(self, o):
        return self.kind == o.kind and self.name == o.name and self.val == o.val


def var(n):
    return Opd("var", n)


def const(v):
    return Opd("const", "", v)


class Instr:
    """op: bin, copy, call, print, br, jmp, ret, phi. A phi's args run
    parallel to its preds."""

    def __init__(self, op, dst="", binop="", args=(), labels=(), func="", line=0):
        self.op, self.dst, self.binop = op, dst, binop
        self.args = list(args)
        self.labels = list(labels)
        self.func = func
        self.line = line
        self.preds = []

    def copy(self):
        i = Instr(self.op, self.dst, self.binop, [Opd(a.kind, a.name, a.val) for a in self.args],
                  self.labels, self.func, self.line)
        i.preds = list(self.preds)
        return i

    def is_term(self):
        return self.op in ("br", "jmp", "ret")

    def pure(self):
        """No effect but its value: a division by a variable or by zero may
        trap, so it is not."""
        if self.op == "bin" and self.binop in ("/", "%"):
            d = self.args[1]
            return d.kind == "const" and d.val != 0
        return self.op in ("bin", "copy", "phi")

    def show(self):
        a = [x.show() for x in self.args]
        if self.op == "bin":
            return f"{self.dst} = {a[0]} {self.binop} {a[1]}"
        if self.op == "copy":
            return f"{self.dst} = {a[0]}"
        if self.op == "call":
            s = f"call {self.func}({', '.join(a)})"
            return f"{self.dst} = {s}" if self.dst else s
        if self.op == "print":
            return f"print {a[0]}"
        if self.op == "br":
            return f"br {a[0]}, {self.labels[0]}, {self.labels[1]}"
        if self.op == "jmp":
            return f"jmp {self.labels[0]}"
        if self.op == "ret":
            return f"ret {a[0]}" if a else "ret"
        pairs = ", ".join(f"[{x}, {p}]" for x, p in zip(a, self.preds))
        return f"{self.dst} = phi {pairs}"


class Block:
    def __init__(self, name, line):
        self.name, self.line = name, line
        self.instrs = []

    def term(self):
        return self.instrs[-1]

    def succs(self):
        t = self.term()
        out = []
        for l in t.labels:
            if l not in out:
                out.append(l)
        return out


class Func:
    def __init__(self, name, params, line):
        self.name, self.params, self.line = name, params, line
        self.blocks = []

    def block(self, name):
        for b in self.blocks:
            if b.name == name:
                return b
        return None

    def copy(self):
        f = Func(self.name, list(self.params), self.line)
        for b in self.blocks:
            nb = Block(b.name, b.line)
            nb.instrs = [i.copy() for i in b.instrs]
            f.blocks.append(nb)
        return f

    def show(self):
        out = [f"func {self.name}({', '.join(self.params)}) {{"]
        for b in self.blocks:
            out.append(f"{b.name}:")
            for i in b.instrs:
                out.append("  " + i.show())
        out.append("}")
        return out


# ------------------------------------------------------------------ parser


class IrError(Exception):
    def __init__(self, line, msg):
        self.line, self.msg = line, msg


def is_name(s):
    if not s or not (s[0].isalpha() or s[0] == "_"):
        return False
    return all(c.isalnum() or c == "_" for c in s)


def is_int(s):
    t = s[1:] if s.startswith("-") else s
    return t.isdigit()


def operand(tok, line):
    if is_int(tok):
        return const(wrap(int(tok)))
    if is_name(tok):
        return var(tok)
    raise IrError(line, f"bad operand '{tok}'")


def split_args(text, line):
    text = text.strip()
    if not text:
        return []
    return [operand(p.strip(), line) for p in text.split(",")]


def parse_instr(text, line):
    words = text.split()
    head = words[0]
    if head == "print":
        if len(words) != 2:
            raise IrError(line, "print takes one operand")
        return Instr("print", args=[operand(words[1], line)], line=line)
    if head == "jmp":
        if len(words) != 2 or not is_name(words[1]):
            raise IrError(line, "jmp takes one label")
        return Instr("jmp", labels=[words[1]], line=line)
    if head == "ret":
        if len(words) == 1:
            return Instr("ret", line=line)
        if len(words) != 2:
            raise IrError(line, "ret takes at most one operand")
        return Instr("ret", args=[operand(words[1], line)], line=line)
    if head == "br":
        parts = [p.strip() for p in text[2:].split(",")]
        if len(parts) != 3 or not is_name(parts[1]) or not is_name(parts[2]):
            raise IrError(line, "br takes a condition and two labels")
        return Instr("br", args=[operand(parts[0], line)], labels=[parts[1], parts[2]], line=line)
    if head == "call":
        return parse_call("", text, line)
    if len(words) >= 3 and words[1] == "=":
        dst = words[0]
        if not is_name(dst):
            raise IrError(line, f"bad destination '{dst}'")
        rhs = text[text.index("=") + 1:].strip()
        if rhs.startswith("call "):
            return parse_call(dst, rhs, line)
        r = rhs.split()
        if len(r) == 1:
            return Instr("copy", dst, args=[operand(r[0], line)], line=line)
        if len(r) == 3 and r[1] in BINOPS:
            return Instr("bin", dst, r[1], [operand(r[0], line), operand(r[2], line)], line=line)
        raise IrError(line, f"cannot read '{rhs}'")
    raise IrError(line, f"unknown instruction '{head}'")


def parse_call(dst, text, line):
    rest = text[len("call"):].strip()
    if "(" not in rest or not rest.endswith(")"):
        raise IrError(line, "a call is written call f(args)")
    name = rest[:rest.index("(")].strip()
    if not is_name(name):
        raise IrError(line, f"bad function name '{name}'")
    args = split_args(rest[rest.index("(") + 1:-1], line)
    return Instr("call", dst, args=args, func=name, line=line)


def parse(src):
    funcs = []
    cur = None
    blk = None
    for n, raw in enumerate(src.split("\n"), 1):
        text = raw.split("#")[0].strip()
        if not text:
            continue
        if cur is None:
            if not (text.startswith("func ") and text.endswith("{")):
                raise IrError(n, "expected 'func name(params) {'")
            head = text[5:-1].strip()
            if "(" not in head or not head.endswith(")"):
                raise IrError(n, "expected 'func name(params) {'")
            name = head[:head.index("(")].strip()
            ps = [p.strip() for p in head[head.index("(") + 1:-1].split(",") if p.strip()]
            for p in ps:
                if not is_name(p):
                    raise IrError(n, f"bad parameter '{p}'")
            for f in funcs:
                if f.name == name:
                    raise IrError(n, f"function {name} is defined twice")
            cur = Func(name, ps, n)
            blk = None
            continue
        if text == "}":
            if not cur.blocks:
                raise IrError(n, f"function {cur.name} has no blocks")
            funcs.append(cur)
            cur = None
            continue
        if text.endswith(":"):
            label = text[:-1].strip()
            if not is_name(label):
                raise IrError(n, f"bad label '{label}'")
            if cur.block(label) is not None:
                raise IrError(n, f"label {label} is defined twice")
            blk = Block(label, n)
            cur.blocks.append(blk)
            continue
        if blk is None:
            raise IrError(n, "an instruction before the first label")
        if blk.instrs and blk.instrs[-1].is_term():
            raise IrError(n, f"an instruction after the terminator of block {blk.name}")
        blk.instrs.append(parse_instr(text, n))
    if cur is not None:
        raise IrError(len(src.split("\n")), f"function {cur.name} is not closed")
    for f in funcs:
        for b in f.blocks:
            if not b.instrs or not b.instrs[-1].is_term():
                raise IrError(b.line, f"block {b.name} has no terminator")
            for l in b.term().labels:
                if f.block(l) is None:
                    raise IrError(b.term().line, f"unknown label {l}")
                if l == f.blocks[0].name:
                    raise IrError(b.term().line, f"the entry block {l} cannot be a jump target")
            for i in b.instrs:
                if i.op == "call":
                    g = None
                    for h in funcs:
                        if h.name == i.func:
                            g = h
                    if g is None:
                        raise IrError(i.line, f"unknown function {i.func}")
                    if len(g.params) != len(i.args):
                        raise IrError(i.line, f"{i.func} takes {len(g.params)} argument(s), "
                                              f"given {len(i.args)}")
    return funcs


# ------------------------------------------------------------------ CFG


class Cfg:
    """Reachable blocks, their edges, the RPO and the dominator tree."""

    def __init__(self, f):
        self.f = f
        self.reach = self.reachable()
        names = [b.name for b in f.blocks if b.name in self.reach]
        self.names = names
        self.succ = {n: f.block(n).succs() for n in names}
        self.pred = {n: [] for n in names}
        for n in names:
            for s in self.succ[n]:
                self.pred[s].append(n)
        self.rpo = self.order()
        self.index = {n: k for k, n in enumerate(self.rpo)}
        self.idom = self.dominators()
        self.children = {n: [] for n in self.rpo}
        for n in self.rpo[1:]:
            self.children[self.idom[n]].append(n)
        self.df = self.frontiers()

    def reachable(self):
        seen = set()
        stack = [self.f.blocks[0].name]
        while stack:
            n = stack.pop()
            if n in seen:
                continue
            seen.add(n)
            for s in self.f.block(n).succs():
                stack.append(s)
        return seen

    def order(self):
        post = []
        seen = set()

        def dfs(n):
            seen.add(n)
            for s in self.succ[n]:
                if s not in seen:
                    dfs(s)
            post.append(n)
        dfs(self.names[0])
        return post[::-1]

    def dominators(self):
        entry = self.rpo[0]
        idom = {entry: entry}
        changed = True
        while changed:
            changed = False
            for b in self.rpo[1:]:
                new = None
                for p in self.pred[b]:
                    if p in idom:
                        new = p if new is None else self.intersect(idom, p, new)
                if idom.get(b) != new:
                    idom[b] = new
                    changed = True
        return idom

    def intersect(self, idom, a, b):
        while a != b:
            while self.index[a] > self.index[b]:
                a = idom[a]
            while self.index[b] > self.index[a]:
                b = idom[b]
        return a

    def dominates(self, a, b):
        while True:
            if a == b:
                return True
            if b == self.rpo[0]:
                return False
            b = self.idom[b]

    def frontiers(self):
        df = {n: [] for n in self.rpo}
        for b in self.rpo:
            if len(self.pred[b]) >= 2:
                for p in self.pred[b]:
                    r = p
                    while r != self.idom[b]:
                        if b not in df[r]:
                            df[r].append(b)
                        r = self.idom[r]
        for n in df:
            df[n].sort(key=lambda x: self.index[x])
        return df

    def loops(self):
        out = []
        for h in self.rpo:
            tails = [t for t in self.pred[h] if self.dominates(h, t)]
            if not tails:
                continue
            body = {h}
            stack = list(tails)
            while stack:
                n = stack.pop()
                if n in body:
                    continue
                body.add(n)
                stack.extend(self.pred[n])
            out.append((h, sorted(tails, key=lambda x: self.index[x]),
                        sorted(body, key=lambda x: self.index[x])))
        return out


def drop_unreachable(f, cfg):
    f.blocks = [b for b in f.blocks if b.name in cfg.reach]
    for b in f.blocks:
        for i in b.instrs:
            if i.op == "phi":
                keep = [k for k, p in enumerate(i.preds) if p in cfg.reach]
                i.args = [i.args[k] for k in keep]
                i.preds = [i.preds[k] for k in keep]


# ------------------------------------------------------------------ liveness


def uses_defs(b):
    uses, defs = [], []
    for i in b.instrs:
        for a in i.args:
            if a.kind == "var" and a.name not in defs and a.name not in uses:
                uses.append(a.name)
        if i.dst and i.dst not in defs:
            defs.append(i.dst)
    return uses, defs


def liveness(f, cfg):
    ud = {n: uses_defs(f.block(n)) for n in cfg.rpo}
    live_in = {n: set() for n in cfg.rpo}
    live_out = {n: set() for n in cfg.rpo}
    changed = True
    while changed:
        changed = False
        for n in reversed(cfg.rpo):
            out = set()
            for s in cfg.succ[n]:
                out |= live_in[s]
            uses, defs = ud[n]
            inn = set(uses) | (out - set(defs))
            if out != live_out[n] or inn != live_in[n]:
                live_out[n], live_in[n] = out, inn
                changed = True
    return live_in, live_out


# ------------------------------------------------------------------ SSA


def to_ssa(f, notes):
    """Semi-pruned SSA: a phi only for a name used in some block before
    that block defines it."""
    cfg = Cfg(f)
    drop_unreachable(f, cfg)
    live_in, _ = liveness(f, cfg)
    globals_ = []
    defsites = {}
    for p in f.params:
        defsites.setdefault(p, []).append(cfg.rpo[0])
    for n in cfg.rpo:
        uses, defs = uses_defs(f.block(n))
        for u in uses:
            if u not in globals_:
                globals_.append(u)
        for d in defs:
            if n not in defsites.setdefault(d, []):
                defsites[d].append(n)
    phis = {n: [] for n in cfg.rpo}
    for x in sorted(globals_):
        work = list(defsites.get(x, []))
        has = set()
        while work:
            n = work.pop(0)
            for d in cfg.df[n]:
                if d not in has:
                    has.add(d)
                    phis[d].append(x)
                    if d not in work:
                        work.append(d)
    for n in cfg.rpo:
        b = f.block(n)
        new = []
        for x in sorted(phis[n]):
            i = Instr("phi", x, args=[var(x) for _ in cfg.pred[n]])
            i.preds = list(cfg.pred[n])
            new.append(i)
        b.instrs = new + b.instrs
    counter = {}
    stacks = {}
    warned = set()

    def fresh(x):
        k = counter.get(x, 0)
        counter[x] = k + 1
        name = f"{x}.{k}"
        stacks.setdefault(x, []).append(name)
        return name

    def top(x, block, line):
        s = stacks.get(x)
        if s:
            return var(s[-1])
        if x not in warned:
            warned.add(x)
            notes.append(f"line {line}: {x} may be used before it is set (in block {block})")
        return Opd("undef")

    params = [fresh(p) for p in f.params]

    def rename(n):
        b = f.block(n)
        pushed = []
        for i in b.instrs:
            if i.op != "phi":
                i.args = [top(a.name, n, i.line) if a.kind == "var" else a for a in i.args]
            if i.dst:
                pushed.append(i.dst)
                i.dst = fresh(i.dst)
        for s in cfg.succ[n]:
            for i in f.block(s).instrs:
                if i.op != "phi":
                    break
                k = i.preds.index(n)
                base = i.args[k].name
                st = stacks.get(base)
                if st:
                    i.args[k] = var(st[-1])
                    continue
                i.args[k] = Opd("undef")
                # an edge on which nothing has set a name the join reads
                if base in live_in[s] and base not in warned:
                    warned.add(base)
                    notes.append(f"line {f.block(s).line}: {base} may be used before it is set "
                                 f"(in block {s})")
        for c in cfg.children[n]:
            rename(c)
        for x in pushed:
            stacks[x].pop()

    # phis keep their variable's base name until renamed; record it first
    for n in cfg.rpo:
        for i in f.block(n).instrs:
            if i.op == "phi":
                i.args = [var(i.dst) for _ in i.args]
    rename(cfg.rpo[0])
    f.params = params
    return f


# ------------------------------------------------------------------ SCCP

TOP, CONST, BOT = 0, 1, 2


def sccp(f, stats):
    """Sparse conditional constant propagation, run to its fixpoint by
    sweeping the executable blocks in RPO (the same fixpoint as the
    work-list form). Returns the lattice and the executable edges."""
    cfg = Cfg(f)
    val = {}
    for p in f.params:
        val[p] = (BOT, 0)
    for b in f.blocks:
        for i in b.instrs:
            if i.dst:
                val[i.dst] = (TOP, 0)
    exe_block = {cfg.rpo[0]}
    exe_edge = set()

    def get(a):
        if a.kind == "const":
            return (CONST, a.val)
        if a.kind == "undef":
            return (CONST, 0)
        return val[a.name]

    def meet(x, y):
        if x[0] == TOP:
            return y
        if y[0] == TOP:
            return x
        if x[0] == BOT or y[0] == BOT:
            return (BOT, 0)
        return x if x[1] == y[1] else (BOT, 0)

    changed = True
    while changed:
        changed = False
        for n in cfg.rpo:
            if n not in exe_block:
                continue
            b = f.block(n)
            for i in b.instrs:
                if i.op == "phi":
                    v = (TOP, 0)
                    for a, p in zip(i.args, i.preds):
                        if (p, n) in exe_edge:
                            v = meet(v, get(a))
                elif i.op == "bin":
                    x, y = get(i.args[0]), get(i.args[1])
                    if x[0] == BOT or y[0] == BOT:
                        v = (BOT, 0)
                    elif x[0] == TOP or y[0] == TOP:
                        v = (TOP, 0)
                    else:
                        r = fold(i.binop, x[1], y[1])
                        v = (BOT, 0) if r is None else (CONST, r)
                elif i.op == "copy":
                    v = get(i.args[0])
                elif i.op == "call":
                    v = (BOT, 0)
                else:
                    v = None
                if i.dst and v is not None and v != val[i.dst]:
                    val[i.dst] = v
                    changed = True
            t = b.term()
            targets = []
            if t.op == "jmp":
                targets = [t.labels[0]]
            elif t.op == "br":
                c = get(t.args[0])
                if c[0] == CONST:
                    targets = [t.labels[0] if c[1] != 0 else t.labels[1]]
                elif c[0] == BOT:
                    targets = list(t.labels)
            for s in targets:
                if (n, s) not in exe_edge:
                    exe_edge.add((n, s))
                    changed = True
                if s not in exe_block:
                    exe_block.add(s)
                    changed = True
    return val, exe_block, exe_edge


def optimize(f, stats):
    val, exe_block, exe_edge = sccp(f, stats)
    # constants replace their uses; constant branches become jumps
    for b in f.blocks:
        if b.name not in exe_block:
            continue
        keep = []
        for i in b.instrs:
            i.args = [const(val[a.name][1]) if a.kind == "var" and val[a.name][0] == CONST
                      else a for a in i.args]
            if i.op == "phi":
                k = [j for j, p in enumerate(i.preds) if (p, b.name) in exe_edge]
                i.args = [i.args[j] for j in k]
                i.preds = [i.preds[j] for j in k]
            if i.dst and i.op in ("bin", "copy", "phi") and val[i.dst][0] == CONST:
                stats["folded"] += 1
                continue
            if i.op == "br" and i.args[0].kind == "const":
                taken = i.labels[0] if i.args[0].val != 0 else i.labels[1]
                stats["branches"] += 1
                i = Instr("jmp", labels=[taken], line=i.line)
            keep.append(i)
        b.instrs = keep
    before = len(f.blocks)
    f.blocks = [b for b in f.blocks if b.name in exe_block]
    stats["blocks"] += before - len(f.blocks)
    fix_phis(f)
    copy_propagate(f, stats)
    dce(f, stats)
    simplify(f, stats)
    copy_propagate(f, stats)
    dce(f, stats)
    return f


def fix_phis(f):
    """Phis keep an argument only for a predecessor that still jumps to
    them, and a phi with one argument, or with the same argument
    everywhere, becomes a copy."""
    cfg = Cfg(f)
    for b in f.blocks:
        preds = cfg.pred.get(b.name, [])
        new = []
        for i in b.instrs:
            if i.op == "phi":
                k = [j for j, p in enumerate(i.preds) if p in preds]
                i.args = [i.args[j] for j in k]
                i.preds = [i.preds[j] for j in k]
                distinct = []
                for a in i.args:
                    if not (a.kind == "var" and a.name == i.dst) and \
                            not any(a.same(d) for d in distinct):
                        distinct.append(a)
                if len(distinct) == 1:
                    i = Instr("copy", i.dst, args=[distinct[0]], line=i.line)
            new.append(i)
        b.instrs = new


def copy_propagate(f, stats):
    changed = True
    while changed:
        changed = False
        sub = {}
        for b in f.blocks:
            for i in b.instrs:
                if i.op == "copy":
                    sub[i.dst] = i.args[0]
        if not sub:
            return

        def resolve(a, depth=0):
            while a.kind == "var" and a.name in sub and depth < 1000:
                a = sub[a.name]
                depth += 1
            return a
        for b in f.blocks:
            keep = []
            for i in b.instrs:
                if i.op == "copy":
                    stats["copies"] += 1
                    changed = True
                    continue
                i.args = [resolve(a) for a in i.args]
                keep.append(i)
            b.instrs = keep
        fix_phis(f)


def dce(f, stats):
    defs = {}
    for b in f.blocks:
        for i in b.instrs:
            if i.dst:
                defs[i.dst] = i
    live = set()
    work = []
    for b in f.blocks:
        for i in b.instrs:
            if not i.pure():
                for a in i.args:
                    if a.kind == "var":
                        work.append(a.name)
    while work:
        x = work.pop()
        if x in live:
            continue
        live.add(x)
        d = defs.get(x)
        if d is not None:
            for a in d.args:
                if a.kind == "var":
                    work.append(a.name)
    for b in f.blocks:
        keep = []
        for i in b.instrs:
            if i.pure() and i.dst not in live:
                stats["dead"] += 1
                continue
            keep.append(i)
        b.instrs = keep


def simplify(f, stats):
    """Thread jumps through empty blocks and merge a block into its only
    predecessor when that predecessor has no other successor."""
    for b in f.blocks:
        t = b.term()
        if t.op == "br" and t.labels[0] == t.labels[1]:
            b.instrs[-1] = Instr("jmp", labels=[t.labels[0]], line=t.line)
            stats["branches"] += 1
    changed = True
    while changed:
        changed = False
        cfg = Cfg(f)
        entry = f.blocks[0].name
        for b in f.blocks:
            if b.name == entry or len(b.instrs) != 1 or b.instrs[0].op != "jmp":
                continue
            target = b.instrs[0].labels[0]
            if target == b.name:
                continue
            t = f.block(target)
            if any(i.op == "phi" for i in t.instrs):
                continue
            for p in cfg.pred[b.name]:
                pt = f.block(p).term()
                pt.labels = [target if l == b.name else l for l in pt.labels]
                if pt.op == "br" and pt.labels[0] == pt.labels[1]:
                    f.block(p).instrs[-1] = Instr("jmp", labels=[pt.labels[0]], line=pt.line)
            f.blocks = [x for x in f.blocks if x.name != b.name]
            stats["blocks"] += 1
            changed = True
            break
        if changed:
            continue
        for b in f.blocks:
            if b.term().op != "jmp":
                continue
            s = b.term().labels[0]
            if s == entry or s == b.name or len(cfg.pred[s]) != 1:
                continue
            sb = f.block(s)
            body = []
            for i in sb.instrs:
                if i.op == "phi":
                    i = Instr("copy", i.dst, args=[i.args[0]], line=i.line)
                body.append(i)
            b.instrs = b.instrs[:-1] + body
            f.blocks = [x for x in f.blocks if x.name != s]
            for x in f.blocks:
                for i in x.instrs:
                    if i.op == "phi":
                        i.preds = [b.name if p == s else p for p in i.preds]
            stats["blocks"] += 1
            changed = True
            break
        if changed:
            copy_propagate(f, stats)


# ------------------------------------------------------------------ out of SSA


def out_of_ssa(f):
    # a branch to one label twice is a jump, so no copy lands before a br
    for b in f.blocks:
        t = b.term()
        if t.op == "br" and t.labels[0] == t.labels[1]:
            b.instrs[-1] = Instr("jmp", labels=[t.labels[0]], line=t.line)
    cfg = Cfg(f)
    # split each critical edge that reaches a phi
    edges = []
    for b in f.blocks:
        if any(i.op == "phi" for i in b.instrs) and len(cfg.pred[b.name]) >= 2:
            for p in cfg.pred[b.name]:
                if len(cfg.succ[p]) >= 2:
                    edges.append((p, b.name))
    for p, s in edges:
        name = f"{p}_{s}"
        while f.block(name) is not None:
            name += "_"
        nb = Block(name, 0)
        nb.instrs = [Instr("jmp", labels=[s])]
        t = f.block(p).term()
        t.labels = [name if l == s else l for l in t.labels]
        k = [x.name for x in f.blocks].index(p)
        f.blocks.insert(k + 1, nb)
        for i in f.block(s).instrs:
            if i.op == "phi":
                i.preds = [name if q == p else q for q in i.preds]
    tmp = [0]
    for b in f.blocks:
        phis = [i for i in b.instrs if i.op == "phi"]
        if not phis:
            continue
        b.instrs = [i for i in b.instrs if i.op != "phi"]
        preds = []
        for i in phis:
            for q in i.preds:
                if q not in preds:
                    preds.append(q)
        for q in preds:
            copies = []
            for i in phis:
                a = i.args[i.preds.index(q)]
                if not (a.kind == "var" and a.name == i.dst):
                    copies.append((i.dst, a))
            seq = sequentialize(copies, tmp)
            pb = f.block(q)
            pb.instrs = pb.instrs[:-1] + [Instr("copy", d, args=[a]) for d, a in seq] + [pb.instrs[-1]]
    return f


def sequentialize(copies, tmp):
    """A parallel copy as a sequence: a copy whose destination no other
    pending copy reads goes first; a cycle is broken through a temporary."""
    pending = list(copies)
    out = []
    while pending:
        k = None
        for j, (d, a) in enumerate(pending):
            if not any(o[1].kind == "var" and o[1].name == d for jj, o in enumerate(pending) if jj != j):
                k = j
                break
        if k is not None:
            out.append(pending.pop(k))
            continue
        d, a = pending[0]
        t = f"$t{tmp[0]}"
        tmp[0] += 1
        out.append((t, var(d)))
        pending = [(dd, var(t) if aa.kind == "var" and aa.name == d else aa) for dd, aa in pending]
    return out


# ------------------------------------------------------------------ interpreter


class Trap(Exception):
    pass


class Machine:
    def __init__(self, funcs):
        self.funcs = {f.name: f for f in funcs}
        self.steps = 0
        self.out = []

    def call(self, name, args, depth):
        if depth > DEPTH_LIMIT:
            raise Trap("call depth limit")
        f = self.funcs[name]
        env = dict(zip(f.params, args))
        blocks = {b.name: b for b in f.blocks}
        cur = f.blocks[0]
        prev = None
        while True:
            # phis read their arguments in parallel on entry, and cost no
            # step: they are what the copies out of SSA will pay for
            vals = []
            k = 0
            for i in cur.instrs:
                if i.op != "phi":
                    break
                a = i.args[i.preds.index(prev)]
                vals.append((i.dst, self.read(env, a)))
                k += 1
            for d, v in vals:
                env[d] = v
            for i in cur.instrs[k:]:
                self.steps += 1
                if self.steps > STEP_LIMIT:
                    raise Trap("step limit")
                if i.op == "bin":
                    r = fold(i.binop, self.read(env, i.args[0]), self.read(env, i.args[1]))
                    if r is None:
                        raise Trap(f"division by zero in {name}, block {cur.name}")
                    env[i.dst] = r
                elif i.op == "copy":
                    env[i.dst] = self.read(env, i.args[0])
                elif i.op == "call":
                    r = self.call(i.func, [self.read(env, a) for a in i.args], depth + 1)
                    if i.dst:
                        env[i.dst] = r
                elif i.op == "print":
                    self.out.append(str(self.read(env, i.args[0])))
                elif i.op == "ret":
                    return self.read(env, i.args[0]) if i.args else 0
                elif i.op == "jmp":
                    prev, cur = cur.name, blocks[i.labels[0]]
                    break
                elif i.op == "br":
                    c = self.read(env, i.args[0])
                    prev, cur = cur.name, blocks[i.labels[0] if c != 0 else i.labels[1]]
                    break

    @staticmethod
    def read(env, a):
        if a.kind == "const":
            return a.val
        if a.kind == "undef":
            return 0
        return env.get(a.name, 0)


def execute(funcs, name, args):
    m = Machine(funcs)
    try:
        r = m.call(name, args, 0)
        res = f"returned {r}"
    except Trap as t:
        res = f"trap: {t}"
    return m.out, res, m.steps


# ------------------------------------------------------------------ jobs


def new_stats():
    return {"folded": 0, "branches": 0, "copies": 0, "dead": 0, "blocks": 0}


def stage(funcs, which, notes):
    """Every function at a stage: ssa, opt or out."""
    out = []
    stats = new_stats()
    for f in funcs:
        g = to_ssa(f.copy(), notes)
        if which in ("opt", "out"):
            g = optimize(g, stats)
        if which == "out":
            g = out_of_ssa(g)
        out.append(g)
    return out, stats


def fmt_set(s):
    items = sorted(s)
    return ", ".join(items) if items else "-"


def run_job(mode, rest, fname, src):
    out = []
    try:
        funcs = parse(src)
    except IrError as e:
        return [f"{fname}:{e.line}: error: {e.msg}"]
    if mode in ("cfg", "dom", "live", "ssa", "opt", "out"):
        target = rest[0] if rest else funcs[0].name
        f = None
        for g in funcs:
            if g.name == target:
                f = g
        if f is None:
            return [f"{fname}: error: no function {target}"]
        idx = funcs.index(f)
    if mode == "cfg":
        cfg = Cfg(f)
        for b in f.blocks:
            if b.name not in cfg.reach:
                out.append(f"note: block {b.name} (line {b.line}) is unreachable")
        out.append("rpo: " + " ".join(cfg.rpo))
        for n in cfg.names:
            out.append(f"{n}: preds {', '.join(cfg.pred[n]) or '-'}; succs {', '.join(cfg.succ[n]) or '-'}")
        return out
    if mode == "dom":
        cfg = Cfg(f)
        for n in cfg.rpo:
            idom = "-" if n == cfg.rpo[0] else cfg.idom[n]
            out.append(f"{n}: idom {idom}; df {', '.join(cfg.df[n]) or '-'}")
        out.append("tree:")

        def tree(n, depth):
            out.append("  " * (depth + 1) + n)
            for c in cfg.children[n]:
                tree(c, depth + 1)
        tree(cfg.rpo[0], 0)
        loops = cfg.loops()
        if not loops:
            out.append("loops: none")
        for h, tails, body in loops:
            out.append(f"loop {h}: back edges from {', '.join(tails)}; body {', '.join(body)}")
        return out
    if mode == "live":
        cfg = Cfg(f)
        li, lo = liveness(f, cfg)
        for n in cfg.rpo:
            out.append(f"{n}: in {fmt_set(li[n])}; out {fmt_set(lo[n])}")
        entry_live = sorted(x for x in li[cfg.rpo[0]] if x not in f.params)
        for x in entry_live:
            out.append(f"warning: {x} is live on entry but is not a parameter")
        return out
    if mode in ("ssa", "opt", "out"):
        notes = []
        stats = new_stats()
        g = to_ssa(f.copy(), notes)
        if mode in ("opt", "out"):
            g = optimize(g, stats)
        if mode == "out":
            g = out_of_ssa(g)
        for n in notes:
            out.append("warning: " + n)
        out += g.show()
        if mode == "opt":
            out.append(f"; folded {stats['folded']}, branches {stats['branches']}, "
                       f"copies {stats['copies']}, dead {stats['dead']}, blocks {stats['blocks']}")
        return out
    if mode == "run":
        name = rest[0]
        if not any(g.name == name for g in funcs):
            return [f"{fname}: error: no function {name}"]
        args = [wrap(int(a)) for a in rest[1:]]
        g = None
        for h in funcs:
            if h.name == name:
                g = h
        if len(args) != len(g.params):
            return [f"{fname}: error: {name} takes {len(g.params)} argument(s), given {len(args)}"]
        notes = []
        results = [("source", funcs)]
        for which in ("ssa", "opt", "out"):
            fs, _ = stage(funcs, which, [])
            results.append((which, fs))
        first = None
        for label, fs in results:
            printed, res, steps = execute(fs, name, args)
            line = f"{label}: {res} after {steps} steps"
            if printed:
                line += "; printed " + " ".join(printed)
            out.append(line)
            key = (printed, res)
            if first is None:
                first = key
            elif key != first:
                out.append(f"MISMATCH: {label} differs from the source")
        return out
    return [f"unknown mode {mode}"]


def unescape(s):
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            out.append({"n": "\n", "t": "\t"}.get(s[i + 1], s[i + 1]))
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def job(line):
    out = [f"$ {line}"]
    words = line.split(" ")
    if words[0] == "snip":
        mode = words[1]
        src = unescape(" ".join(words[2:]))
        rest = []
        if " ;; " in src:
            src, tail = src.split(" ;; ", 1)
            rest = tail.split(" ")
        out += run_job(mode, rest, "snip.ir", src)
    else:
        mode, fname = words[0], words[1]
        with open(os.path.join("data", fname), encoding="utf-8") as fh:
            src = fh.read()
        out += run_job(mode, words[2:], fname, src)
    return "\n".join(out) + "\n"


def main():
    with open(os.path.join("data", "jobs.txt"), encoding="utf-8") as fh:
        jobs = [l.rstrip("\r") for l in fh.read().split("\n") if l.strip()]
    sys.stdout.write("".join(job(j) for j in jobs))


if __name__ == "__main__":
    main()
