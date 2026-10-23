#!/usr/bin/env python3
"""Replays data/jobs.tsv against the vendored Apache Thrift 0.21.0 Python
library (its pure Python protocols; the C accelerator is not built) and
prints what each job produces.

data/app.thrift is compiled here the way `thrift --gen py:dynamic` would
compile it: each struct, exception, method argument list and method result
becomes a TBase subclass with a thrift_spec, and each service gets the
generated client and processor logic. The jobs then run against those.

Run: python3 -I -B oracle.py > expected.out"""
import ast
import copy
import io
import logging
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "vendor"))

from thrift.Thrift import TType, TMessageType, TApplicationException  # noqa: E402
from thrift.protocol.TBase import TBase, TExceptionBase  # noqa: E402
from thrift.protocol import TBinaryProtocol, TCompactProtocol, TJSONProtocol  # noqa: E402
from thrift.protocol.TMultiplexedProtocol import TMultiplexedProtocol  # noqa: E402
from thrift.transport import TTransport  # noqa: E402
from thrift.TMultiplexedProcessor import TMultiplexedProcessor  # noqa: E402
from thrift.TRecursive import fix_spec  # noqa: E402

LOG = []


class Capture(logging.Handler):
    def emit(self, record):
        LOG.append(record.getMessage())


logging.getLogger().addHandler(Capture())
logging.getLogger().setLevel(logging.INFO)


def out(*parts):
    print("  " + " ".join(str(p) for p in parts))


def err(e):
    cls = type(e)
    name = cls.__qualname__
    if cls.__module__ != "builtins":
        name = cls.__module__ + "." + name
    return "error %s: %s" % (name, e)


# ------------------------------------------------------------ IDL

class Tok:
    def __init__(self, text):
        self.toks = []
        i = 0
        n = len(text)
        while i < n:
            c = text[i]
            if c in " \t\r\n":
                i += 1
            elif text.startswith("//", i) or c == "#":
                while i < n and text[i] != "\n":
                    i += 1
            elif text.startswith("/*", i):
                j = text.index("*/", i + 2)
                i = j + 2
            elif c in "\"'":
                j = i + 1
                buf = []
                while text[j] != c:
                    if text[j] == "\\":
                        j += 1
                        buf.append({"n": "\n", "t": "\t", "\\": "\\", '"': '"', "'": "'"}[text[j]])
                    else:
                        buf.append(text[j])
                    j += 1
                self.toks.append(("str", "".join(buf)))
                i = j + 1
            elif c.isdigit() or (c in "+-" and i + 1 < n and text[i + 1].isdigit()):
                j = i + 1
                while j < n and (text[j].isalnum() or text[j] in ".+-") and not (
                        text[j] in "+-" and text[j - 1] not in "eE"):
                    j += 1
                word = text[i:j]
                if any(ch in word for ch in ".eE") and not word.lower().startswith(("0x", "-0x", "+0x")):
                    self.toks.append(("num", float(word)))
                else:
                    self.toks.append(("num", int(word, 0)))
                i = j
            elif c.isalpha() or c == "_":
                j = i
                while j < n and (text[j].isalnum() or text[j] in "_."):
                    j += 1
                self.toks.append(("id", text[i:j]))
                i = j
            else:
                self.toks.append(("p", c))
                i += 1
        self.pos = 0

    def peek(self):
        return self.toks[self.pos] if self.pos < len(self.toks) else ("eof", None)

    def next(self):
        t = self.peek()
        self.pos += 1
        return t

    def take(self, v):
        if self.peek()[1] == v:
            self.pos += 1
            return True
        return False

    def expect(self, v):
        t = self.next()
        if t[1] != v:
            raise SyntaxError("expected %r, got %r" % (v, t))


BASE = {"bool": TType.BOOL, "byte": TType.BYTE, "i8": TType.BYTE, "i16": TType.I16,
        "i32": TType.I32, "i64": TType.I64, "double": TType.DOUBLE,
        "string": TType.STRING, "binary": TType.STRING}


class Module:
    def __init__(self):
        self.typedefs = {}
        self.enums = {}
        self.consts = {}
        self.structs = {}      # name -> class
        self.decls = []        # (name, kind, fields)
        self.services = {}     # name -> (base, [methods])
        self.order = []


