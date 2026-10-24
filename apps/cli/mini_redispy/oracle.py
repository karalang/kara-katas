"""Plays data/jobs.txt through redis-py 5.2.1 (the copy in vendor/,
unchanged) against a scripted fake server, and prints what the client sent
and what each call returned.

Run: python3 -I -B oracle.py > expected.out (after mk.py wrote the jobs)"""
import errno
import os
import socket
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))

import redis  # noqa: E402
from redis.connection import Connection, parse_url  # noqa: E402

MASK32 = 4294967295
OUT = []


def emit(line):
    OUT.append(line)


# ------------------------------------------------------------ showing values

def show(v):
    if isinstance(v, (set, frozenset)):
        if not v:
            return "set()"
        return "{" + ", ".join(sorted(show(x) for x in v)) + "}"
    if isinstance(v, list):
        return "[" + ", ".join(show(x) for x in v) + "]"
    if isinstance(v, tuple):
        if len(v) == 1:
            return "(" + show(v[0]) + ",)"
        return "(" + ", ".join(show(x) for x in v) + ")"
    if isinstance(v, dict):
        return "{" + ", ".join(show(k) + ": " + show(x) for k, x in v.items()) + "}"
    if isinstance(v, BaseException):
        return type(v).__name__ + "(" + ", ".join(show(a) for a in v.args) + ")"
    if isinstance(v, type):
        return f"<class '{v.__module__}.{v.__name__}'>"
    return repr(v)


def fnv(data):
    h = 2166136261
    for b in data:
        h = ((h ^ b) * 16777619) & MASK32
    return h


def wire(data):
    if len(data) > 160:
        return f"<{len(data)} bytes, fnv {fnv(data):08x}>"
    return show(bytes(data))


# ------------------------------------------------------------ the fake server

CLOSE = "close"
HANG = "hang"


class Server:
    def __init__(self):
        self.units = []
        self.next = 0
        self.connects = 0


SERVER = Server()


def command_count(buf):
    """How many complete RESP arrays buf holds, and the bytes they take."""
    n = 0
    pos = 0
    while True:
        if pos >= len(buf) or buf[pos:pos + 1] != b"*":
            return n, pos
        end = buf.find(b"\r\n", pos)
        if end < 0:
            return n, pos
        count = int(buf[pos + 1:end])
        p = end + 2
        ok = True
        for _ in range(count):
            e = buf.find(b"\r\n", p)
            if e < 0:
                ok = False
                break
            size = int(buf[p + 1:e])
            p = e + 2 + size + 2
            if p > len(buf):
                ok = False
                break
        if not ok:
            return n, pos
        n += 1
        pos = p


class FakeSocket:
    def __init__(self, server):
        self.server = server
        self.inbox = b""
        self.out = b""
        self.eof = False
        self.timeout = None

    def settimeout(self, t):
        self.timeout = t

    def setsockopt(self, *a):
        pass

    def sendall(self, data):
        data = bytes(data)
        emit("send " + wire(data))
        self.inbox += data
        n, used = command_count(self.inbox)
        self.inbox = self.inbox[used:]
        for _ in range(n):
            if self.eof:
                break
            srv = self.server
            if srv.next >= len(srv.units):
                unit = HANG
            else:
                unit = srv.units[srv.next]
                srv.next += 1
            if unit == CLOSE:
                self.eof = True
            elif unit == HANG:
                pass
            else:
                self.out += unit

    def recv(self, size):
        if self.out:
            data = self.out[:size]
            self.out = self.out[size:]
            return data
        if self.eof:
            return b""
        if self.timeout == 0:
            raise BlockingIOError(errno.EWOULDBLOCK, "Resource temporarily unavailable")
        raise socket.timeout("timed out")

    def shutdown(self, how):
        pass

    def close(self):
        emit("close")


class FakeConnection(Connection):
    def _connect(self):
        SERVER.connects += 1
        emit(f"connect #{SERVER.connects}")
        return FakeSocket(SERVER)


# ------------------------------------------------------------ the job language

def unescape(text):
    out = bytearray()
    i = 0
    raw = text.encode()
    while i < len(raw):
        if raw[i:i + 1] == b"%":
            out.append(int(raw[i + 1:i + 3], 16))
            i += 3
        else:
            out.append(raw[i])
            i += 1
    return bytes(out)


def parse_tokens(tokens, i, stop):
    vals = []
    while i < len(tokens) and tokens[i] != stop:
        v, i = parse_value(tokens, i)
        vals.append(v)
    return vals, i + 1


