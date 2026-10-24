"""Runs data/jobs.txt on the vendored pg8000 and prints what it does.

Values in the jobs are Python literals plus these constructors, evaluated
by walking the expression's AST (nothing is exec'd): Decimal, UUID,
date, time, datetime (tz=<offset seconds> gives a fixed-offset zone),
timedelta, bytearray, float, IPv4Address, IPv4Network, IPv6Address,
IPv6Network, Range and PGInterval; and, for `stream=`, out_bytes(),
out_text(), in_lines(list), in_bytes(bytes) and in_text(str).

A session talks to a fake socket that replays data/<session>.bin and
prints every message pg8000 flushes. Warnings (dateutil's on a BC
timestamp) are printed where they are raised, every time.

Run: python3 -I -B oracle.py > expected.out"""
import ast
import datetime
import decimal
import io
import ipaddress
import os
import sys
import uuid
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pgstub  # noqa: E402

pgstub.install()

from pg8000 import converters, dbapi, native  # noqa: E402
from pg8000.types import PGInterval, Range  # noqa: E402

DATA = os.path.join(HERE, "data")


def mk_datetime(*a, tz=None):
    if tz is None:
        return datetime.datetime(*a)
    return datetime.datetime(*a, tzinfo=datetime.timezone(datetime.timedelta(seconds=tz)))


CALLS = {
    "Decimal": decimal.Decimal, "UUID": uuid.UUID, "date": datetime.date, "time": datetime.time,
    "datetime": mk_datetime, "timedelta": datetime.timedelta, "bytearray": bytearray, "float": float,
    "IPv4Address": ipaddress.IPv4Address, "IPv4Network": ipaddress.IPv4Network,
    "IPv6Address": ipaddress.IPv6Address, "IPv6Network": ipaddress.IPv6Network,
    "Range": Range, "PGInterval": PGInterval,
    "out_bytes": io.BytesIO, "out_text": io.StringIO, "in_lines": list, "in_bytes": io.BytesIO,
    "in_text": io.StringIO,
}