def parse_type(t):
    kind, v = t.next()
    if v in ("list", "set"):
        t.expect("<")
        e = parse_type(t)
        t.expect(">")
        return (v, e)
    if v == "map":
        t.expect("<")
        k = parse_type(t)
        t.expect(",")
        val = parse_type(t)
        t.expect(">")
        return ("map", k, val)
    return ("name", v)


def parse_value(t):
    kind, v = t.next()
    if kind in ("num", "str"):
        return ("lit", v)
    if v == "[":
        items = []
        while not t.take("]"):
            items.append(parse_value(t))
            t.take(",")
        return ("list", items)
    if v == "{":
        items = []
        while not t.take("}"):
            k = parse_value(t)
            t.expect(":")
            items.append((k, parse_value(t)))
            t.take(",")
        return ("map", items)
    if v == "true":
        return ("lit", True)
    if v == "false":
        return ("lit", False)
    return ("ref", v)


def parse_fields(t, close):
    fields = []
    while not t.take(close):
        fid = None
        if t.peek()[0] == "num":
            fid = t.next()[1]
            t.expect(":")
        req = "default"
        if t.peek()[1] in ("required", "optional"):
            req = t.next()[1]
        typ = parse_type(t)
        name = t.next()[1]
        default = None
        if t.take("="):
            default = parse_value(t)
        t.take(",") or t.take(";")
        fields.append((fid, name, typ, default, req))
    return fields


def parse_idl(text):
    t = Tok(text)
    m = Module()
    while t.peek()[0] != "eof":
        kw = t.next()[1]
        if kw == "namespace":
            t.next()
            t.next()
        elif kw == "typedef":
            typ = parse_type(t)
            m.typedefs[t.next()[1]] = typ
        elif kw == "const":
            typ = parse_type(t)
            name = t.next()[1]
            t.expect("=")
            m.consts[name] = (typ, parse_value(t))
            t.take(",") or t.take(";")
        elif kw == "enum":
            name = t.next()[1]
            t.expect("{")
            vals = []
            nxt = 0
            while not t.take("}"):
                ident = t.next()[1]
                if t.take("="):
                    nxt = t.next()[1]
                vals.append((ident, nxt))
                nxt += 1
                t.take(",") or t.take(";")
            m.enums[name] = vals
        elif kw in ("struct", "exception"):
            name = t.next()[1]
            t.expect("{")
            m.decls.append((name, kw, parse_fields(t, "}")))
        elif kw == "service":
            name = t.next()[1]
            base = None
            if t.take("extends"):
                base = t.next()[1]
            t.expect("{")
            methods = []
            while not t.take("}"):
                oneway = t.take("oneway")
                if t.peek()[1] == "void":
                    t.next()
                    ret = None
                else:
                    ret = parse_type(t)
                mname = t.next()[1]
                t.expect("(")
                args = parse_fields(t, ")")
                throws = []
                if t.take("throws"):
                    t.expect("(")
                    throws = parse_fields(t, ")")
                t.take(",") or t.take(";")
                methods.append((mname, oneway, ret, args, throws))
            m.services[name] = (base, methods)
        else:
            raise SyntaxError("unexpected %r" % kw)
    return m


class Enum:
    pass


