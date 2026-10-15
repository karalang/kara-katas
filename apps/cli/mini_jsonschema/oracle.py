# Python mirror of mini_jsonschema: a JSON Schema (draft 2020-12) validator
# written without the jsonschema, json or re modules, matching what
# jsonschema 4.26 reports. It carries its own JSON decoder (Python's error
# messages and positions), Python's repr of the decoded values, a
# backtracking regex matcher for the pattern subset the schemas use, and
# jsonschema's keywords, error paths and best_match.
import os, sys

out = []

# ---------------------------------------------------------------- values
NULL, BOOL, INT, FLOAT, STR, ARR, OBJ = range(7)

class J:
    def __init__(self, kind, b=False, i=0, f=0.0, s="", items=None, keys=None, vals=None):
        self.kind = kind; self.b = b; self.i = i; self.f = f; self.s = s
        self.items = items if items is not None else []
        self.keys = keys if keys is not None else []
        self.vals = vals if vals is not None else []

def get(o, k):
    for n, key in enumerate(o.keys):
        if key == k:
            return o.vals[n]
    return None

def has(o, k):
    return k in o.keys

# ---------------------------------------------------------------- JSON decoding
class Bad(Exception):
    def __init__(self, msg, pos):
        self.msg = msg; self.pos = pos

WS = " \t\n\r"

def skip_ws(s, i):
    while i < len(s) and s[i] in WS:
        i += 1
    return i

ESC = {'"': '"', '\\': '\\', '/': '/', 'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t'}

def hex4(s, i):
    t = s[i:i + 4]
    if len(t) != 4 or any(c not in "0123456789abcdefABCDEF" for c in t):
        raise Bad("Invalid \\uXXXX escape", i - 1)
    return int(t, 16)

def scan_string(s, end):
    begin = end - 1
    o = []
    while True:
        if end >= len(s):
            raise Bad("Unterminated string starting at", begin)
        c = s[end]
        if c == '"':
            return "".join(o), end + 1
        if c == '\\':
            if end + 1 >= len(s):
                raise Bad("Unterminated string starting at", begin)
            e = s[end + 1]
            if e != 'u':
                if e not in ESC:
                    raise Bad("Invalid \\escape", end)
                o.append(ESC[e]); end += 2
                continue
            u = hex4(s, end + 2)
            end += 6
            if 0xd800 <= u <= 0xdbff and s[end:end + 2] == "\\u":
                u2 = hex4(s, end + 2)
                if 0xdc00 <= u2 <= 0xdfff:
                    u = 0x10000 + (((u - 0xd800) << 10) | (u2 - 0xdc00))
                    end += 6
            o.append(chr(u))
            continue
        if ord(c) < 0x20:
            raise Bad("Invalid control character at", end)
        o.append(c); end += 1

def scan_number(s, i):
    j = i
    if j < len(s) and s[j] == '-':
        j += 1
    if j >= len(s) or not s[j].isdigit() or not s[j].isascii():
        return None
    if s[j] == '0':
        j += 1
    else:
        while j < len(s) and s[j] in "0123456789":
            j += 1
    is_float = False
    if j + 1 < len(s) and s[j] == '.' and s[j + 1] in "0123456789":
        j += 2
        while j < len(s) and s[j] in "0123456789":
            j += 1
        is_float = True
    if j < len(s) and s[j] in "eE":
        k = j + 1
        if k < len(s) and s[k] in "+-":
            k += 1
        if k < len(s) and s[k] in "0123456789":
            while k < len(s) and s[k] in "0123456789":
                k += 1
            j = k
            is_float = True
    text = s[i:j]
    if is_float:
        return J(FLOAT, f=float(text)), j
    return J(INT, i=int(text)), j

