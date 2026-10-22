#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_pygtrie: a scripted sequence of operations on
one evolving CharTrie (sorted-sibling iteration enabled), one op per line
(tab-separated):

    s  \t <key> \t <val>   set key -> int val         ( prints `len <n>` )
    g  \t <key>            get                        ( prints the value, or `miss` )
    hk \t <key>            has_key                     ( yes / no )
    hs \t <key>            has_subtrie                 ( yes / no )
    hn \t <key>            has_node bit-field          ( 0 / 1 / 2 / 3 )
    d  \t <key>            delete + prune empty nodes   ( `len <n>` | `short` | `miss` )
    lp \t <key>            longest_prefix              ( `<key> <val>` | none )
    sp \t <key>            shortest_prefix             ( `<key> <val>` | none )
    pf \t <key>            prefixes along the path      ( [(k v), ...] | [] )
    ks \t <prefix>         keys(prefix), sorted         ( [k, ...] | nokey )
    ka                     all keys, sorted
    l                      current length

Keys are lowercase ASCII (and the empty string); values are small ints. The set
is built to share prefixes (car/card/care/cart/cat, do/dog/dodge, a/an/and/ant)
so the trie branches into real sub-nodes; `has_node`/`has_subtrie` distinguish a
value node, a prefix-only node, and an absent node; delete exercises the
leaf-prune, the value-on-a-prefix (children kept), the ShortKeyError on a
prefix-only key, and the plain miss; and the key order is snapshotted throughout.
`oracle.py` replays the sequence against the vendored pygtrie.CharTrie.
"""
import os

KEYS = [
    ("", 0),
    ("a", 1), ("an", 2), ("and", 3), ("ant", 4), ("any", 5),
    ("car", 6), ("card", 7), ("care", 8), ("cart", 9), ("cat", 10),
    ("do", 11), ("dog", 12), ("dodge", 13), ("doll", 14),
    ("be", 15), ("bee", 16),
]

ops = []

# Fill, snapshotting length and the full (sorted) key order as the tree grows.
for k, v in KEYS:
    ops.append(("s", k, v))
ops.append(("l",))
ops.append(("ka",))

# Point gets: present, prefix-only (miss), absent.
for k in ["car", "care", "ca", "c", "cab", "", "doll", "zzz"]:
    ops.append(("g", k))

# has_key / has_subtrie / has_node across value, prefix-only and absent nodes.
for k in ["car", "ca", "card", "do", "dodge", "d", "nope", ""]:
    ops.append(("hk", k))
    ops.append(("hs", k))
    ops.append(("hn", k))

# Prefix queries: shortest / longest / full chain, with and without a match.
for k in ["card", "care", "cart", "cat", "a", "and", "ant", "dodge", "xyz"]:
    ops.append(("sp", k))
    ops.append(("lp", k))
    ops.append(("pf", k))

# Update an existing key (value changes, length unchanged).
ops.append(("s", "car", 60))
ops.append(("g", "car"))
ops.append(("l",))

# keys(prefix): a branching prefix, an exact leaf, a prefix-only node, absent.
for p in ["car", "ca", "do", "a", "b", "z"]:
    ops.append(("ks", p))

# Deletes: a leaf that prunes, a value-on-a-prefix (children kept), a
# prefix-only key (ShortKeyError -> short), an absent key (miss), then re-check.
for k in ["cart", "car", "ca", "zzz", "dodge", "do"]:
    ops.append(("d", k))
    ops.append(("l",))
    ops.append(("hn", k))
ops.append(("ka",))

# After the pruning, re-probe the structure that is left.
for k in ["card", "care", "cat", "dog", "doll"]:
    ops.append(("hk", k))
ops.append(("ks", "ca"))
ops.append(("ks", "do"))
ops.append(("lp", "cardboard"))
ops.append(("sp", "cardboard"))

# Delete down the empty-string root value too.
ops.append(("d", ""))
ops.append(("hn", ""))
ops.append(("ka",))
ops.append(("l",))

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op in ops:
        fh.write("\t".join(str(x) for x in op) + "\n")