def build(m):
    """What `thrift --gen py:dynamic` emits for the module."""
    enums = {}
    for name, vals in m.enums.items():
        e = type(name, (Enum,), {k: v for k, v in vals})
        e._VALUES_TO_NAMES = {v: k for k, v in vals}
        e._NAMES_TO_VALUES = {k: v for k, v in vals}
        enums[name] = e
    m.enum_classes = enums

    def resolve(typ):
        while typ[0] == "name" and typ[1] in m.typedefs:
            typ = m.typedefs[typ[1]]
        return typ

    def ttype(typ):
        typ = resolve(typ)
        if typ[0] == "list":
            return TType.LIST
        if typ[0] == "set":
            return TType.SET
        if typ[0] == "map":
            return TType.MAP
        if typ[1] in BASE:
            return BASE[typ[1]]
        if typ[1] in m.enums:
            return TType.I32
        return TType.STRUCT

    def tspec(typ):
        typ = resolve(typ)
        if typ[0] in ("list", "set"):
            return (ttype(typ[1]), tspec(typ[1]), False)
        if typ[0] == "map":
            return (ttype(typ[1]), tspec(typ[1]), ttype(typ[2]), tspec(typ[2]), False)
        if typ[1] == "string":
            return "UTF8"
        if typ[1] == "binary":
            return "BINARY"
        if typ[1] in BASE or typ[1] in m.enums:
            return None
        return [m.structs[typ[1]], None]

    def value(v):
        kind = v[0]
        if kind == "lit":
            return v[1]
        if kind == "list":
            return [value(x) for x in v[1]]
        if kind == "map":
            return {value(k): value(x) for k, x in v[1]}
        ref = v[1]
        if "." in ref:
            en, mem = ref.split(".", 1)
            return getattr(enums[en], mem)
        return value(m.consts[ref][1])

    m.const_values = {k: value(v[1]) for k, v in m.consts.items()}

    def make_struct(name, kind, fields, module):
        slots = tuple(f[1] for f in fields)
        defaults = [(f[1], value(f[3]) if f[3] is not None else None) for f in fields]

        def __init__(self, *args, **kw):
            for i, (fname, dv) in enumerate(defaults):
                if i < len(args):
                    v = args[i]
                elif fname in kw:
                    v = kw.pop(fname)
                else:
                    v = copy.deepcopy(dv)
                setattr(self, fname, v)
            if kw:
                raise TypeError("%s.__init__() got an unexpected keyword argument '%s'"
                                % (name, next(iter(kw))))
        __init__.__qualname__ = name + ".__init__"
        ns = {"__slots__": slots, "__init__": __init__, "__module__": module}
        if kind == "exception":
            ns["__str__"] = lambda self: repr(self)
            base = TExceptionBase
        else:
            base = TBase
        cls = type(name, (base,), ns)
        m.structs[name] = cls
        m.order.append((cls, fields))
        return cls

    for name, kind, fields in m.decls:
        make_struct(name, kind, fields, "app.ttypes")
    m.methods = {}
    for sname, (base, methods) in m.services.items():
        for mname, oneway, ret, args, throws in methods:
            a = make_struct(mname + "_args", "struct", args, "app." + sname)
            r = None
            if not oneway:
                rf = []
                if ret is not None:
                    rf.append((0, "success", ret, None, "default"))
                rf.extend(throws)
                r = make_struct(mname + "_result", "struct", rf, "app." + sname)
            m.methods[(sname, mname)] = (a, r, oneway, ret, [f[1] for f in throws])
    for cls, fields in m.order:
        if not fields:
            cls.thrift_spec = ()
            continue
        top = max(f[0] for f in fields)
        spec = [None] * (top + 1)
        for fid, fname, typ, default, req in fields:
            spec[fid] = (fid, ttype(typ), fname, tspec(typ),
                         value(default) if default is not None else None)
        cls.thrift_spec = tuple(spec)
    fix_spec([c for c, _ in m.order])
    return m


def service_methods(m, sname):
    """A service's methods, inherited ones first, as the processor maps them."""
    base, methods = m.services[sname]
    names = service_methods(m, base) if base else []
    return names + [(sname, x[0]) for x in methods]


# ------------------------------------------------------------ values

def lit(m, text):
    def ev(n):
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -ev(n.operand)
        if isinstance(n, ast.List):
            return [ev(x) for x in n.elts]
        if isinstance(n, ast.Dict):
            d = {}
            for k, v in zip(n.keys, n.values):
                d[ev(k)] = ev(v)
            return d
        if isinstance(n, ast.Name):
            if n.id == "inf":
                return float("inf")
            if n.id == "nan":
                return float("nan")
            raise ValueError("unknown name " + n.id)
        if isinstance(n, ast.Attribute):
            return getattr(m.enum_classes[n.value.id], n.attr)
        if isinstance(n, ast.Call):
            cls = m.structs[n.func.id]
            return cls(*[ev(a) for a in n.args], **{k.arg: ev(k.value) for k in n.keywords})
        raise ValueError("bad literal")
    return ev(ast.parse(text, mode="eval").body)


def show(v):
    """repr(), with a set's members sorted (CPython orders a set of str by a
    per-process hash)."""
    if isinstance(v, TBase):
        return "%s(%s)" % (type(v).__name__,
                           ", ".join("%s=%s" % (k, show(getattr(v, k))) for k in v.__slots__))
    if isinstance(v, list):
        return "[" + ", ".join(show(x) for x in v) + "]"
    if isinstance(v, (set, frozenset)):
        if not v:
            return "set()"
        return "{" + ", ".join(show(x) for x in sorted(v)) + "}"
    if isinstance(v, dict):
        return "{" + ", ".join("%s: %s" % (show(k), show(x)) for k, x in v.items()) + "}"
    return repr(v)