def scan_value(s, i):
    if i >= len(s):
        raise Bad("Expecting value", i)
    c = s[i]
    if c == '"':
        t, e = scan_string(s, i + 1)
        return J(STR, s=t), e
    if c == '{':
        return scan_object(s, i + 1)
    if c == '[':
        return scan_array(s, i + 1)
    if s.startswith("null", i):
        return J(NULL), i + 4
    if s.startswith("true", i):
        return J(BOOL, b=True), i + 4
    if s.startswith("false", i):
        return J(BOOL, b=False), i + 5
    r = scan_number(s, i)
    if r is not None:
        return r
    if s.startswith("NaN", i):
        return J(FLOAT, f=float("nan")), i + 3
    if s.startswith("Infinity", i):
        return J(FLOAT, f=float("inf")), i + 8
    if s.startswith("-Infinity", i):
        return J(FLOAT, f=float("-inf")), i + 9
    raise Bad("Expecting value", i)

def put(o, k, v):
    for n, key in enumerate(o.keys):
        if key == k:
            o.vals[n] = v
            return
    o.keys.append(k); o.vals.append(v)

def scan_object(s, end):
    o = J(OBJ)
    nc = s[end:end + 1]
    if nc != '"':
        if nc != "" and nc in WS:
            end = skip_ws(s, end); nc = s[end:end + 1]
        if nc == '}':
            return o, end + 1
        if nc != '"':
            raise Bad("Expecting property name enclosed in double quotes", end)
    end += 1
    while True:
        key, end = scan_string(s, end)
        if s[end:end + 1] != ':':
            end = skip_ws(s, end)
            if s[end:end + 1] != ':':
                raise Bad("Expecting ':' delimiter", end)
        end += 1
        end = skip_ws(s, end)
        v, end = scan_value(s, end)
        put(o, key, v)
        end = skip_ws(s, end)
        nc = s[end:end + 1]
        end += 1
        if nc == '}':
            return o, end
        if nc != ',':
            raise Bad("Expecting ',' delimiter", end - 1)
        comma = end - 1
        end = skip_ws(s, end)
        nc = s[end:end + 1]
        end += 1
        if nc != '"':
            if nc == '}':
                raise Bad("Illegal trailing comma before end of object", comma)
            raise Bad("Expecting property name enclosed in double quotes", end - 1)

def scan_array(s, end):
    a = J(ARR)
    end = skip_ws(s, end)
    if s[end:end + 1] == ']':
        return a, end + 1
    while True:
        v, end = scan_value(s, end)
        a.items.append(v)
        end = skip_ws(s, end)
        nc = s[end:end + 1]
        end += 1
        if nc == ']':
            return a, end
        if nc != ',':
            raise Bad("Expecting ',' delimiter", end - 1)
        comma = end - 1
        end = skip_ws(s, end)
        if s[end:end + 1] == ']':
            raise Bad("Illegal trailing comma before end of array", comma)

def decode(s):
    i = skip_ws(s, 0)
    v, end = scan_value(s, i)
    end = skip_ws(s, end)
    if end != len(s):
        raise Bad("Extra data", end)
    return v

def where(s, pos):
    line = s.count("\n", 0, pos) + 1
    col = pos - s.rfind("\n", 0, pos)
    return f"line {line} column {col} (char {pos})"

# ---------------------------------------------------------------- Python's repr
def repr_str(s):
    q = '"' if ("'" in s and '"' not in s) else "'"
    o = [q]
    for c in s:
        if c == q or c == '\\':
            o.append('\\' + c)
        elif c == '\t':
            o.append('\\t')
        elif c == '\n':
            o.append('\\n')
        elif c == '\r':
            o.append('\\r')
        elif ord(c) < 0x20 or ord(c) == 0x7f:
            o.append('\\x%02x' % ord(c))
        else:
            o.append(c)
    o.append(q)
    return "".join(o)

def repr_float(f):
    return repr(f)

def py_repr(v):
    k = v.kind
    if k == NULL:
        return "None"
    if k == BOOL:
        return "True" if v.b else "False"
    if k == INT:
        return str(v.i)
    if k == FLOAT:
        return repr_float(v.f)
    if k == STR:
        return repr_str(v.s)
    if k == ARR:
        return "[" + ", ".join(py_repr(x) for x in v.items) + "]"
    return "{" + ", ".join(repr_str(key) + ": " + py_repr(val) for key, val in zip(v.keys, v.vals)) + "}"

