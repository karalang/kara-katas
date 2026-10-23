#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored python-osc 1.10.2, printing
what mini_pythonosc.kara must print. The clock (time.time / time.sleep) is
replaced by a fake that starts at each job's <now> and moves only when
something sleeps; logging warnings are collected and printed as "log"
lines. An exception prints as "error <module.Class>: <str(e)>".
Run: python3 -I -B oracle.py > expected.out"""
import logging
import os
import struct
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
from pythonosc import dispatcher, osc_bundle, osc_bundle_builder, osc_message  # noqa: E402
from pythonosc import osc_message_builder, osc_packet, slip  # noqa: E402
from pythonosc.parsing import ntp, osc_types  # noqa: E402

US = "\x1f"
CLIENT = ("192.168.1.20", 53000)
CLOCK = [0.0]
LOG = []


def fake_sleep(d):
    print("  sleep %r" % d)
    CLOCK[0] += d


time.time = lambda: CLOCK[0]
time.sleep = fake_sleep


class Collect(logging.Handler):
    def emit(self, record):
        LOG.append("%s:%s:%s" % (record.levelname, record.name, record.getMessage()))


logging.getLogger().addHandler(Collect())
logging.getLogger().setLevel(logging.WARNING)


def flush_log():
    for line in LOG:
        print("log " + line)
    LOG.clear()


def err(e):
    flush_log()
    mod = type(e).__module__
    name = type(e).__name__
    if mod.startswith("pythonosc"):
        name = mod.split(".")[-1] + "." + name
    elif mod == "struct":
        name = "struct." + name
    print("error %s: %s" % (name, e))


# ---- the value grammar of mk.py

def parse_type(t):
    if t.startswith("<"):
        inner = t[1:-1]
        return [] if inner == "" else [parse_type(x) for x in inner.split(",")]
    return t


def atom(t):
    k, rest = t[0], t[1:]
    if k == "i":
        return int(rest)
    if k == "f":
        return float(rest)
    if k == "s":
        return bytes.fromhex(rest).decode("utf-8")
    if k == "b":
        return bytes.fromhex(rest)
    if k == "T":
        return True
    if k == "F":
        return False
    if k == "N":
        return None
    if k in "mu":
        return tuple(int(x) for x in rest.split(","))
    raise SystemExit("bad atom " + t)


def parse_args(text):
    """[(value, type or None)] from the value grammar."""
    toks = text.split(" ") if text else []
    pos = [0]

    def one():
        t = toks[pos[0]]
        pos[0] += 1
        if t == "(":
            items = []
            while not toks[pos[0]].startswith(")"):
                items.append(one()[0])
            close = toks[pos[0]]
            pos[0] += 1
            ty = parse_type(close[2:]) if close.startswith(")@") else None
            return items, ty
        if "@" in t:
            v, ty = t.split("@", 1)
            return atom(v), parse_type(ty)
        return atom(t), None

    out = []
    while pos[0] < len(toks):
        out.append(one())
    return out


def addr_of(f):
    return None if f == "-" else bytes.fromhex(f[1:]).decode("utf-8")


def ts_of(f):
    if f == "imm":
        return osc_types.IMMEDIATELY
    if f[0] == "i":
        return int(f[1:])
    return float(f[1:])


# ---- printing

def show_msg(m, ind=""):
    print("%smsg %r %r size %d" % (ind, m.address, m.params, m.size))
    print("%sstr %s" % (ind, str(m)))


def show_bundle(bu, ind=""):
    print("%sbundle ts %r n %d size %d" % (ind, bu.timestamp, bu.num_contents, bu.size))
    for c in bu:
        if isinstance(c, osc_bundle.OscBundle):
            show_bundle(c, ind + "  ")
        else:
            show_msg(c, ind + "  ")


# ---- handlers for the servers

class Callback:
    def __init__(self, name, ret):
        self.name = name
        self.ret = ret

    def __call__(self, *a):
        print("  %s%r" % (self.name, a))
        return self.ret(a)

    def __repr__(self):
        return "<%s>" % self.name


CBS = {
    "log": Callback("log", lambda a: None),
    "echo": Callback("echo", lambda a: ("/echo",) + a[1:]),
    "ack": Callback("ack", lambda a: "/ack"),
    "bad": Callback("bad", lambda a: ("/bad", (1, 2, 3))),
    "empty": Callback("empty", lambda a: ""),
    "who": Callback("who", lambda a: ("/seen", a[0][0], a[0][1])),
}


def make_dispatcher(setup):
    ops = setup.split(US)
    strict = True
    if ops and ops[0] == "strict 0":
        strict = False
        ops = ops[1:]
    d = dispatcher.Dispatcher(strict_timing=strict)
    for op in ops:
        p = op.split(" ")
        if p[0] == "map":
            d.map(p[1], CBS[p[2]], *[v for v, _ in parse_args(" ".join(p[3:]))])
        elif p[0] == "mapr":
            d.map(p[1], CBS[p[2]], needs_reply_address=True)
        elif p[0] == "unmap":
            try:
                d.unmap(p[1], CBS[p[2]])
            except ValueError as e:
                print("unmap error: %s" % e)
        elif p[0] == "default":
            d.set_default_handler(None if p[1] == "-" else CBS[p[1]])
    return d


def reply_msg(r):
    if not isinstance(r, tuple):
        r = [r]
    return osc_message_builder.build_msg(r[0], r[1:])


class Sock:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def recv(self, n):
        chunk = self.data[self.pos:self.pos + n]
        self.pos += len(chunk)
        return chunk


def serve_udp(d, stream):
    for dg in stream.split(","):
        print("<< %s" % (dg or "(empty)"))
        data = bytes.fromhex(dg)
        if not (osc_bundle.OscBundle.dgram_is_bundle(data) or osc_message.OscMessage.dgram_is_message(data)):
            print("ignored")
            continue
        try:
            for r in d.call_handlers_for_packet(data, CLIENT):
                m = reply_msg(r)
                print(">> %s %s" % (m.dgram.hex(), m))
        except Exception as e:
            err(e)
        flush_log()


def serve_tcp10(d, stream):
    sock = Sock(bytes.fromhex(stream))

    def recvall(count):
        buf = b""
        while count > 0:
            newbuf = sock.recv(count)
            if not newbuf:
                return b""
            buf += newbuf
            count -= len(newbuf)
        return buf

    while True:
        lengthbuf = recvall(4)
        if lengthbuf == b"":
            break
        (length,) = struct.unpack("!I", lengthbuf)
        data = recvall(length)
        if data == b"":
            break
        print("<< %s" % data.hex())
        for r in d.call_handlers_for_packet(data, CLIENT):
            m = reply_msg(r)
            print(">> %s %s" % ((struct.pack("!I", len(m.dgram)) + m.dgram).hex(), m))
    print("closed")


def serve_tcp11(d, stream):
    sock = Sock(bytes.fromhex(stream))

    def recvall():
        buf = sock.recv(4096)
        if not buf:
            return []
        while buf[-1] != 192:
            newbuf = sock.recv(4096)
            if not newbuf:
                break
            buf += newbuf
        return [slip.decode(p) for p in buf.split(slip.END_END)]

    while True:
        packets = recvall()
        if not packets:
            break
        for p in packets:
            print("<< %s" % (p.hex() or "(empty)"))
            for r in d.call_handlers_for_packet(p, CLIENT):
                m = reply_msg(r)
                print(">> %s %s" % (slip.encode(m.dgram).hex(), m))
    print("closed")


def main():
    labels = {}
    with open(os.path.join(HERE, "data", "jobs.tsv"), encoding="utf-8") as fh:
        jobs = [ln.split("\t") for ln in fh.read().split("\n") if ln]
    for job in jobs:
        kind, a = job[0], job[1:]
        print("== " + " ".join(job).replace(US, " | "))
        try:
            if kind == "build":
                b = osc_message_builder.OscMessageBuilder(address=addr_of(a[1]))
                for v, t in parse_args(a[2]):
                    b.add_arg(v, t)
                print("args %r" % (b.args,))
                m = b.build()
                print("dgram %s" % m.dgram.hex())
                show_msg(m)
                if a[0] != "-":
                    labels[a[0]] = m
            elif kind == "bmsg":
                if a[1] == "-":
                    m = osc_message_builder.build_msg(addr_of(a[0]))
                else:
                    m = osc_message_builder.build_msg(addr_of(a[0]), parse_args(a[1])[0][0])
                print("dgram %s" % m.dgram.hex())
                show_msg(m)
            elif kind == "parse":
                m = osc_message.OscMessage(b"" if a[0] == "-" else bytes.fromhex(a[0]))
                flush_log()
                show_msg(m)
            elif kind == "bundle":
                bb = osc_bundle_builder.OscBundleBuilder(ts_of(a[1]))
                for lab in (a[2].split(" ") if a[2] else []):
                    bb.add_content(labels[lab])
                bu = bb.build()
                flush_log()
                print("dgram %s" % bu.dgram.hex())
                show_bundle(bu)
                if a[0] != "-":
                    labels[a[0]] = bu
            elif kind == "bparse":
                bu = osc_bundle.OscBundle(bytes.fromhex(a[0]))
                flush_log()
                show_bundle(bu)
            elif kind == "packet":
                CLOCK[0] = float(a[0])
                p = osc_packet.OscPacket(b"" if a[1] == "-" else bytes.fromhex(a[1]))
                flush_log()
                for tm in p.messages:
                    print("at %r" % (tm.time,))
                    show_msg(tm.message, "  ")
            elif kind == "ntp":
                if a[0] == "tontp":
                    print(osc_types.write_date(ts_of(a[1])).hex())
                elif a[0] == "tosys":
                    print(repr(ntp.ntp_to_system_time(b"" if a[1] == "-" else bytes.fromhex(a[1]))))
                else:
                    print(ntp.parse_timestamp(int(a[1])))
            elif kind == "slip":
                data = b"" if a[1] == "-" else bytes.fromhex(a[1])
                if a[0] == "enc":
                    print(slip.encode(data).hex())
                elif a[0] == "dec":
                    print(slip.decode(data).hex() or "(empty)")
                else:
                    print(slip.is_valid(data))
            elif kind == "match":
                d = dispatcher.Dispatcher()
                for m in a[0].split(US):
                    d.map(m, CBS["log"], m)
                print([h.args[0] for h in d.handlers_for_address(a[1])])
            elif kind == "serve":
                d = make_dispatcher(a[2])
                CLOCK[0] = float(a[1])
                if a[0] == "udp":
                    serve_udp(d, a[3])
                elif a[0] == "tcp10":
                    serve_tcp10(d, a[3])
                else:
                    serve_tcp11(d, a[3])
            else:
                raise SystemExit("bad job " + kind)
        except SystemExit:
            raise
        except Exception as e:
            err(e)
        flush_log()


main()
