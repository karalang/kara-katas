"""LeetCode 271 — Encode and Decode Strings (Python mirror / oracle).

Mirrors encode_decode.kara algorithm-for-algorithm: a decimal byte-length
header terminated by '#', with the payload copied verbatim and reassembled
from BYTES so multi-byte text survives.
"""


def encode(items):
    out = b""
    for s in items:
        b = s.encode()
        out += str(len(b)).encode() + b"#" + b
    return out


def decode(data):
    out = []
    p = 0
    while p < len(data):
        n = 0
        while data[p] != 35:  # '#'
            n = n * 10 + (data[p] - 48)
            p += 1
        p += 1
        out.append(data[p:p + n].decode())
        p += n
    return out


def show(items):
    return "[" + ",".join(f'"{s}"' for s in items) + "]"


def report(items):
    enc = encode(items)
    dec = decode(enc)
    ok = "OK" if show(dec) == show(items) else "ROUND-TRIP FAILED"
    print(f'{show(items)} -> "{enc.decode()}" -> {show(dec)} {ok}')


def main():
    report(["abc", "de"])
    report([])
    report([""])
    report(["", ""])
    report(["a#b", "3#c"])
    report(["12345", "#"])
    report(["2#hi", "x"])
    report(["a,b", "c|d", ",,,"])
    report(["héllo", "wörld", "日本語"])
    report(["z" * 120, "end"])


main()
