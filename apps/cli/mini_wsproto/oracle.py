#!/usr/bin/env python3
"""Runs data/jobs.tsv through wsproto's frame_protocol and prints expected.out.

Each job prints "== " and its fields joined by " | ", then two-space result
lines. A `recv` job prints one line per frame it decodes (or err=<msg>
code=<n> when the protocol raises ParseFailed); a `send` job prints
bytes=<hex> per op.
"""
import sys

sys.path.insert(0, "vendor")

MASK_KEY = b"\x37\xfa\x1c\x8e"
import wsproto.frame_protocol as fp  # noqa: E402

fp.os.urandom = lambda n: MASK_KEY  # deterministic client mask


def tf(b):
    return "T" if b else "F"


def render_frame(frame):
    op = fp.Opcode(frame.opcode)
    head = f"op={op.name} ff={tf(frame.frame_finished)} mf={tf(frame.message_finished)}"
    if op is fp.Opcode.CLOSE:
        code, reason = frame.payload
        return f"{head} code={int(code)} reason={reason.encode('utf-8').hex()}"
    if op is fp.Opcode.TEXT:
        return f"{head} text={frame.payload.encode('utf-8').hex()}"
    # BINARY, PING, PONG
    return f"{head} bin={bytes(frame.payload).hex()}"


def do_recv(role, chunks):
    proto = fp.FrameProtocol(client=(role == "client"), extensions=[])
    out = []
    try:
        for ch in chunks:
            proto.receive_bytes(bytes.fromhex(ch))
            for frame in proto.received_frames():
                out.append(render_frame(frame))
    except fp.ParseFailed as e:
        out.append(f"err={e} code={int(e.code)}")
    return out


def do_send(role, ops):
    proto = fp.FrameProtocol(client=(role == "client"), extensions=[])
    out = []
    for op in ops:
        parts = op.split(" ")
        kind = parts[0]
        if kind == "data":
            t, fin, hexp = parts[1], parts[2] == "1", parts[3] if len(parts) > 3 else ""
            payload = bytes.fromhex(hexp)
            raw = payload.decode("utf-8") if t == "t" else payload
            data = proto.send_data(raw, fin)
        elif kind == "ping":
            data = proto.ping(bytes.fromhex(parts[1]) if len(parts) > 1 else b"")
        elif kind == "pong":
            data = proto.pong(bytes.fromhex(parts[1]) if len(parts) > 1 else b"")
        elif kind == "close":
            code = None if parts[1] == "-" else int(parts[1])
            reason = None if parts[2] == "-" else bytes.fromhex(parts[2]).decode("utf-8")
            data = proto.close(code, reason)
        else:
            raise SystemExit("unknown op: " + kind)
        out.append("bytes=" + bytes(data).hex())
    return out


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        f = line.split("\t")
        out.append("== " + " | ".join(f))
        if f[0] == "recv":
            lines = do_recv(f[1], f[2:])
        elif f[0] == "send":
            lines = do_send(f[1], f[2].split("|"))
        else:
            raise SystemExit("unknown job: " + f[0])
        for r in lines:
            out.append("  " + r)
sys.stdout.write("\n".join(out) + "\n")
