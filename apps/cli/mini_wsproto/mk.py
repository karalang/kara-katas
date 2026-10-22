#!/usr/bin/env python3
"""Writes data/jobs.tsv: WebSocket frame-protocol operations that both
oracle.py and the Kara port run through wsproto's frame_protocol.

Two job kinds, one tab-separated line each; field 0 names the kind.

  recv  <role> <hexchunk> [<hexchunk> ...]
        Make a FrameProtocol for that role (client|server), feed each hex
        chunk with a separate receive_bytes() call (so a frame split across
        reads exercises the buffer and the masker's key rotation), then drain
        received_frames(). Prints one line per frame, or err=<msg> code=<n>.

  send  <role> <op>|<op>|...
        Make a FrameProtocol for that role and run each op in turn on it
        (ops share the protocol, so a data/fin=0 op starts a message the next
        op continues). Each op prints bytes=<hex>. An op is space-separated:
          data <t|b> <0|1> <payloadhex>   send_data (t=text, utf-8 hex)
          ping <payloadhex>               ping
          pong <payloadhex>               pong
          close <code|-> <reasonhex|->    close

Client serialization masks with a random 4-byte key; os.urandom is pinned to
one fixed key (MASK_KEY below) in both the oracle and the port so the masked
bytes are reproducible. The decode path still exercises XorMaskerSimple with
real multi-chunk key rotation.
"""
import os
import struct

os.makedirs("data", exist_ok=True)

import sys
sys.path.insert(0, "vendor")

MASK_KEY = b"\x37\xfa\x1c\x8e"
import wsproto.frame_protocol as fp
fp.os.urandom = lambda n: MASK_KEY  # deterministic client mask


def hx(b):
    return b.hex()


def build(role_client, op, payload=b"", fin=True):
    """Serialize one frame with a throwaway protocol of the given role."""
    p = fp.FrameProtocol(client=role_client, extensions=[])
    if op == "text":
        return bytes(p.send_data(payload.decode("utf-8"), fin))
    if op == "binary":
        return bytes(p.send_data(payload, fin))
    if op == "ping":
        return bytes(p.ping(payload))
    if op == "pong":
        return bytes(p.pong(payload))
    raise ValueError(op)


def frame_bytes(opcode, payload, fin=True, mask=None, rsv=0):
    """Hand-build a raw frame (for cases the library would not emit)."""
    b0 = (0x80 if fin else 0) | (rsv << 4) | opcode
    n = len(payload)
    if n <= 125:
        lenbytes = bytes([n])
    elif n <= 0xFFFF:
        lenbytes = bytes([126]) + struct.pack("!H", n)
    else:
        lenbytes = bytes([127]) + struct.pack("!Q", n)
    body = payload
    if mask is not None:
        lenbytes = bytes([lenbytes[0] | 0x80]) + lenbytes[1:]
        body = bytes(a ^ mask[i % 4] for i, a in enumerate(payload))
        return bytes([b0]) + lenbytes + mask + body
    return bytes([b0]) + lenbytes + body


def mask_payload(payload, key):
    return bytes(a ^ key[i % 4] for i, a in enumerate(payload))


jobs = []


def recv(role, *chunks):
    jobs.append("recv\t" + role + "\t" + "\t".join(chunks))


def send(role, ops):
    jobs.append("send\t" + role + "\t" + "|".join(ops))


# ---- recv: a server decoding masked client frames -------------------------
K = MASK_KEY
# single text, single binary, ping, pong, empty text
recv("server", hx(frame_bytes(0x1, b"hello", mask=K)))
recv("server", hx(frame_bytes(0x2, bytes(range(8)), mask=K)))
recv("server", hx(frame_bytes(0x9, b"pingpong", mask=K)))
recv("server", hx(frame_bytes(0xA, b"", mask=K)))
recv("server", hx(frame_bytes(0x1, b"", mask=K)))
# multibyte text (snowman + accented)
recv("server", hx(frame_bytes(0x1, "héllo ☃ \U0001f600".encode(), mask=K)))
# a 200-byte binary (two-byte length)
recv("server", hx(frame_bytes(0x2, bytes((i * 7) & 0xFF for i in range(200)), mask=K)))

# ---- recv: a client decoding unmasked server frames -----------------------
recv("client", hx(frame_bytes(0x1, b"from server")))
recv("client", hx(frame_bytes(0x2, b"\xde\xad\xbe\xef")))

# ---- recv: fragmentation (text in two data frames + continuation) ---------
# server receiving: fin=0 TEXT "Hel", fin=1 CONT "lo!"
f1 = frame_bytes(0x1, mask_payload(b"Hel", K), fin=False, mask=None)  # need mask flag
f1 = frame_bytes(0x1, b"Hel", fin=False, mask=K)
f2 = frame_bytes(0x0, b"lo!", fin=True, mask=K)
recv("server", hx(f1), hx(f2))
# binary fragmented three ways
b1 = frame_bytes(0x2, b"\x01\x02", fin=False, mask=K)
b2 = frame_bytes(0x0, b"\x03\x04", fin=False, mask=K)
b3 = frame_bytes(0x0, b"\x05", fin=True, mask=K)
recv("server", hx(b1), hx(b2), hx(b3))
# a ping interleaved is illegal between fragments? No: control frames may
# interleave. fin=0 TEXT, then PING, then CONT fin=1.
recv("server", hx(frame_bytes(0x1, b"ab", fin=False, mask=K)),
     hx(frame_bytes(0x9, b"hi", mask=K)),
     hx(frame_bytes(0x0, b"cd", fin=True, mask=K)))