# ---------------------------------------------------------------- regex
# A backtracking matcher compiled to a small instruction list: CHAR, ANY,
# SET (ranges, negation), SPLIT (prefer the first target), JMP, BOL, EOL,
# MATCH. Counted repeats are expanded. Python's `$` also matches before a
# final newline.
class Rx:
    def __init__(self, src):
        self.src = src; self.p = 0; self.prog = []
        self.alt()
        self.prog.append(("MATCH",))

    def peek(self):
        return self.src[self.p] if self.p < len(self.src) else ""

    def emit(self, ins):
        self.prog.append(ins)
        return len(self.prog) - 1

    def alt(self):
        start = len(self.prog)
        self.seq()
        if self.peek() != "|":
            return
        jumps = []
        while self.peek() == "|":
            self.p += 1
            body = self.prog[start:]
            del self.prog[start:]
            # SPLIT start+1, after-branch ; branch ; JMP end
            self.prog.append(("SPLIT", start + 1, start + 2 + len(body)))
            self.prog.extend(shift(body, 1))
            jumps.append(len(self.prog))
            self.prog.append(("JMP", -1))
            start = len(self.prog)
            self.seq()
        end = len(self.prog)
        for j in jumps:
            self.prog[j] = ("JMP", end)

    def seq(self):
        while self.p < len(self.src) and self.peek() not in "|)":
            self.repeat()

    def atom(self):
        c = self.src[self.p]; self.p += 1
        if c == "(":
            if self.src.startswith("?:", self.p):
                self.p += 2
            self.alt()
            self.p += 1
        elif c == "^":
            self.emit(("BOL",))
        elif c == "$":
            self.emit(("EOL",))
        elif c == ".":
            self.emit(("ANY",))
        elif c == "[":
            self.emit(("SET",) + self.cls())
        elif c == "\\":
            e = self.src[self.p]; self.p += 1
            if e in "dDwWsS":
                self.emit(("SET",) + class_esc(e))
            else:
                self.emit(("CHAR", e))
        else:
            self.emit(("CHAR", c))

    def cls(self):
        neg = False
        if self.peek() == "^":
            neg = True; self.p += 1
        ranges = []
        first = True
        while first or self.peek() != "]":
            first = False
            c = self.src[self.p]; self.p += 1
            if c == "\\":
                e = self.src[self.p]; self.p += 1
                if e in "dws":
                    ranges.extend(class_esc(e)[1])
                    continue
                c = e
            if self.peek() == "-" and self.p + 1 < len(self.src) and self.src[self.p + 1] != "]":
                self.p += 1
                hi = self.src[self.p]; self.p += 1
                if hi == "\\":
                    hi = self.src[self.p]; self.p += 1
                ranges.append((ord(c), ord(hi)))
            else:
                ranges.append((ord(c), ord(c)))
        self.p += 1
        return (neg, ranges)

    def repeat(self):
        start = len(self.prog)
        self.atom()
        c = self.peek()
        if c not in ("*", "+", "?", "{"):
            return
        lo, hi = 0, -1
        if c == "{":
            q = self.src.index("}", self.p)
            body = self.src[self.p + 1:q]
            self.p = q + 1
            if "," in body:
                a, b = body.split(",")
                lo = int(a); hi = int(b) if b else -1
            else:
                lo = hi = int(body)
        else:
            self.p += 1
            lo, hi = {"*": (0, -1), "+": (1, -1), "?": (0, 1)}[c]
        lazy = False
        if self.peek() == "?":
            lazy = True; self.p += 1
        body = self.prog[start:]
        del self.prog[start:]
        for _ in range(lo):
            self.prog.extend(shift(body, len(self.prog) - start))
        if hi == -1:
            # L: SPLIT body, out ; body ; JMP L
            l = len(self.prog)
            self.prog.append(("SPLIT", l + 1, l + 2 + len(body)) if not lazy else ("SPLIT", l + 2 + len(body), l + 1))
            self.prog.extend(shift(body, l + 1 - start))
            self.prog.append(("JMP", l))
        else:
            ends = []
            for _ in range(hi - lo):
                l = len(self.prog)
                ends.append(l)
                self.prog.append(None)
                self.prog.extend(shift(body, l + 1 - start))
            end = len(self.prog)
            for l in ends:
                self.prog[l] = ("SPLIT", l + 1, end) if not lazy else ("SPLIT", end, l + 1)

