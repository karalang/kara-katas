"""LeetCode 271 — differential harness (Python mirror / oracle).

Mirrors differential.kara draw-for-draw: the same LCG, the same order of seed
advances, the same weighted byte draws, so the printed digest must match byte
for byte.
"""

MASK = 2147483647
DIGEST_MOD = 1000000007


def show(items):
    return "[" + ",".join(f'"{s}"' for s in items) + "]"


def enc_hash(items):
    out = b""
    for s in items:
        b = s.encode()
        out += str(len(b)).encode() + b"#" + b
    return out


def dec_hash(data):
    out, p = [], 0
    while p < len(data):
        n = 0
        while data[p] != 35:
            n = n * 10 + (data[p] - 48)
            p += 1
        p += 1
        out.append(data[p:p + n].decode())
        p += n
    return out


def enc_fixed(items):
    out = b""
    for s in items:
        b = s.encode()
        out += str(len(b)).zfill(8).encode() + b
    return out


def dec_fixed(data):
    out, p = [], 0
    while p < len(data):
        n = int(data[p:p + 8])
        p += 8
        out.append(data[p:p + n].decode())
        p += n
    return out


def enc_esc(items):
    out = bytearray()
    for s in items:
        out.append(59)
        for b in s.encode():
            if b == 59:
                out += b"\;"
            elif b == 92:
                out += b"\\\\"
            else:
                out.append(b)
    return bytes(out)


def dec_esc(data):
    out, raw, started, p = [], bytearray(), False, 0
    while p < len(data):
        b = data[p]
        if b == 59:
            if started:
                out.append(raw.decode())
                raw = bytearray()
            started = True
            p += 1
        elif b == 92:
            raw.append(data[p + 1])
            p += 2
        else:
            raw.append(b)
            p += 1
    if started:
        out.append(raw.decode())
    return out


def main():
    cases = 4000
    seed = 271271

    fail_hash = fail_fixed = fail_esc = 0
    had_sep = had_backslash = had_hash = had_empty = had_multibyte = 0
    total_bytes = digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & MASK
        m = (seed // 65536) % 5

        items = []
        saw_sep = saw_bs = saw_hash = saw_empty = saw_mb = False

        for _w in range(m):
            seed = (seed * 1103515245 + 12345) & MASK
            ln = (seed // 65536) % 6
            raw = bytearray()
            for _p in range(ln):
                seed = (seed * 1103515245 + 12345) & MASK
                pick = (seed // 65536) % 10
                if pick == 0:
                    raw.append(59); saw_sep = True
                if pick == 1:
                    raw.append(92); saw_bs = True
                if pick == 2:
                    raw.append(35); saw_hash = True
                if pick == 3:
                    raw.append(48 + (seed // 4096) % 10)
                if pick == 4:
                    raw.append(195); raw.append(169); saw_mb = True
                if pick >= 5:
                    raw.append(97 + (seed // 4096) % 26)
            if len(raw) == 0:
                saw_empty = True
            total_bytes += len(raw)
            items.append(bytes(raw).decode())
        if m == 0:
            saw_empty = True

        want = show(items)
        if show(dec_hash(enc_hash(items))) != want:
            fail_hash += 1
        if show(dec_fixed(enc_fixed(items))) != want:
            fail_fixed += 1
        if show(dec_esc(enc_esc(items))) != want:
            fail_esc += 1

        had_sep += saw_sep
        had_backslash += saw_bs
        had_hash += saw_hash
        had_empty += saw_empty
        had_multibyte += saw_mb

        for ch in want.encode():
            digest = (digest * 31 + ch) % DIGEST_MOD

    apart = 0
    if enc_hash([]) != enc_hash([""]):
        apart += 1
    if enc_fixed([]) != enc_fixed([""]):
        apart += 1
    if enc_esc([]) != enc_esc([""]):
        apart += 1

    print(f"cases {cases}")
    print(f"payload bytes {total_bytes}")
    print(f"lists containing ';' {had_sep}")
    print(f"lists containing '\\' {had_backslash}")
    print(f"lists containing '#' {had_hash}")
    print(f"lists containing multi-byte {had_multibyte}")
    print(f"lists with an empty element or no elements {had_empty}")
    print(f'codecs keeping [] and [""] distinct {apart} of 3')
    print(f"digest {digest}")
    print(f"round-trip failures: hash {fail_hash} fixed {fail_fixed} escape {fail_esc}")


main()