def parse_value(tokens, i):
    t = tokens[i]
    if t == "[":
        vals, i = parse_tokens(tokens, i + 1, "]")
        return vals, i
    if t == "(":
        vals, i = parse_tokens(tokens, i + 1, ")")
        return tuple(vals), i
    if t == "{":
        vals, i = parse_tokens(tokens, i + 1, "}")
        return {vals[j]: vals[j + 1] for j in range(0, len(vals), 2)}, i
    kind, payload = t[0], t[2:]
    if kind == "s":
        return unescape(payload).decode(), i + 1
    if kind == "b":
        return unescape(payload), i + 1
    if kind == "i":
        return int(payload), i + 1
    if kind == "f":
        return float(payload), i + 1
    if kind == "N":
        return None, i + 1
    if kind == "T":
        return True, i + 1
    if kind == "F":
        return False, i + 1
    if kind == "r":
        star = payload.rfind("*")
        return unescape(payload[:star]).decode() * int(payload[star + 1:]), i + 1
    if kind == "c":
        return {"float": float, "int": int}[payload], i + 1
    raise ValueError("bad token " + t)


def parse_args(tokens):
    args, kwargs = [], {}
    i = 0
    while i < len(tokens):
        t = tokens[i]
        eq = t.find("=")
        if eq > 0 and t[1] != ":":
            name = t[:eq]
            rest = t[eq + 1:]
            sub = [rest] + tokens[i + 1:]
            v, j = parse_value(sub, 0)
            kwargs[name] = v
            i = i + j
        else:
            v, i = parse_value(tokens, i)
            args.append(v)
    return args, kwargs


def outcome(fn):
    try:
        r = fn()
        if isinstance(r, redis.client.Pipeline):
            emit("= queued")
        else:
            line = "= " + show(r)
            if len(line) > 400:
                line = f"= <{len(line) - 2} chars, fnv {fnv(line[2:].encode()):08x}>"
            emit(line)
    except Exception as e:
        emit(f"! {type(e).__name__}: {e}")


def make_client(tokens):
    _, kw = parse_args(tokens)
    opts = {
        "protocol": kw.get("proto", 2),
        "decode_responses": kw.get("decode", False),
        "lib_name": kw.get("lib_name", "redis-py"),
        "lib_version": kw.get("lib_version", "5.2.1"),
        "connection_class": FakeConnection,
    }
    for k in ("password", "username", "db", "client_name", "retry_on_timeout"):
        if k in kw:
            opts[k] = kw[k]
    pool = redis.ConnectionPool(**opts)
    return redis.Redis(connection_pool=pool)


def run_bitfield(target, tokens):
    groups = []
    cur = []
    for t in tokens:
        if t == "|":
            groups.append(cur)
            cur = []
        else:
            cur.append(t)
    groups.append(cur)
    args, kwargs = parse_args(groups[0])
    op = target.bitfield(*args, **kwargs)
    for g in groups[1:]:
        name = g[0]
        a, k = parse_args(g[1:])
        if name == "execute":
            return op.execute()
        getattr(op, name)(*a, **k)
    return op.command


def main():
    global SERVER
    text = open(os.path.join("data", "jobs.txt")).read()
    client = None
    pipe = None
    for line in text.split("\n"):
        if line == "":
            continue
        tokens = line.split(" ")
        head = tokens[0]
        if head == "job":
            if client is not None:
                client.connection_pool.disconnect()
            emit("")
            emit("== " + " ".join(tokens[1:]))
            SERVER = Server()
            client = None
            pipe = None
        elif head == "client":
            emit(" ".join(tokens))
            client = make_client(tokens[1:])
        elif head == "reply":
            if tokens[1] == "@close":
                SERVER.units.append(CLOSE)
            elif tokens[1] == "@hang":
                SERVER.units.append(HANG)
            else:
                SERVER.units.append(unescape(tokens[1]))
        elif head == "call":
            emit("call " + " ".join(tokens[1:]))
            target = pipe if pipe is not None else client
            args, kwargs = parse_args(tokens[2:])
            name = tokens[1]
            outcome(lambda: getattr(target, name)(*args, **kwargs))
        elif head == "bitfield":
            emit("bitfield " + " ".join(tokens[1:]))
            target = pipe if pipe is not None else client
            outcome(lambda: run_bitfield(target, tokens[1:]))
        elif head == "pipe":
            emit("pipe " + " ".join(tokens[1:]))
            args, kwargs = parse_args(tokens[2:])
            what = tokens[1]
            if what == "begin":
                pipe = client.pipeline(**kwargs)
                emit("= pipeline")
            elif what == "end":
                pipe = None
                emit("= client")
            else:
                outcome(lambda: getattr(pipe, what)(*args, **kwargs))
        elif head == "url":
            emit("url " + tokens[1])
            outcome(lambda: parse_url(unescape(tokens[1]).decode()))
        else:
            raise SystemExit("bad line " + line)
    if client is not None:
        client.connection_pool.disconnect()
    sys.stdout.write("\n".join(OUT[1:]) + "\n")


main()