def shift(body, d):
    o = []
    for ins in body:
        if ins[0] == "SPLIT":
            o.append(("SPLIT", ins[1] + d, ins[2] + d))
        elif ins[0] == "JMP":
            o.append(("JMP", ins[1] + d))
        else:
            o.append(ins)
    return o

DIGIT = [(48, 57)]
WORD = [(48, 57), (65, 90), (95, 95), (97, 122)]
SPACE = [(9, 13), (32, 32)]

def class_esc(e):
    r = {"d": DIGIT, "w": WORD, "s": SPACE}[e.lower()]
    return (e.isupper(), list(r))

def in_set(ins, c):
    hit = any(lo <= c <= hi for lo, hi in ins[2])
    return hit != ins[1]

def run_at(prog, s, start):
    stack = [(0, start)]
    while stack:
        pc, sp = stack.pop()
        while True:
            ins = prog[pc]
            op = ins[0]
            if op == "MATCH":
                return True
            if op == "CHAR":
                if sp < len(s) and s[sp] == ord(ins[1]):
                    pc += 1; sp += 1
                    continue
                break
            if op == "ANY":
                if sp < len(s) and s[sp] != 10:
                    pc += 1; sp += 1
                    continue
                break
            if op == "SET":
                if sp < len(s) and in_set(ins, s[sp]):
                    pc += 1; sp += 1
                    continue
                break
            if op == "BOL":
                if sp == 0:
                    pc += 1
                    continue
                break
            if op == "EOL":
                if sp == len(s) or (sp == len(s) - 1 and s[sp] == 10):
                    pc += 1
                    continue
                break
            if op == "JMP":
                pc = ins[1]
                continue
            if op == "SPLIT":
                stack.append((ins[2], sp))
                pc = ins[1]
                continue
    return False

RX = {}

def search(pattern, text):
    if pattern not in RX:
        RX[pattern] = Rx(pattern).prog
    prog = RX[pattern]
    s = [ord(c) for c in text]
    for i in range(len(s) + 1):
        if run_at(prog, s, i):
            return True
    return False

# ---------------------------------------------------------------- the validator
WEAK = ("anyOf", "oneOf")

class Err:
    def __init__(self, message, validator=None, set_validator=False):
        self.message = message
        self.path = []
        self.schema_path = []
        self.validator = validator
        self.validator_set = set_validator
        self.instance = None
        self.schema = None
        self.schema_set = False
        self.context = []

def is_type(v, t):
    k = v.kind
    if t == "null":
        return k == NULL
    if t == "boolean":
        return k == BOOL
    if t == "integer":
        if k == FLOAT:
            return v.f == v.f and abs(v.f) != float("inf") and v.f == int(v.f)
        return k == INT
    if t == "number":
        return k == INT or k == FLOAT
    if t == "string":
        return k == STR
    if t == "array":
        return k == ARR
    if t == "object":
        return k == OBJ
    return False

def num(v):
    return float(v.i) if v.kind == INT else v.f

def num_lt(a, b):
    if a.kind == INT and b.kind == INT:
        return a.i < b.i
    return num(a) < num(b)