def canon(v):
    """Sets become sorted lists, so a re-encoded record is the same bytes in
    every run."""
    if isinstance(v, TBase):
        c = copy.copy(v)
        for k in v.__slots__:
            setattr(c, k, canon(getattr(v, k)))
        return c
    if isinstance(v, list):
        return [canon(x) for x in v]
    if isinstance(v, (set, frozenset)):
        return [canon(x) for x in sorted(v)]
    if isinstance(v, dict):
        return {k: canon(x) for k, x in v.items()}
    return v


# ------------------------------------------------------------ protocols

def factory(name, limits=None):
    lim = {}
    if limits:
        s, c = limits
        if s >= 0:
            lim["string_length_limit"] = s
        if c >= 0:
            lim["container_length_limit"] = c
    if name == "binary":
        return lambda tr: TBinaryProtocol.TBinaryProtocol(tr, **lim)
    if name == "binary-strict":
        return lambda tr: TBinaryProtocol.TBinaryProtocol(tr, strictRead=True, **lim)
    if name == "binary-loose":
        return lambda tr: TBinaryProtocol.TBinaryProtocol(tr, strictWrite=False, **lim)
    if name == "compact":
        return lambda tr: TCompactProtocol.TCompactProtocol(tr, **lim)
    if name == "json":
        return lambda tr: TJSONProtocol.TJSONProtocol(tr)
    if name == "sjson":
        return lambda tr: TJSONProtocol.TSimpleJSONProtocol(tr)
    raise ValueError("no protocol " + name)


def is_text(proto):
    return proto in ("json", "sjson")


def payload(spec):
    """x:<hex> is bytes, t:<text> text with \\xNN escapes, @path a file."""
    if spec.startswith("x:"):
        return bytes.fromhex(spec[2:])
    if spec.startswith("t:"):
        return spec[2:].encode("utf-8").decode("unicode_escape").encode("latin-1")
    if spec.startswith("@"):
        with open(spec[1:], "rb") as f:
            return f.read()
    raise ValueError("bad payload")


def wire(proto, b):
    if is_text(proto):
        return repr(b)
    return b.hex() if b else "(empty)"


def encode(proto, obj, limits=None):
    tr = TTransport.TMemoryBuffer()
    obj.write(factory(proto, limits)(tr))
    return tr.getvalue()


def decode(m, proto, tname, data, limits=None):
    tr = TTransport.TMemoryBuffer(data)
    obj = m.structs[tname]()
    obj.read(factory(proto, limits)(tr))
    return obj, len(data) - tr._buffer.tell()


# ------------------------------------------------------------ schema-less dump

NAMES = {TType.BOOL: "bool", TType.BYTE: "byte", TType.I16: "i16", TType.I32: "i32",
         TType.I64: "i64", TType.DOUBLE: "double", TType.STRING: "string",
         TType.STRUCT: "struct", TType.MAP: "map", TType.SET: "set", TType.LIST: "list"}


def tname(t):
    return NAMES.get(t, "type%d" % t)


