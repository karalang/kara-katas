#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_immutables: a scripted sequence of operations
on one persistent HAMT, one op per line (tab-separated):

    s \t <k> \t <v>    set key k to value v
    d \t <k>           delete key k   ( prints `miss` if absent )
    g \t <k>           get key k      ( prints the value, or `miss` )
    h \t <k>           has key k      ( prints yes / no )
    l                  the current length
    k                  the keys, in the HAMT's structural iteration order

Keys are non-negative ints; `map_hash` folds a 64-bit hash to 32 bits, so a key
above 2^32 collides with the key equal to its folded hash — those pairs drive
the CollisionNode path. The sequence fills a tree deep enough to branch
(BitmapNode subnodes), updates existing keys (no length change), deletes present
and absent keys, collapses subnodes back to leaves, and snapshots the key order
throughout. `oracle.py` replays it against the vendored immutables.Map.
"""
import os


def map_hash(k):
    return (k & 0xffffffff) ^ ((k >> 32) & 0xffffffff)


ops = []

# Fill 0..33, snapshot length and key order.
for i in range(34):
    ops.append(("s", i, i * 10))
ops.append(("l",))
ops.append(("k",))

# Point queries: present and absent.
for k in [0, 17, 33, 34, 100, 5]:
    ops.append(("g", k))
    ops.append(("h", k))

# Update existing keys (added is False, length unchanged).
for i in [0, 5, 17, 33]:
    ops.append(("s", i, i + 1))
ops.append(("l",))
ops.append(("g", 5))

# Collision keys: k and (k | (hi<<32)) fold to the same 32-bit hash.
coll = []
seen = {}
for lo in [5, 17, 200, 1, 33]:
    for hi in [1, 2, 3]:
        k = (hi << 32) | lo
        coll.append(k)
# also the plain colliders they land with
coll += [5, 17, 200, 1, 33]
# dedupe, keep order
coll = list(dict.fromkeys(coll))
for k in coll:
    ops.append(("s", k, k % 1000))
ops.append(("l",))
ops.append(("k",))
for k in coll[:6]:
    ops.append(("g", k))

# Deletes: present keys, absent keys (miss), and collision members.
for k in [3, 7, 11, 999, 34, coll[0], coll[1], 20, 20]:
    ops.append(("d", k))
    ops.append(("l",))
ops.append(("k",))

# Delete the rest of a collision group to collapse it back to a leaf.
for k in coll:
    ops.append(("d", k))
ops.append(("k",))
ops.append(("l",))

# Final mixed probes.
for k in [0, 1, 2, 15, 33, 500]:
    ops.append(("g", k))

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op in ops:
        fh.write("\t".join(str(x) for x in op) + "\n")