def equal(a, b):
    if a.kind == STR or b.kind == STR:
        return a.kind == b.kind and a.s == b.s
    if a.kind == ARR and b.kind == ARR:
        return len(a.items) == len(b.items) and all(equal(x, y) for x, y in zip(a.items, b.items))
    if a.kind == OBJ and b.kind == OBJ:
        if len(a.keys) != len(b.keys):
            return False
        for k, v in zip(a.keys, a.vals):
            w = get(b, k)
            if w is None or not equal(v, w):
                return False
        return True
    if a.kind == BOOL or b.kind == BOOL:
        return a.kind == b.kind and a.b == b.b
    if a.kind == NULL or b.kind == NULL:
        return a.kind == b.kind
    if a.kind in (INT, FLOAT) and b.kind in (INT, FLOAT):
        if a.kind == INT and b.kind == INT:
            return a.i == b.i
        return num(a) == num(b)
    return False

def length(s):
    return len(s)

class V:
    def __init__(self, root):
        self.root = root

    def resolve(self, ref):
        if not ref.startswith("#"):
            raise Exception("only local $ref is supported")
        node = self.root
        part = ref[1:]
        if part == "":
            return node
        for seg in part[1:].split("/"):
            seg = seg.replace("~1", "/").replace("~0", "~")
            if node.kind == OBJ:
                node = get(node, seg)
            else:
                node = node.items[int(seg)]
        return node

    def errors(self, inst, schema):
        # jsonschema's iter_errors and descend: run each keyword in the
        # schema's order and stamp the keyword onto its errors.
        if schema.kind == BOOL:
            if schema.b:
                return []
            e = Err(f"False schema does not allow {py_repr(inst)}", None, True)
            e.instance = inst; e.schema = schema; e.schema_set = True
            return [e]
        res = []
        for k, v in zip(schema.keys, schema.vals):
            errs = self.keyword(k, v, inst, schema)
            if errs is None:
                continue
            for e in errs:
                if not e.validator_set:
                    e.validator = k; e.validator_set = True
                if e.instance is None:
                    e.instance = inst
                if not e.schema_set:
                    e.schema = schema; e.schema_set = True
                if k not in ("if", "$ref"):
                    e.schema_path.insert(0, k)
                res.append(e)
        return res

    def descend(self, inst, schema, path=None, schema_path=None):
        errs = self.errors(inst, schema)
        if schema.kind == BOOL:
            return errs
        for e in errs:
            if path is not None:
                e.path.insert(0, path)
            if schema_path is not None:
                e.schema_path.insert(0, schema_path)
        return errs

    def valid(self, inst, schema):
        return len(self.errors(inst, schema)) == 0

    def keyword(self, k, v, inst, schema):
        R = py_repr
        if k == "$ref":
            return self.descend(inst, self.resolve(v.s))
        if k == "type":
            types = [v.s] if v.kind == STR else [t.s for t in v.items]
            if not any(is_type(inst, t) for t in types):
                return [Err(f"{R(inst)} is not of type " + ", ".join(repr_str(t) for t in types))]
            return []
        if k == "enum":
            if not any(equal(e, inst) for e in v.items):
                return [Err(f"{R(inst)} is not one of {R(v)}")]
            return []
        if k == "const":
            if not equal(inst, v):
                return [Err(f"{R(v)} was expected")]
            return []
        if k in ("minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum"):
            if not is_type(inst, "number"):
                return []
            if k == "minimum" and num_lt(inst, v):
                return [Err(f"{R(inst)} is less than the minimum of {R(v)}")]
            if k == "maximum" and num_lt(v, inst):
                return [Err(f"{R(inst)} is greater than the maximum of {R(v)}")]
            if k == "exclusiveMinimum" and not num_lt(v, inst):
                return [Err(f"{R(inst)} is less than or equal to the minimum of {R(v)}")]
            if k == "exclusiveMaximum" and not num_lt(inst, v):
                return [Err(f"{R(inst)} is greater than or equal to the maximum of {R(v)}")]
            return []
        if k == "multipleOf":
            if not is_type(inst, "number"):
                return []
            if v.kind == FLOAT:
                q = num(inst) / v.f
                failed = int(q) != q
            elif inst.kind == INT:
                failed = inst.i % v.i != 0
            else:
                failed = inst.f % v.i != 0
            if failed:
                return [Err(f"{R(inst)} is not a multiple of {R(v)}")]
            return []
        if k in ("minLength", "maxLength"):
            if inst.kind != STR:
                return []
            n = length(inst.s)
            if k == "minLength" and n < v.i:
                return [Err(f"{R(inst)} " + ("should be non-empty" if v.i == 1 else "is too short"))]
            if k == "maxLength" and n > v.i:
                return [Err(f"{R(inst)} " + ("is expected to be empty" if v.i == 0 else "is too long"))]
            return []
        if k == "pattern":
            if inst.kind == STR and not search(v.s, inst.s):
                return [Err(f"{R(inst)} does not match {repr_str(v.s)}")]
            return []
        if k in ("minItems", "maxItems"):
            if inst.kind != ARR:
                return []
            n = len(inst.items)
            if k == "minItems" and n < v.i:
                return [Err(f"{R(inst)} " + ("should be non-empty" if v.i == 1 else "is too short"))]
            if k == "maxItems" and n > v.i:
                return [Err(f"{R(inst)} " + ("is expected to be empty" if v.i == 0 else "is too long"))]
            return []
        if k == "uniqueItems":
            if v.kind == BOOL and v.b and inst.kind == ARR:
                xs = inst.items
                for a in range(len(xs)):
                    for b in range(a + 1, len(xs)):
                        if equal(xs[a], xs[b]):
                            return [Err(f"{R(inst)} has non-unique elements")]
            return []
        if k in ("minProperties", "maxProperties"):
            if inst.kind != OBJ:
                return []
            n = len(inst.keys)
            if k == "minProperties" and n < v.i:
                return [Err(f"{R(inst)} " + ("should be non-empty" if v.i == 1 else "does not have enough properties"))]
            if k == "maxProperties" and n > v.i:
                return [Err(f"{R(inst)} " + ("is expected to be empty" if v.i == 0 else "has too many properties"))]
            return []
        if k == "required":
            if inst.kind != OBJ:
                return []
            return [Err(f"{repr_str(p.s)} is a required property") for p in v.items if not has(inst, p.s)]
        if k == "properties":
            if inst.kind != OBJ:
                return []
            res = []
            for p, sub in zip(v.keys, v.vals):
                w = get(inst, p)
                if w is not None:
                    res.extend(self.descend(w, sub, p, p))
            return res
        if k == "patternProperties":
            if inst.kind != OBJ:
                return []
            res = []
            for p, sub in zip(v.keys, v.vals):
                for key, w in zip(inst.keys, inst.vals):
                    if search(p, key):
                        res.extend(self.descend(w, sub, key, p))
            return res
        if k == "additionalProperties":
            if inst.kind != OBJ:
                return []
            props = get(schema, "properties")
            pats = get(schema, "patternProperties")
            joined = "|".join(pats.keys) if pats is not None else ""
            extras = []
            for key in inst.keys:
                if props is not None and has(props, key):
                    continue
                if joined != "" and search(joined, key):
                    continue
                extras.append(key)
            if v.kind == OBJ:
                res = []
                for key in extras:
                    res.extend(self.descend(get(inst, key), v, key))
                return res
            if v.kind == BOOL and not v.b and extras:
                extras = sorted(extras)
                if pats is not None:
                    verb = "does" if len(extras) == 1 else "do"
                    joined_x = ", ".join(repr_str(x) for x in extras)
                    pl = ", ".join(repr_str(x) for x in sorted(pats.keys))
                    return [Err(f"{joined_x} {verb} not match any of the regexes: {pl}")]
                verb = "was" if len(extras) == 1 else "were"
                return [Err("Additional properties are not allowed (" + ", ".join(repr_str(x) for x in extras) + f" {verb} unexpected)")]
            return []
        if k == "propertyNames":
            if inst.kind != OBJ:
                return []
            res = []
            for key in inst.keys:
                res.extend(self.descend(J(STR, s=key), v))
            return res
        if k == "items":
            if inst.kind != ARR:
                return []
            pre = get(schema, "prefixItems")
            prefix = len(pre.items) if pre is not None else 0
            total = len(inst.items)
            extra = total - prefix
            if extra <= 0:
                return []
            if v.kind == BOOL and not v.b:
                rest = J(ARR, items=inst.items[prefix:]) if extra != 1 else inst.items[prefix]
                item = "items" if prefix != 1 else "item"
                return [Err(f"Expected at most {prefix} {item} but found {extra} extra: {R(rest)}")]
            res = []
            for n in range(prefix, total):
                res.extend(self.descend(inst.items[n], v, n))
            return res
        if k == "prefixItems":
            if inst.kind != ARR:
                return []
            res = []
            for n in range(min(len(inst.items), len(v.items))):
                res.extend(self.descend(inst.items[n], v.items[n], n, n))
            return res
        if k == "contains":
            if inst.kind != ARR:
                return []
            mn = get(schema, "minContains")
            mx = get(schema, "maxContains")
            min_c = mn.i if mn is not None else 1
            max_c = mx.i if mx is not None else len(inst.items)
            matches = 0
            for w in inst.items:
                if self.valid(w, v):
                    matches += 1
                    if matches > max_c:
                        return [Err(f"Too many items match the given schema (expected at most {max_c})", "maxContains", True)]
            if matches < min_c:
                if matches == 0:
                    return [Err(f"{R(inst)} does not contain items matching the given schema")]
                return [Err(f"Too few items match the given schema (expected at least {min_c} but only {matches} matched)", "minContains", True)]
            return []
        if k == "dependentRequired":
            if inst.kind != OBJ:
                return []
            res = []
            for p, deps in zip(v.keys, v.vals):
                if not has(inst, p):
                    continue
                for d in deps.items:
                    if not has(inst, d.s):
                        res.append(Err(f"{repr_str(d.s)} is a dependency of {repr_str(p)}"))
            return res
        if k == "dependentSchemas":
            if inst.kind != OBJ:
                return []
            res = []
            for p, sub in zip(v.keys, v.vals):
                if has(inst, p):
                    res.extend(self.descend(inst, sub, None, p))
            return res
        if k == "allOf":
            res = []
            for n, sub in enumerate(v.items):
                res.extend(self.descend(inst, sub, None, n))
            return res
        if k == "anyOf":
            all_errs = []
            for n, sub in enumerate(v.items):
                errs = self.descend(inst, sub, None, n)
                if not errs:
                    return []
                all_errs.extend(errs)
            e = Err(f"{R(inst)} is not valid under any of the given schemas")
            e.context = all_errs
            return [e]
        if k == "oneOf":
            all_errs = []
            first = -1
            for n, sub in enumerate(v.items):
                errs = self.descend(inst, sub, None, n)
                if not errs:
                    first = n
                    break
                all_errs.extend(errs)
            res = []
            if first < 0:
                e = Err(f"{R(inst)} is not valid under any of the given schemas")
                e.context = all_errs
                res.append(e)
                return res
            more = [sub for sub in v.items[first + 1:] if self.valid(inst, sub)]
            if more:
                more.append(v.items[first])
                res.append(Err(f"{R(inst)} is valid under each of " + ", ".join(R(x) for x in more)))
            return res
        if k == "not":
            if self.valid(inst, v):
                return [Err(f"{R(inst)} should not be valid under {R(v)}")]
            return []
        if k == "if":
            if self.valid(inst, v):
                t = get(schema, "then")
                if t is not None:
                    return self.descend(inst, t, None, "then")
            else:
                e = get(schema, "else")
                if e is not None:
                    return self.descend(inst, e, None, "else")
            return []
        return None