def walk(p, t, depth, lines, label):
    pad = "  " * depth
    if t == TType.STRUCT:
        lines.append(pad + label + "struct")
        p.readStructBegin()
        while True:
            _, ft, fid = p.readFieldBegin()
            if ft == TType.STOP:
                break
            walk(p, ft, depth + 1, lines, "%d: " % fid)
            p.readFieldEnd()
        p.readStructEnd()
    elif t == TType.LIST or t == TType.SET:
        et, n = p.readListBegin() if t == TType.LIST else p.readSetBegin()
        lines.append(pad + label + "%s<%s> %d" % (tname(t), tname(et), n))
        for i in range(n):
            walk(p, et, depth + 1, lines, "[%d] " % i)
        p.readListEnd() if t == TType.LIST else p.readSetEnd()
    elif t == TType.MAP:
        kt, vt, n = p.readMapBegin()
        lines.append(pad + label + "map<%s,%s> %d" % (tname(kt), tname(vt), n))
        for i in range(n):
            walk(p, kt, depth + 1, lines, "key ")
            walk(p, vt, depth + 1, lines, "val ")
        p.readMapEnd()
    elif t == TType.STRING and isinstance(p, TJSONProtocol.TJSONProtocolBase):
        lines.append(pad + label + "string " + repr(p.readString()))
    elif t == TType.STRING:
        b = p.readBinary()
        try:
            s = b.decode("utf-8")
            lines.append(pad + label + "string " + repr(s))
        except UnicodeDecodeError:
            lines.append(pad + label + "binary " + b.hex())
    elif t == TType.BOOL:
        lines.append(pad + label + "bool " + repr(p.readBool()))
    elif t == TType.BYTE:
        lines.append(pad + label + "byte %d" % p.readByte())
    elif t == TType.I16:
        lines.append(pad + label + "i16 %d" % p.readI16())
    elif t == TType.I32:
        lines.append(pad + label + "i32 %d" % p.readI32())
    elif t == TType.I64:
        lines.append(pad + label + "i64 %d" % p.readI64())
    elif t == TType.DOUBLE:
        lines.append(pad + label + "double " + repr(p.readDouble()))
    else:
        raise ValueError("cannot dump type %d" % t)


# ------------------------------------------------------------ RPC

class Handler:
    """The tutorial's CalculatorHandler."""

    def __init__(self, m):
        self.m = m
        self.log = {}

    def ping(self):
        out("server: ping()")

    def add(self, n1, n2):
        out("server: add(%d,%d)" % (n1, n2))
        return n1 + n2

    def calculate(self, logid, work):
        out("server: calculate(%d, %s)" % (logid, show(work)))
        Op = self.m.enum_classes["Operation"]
        if work.op == Op.ADD:
            val = work.num1 + work.num2
        elif work.op == Op.SUBTRACT:
            val = work.num1 - work.num2
        elif work.op == Op.MULTIPLY:
            val = work.num1 * work.num2
        elif work.op == Op.DIVIDE:
            if work.num2 == 0:
                raise self.m.structs["InvalidOperation"](work.op, "Cannot divide by 0")
            val = work.num1 / work.num2
        else:
            raise self.m.structs["InvalidOperation"](work.op, "Invalid operation")
        log = self.m.structs["SharedStruct"]()
        log.key = logid
        log.value = "%d" % (val)
        self.log[logid] = log
        return val

    def getStruct(self, key):
        out("server: getStruct(%d)" % (key))
        return self.log[key]

    def zip(self):
        out("server: zip()")