def value(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -value(node.operand)
    if isinstance(node, ast.List):
        return [value(e) for e in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(value(e) for e in node.elts)
    if isinstance(node, ast.Dict):
        return {value(k): value(v) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in CALLS:
        args = [value(a) for a in node.args]
        kw = {k.arg: value(k.value) for k in node.keywords}
        return CALLS[node.func.id](*args, **kw)
    raise ValueError(f"unsupported value {ast.dump(node)}")


def parse_value(src):
    return value(ast.parse(src, mode="eval").body)


def split_top(src):
    """Splits on spaces outside quotes and brackets."""
    out, cur, depth, quote, i = [], "", 0, None, 0
    while i < len(src):
        c = src[i]
        if quote:
            cur += c
            if c == "\\":
                cur += src[i + 1]
                i += 1
            elif c == quote:
                quote = None
        elif c in "'\"":
            quote = c
            cur += c
        elif c in "([{":
            depth += 1
            cur += c
        elif c in ")]}":
            depth -= 1
            cur += c
        elif c == " " and depth == 0:
            if cur:
                out.append(cur)
            cur = ""
        else:
            cur += c
        i += 1
    if cur:
        out.append(cur)
    return out


def kwargs(words):
    out = {}
    for w in words:
        k, v = w.split("=", 1)
        out[k] = parse_value(v)
    return out


def err(e):
    return f"error {type(e).__name__}: {e}"


class FakeSock:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.out = bytearray()
        self.started = False

    def sendall(self, d):
        print(f"    > ssl-request {bytes(d)!r}")

    def recv(self, n):
        b = self.data[self.pos:self.pos + n]
        self.pos += len(b)
        return b

    read = recv

    def makefile(self, mode):
        return self

    def write(self, d):
        self.out += d

    def flush(self):
        b = bytes(self.out)
        self.out.clear()
        i = 0
        if not self.started and len(b) >= 4:
            n = int.from_bytes(b[0:4], "big")
            print(f"    > startup {b[4:n]!r}")
            i = n
            self.started = True
        while i + 5 <= len(b):
            n = int.from_bytes(b[i + 1:i + 5], "big")
            print(f"    > {b[i:i + 1].decode()} {b[i + 5:i + 1 + n]!r}")
            i += 1 + n

    def close(self):
        pass


def show_warnings(caught):
    for w in caught:
        print(f"    warning {w.category.__name__}: {w.message}")
    caught.clear()


def run_session(name, opts, ops, caught):
    o = kwargs(opts)
    ssl = o.pop("ssl")
    with open(os.path.join(DATA, name + ".bin"), "rb") as f:
        sock = FakeSock(f.read())
    try:
        con = native.Connection(o.pop("user"), sock=sock, ssl_context=ssl, **o)
    except Exception as e:
        print(f"    {err(e)}")
        return
    print("    connected")
    stmts = {}
    for op in ops:
        print(f"  op {op}")
        words = split_top(op)
        cmd = words[0]
        try:
            if cmd == "run":
                sql = parse_value(words[1])
                kw = kwargs(words[2:])
                stream = kw.get("stream")
                rows = con.run(sql, **kw)
                show_warnings(caught)
                print(f"    rows {rows!r}")
                print(f"    columns {con.columns!r}")
                print(f"    row_count {con.row_count!r}")
                if isinstance(stream, (io.BytesIO, io.StringIO)) and "TO STDOUT" in sql:
                    print(f"    stream {stream.getvalue()!r}")
            elif cmd == "prepare":
                ps = con.prepare(parse_value(words[2]))
                stmts[words[1]] = ps
                print(f"    name {ps.name_bin!r} columns {ps.cols!r}")
            elif cmd == "exec":
                ps = stmts[words[1]]
                rows = ps.run(**kwargs(words[2:]))
                print(f"    rows {rows!r}")
                print(f"    columns {ps.columns!r}")
            elif cmd == "closestmt":
                stmts[words[1]].close()
            elif cmd == "show":
                print(f"    status {con._transaction_status!r} key {con._backend_key_data!r}")
                print(f"    parameter_statuses {con.parameter_statuses!r}")
                print(f"    notices {con.notices!r}")
                print(f"    notifications {con.notifications!r}")
            elif cmd == "close":
                con.close()
        except Exception as e:
            show_warnings(caught)
            print(f"    {err(e)}")


def run_job(job, caught):
    kind, rest = job.split(" ", 1)
    if kind == "stmt":
        names, sql = rest.split(" ", 1)
        names = [] if names == "-" else names.split(",")
        statement, make_vals = native.to_statement(parse_value(sql))
        print(f"    {statement!r}")
        print(f"    vals {make_vals({n: n for n in names})!r}")
    elif kind == "style":
        style, names, sql = rest.split(" ", 2)
        names = [] if names == "-" else names.split(",")
        args = {n: n for n in names} if style in ("named", "pyformat") else tuple(names)
        print(f"    {dbapi.convert_paramstyle(style, parse_value(sql), args)!r}")
    elif kind == "ident":
        print(f"    {converters.identifier(parse_value(rest))!r}")
    elif kind == "literal":
        print(f"    {converters.literal(parse_value(rest))!r}")
    elif kind == "out":
        print(f"    {converters.make_param(converters.PY_TYPES, parse_value(rest))!r}")
    elif kind == "in":
        oid, text = rest.split(" ", 1)
        func = converters.PG_TYPES.get(int(oid), converters.string_in)
        v = func(parse_value(text))
        show_warnings(caught)
        print(f"    {v!r}")


def main():
    with open(os.path.join(DATA, "jobs.txt")) as f:
        lines = [ln for ln in f.read().split("\n") if ln]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        i = 0
        while i < len(lines):
            job = lines[i]
            print(f"> {job}")
            if job.startswith("session "):
                _, name, opts = job.split(" ", 2)
                j = i + 1
                while lines[j] != "end":
                    j += 1
                run_session(name, split_top(opts), [ln[3:] for ln in lines[i + 1:j]], caught)
                i = j + 1
                continue
            try:
                run_job(job, caught)
            except Exception as e:
                show_warnings(caught)
                print(f"    {err(e)}")
            i += 1


main()