# ---- recv: one frame split across receive_bytes (masker rotation) ---------
full = frame_bytes(0x2, bytes((i * 3) & 0xFF for i in range(20)), mask=K)
recv("server", hx(full[:7]), hx(full[7:11]), hx(full[11:]))
# text split mid-codepoint across reads: "ab☃cd" split inside snowman
t = frame_bytes(0x1, "ab☃cd".encode(), mask=K)
# header is 2 + 4(mask) = 6 bytes; payload "ab"=2, snowman=3, "cd"=2 → 7 bytes
recv("server", hx(t[:6 + 3]), hx(t[6 + 3:]))

# ---- recv: close frames ---------------------------------------------------
recv("server", hx(frame_bytes(0x8, struct.pack("!H", 1000) + b"bye", mask=K)))
recv("server", hx(frame_bytes(0x8, struct.pack("!H", 1001), mask=K)))
recv("server", hx(frame_bytes(0x8, b"", mask=K)))  # no status -> 1005
recv("server", hx(frame_bytes(0x8, struct.pack("!H", 3000) + b"app", mask=K)))
recv("server", hx(frame_bytes(0x8, struct.pack("!H", 4999), mask=K)))

# ---- recv: error paths ----------------------------------------------------
recv("server", hx(frame_bytes(0x3, b"x", mask=K)))                 # bad opcode 0x3
recv("client", hx(frame_bytes(0x1, b"x", mask=K)))                 # client gets masked
recv("server", hx(frame_bytes(0x1, b"x")))                         # server gets unmasked
recv("server", hx(frame_bytes(0x9, b"x" * 126, mask=K)))           # control too long
recv("server", hx(frame_bytes(0x8, struct.pack("!H", 999), mask=K)))   # close code 999
recv("server", hx(frame_bytes(0x8, struct.pack("!H", 1005), mask=K)))  # local-only 1005
recv("server", hx(frame_bytes(0x8, struct.pack("!H", 2000), mask=K)))  # reserved unknown
recv("server", hx(frame_bytes(0x8, b"\x03", mask=K)))              # 1-byte close
recv("server", hx(frame_bytes(0x1, b"\xff\xfe", mask=K)))          # invalid utf-8 text
recv("server", hx(frame_bytes(0x8, struct.pack("!H", 1000) + b"\xff", mask=K)))  # bad reason
# fragmented control frame (fin=0 on a ping) -> illegal
recv("server", hx(frame_bytes(0x9, b"x", fin=False, mask=K)))
# unexpected CONTINUATION with no message open
recv("server", hx(frame_bytes(0x0, b"orphan", mask=K)))
# two-byte length used when one would do (126 with len<=125)
recv("server", "81fe007d" + "11223344" + "00" * 125)  # fin+text, 126, len=125, masked
# reserved bit set with no extension
recv("server", hx(frame_bytes(0x1, b"x", mask=K, rsv=0x4)))
# 8-byte length when 2 would do
recv("server", "82ff0000000000000005" + "11223344" + "0000000000")

# ---- send: server serialization (unmasked) --------------------------------
send("server", ["data t 1 " + hx("hi there".encode())])
send("server", ["data b 1 " + hx(b"\x00\x01\x02\xff")])
send("server", ["ping " + hx(b"ping!")])
send("server", ["pong " + hx(b"")])
send("server", ["close 1000 " + hx(b"done")])
send("server", ["close 1001 -"])
send("server", ["close - -"])          # no code
send("server", ["close 1005 -"])       # NO_STATUS_RCVD -> no payload
send("server", ["close 1006 -"])       # ABNORMAL -> remapped to 1000
# multibyte text
send("server", ["data t 1 " + hx("héllo ☃".encode())])
# a 300-byte binary -> two-byte length
send("server", ["data b 1 " + hx(bytes((i * 5) & 0xFF for i in range(300)))])
# fragmented message: text fin=0 then continuation fin=1
send("server", ["data t 0 " + hx(b"Hel"), "data t 1 " + hx(b"lo")])
# close with a long reason that gets truncated to 123 bytes
send("server", ["close 1000 " + hx(("x" * 200).encode())])

# ---- send: client serialization (masked with the fixed key) ---------------
send("client", ["data t 1 " + hx("hi there".encode())])
send("client", ["data b 1 " + hx(b"\x00\x01\x02\xff")])
send("client", ["ping " + hx(b"ping!")])
send("client", ["close 1000 " + hx(b"done")])
send("client", ["data t 1 " + hx("héllo ☃".encode())])
send("client", ["data b 1 " + hx(bytes((i * 5) & 0xFF for i in range(300)))])

with open("data/jobs.tsv", "w") as f:
    f.write("\n".join(jobs) + "\n")

print("jobs:", len(jobs))