class Processor:
    """The generated Calculator.Processor (which extends SharedService's)."""

    def __init__(self, m, sname, handler):
        self.m = m
        self.handler = handler
        self.names = {name: s for s, name in service_methods(m, sname)}

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if name not in self.names:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD,
                                      'Unknown function %s' % (name))
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        a, r, oneway, ret, throws = self.m.methods[(self.names[name], name)]
        args = a()
        args.read(iprot)
        iprot.readMessageEnd()
        fn = getattr(self.handler, name)
        if oneway:
            try:
                fn(*[getattr(args, k) for k in a.__slots__])
            except Exception:
                logging.exception('Exception in oneway handler')
            return True
        result = r()
        try:
            v = fn(*[getattr(args, k) for k in a.__slots__])
            if ret is not None:
                result.success = v
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TApplicationException as ex:
            logging.exception('TApplication exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception as ex:
            for t in throws:
                spec = [s for s in r.thrift_spec if s is not None and s[2] == t][0]
                if isinstance(ex, spec[3][0]):
                    msg_type = TMessageType.REPLY
                    setattr(result, t, ex)
                    break
            else:
                logging.exception('Unexpected exception in handler')
                msg_type = TMessageType.EXCEPTION
                result = TApplicationException(TApplicationException.INTERNAL_ERROR,
                                               'Internal error')
        oprot.writeMessageBegin(name, msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()
        return True


def send(m, sname, oprot, method, args):
    """The generated Client.send_<method>; the generated client never moves
    its sequence id off 0."""
    a, r, oneway, ret, throws = m.methods[(dict((n, s) for s, n in service_methods(m, sname))[method], method)]
    oprot.writeMessageBegin(method, TMessageType.ONEWAY if oneway else TMessageType.CALL, 0)
    args.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()
    return a, r, oneway, ret, throws


def recv(m, iprot, method, r, ret, throws):
    """The generated Client.recv_<method>."""
    (fname, mtype, rseqid) = iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
        x = TApplicationException()
        x.read(iprot)
        iprot.readMessageEnd()
        raise x
    result = r()
    result.read(iprot)
    iprot.readMessageEnd()
    if ret is None:
        for t in throws:
            if getattr(result, t) is not None:
                raise getattr(result, t)
        return None
    if result.success is not None:
        return result.success
    for t in throws:
        if getattr(result, t) is not None:
            raise getattr(result, t)
    raise TApplicationException(TApplicationException.MISSING_RESULT,
                                "%s failed: unknown result" % method)


def transport_for(kind, fileobj):
    base = TTransport.TFileObjectTransport(fileobj)
    if kind == "framed":
        return TTransport.TFramedTransport(base)
    if kind == "buffered":
        return TTransport.TBufferedTransport(base)
    return base


def read_file(path):
    with open(path, "rb") as f:
        return f.read()


def write_file(path, data):
    with open(path, "wb") as f:
        f.write(data)


# ------------------------------------------------------------ the app's programs

def events_rows():
    rows = []
    with open("data/events.tsv", encoding="utf-8") as f:
        for line in f.read().split("\n")[1:]:
            if not line:
                continue
            ts, kind, user, ms, attrs = line.split("\t")
            a = {}
            if attrs:
                for kv in attrs.split(";"):
                    k, v = kv.split("=", 1)
                    a[k] = v
            rows.append((int(ts), kind, int(user), float(ms), a))
    return rows


def eventlog_write(m, proto, path):
    Event = m.structs["Event"]
    with open(path, "wb") as f:
        tr = TTransport.TFramedTransport(TTransport.TFileObjectTransport(f))
        p = factory(proto)(tr)
        n = 0
        for ts, kind, user, ms, attrs in events_rows():
            Event(ts=ts, kind=kind, user=user, ms=ms, attrs=attrs).write(p)
            tr.flush()
            n += 1
    out("wrote %d events, %d bytes" % (n, os.path.getsize(path)))


def frames(m, proto, path, tname):
    """Yields each framed record of the file, read as tname."""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        tr = TTransport.TFramedTransport(TTransport.TFileObjectTransport(f))
        while f.tell() < size:
            obj = m.structs[tname]()
            obj.read(factory(proto)(tr))
            yield obj


def eventlog_report(m, proto, path, tname):
    kinds = {}
    users = set()
    n = 0
    try:
        for ev in frames(m, proto, path, tname):
            n += 1
            k = kinds.setdefault(ev.kind, [0, 0.0, 0.0])
            k[0] += 1
            k[1] += ev.ms
            k[2] = max(k[2], ev.ms)
            users.add(ev.user)
            if tname == "EventV2" and n <= 3:
                out("v2 %s extra=%s flag=%s" % (ev.kind, show(ev.extra), show(ev.flag)))
    finally:
        out("%d events from %d users" % (n, len(users)))
        for kind in sorted(kinds):
            c, total, mx = kinds[kind]
            out("%-8s %3d  mean %8.2f ms  max %8.2f ms" % (kind, c, total / c, mx))


def users_rows():
    rows = []
    with open("data/users.tsv", encoding="utf-8") as f:
        for line in f.read().split("\n")[1:]:
            if line:
                uid, name, email = line.split("\t")
                rows.append((int(uid), name, email))
    return rows


def legacy_write(m, proto, path):
    """The old service's writer: UserV1 records, one frame each."""
    UserV1 = m.structs["UserV1"]
    with open(path, "wb") as f:
        tr = TTransport.TFramedTransport(TTransport.TFileObjectTransport(f))
        p = factory(proto)(tr)
        for uid, name, email in users_rows():
            UserV1(id=uid, name=name, email=email).write(p)
            tr.flush()
    out("wrote %d users, %d bytes" % (len(users_rows()), os.path.getsize(path)))


def migrate(m, inproto, inpath, outproto, outpath):
    """Reads UserV1 frames as UserV2 (the new fields take their IDL
    defaults), grants roles, and writes UserV2 frames."""
    admins = set()
    with open("data/admins.txt", encoding="utf-8") as f:
        for line in f.read().split("\n"):
            if line:
                admins.add(line)
    n = 0
    with open(outpath, "wb") as f:
        tr = TTransport.TFramedTransport(TTransport.TFileObjectTransport(f))
        p = factory(outproto)(tr)
        for u in frames(m, inproto, inpath, "UserV2"):
            if u.email in admins and "admin" not in u.roles:
                u.roles.append("admin")
            if u.email.endswith("@example.invalid"):
                u.active = False
            u.score = len(u.name) / 4.0
            u.write(p)
            tr.flush()
            n += 1
    out("migrated %d users, %d bytes" % (n, os.path.getsize(outpath)))


def export(m, inproto, inpath, tname, outpath):
    """One SimpleJSON line a record."""
    lines = []
    for u in frames(m, inproto, inpath, tname):
        lines.append(encode("sjson", canon(u)))
    write_file(outpath, b"\n".join(lines) + b"\n")
    for ln in lines:
        out(ln.decode("utf-8"))


# ------------------------------------------------------------ jobs

def run(m, parts):
    op = parts[0]
    a = parts[1:]
    if op == "enc":
        b = encode(a[0], lit(m, a[1]))
        out(len(b), wire(a[0], b))
    elif op == "dec":
        obj, rest = decode(m, a[0], a[1], payload(a[2]))
        out(show(obj) + ("" if rest == 0 else "  rest %d" % rest))
    elif op == "lim":
        lim = (int(a[1]), int(a[2]))
        obj, rest = decode(m, a[0], a[3], payload(a[4]), lim)
        out(show(obj))
    elif op == "rt":
        obj = lit(m, a[1])
        b = encode(a[0], obj)
        out(len(b), wire(a[0], b))
        back, rest = decode(m, a[0], type(obj).__name__, b)
        out(show(back))
        out("equal", back == obj)
    elif op == "conv":
        obj, rest = decode(m, a[0], a[2], payload(a[3]))
        b = encode(a[1], canon(obj))
        out(len(b), wire(a[1], b))
        back, rest = decode(m, a[1], a[2], b)
        out("equal", back == obj)
    elif op == "sizes":
        obj = lit(m, a[0])
        for proto in ("binary", "compact", "json", "sjson"):
            out("%-8s %4d" % (proto, len(encode(proto, obj))))
    elif op == "msgw":
        tr = TTransport.TMemoryBuffer()
        p = factory(a[0])(tr)
        p.writeMessageBegin(a[1], int(a[2]), int(a[3]))
        p.writeStructBegin("x")
        p.writeFieldStop()
        p.writeStructEnd()
        p.writeMessageEnd()
        b = tr.getvalue()
        out(len(b), wire(a[0], b))
    elif op == "msgr":
        tr = TTransport.TMemoryBuffer(payload(a[1]))
        p = factory(a[0])(tr)
        name, mtype, seqid = p.readMessageBegin()
        out("name %r type %d seqid %d" % (name, mtype, seqid))
    elif op == "dump":
        data = payload(a[1])
        tr = TTransport.TMemoryBuffer(data)
        p = factory(a[0])(tr)
        lines = []
        try:
            if a[2] == "message":
                name, mtype, seqid = p.readMessageBegin()
                lines.append("message %r type %d seqid %d" % (name, mtype, seqid))
                walk(p, TType.STRUCT, 1, lines, "")
                p.readMessageEnd()
            else:
                walk(p, TType.STRUCT, 0, lines, "")
        finally:
            for ln in lines:
                out(ln)
        rest = len(data) - tr._buffer.tell()
        if rest:
            out("rest %d" % rest)
    elif op == "skip":
        data = payload(a[2])
        tr = TTransport.TMemoryBuffer(data)
        p = factory(a[0])(tr)
        p.skip(int(a[1]))
        out("skipped %d of %d bytes" % (tr._buffer.tell(), len(data)))
    elif op == "frames":
        # frames <proto> <path> <literal>...
        with open(a[1], "wb") as f:
            tr = TTransport.TFramedTransport(TTransport.TFileObjectTransport(f))
            p = factory(a[0])(tr)
            for text in a[2:]:
                lit(m, text).write(p)
                tr.flush()
        out(os.path.getsize(a[1]), "bytes")
    elif op == "readframes":
        n = 0
        try:
            for obj in frames(m, a[0], a[1], a[2]):
                out(show(obj))
                n += 1
        finally:
            out("%d records" % n)
    elif op == "file":
        b = read_file(a[0])
        out(len(b), "(empty)" if not b else b.hex() if len(b) <= 96 else b[:96].hex() + "...")
    elif op == "patch":
        b = bytearray(read_file(a[0]))
        b[int(a[1])] = int(a[2], 16)
        write_file(a[0], bytes(b))
        out("patched")
    elif op == "truncate":
        b = read_file(a[0])
        write_file(a[0], b[:int(a[1])])
        out("truncated to", int(a[1]))
    elif op == "call":
        # call <proto> <transport> <service> <method> <args literal>
        proto, kind, sname, method = a[0], a[1], a[2], a[3]
        LOG.clear()
        server = Processor(m, "Calculator", HANDLER)
        with open("data/out/req.bin", "wb") as f:
            p = factory(proto)(transport_for(kind, f))
            if sname != "-":
                p = TMultiplexedProtocol(p, sname)
            a_cls = m.methods[(dict((n, s) for s, n in service_methods(m, "Calculator"))[method], method)][0]
            args = a_cls(*[lit(m, x) for x in a[4:]])
            _, r, oneway, ret, throws = send(m, "Calculator", p, method, args)
        out("request", wire(proto, read_file("data/out/req.bin")))
        serve(m, proto, kind, server if sname == "-" else MUX)
        if oneway:
            return
        with open("data/out/resp.bin", "rb") as f:
            p = factory(proto)(transport_for(kind, f))
            v = recv(m, p, method, r, ret, throws)
        out("result", show(v))
    elif op == "raw":
        # raw <proto> <transport> <mux|plain> <payload>
        LOG.clear()
        write_file("data/out/req.bin", payload(a[3]))
        serve(m, a[0], a[1], MUX if a[2] == "mux" else Processor(m, "Calculator", HANDLER))
    elif op == "eventlog":
        if a[0] == "write":
            eventlog_write(m, a[1], a[2])
        else:
            eventlog_report(m, a[1], a[2], a[3])
    elif op == "legacy":
        legacy_write(m, a[0], a[1])
    elif op == "migrate":
        migrate(m, a[0], a[1], a[2], a[3])
    elif op == "export":
        export(m, a[0], a[1], a[2], a[3])
    elif op == "const":
        out(show(m.const_values[a[0]]))
    elif op == "enum":
        e = m.enum_classes[a[0]]
        out(", ".join("%s=%d" % (k, v) for k, v in sorted(e._NAMES_TO_VALUES.items(), key=lambda kv: kv[1])))
    elif op == "spec":
        cls = m.structs[a[0]]
        out("slots", ", ".join(cls.__slots__))
        for s in cls.thrift_spec:
            if s is None:
                out("-")
            else:
                out("%d %s %s" % (s[0], s[2], tname(s[1])))
    else:
        raise ValueError("unknown op " + op)


def serve(m, proto, kind, processor):
    """One server turn: reads the request file, writes the response file."""
    try:
        with open("data/out/req.bin", "rb") as fi, open("data/out/resp.bin", "wb") as fo:
            iprot = factory(proto)(transport_for(kind, fi))
            oprot = factory(proto)(transport_for(kind, fo))
            processor.process(iprot, oprot)
    except Exception as e:
        out("server " + err(e))
    finally:
        for msg in LOG:
            out("server log: " + msg)
        LOG.clear()
    resp = read_file("data/out/resp.bin")
    out("response", wire(proto, resp))


def main():
    global HANDLER, MUX
    with open("data/app.thrift", encoding="utf-8") as f:
        m = build(parse_idl(f.read()))
    HANDLER = Handler(m)
    MUX = TMultiplexedProcessor()
    MUX.registerProcessor("Calculator", Processor(m, "Calculator", HANDLER))
    os.makedirs("data/out", exist_ok=True)
    with open("data/jobs.tsv", "rb") as f:
        jobs = [j for j in f.read().decode("utf-8").split("\n") if j]
    n = 0
    nerr = 0
    for line in jobs:
        parts = line.split("\t")
        print("> " + " ".join(parts))
        try:
            run(m, parts)
        except Exception as e:
            out(err(e))
            nerr += 1
        n += 1
    print("%d jobs, %d ended in an error" % (n, nerr))


main()
