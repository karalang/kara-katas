"""The Python mirror of mini_regalloc: the same compiler back end, written
first, whose transcript is expected.out. It reads mini_ssa's three-address
IR, selects instructions for a small load/store machine, computes
liveness and live intervals, allocates K registers twice (Poletto and
Sarkar's linear scan, and Chaitin-Briggs graph colouring with optimistic
colouring), rewrites spills through two scratch registers and saves the
registers live across each call, and simulates the machine, so each run
job checks both allocations against an interpreter of the IR.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os
import sys

BINOPS = ["==", "!=", "<=", ">=", "<<", ">>", "+", "-", "*", "/", "%", "<", ">", "&", "|", "^"]
STEP_LIMIT = 100000
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


# ------------------------------------------------------------------ the IR interpreter


class Trap(Exception):
    pass


def ir_read(env, a):
    if a.kind == "const":
        return a.val
    return env.get(a.name, 0)


class IrMachine:
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
        while True:
            nxt = None
            for i in cur.instrs:
                self.steps += 1
                if self.steps > STEP_LIMIT:
                    raise Trap("step limit")
                if i.op == "bin":
                    r = fold(i.binop, ir_read(env, i.args[0]), ir_read(env, i.args[1]))
                    if r is None:
                        raise Trap(f"division by zero in {name}")
                    env[i.dst] = r
                elif i.op == "copy":
                    env[i.dst] = ir_read(env, i.args[0])
                elif i.op == "call":
                    r = self.call(i.func, [ir_read(env, a) for a in i.args], depth + 1)
                    if i.dst:
                        env[i.dst] = r
                elif i.op == "print":
                    self.out.append(str(ir_read(env, i.args[0])))
                elif i.op == "ret":
                    return ir_read(env, i.args[0]) if i.args else 0
                elif i.op == "jmp":
                    nxt = i.labels[0]
                    break
                elif i.op == "br":
                    nxt = i.labels[0] if ir_read(env, i.args[0]) != 0 else i.labels[1]
                    break
            cur = blocks[nxt]


# ------------------------------------------------------------------ the machine

# Registers: r1..rK are allocated; t0 and t1 are scratch for spilled
# values; a0..a3 carry arguments and the result. Every register is
# caller-saved. A virtual register is a %name.

MAX_ARGS = 4
RRI = {"+": "addi", "-": "subi", "&": "andi", "|": "ori", "^": "xori", "<<": "slli", ">>": "srai"}
RRR = {"+": "add", "-": "sub", "*": "mul", "/": "div", "%": "rem", "&": "and", "|": "or",
       "^": "xor", "<<": "sll", ">>": "sra", "==": "seq", "!=": "sne", "<": "slt",
       "<=": "sle", ">": "sgt", ">=": "sge"}
COMMUTES = ["+", "*", "&", "|", "^", "==", "!="]
BINOP_OF = {}
for k, v in RRR.items():
    BINOP_OF[v] = k
for k, v in RRI.items():
    BINOP_OF[v] = k


class R:
    """A register operand: kind v (virtual), r, t, a (physical)."""
    __slots__ = ("kind", "name")

    def __init__(self, kind, name):
        self.kind, self.name = kind, name

    def show(self):
        return "%" + self.name if self.kind == "v" else self.name

    def key(self):
        return self.kind + ":" + self.name


def vr(n):
    return R("v", n)


def ar(k):
    return R("a", f"a{k}")


class MI:
    """op is a mnemonic. dst and srcs are registers; imm is an immediate or
    a stack slot; label a branch target; func and nargs describe a call."""

    def __init__(self, op, dst=None, srcs=(), imm=0, label="", func="", nargs=0):
        self.op, self.dst, self.srcs = op, dst, list(srcs)
        self.imm, self.label, self.func, self.nargs = imm, label, func, nargs

    def show(self):
        s = [x.show() for x in self.srcs]
        op = self.op
        if op == "li":
            return f"li {self.dst.show()}, {self.imm}"
        if op == "mv":
            return f"mv {self.dst.show()}, {s[0]}"
        if op in BINOP_OF and op in RRI.values():
            return f"{op} {self.dst.show()}, {s[0]}, {self.imm}"
        if op in BINOP_OF:
            return f"{op} {self.dst.show()}, {s[0]}, {s[1]}"
        if op == "print":
            return f"print {s[0]}"
        if op in ("bnez", "beqz"):
            return f"{op} {s[0]}, {self.label}"
        if op == "j":
            return f"j {self.label}"
        if op == "call":
            return f"call {self.func}"
        if op == "ret":
            return "ret"
        if op == "ld":
            return f"ld {self.dst.show()}, [sp+{self.imm}]"
        if op == "st":
            return f"st {s[0]}, [sp+{self.imm}]"
        return op

    def vdefs(self):
        return [self.dst.name] if self.dst is not None and self.dst.kind == "v" else []

    def vuses(self):
        out = []
        for x in self.srcs:
            if x.kind == "v" and x.name not in out:
                out.append(x.name)
        return out


class MBlock:
    def __init__(self, name, succs):
        self.name, self.succs = name, succs
        self.code = []


class MFunc:
    def __init__(self, name, nparams):
        self.name, self.nparams = name, nparams
        self.blocks = []
        self.frame = 0

    def show(self):
        out = [f"{self.name}:  # frame {self.frame}"]
        for b in self.blocks:
            out.append(f".{b.name}:")
            for m in b.code:
                out.append("  " + m.show())
        return out


class SelError(Exception):
    def __init__(self, line, msg):
        self.line, self.msg = line, msg


# ------------------------------------------------------------------ instruction selection


class Selector:
    def __init__(self):
        self.k = 0

    def const(self, code, v):
        r = vr(f"c.{self.k}")
        self.k += 1
        code.append(MI("li", r, imm=v))
        return r

    def reg(self, code, a):
        if a.kind == "const":
            return self.const(code, a.val)
        return vr(a.name)


def select(f):
    """Machine code over virtual registers. Unreachable blocks are dropped,
    as a back end does."""
    cfg = Cfg(f)
    blocks = [b for b in f.blocks if b.name in cfg.reach]
    m = MFunc(f.name, len(f.params))
    if len(f.params) > MAX_ARGS:
        raise SelError(f.line, f"{f.name} has {len(f.params)} parameters; "
                               f"the calling convention passes at most {MAX_ARGS}")
    sel = Selector()
    for n, b in enumerate(blocks):
        mb = MBlock(b.name, cfg.succ[b.name])
        code = mb.code
        if n == 0:
            for k, p in enumerate(f.params):
                code.append(MI("mv", vr(p), [ar(k)]))
        nxt = blocks[n + 1].name if n + 1 < len(blocks) else None
        for i in b.instrs:
            if i.op == "bin":
                x, y = i.args
                op = i.binop
                if x.kind == "const" and y.kind != "const" and op in COMMUTES:
                    x, y = y, x
                if y.kind == "const" and op in RRI:
                    code.append(MI(RRI[op], vr(i.dst), [sel.reg(code, x)], imm=y.val))
                else:
                    rx = sel.reg(code, x)
                    ry = sel.reg(code, y)
                    code.append(MI(RRR[op], vr(i.dst), [rx, ry]))
            elif i.op == "copy":
                a = i.args[0]
                if a.kind == "const":
                    code.append(MI("li", vr(i.dst), imm=a.val))
                else:
                    code.append(MI("mv", vr(i.dst), [vr(a.name)]))
            elif i.op == "call":
                if len(i.args) > MAX_ARGS:
                    raise SelError(i.line, f"call {i.func} passes {len(i.args)} arguments; "
                                           f"the calling convention passes at most {MAX_ARGS}")
                for k, a in enumerate(i.args):
                    if a.kind == "const":
                        code.append(MI("li", ar(k), imm=a.val))
                    else:
                        code.append(MI("mv", ar(k), [vr(a.name)]))
                code.append(MI("call", func=i.func, nargs=len(i.args)))
                if i.dst:
                    code.append(MI("mv", vr(i.dst), [ar(0)]))
            elif i.op == "print":
                code.append(MI("print", srcs=[sel.reg(code, i.args[0])]))
            elif i.op == "ret":
                if i.args:
                    a = i.args[0]
                    if a.kind == "const":
                        code.append(MI("li", ar(0), imm=a.val))
                    else:
                        code.append(MI("mv", ar(0), [vr(a.name)]))
                else:
                    # a bare ret returns 0, as the IR defines it
                    code.append(MI("li", ar(0), imm=0))
                code.append(MI("ret"))
            elif i.op == "jmp":
                if i.labels[0] != nxt:
                    code.append(MI("j", label=i.labels[0]))
            elif i.op == "br":
                c = sel.reg(code, i.args[0])
                t, e = i.labels
                if t == e:
                    if t != nxt:
                        code.append(MI("j", label=t))
                elif t == nxt:
                    code.append(MI("beqz", srcs=[c], label=e))
                else:
                    code.append(MI("bnez", srcs=[c], label=t))
                    if e != nxt:
                        code.append(MI("j", label=e))
        m.blocks.append(mb)
    # a name read before any assignment reaches it reads 0, as in the IR
    li, _ = mliveness(m)
    zero = [MI("li", vr(v), imm=0) for v in sorted(li[m.blocks[0].name])]
    m.blocks[0].code = zero + m.blocks[0].code
    loops = cfg.loops()
    m.depth = {b.name: sum(1 for _, _, body in loops if b.name in body) for b in m.blocks}
    return m


# ------------------------------------------------------------------ liveness


def mliveness(m):
    order = [b.name for b in m.blocks]
    blk = {b.name: b for b in m.blocks}
    ud = {}
    for b in m.blocks:
        uses, defs = [], []
        for i in b.code:
            for u in i.vuses():
                if u not in defs and u not in uses:
                    uses.append(u)
            for d in i.vdefs():
                if d not in defs:
                    defs.append(d)
        ud[b.name] = (set(uses), set(defs))
    live_in = {n: set() for n in order}
    live_out = {n: set() for n in order}
    changed = True
    while changed:
        changed = False
        for n in reversed(order):
            out = set()
            for s in blk[n].succs:
                out |= live_in[s]
            uses, defs = ud[n]
            inn = uses | (out - defs)
            if out != live_out[n] or inn != live_in[n]:
                live_out[n], live_in[n] = out, inn
                changed = True
    return live_in, live_out


def number(m):
    """Linear positions: instruction k of the layout reads at 2k and writes
    at 2k+1."""
    pos = 0
    first = {}
    for b in m.blocks:
        first[b.name] = pos
        pos += len(b.code)
    return first


def intervals(m):
    li, lo = mliveness(m)
    first = number(m)
    iv = {}

    def extend(v, p):
        if v in iv:
            a, b = iv[v]
            iv[v] = (min(a, p), max(b, p))
        else:
            iv[v] = (p, p)
    calls = []
    for b in m.blocks:
        base = first[b.name]
        live = set(lo[b.name])
        last = base + len(b.code) - 1
        for v in live:
            extend(v, 2 * last + 1)
        for k in range(len(b.code) - 1, -1, -1):
            i = b.code[k]
            p = base + k
            for d in i.vdefs():
                extend(d, 2 * p + 1)
                live.discard(d)
            if i.op == "call":
                calls.append((2 * p, sorted(live)))
            for u in i.vuses():
                live.add(u)
            for v in live:
                extend(v, 2 * p)
    return iv, calls


def interference(m):
    li, lo = mliveness(m)
    nodes = set()
    edges = {}
    for b in m.blocks:
        for i in b.code:
            for v in i.vdefs() + i.vuses():
                nodes.add(v)
    for v in nodes:
        edges[v] = set()
    for b in m.blocks:
        live = set(lo[b.name])
        for i in reversed(b.code):
            src = i.srcs[0].name if i.op == "mv" and i.srcs[0].kind == "v" else None
            for d in i.vdefs():
                for v in live:
                    if v != d and v != src:
                        edges[d].add(v)
                        edges[v].add(d)
                live.discard(d)
            for u in i.vuses():
                live.add(u)
    return edges


def spill_costs(m):
    cost = {}
    for b in m.blocks:
        w = 10 ** m.depth[b.name]
        for i in b.code:
            for v in i.vdefs() + i.vuses():
                cost[v] = cost.get(v, 0) + w
    return cost


# ------------------------------------------------------------------ the two allocators


def linear_scan(m, K):
    """Poletto and Sarkar's linear scan: intervals by start; at each one,
    expire those ended, and when all K registers are taken spill whichever
    of it and the active intervals ends last."""
    iv, _ = intervals(m)
    order = sorted(iv, key=lambda v: (iv[v][0], v))
    active = []
    free = list(range(1, K + 1))
    loc = {}
    slots = 0
    for v in order:
        s, e = iv[v]
        while active and iv[active[0]][1] < s:
            j = active.pop(0)
            free.append(loc[j])
            free.sort()
        if len(active) == K:
            spill = active[-1]
            if iv[spill][1] > e:
                loc[v] = loc[spill]
                loc[spill] = ("slot", slots)
                slots += 1
                active.pop()
                insert_active(active, v, iv)
            else:
                loc[v] = ("slot", slots)
                slots += 1
        else:
            loc[v] = free.pop(0)
            insert_active(active, v, iv)
    return loc, slots


def insert_active(active, v, iv):
    k = 0
    while k < len(active) and (iv[active[k]][1], active[k]) < (iv[v][1], v):
        k += 1
    active.insert(k, v)


def colour(m, K):
    """Chaitin's simplify with Briggs's optimistic colouring: remove a node
    of degree < K while there is one, else the cheapest per neighbour; then
    colour in reverse, spilling a node only when no colour is left."""
    edges = interference(m)
    cost = spill_costs(m)
    left = set(edges)
    deg = {v: len(edges[v]) for v in edges}
    stack = []
    while left:
        pick = None
        for v in sorted(left):
            if deg[v] < K:
                pick = v
                break
        if pick is None:
            for v in sorted(left):
                if pick is None or cost[v] * deg[pick] < cost[pick] * deg[v]:
                    pick = v
        stack.append(pick)
        left.discard(pick)
        for u in edges[pick]:
            if u in left:
                deg[u] -= 1
    loc = {}
    slots = 0
    for v in reversed(stack):
        used = {loc[u] for u in edges[v] if u in loc and not isinstance(loc[u], tuple)}
        c = None
        for r in range(1, K + 1):
            if r not in used:
                c = r
                break
        if c is None:
            loc[v] = ("slot", slots)
            slots += 1
        else:
            loc[v] = c
    return loc, slots


# ------------------------------------------------------------------ rewriting


def rewrite(m, loc, slots, K):
    """Physical registers for every operand: a spilled value is loaded into
    t0 or t1 before a use and stored after a definition; a register live
    across a call is saved before it and restored after; a move between
    one register and itself goes."""
    _, calls = intervals(m)
    across = {p: live for p, live in calls}
    first = number(m)
    stats = {"spilled": slots, "loads": 0, "stores": 0, "saves": 0, "moves": 0}
    saved = set()
    out = MFunc(m.name, m.nparams)

    def phys(v):
        return R("r", f"r{loc[v]}")
    for b in m.blocks:
        nb = MBlock(b.name, b.succs)
        for k, i in enumerate(b.code):
            p = first[b.name] + k
            pre, post = [], []
            srcs = []
            temps = {}
            for x in i.srcs:
                if x.kind != "v":
                    srcs.append(x)
                elif isinstance(loc[x.name], tuple):
                    if x.name not in temps:
                        t = R("t", f"t{len(temps)}")
                        temps[x.name] = t
                        pre.append(MI("ld", t, imm=loc[x.name][1]))
                        stats["loads"] += 1
                    srcs.append(temps[x.name])
                else:
                    srcs.append(phys(x.name))
            dst = i.dst
            if dst is not None and dst.kind == "v":
                if isinstance(loc[dst.name], tuple):
                    t = R("t", "t0")
                    post.append(MI("st", srcs=[t], imm=loc[dst.name][1]))
                    stats["stores"] += 1
                    dst = t
                else:
                    dst = phys(dst.name)
            if i.op == "call":
                regs = sorted({loc[v] for v in across[2 * p] if not isinstance(loc[v], tuple)})
                for r in regs:
                    saved.add(r)
                    pre.append(MI("st", srcs=[R("r", f"r{r}")], imm=slots + r - 1))
                    post.append(MI("ld", R("r", f"r{r}"), imm=slots + r - 1))
                    stats["saves"] += 1
            ni = MI(i.op, dst, srcs, i.imm, i.label, i.func, i.nargs)
            if ni.op == "mv" and ni.dst.key() == ni.srcs[0].key():
                stats["moves"] += 1
                ni = None
            nb.code += pre + ([ni] if ni else []) + post
        out.blocks.append(nb)
    out.frame = slots + (K if saved else 0)
    stats["size"] = sum(len(b.code) for b in out.blocks)
    return out, stats


def allocate(f, K, how):
    m = select(f)
    loc, slots = linear_scan(m, K) if how == "linear" else colour(m, K)
    return m, loc, rewrite(m, loc, slots, K)


# ------------------------------------------------------------------ the simulator


class Sim:
    def __init__(self, funcs):
        self.funcs = {f.name: f for f in funcs}
        self.regs = {}
        self.steps = 0
        self.mem = 0
        self.out = []

    def get(self, r):
        return self.regs.get(r.name, 0)

    def call(self, name, depth):
        if depth > DEPTH_LIMIT:
            raise Trap("call depth limit")
        f = self.funcs[name]
        frame = [0] * f.frame
        bi = 0
        index = {b.name: k for k, b in enumerate(f.blocks)}
        while True:
            b = f.blocks[bi]
            jumped = None
            for i in b.code:
                self.steps += 1
                if self.steps > 4 * STEP_LIMIT:
                    raise Trap("step limit")
                op = i.op
                if op == "li":
                    self.regs[i.dst.name] = i.imm
                elif op == "mv":
                    self.regs[i.dst.name] = self.get(i.srcs[0])
                elif op in BINOP_OF:
                    a = self.get(i.srcs[0])
                    c = i.imm if op in RRI.values() else self.get(i.srcs[1])
                    r = fold(BINOP_OF[op], a, c)
                    if r is None:
                        raise Trap(f"division by zero in {name}")
                    self.regs[i.dst.name] = r
                elif op == "print":
                    self.out.append(str(self.get(i.srcs[0])))
                elif op == "bnez" or op == "beqz":
                    if (self.get(i.srcs[0]) != 0) == (op == "bnez"):
                        jumped = i.label
                        break
                elif op == "j":
                    jumped = i.label
                    break
                elif op == "call":
                    self.call(i.func, depth + 1)
                elif op == "ret":
                    return self.regs.get("a0", 0)
                elif op == "ld":
                    self.mem += 1
                    self.regs[i.dst.name] = frame[i.imm]
                elif op == "st":
                    self.mem += 1
                    frame[i.imm] = self.get(i.srcs[0])
            bi = index[jumped] if jumped is not None else bi + 1


# ------------------------------------------------------------------ jobs


def fmt_loc(v):
    return f"[sp+{v[1]}]" if isinstance(v, tuple) else f"r{v}"


def fmt_stats(st):
    return (f"; spilled {st['spilled']}, loads {st['loads']}, stores {st['stores']}, "
            f"saves {st['saves']}, moves removed {st['moves']}, size {st['size']}")


def run_job(mode, rest, fname, src):
    try:
        funcs = parse(src)
    except IrError as e:
        return [f"{fname}:{e.line}: error: {e.msg}"]
    out = []
    if mode == "run":
        if not rest:
            return [f"{fname}: error: run needs a function"]
        name, K = rest[0], int(rest[1])
        args = [wrap(int(a)) for a in rest[2:]]
        g = None
        for h in funcs:
            if h.name == name:
                g = h
        if g is None:
            return [f"{fname}: error: no function {name}"]
        if len(args) != len(g.params):
            return [f"{fname}: error: {name} takes {len(g.params)} argument(s), given {len(args)}"]
        ir = IrMachine(funcs)
        try:
            r = ir.call(name, args, 0)
            res = f"returned {r}"
        except Trap as t:
            res = f"trap: {t}"
        line = f"ir: {res} after {ir.steps} steps"
        if ir.out:
            line += "; printed " + " ".join(ir.out)
        out.append(line)
        for how in ("linear", "colour"):
            try:
                mfs = [allocate(f, K, how)[2][0] for f in funcs]
            except SelError as e:
                return out + [f"{fname}:{e.line}: error: {e.msg}"]
            sim = Sim(mfs)
            for k, a in enumerate(args):
                sim.regs[f"a{k}"] = a
            try:
                r = sim.call(name, 0)
                mres = f"returned {r}"
            except Trap as t:
                mres = f"trap: {t}"
            line = f"{how}: {mres} after {sim.steps} instructions, {sim.mem} memory"
            if sim.out:
                line += "; printed " + " ".join(sim.out)
            out.append(line)
            if mres != res or sim.out != ir.out:
                out.append(f"MISMATCH: {how} differs from the IR")
        return out
    target = rest[0] if rest else funcs[0].name
    f = None
    for g in funcs:
        if g.name == target:
            f = g
    if f is None:
        return [f"{fname}: error: no function {target}"]
    try:
        m = select(f)
    except SelError as e:
        return [f"{fname}:{e.line}: error: {e.msg}"]
    if mode == "sel":
        return m.show()
    if mode == "live":
        iv, calls = intervals(m)
        for v in sorted(iv, key=lambda v: (iv[v][0], v)):
            out.append(f"%{v}: [{iv[v][0]}, {iv[v][1]}]")
        for p, live in calls:
            out.append(f"call at {p}: live across " + (", ".join("%" + v for v in live) or "-"))
        return out
    if mode == "graph":
        edges = interference(m)
        cost = spill_costs(m)
        for v in sorted(edges):
            ns = ", ".join("%" + u for u in sorted(edges[v])) or "-"
            out.append(f"%{v}: degree {len(edges[v])}, cost {cost[v]}; {ns}")
        return out
    if mode in ("linear", "colour"):
        K = int(rest[1]) if len(rest) > 1 else 4
        _, loc, (mf, st) = allocate(f, K, mode)
        out.append("; " + ", ".join(f"%{v} {fmt_loc(loc[v])}" for v in sorted(loc)))
        out += mf.show()
        out.append(fmt_stats(st))
        return out
    if mode == "compare":
        for K in (2, 3, 4, 6, 8):
            for how in ("linear", "colour"):
                _, _, (mf, st) = allocate(f, K, how)
                out.append(f"K={K} {how}: spilled {st['spilled']}, loads {st['loads']}, "
                           f"stores {st['stores']}, saves {st['saves']}, size {st['size']}")
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