# ---------------------------------------------------------------- reporting
def path_text(path):
    o = "$"
    for p in path:
        if isinstance(p, int):
            o += f"[{p}]"
        elif simple_key(p):
            o += "." + p
        else:
            o += "['" + p.replace("\\", "\\\\").replace("'", "\\'") + "']"
    return o

def simple_key(p):
    if p == "" or not ("a" <= p[0] <= "z" or "A" <= p[0] <= "Z"):
        return False
    return all("a" <= c <= "z" or "A" <= c <= "Z" or "0" <= c <= "9" or c == "_" for c in p)

def spath(e):
    return "/".join(str(p) for p in e.schema_path)

def matches_type(e):
    if e.schema is None or e.schema.kind != OBJ:
        return False
    t = get(e.schema, "type")
    if t is None:
        return False
    if t.kind == STR:
        return is_type(e.instance, t.s)
    return any(is_type(e.instance, x.s) for x in t.items)

def cmp_path(a, b):
    # Python's comparison of two error paths (deques)
    for x, y in zip(a, b):
        if x != y:
            return -1 if x < y else 1
    return (len(a) > len(b)) - (len(a) < len(b))

def cmp_rel(a, b):
    # compares jsonschema's relevance keys; > 0 when a is more relevant
    if len(a.path) != len(b.path):
        return len(b.path) - len(a.path)
    c = cmp_path(a.path, b.path)
    if c != 0:
        return c
    wa = a.validator not in WEAK
    wb = b.validator not in WEAK
    if wa != wb:
        return 1 if wa else -1
    ma = not matches_type(a)
    mb = not matches_type(b)
    if ma != mb:
        return 1 if ma else -1
    return 0

