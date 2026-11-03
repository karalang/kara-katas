"""Writes data/ for mini_roaring: a week of product events, three hand-made
.roar files in the portable Roaring format (one valid, with array, bitmap
and run containers, and two that are not), and data/jobs.txt.

Run from this directory: python3 -s -P -B mk.py"""
import os
import random
import struct

os.makedirs("data", exist_ok=True)


def write(name, data):
    mode = "wb" if isinstance(data, bytes) else "w"
    kw = {} if mode == "wb" else {"encoding": "utf-8", "newline": ""}
    with open(os.path.join("data", name), mode, **kw) as fh:
        fh.write(data)


# A week of events. Users live in a few id blocks, as ids handed out by
# shards do: a dense block of early accounts, a block past 65536, a sparse
# block past a million, and a handful of ids near the top of u32.
rnd = random.Random(20261103)
blocks = [(1000, 5200), (70000, 76000), (1_048_576, 1_300_000), (4_294_960_000, 4_294_967_295)]
weights = [5, 3, 2, 1]
users = []
for (lo, hi), w in zip(blocks, weights):
    users += rnd.sample(range(lo, hi + 1), 100 * w)
users.sort()
events = ["view", "signup", "cart", "buy"]
rows = ["day,user,event"]
for day in range(1, 8):
    # Each day a slice of the users shows up; fewer as the week goes on.
    active = [u for u in users if rnd.random() < 0.55 - day * 0.03]
    for u in active:
        r = rnd.random()
        ev = "view" if r < 0.6 else "signup" if r < 0.75 else "cart" if r < 0.92 else "buy"
        rows.append(f"{day},{u},{ev}")
# Rows arrive out of order, as a merged log's do, with a few bad lines.
body = rows[1:]
rnd.shuffle(body)
body.insert(17, "3,notanumber,view")
body.insert(400, "9,1234,view")
body.insert(901, "2,4294967296,view")
body.insert(1200, "4,77,refund")
write("events.csv", rows[0] + "\n" + "\n".join(body) + "\n")


def serialize(containers, with_offsets=None):
    """containers: list of (key, kind, payload) with kind array (sorted
    lows), bitmap (set of lows) or run (list of (start, len-1))."""
    n = len(containers)
    hasrun = any(k == "run" for _, k, _ in containers)
    out = bytearray()
    if hasrun:
        out += struct.pack("<I", 12347 | ((n - 1) << 16))
        bits = bytearray((n + 7) // 8)
        for i, (_, k, _) in enumerate(containers):
            if k == "run":
                bits[i // 8] |= 1 << (i % 8)
        out += bits
    else:
        out += struct.pack("<II", 12346, n)
    bodies = []
    for key, kind, p in containers:
        if kind == "array":
            card = len(p)
            body = b"".join(struct.pack("<H", v) for v in p)
        elif kind == "bitmap":
            card = len(p)
            words = [0] * 1024
            for v in p:
                words[v >> 6] |= 1 << (v & 63)
            body = b"".join(struct.pack("<Q", w) for w in words)
        else:
            card = sum(l + 1 for _, l in p)
            body = struct.pack("<H", len(p)) + b"".join(struct.pack("<HH", s, l) for s, l in p)
        out += struct.pack("<HH", key, card - 1)
        bodies.append(body)
    if with_offsets is None:
        with_offsets = (not hasrun) or n >= 4
    if with_offsets:
        pos = len(out) + 4 * n
        for b in bodies:
            out += struct.pack("<I", pos)
            pos += len(b)
    for b in bodies:
        out += b
    return bytes(out)


good = serialize([
    (0, "array", [1, 2, 3, 100, 1000, 65535]),
    (1, "run", [(0, 99), (200, 0), (65000, 535)]),
    (5, "bitmap", set(range(0, 20000, 3))),
    (65535, "run", [(65530, 5)]),
])
write("shipped.roar", good)
write("bad_cookie.roar", b"\x3b\x31\x00\x00" + good[4:])
write("truncated.roar", good[:-700])
unsorted = serialize([(3, "array", [5, 6]), (2, "array", [7])])
write("unsorted.roar", unsorted)

jobs = """\
# A week of product events, as the analytics job reads them.
load events.csv
show d1
stats d1
and both d1 d2
show both
retention d1 d2
retention d1 d7
andnot churn d1 d7
stats churn
or week d1 d2 d3 d4 d5 d6 d7
stats week
and funnel e_signup e_cart e_buy
show funnel
jaccard d1 d2
jaccard d6 d7
xor odd d1 d2
equal odd both
# Ranges: a run container per empty chunk, then back to array or bitmap
addrange blk 65536 140000
stats blk
show blk
add blk 3 70000 4294967295 70000
remove blk 65536 9
show blk
optimize blk
stats blk
removerange blk 100000 131072
show blk
optimize blk
stats blk
# The array/bitmap boundary at 4096
addrange t 0 4096
stats t
remove t 5
stats t
add t 5
stats t
add t 4096
stats t
add t 70000
stats t
remove t 0 1
stats t
optimize t
stats t
# rank and select
rank week 0
rank week 70000
rank week 4294967295
select week 0
select week 1000
select week 99999
contains week 1000 1001 4294967295
flip f 10 20
flip f 15 70000
stats f
show f
flip f 0 200000
stats f
rank f 4294967295
select f 150000
flip f 4294967290 4294967296
show f
# The portable format: written, dumped, read back
addrange small 10 13
add small 1000 65536 131071
hexdump small
optimize small
hexdump small
save small small.roar
loadroar small2 small.roar
equal small small2
save week week.roar
loadroar week2 week.roar
equal week week2
stats week2
optimize week
save week week_opt.roar
loadroar week3 week_opt.roar
stats week3
equal week week3
and empty d1 nosuch
or empty
stats empty
hexdump empty
save empty empty.roar
loadroar empty2 empty.roar
stats empty2
# Files another implementation wrote
loadroar shipped shipped.roar
show shipped
stats shipped
hexdump shipped
save shipped shipped_again.roar
loadroar bad bad_cookie.roar
loadroar bad truncated.roar
loadroar bad unsorted.roar
loadroar bad missing.roar
# Mistakes
show nosuch
add t 4294967296
add t -1
addrange t 5 x
frobnicate t
select t
"""
write("jobs.txt", jobs)
