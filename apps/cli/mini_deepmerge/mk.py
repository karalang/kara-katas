#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_deepmerge: one merge job per line.

    merge \t <merger> \t <base-value> \t <nxt-value>

<merger> names one of the strategy configurations defined in merger_cfg.py
(shared verbatim with oracle.py and mirrored in mini_deepmerge.kara):

  always        list append, dict merge, set union, fallback/conflict override
                (deepmerge.always_merger)
  conservative  as always but fallback/conflict use_existing
                (deepmerge.conservative_merger)
  raise         as always but NO fallback/conflict strategy -> raises on a
                scalar merge or a type conflict (deepmerge.merge_or_raise)
  prepend       list prepend instead of append
  unique        list append_unique (dedup by equality, dicts included)
  intersect     set intersect instead of union
  setoverride   set override (take nxt's set)
  ifnotempty    type-conflict override_if_not_empty (None/empty keeps base)

Values use a tiny JSON-with-sets grammar (the same grammar the merged result
is serialized back into): null / true / false / integers / "strings" /
[lists] / {"k": v} dicts / <sets>. A job the merger would raise on prints
RAISE.
"""
import os

# (merger, base, nxt)
JOBS = [
    # dict merge: recurse; lists append, nested dicts merge, new keys appended
    ("always", '{"a": [1, 2], "b": {"x": 1}}', '{"a": [2, 3], "b": {"y": 2}, "c": 5}'),
    # scalar at a shared key -> fallback: override vs use_existing
    ("always", '{"a": 1}', '{"a": 2}'),
    ("conservative", '{"a": 1}', '{"a": 2}'),
    # type conflict at a shared key (int vs string)
    ("always", '{"a": 1}', '{"a": "s"}'),
    ("conservative", '{"a": 1}', '{"a": "s"}'),
    # top-level list append / prepend
    ("always", '[1, 2]', '[3, 4]'),
    ("prepend", '[1, 2]', '[3, 4]'),
    # append_unique: scalars and whole dicts deduplicated
    ("unique", '[1, 2, 3]', '[2, 3, 4]'),
    ("unique", '[{"a": 1}]', '[{"a": 1}, {"b": 2}]'),
    # sets: union / intersect / override
    ("always", '<1, 2>', '<2, 3>'),
    ("intersect", '<1, 2, 3>', '<2, 3, 4>'),
    ("setoverride", '<1, 2>', '<3, 4>'),
    # set of strings, union (serialized sorted -> deterministic)
    ("always", '<"b", "a">', '<"c", "a">'),
    # merge_or_raise: succeeds when nothing combines two scalars / conflicts
    ("raise", '{"a": [1]}', '{"a": [2], "b": 3}'),
    ("raise", '{"a": 1}', '{"b": 2}'),
    # merge_or_raise: raises on a shared scalar key (fallback empty)
    ("raise", '{"a": 1}', '{"a": 2}'),
    # merge_or_raise: raises on a top-level type conflict
    ("raise", '1', '"s"'),
    # override_if_not_empty across the type-conflict path
    ("ifnotempty", '5', '0'),
    ("ifnotempty", '5', 'null'),
    ("ifnotempty", '5', '"s"'),
    ("ifnotempty", '[1]', '{}'),
    ("ifnotempty", '5', '[]'),
    ("ifnotempty", 'false', 'true'),
    # deeper nesting: list of dicts appended, inner dicts untouched
    ("always", '{"pkgs": [{"n": "a"}], "env": {"p": "3"}}',
     '{"pkgs": [{"n": "b"}], "env": {"q": "4"}, "ci": true}'),
    # set nested inside a dict, unioned
    ("always", '{"tags": <"x">}', '{"tags": <"y", "x">}'),
    # dict override strategy via a config that overrides dicts wholesale
    ("prepend", '{"a": {"x": 1}}', '{"a": {"y": 2}}'),
    # null handling: fallback override replaces null, use_existing keeps it
    ("always", '{"a": null}', '{"a": 7}'),
    ("conservative", '{"a": null}', '{"a": 7}'),
    # empty base dict gains everything
    ("always", '{}', '{"a": 1, "b": [2]}'),
    # string values conflict -> fallback (same type) override
    ("always", '{"name": "old"}', '{"name": "new"}'),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for merger, base, nxt in JOBS:
        fh.write("merge\t" + merger + "\t" + base + "\t" + nxt + "\n")