def best_match(errs):
    best = errs[0]
    for e in errs[1:]:
        if cmp_rel(e, best) > 0:
            best = e
    abs_path = list(best.path)
    while best.context:
        ctx = best.context
        s0 = ctx[0]
        for e in ctx[1:]:
            if cmp_rel(e, s0) < 0:
                s0 = e
        s1 = None
        for e in ctx:
            if e is s0:
                continue
            if s1 is None or cmp_rel(e, s1) < 0:
                s1 = e
        if s1 is not None and cmp_rel(s0, s1) == 0:
            return best, abs_path
        best = s0
        abs_path = abs_path + list(best.path)
    return best, abs_path

def show(e, base, indent):
    ap = base + list(e.path)
    lead = " " * indent + ("- " if indent > 2 else "")
    out.append(f"{lead}{path_text(ap)}: {e.message} ({spath(e)})\n")
    ctx = sorted(e.context, key=lambda c: (path_text(ap + list(c.path)), spath(c), c.message))
    for c in ctx:
        show(c, ap, indent + 2)

def load(base, rel):
    p = os.path.join(base, rel)
    if not os.path.isfile(p):
        return None, f"{rel}: No such file or directory"
    text = open(p, "rb").read().decode("utf-8")
    try:
        return decode(text), None
    except Bad as b:
        return None, f"{rel}: {b.msg}: {where(text, b.pos)}"

def validate(base, args):
    best = False
    if args and args[0] == "--best":
        best = True
        args = args[1:]
    if len(args) < 2:
        out.append("usage: validate [--best] SCHEMA DOC...\n")
        return 2
    schema, err = load(base, args[0])
    if err:
        out.append(err + "\n")
        return 2
    v = V(schema)
    rc = 0
    for rel in args[1:]:
        inst, err = load(base, rel)
        if err:
            out.append(err + "\n")
            rc = 2
            continue
        errs = v.errors(inst, schema)
        if not errs:
            out.append(f"{rel}: valid\n")
            continue
        rc = max(rc, 1)
        if best:
            e, ap = best_match(errs)
            out.append(f"{rel}: {path_text(ap)}: {e.message}\n")
            continue
        n = len(errs)
        out.append(f"{rel}: {n} error{'s' if n != 1 else ''}\n")
        for e in sorted(errs, key=lambda e: (path_text(e.path), spath(e), e.message)):
            show(e, [], 2)
    return rc

def main():
    base = os.path.abspath("data")
    for line in open("data/jobs.txt").read().splitlines():
        if not line or line.startswith("#"):
            continue
        out.append(f"$ {line}\n")
        parts = line.split(" ")
        rc = validate(base, parts[1:])
        if rc:
            out.append(f"[exit status {rc}]\n")
        out.append("\n")
    sys.stdout.write("".join(out))

main()
