#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_jsonref: one resolve job per line.

    resolve \t <merge 0|1> \t <json-document>

`jsonref.replace_refs(doc, proxies=False)` returns a deep copy of a JSON
document with every JSON Reference object `{"$ref": "#/pointer"}` replaced by
the data it points at, resolved against the same document (local fragment
refs only). `<merge>` is the `merge_props` flag: when 1, a reference object's
extra keys are merged into the resolved mapping. A document whose reference
cannot be resolved, or that points directly at itself, prints `ERROR: <msg>`
exactly as the library raises it.
"""
import os

# (merge_props flag, json document)
JOBS = [
    # a plain local reference
    (0, '{"a": {"$ref": "#/b"}, "b": 5}'),
    # nested, an array index, and a chained reference
    (0, '{"x": [10, 20, {"$ref": "#/y"}], "y": {"z": {"$ref": "#/x/1"}}}'),
    # JSON-pointer escapes: ~0 is "~", ~1 is "/"
    (0, '{"a~b": 1, "c/d": 2, "r": [{"$ref": "#/a~0b"}, {"$ref": "#/c~1d"}]}'),
    # a percent-encoded space in the pointer
    (0, '{"a b": 7, "r": {"$ref": "#/a%20b"}}'),
    # reference to a whole subtree
    (0, '{"def": {"x": [1, 2, 3]}, "use": {"$ref": "#/def"}}'),
    # two references to the same target
    (0, '{"t": {"n": 1}, "a": {"$ref": "#/t"}, "b": {"$ref": "#/t"}}'),
    # a deep pointer and scalar leaves (bool / null / negative int)
    (0, '{"a": {"b": {"c": true}}, "r": {"$ref": "#/a/b/c"}, "n": null, "k": -3, "m": {"$ref": "#/k"}}'),
    # references inside an array of objects
    (0, '{"tpl": {"kind": "box"}, "items": [{"$ref": "#/tpl"}, {"id": 2}, {"$ref": "#/tpl"}]}'),
    # merge_props ON: extra keys override and extend the resolved mapping
    (1, '{"base": {"a": 1, "b": 2}, "r": {"$ref": "#/base", "b": 99, "c": 3}}'),
    # merge_props OFF: the extra keys on the reference are dropped
    (0, '{"base": {"a": 1}, "r": {"$ref": "#/base", "x": 9}}'),
    # merge_props ON where the resolved value is not a mapping (no merge)
    (1, '{"base": [1, 2], "r": {"$ref": "#/base", "extra": 1}}'),
    # a reference whose target is itself a reference object (resolved through)
    (0, '{"a": {"$ref": "#/b"}, "b": {"$ref": "#/c"}, "c": 42}'),
    # errors
    (0, '{"r": {"$ref": "#/nope"}}'),
    (0, '{"a": [1, 2], "r": {"$ref": "#/a/5"}}'),
    (0, '{"r": {"$ref": "#/r"}}'),
    (0, '{"a": {"b": 1}, "r": {"$ref": "#/a/b/c"}}'),
    # a document with no references at all is returned unchanged
    (0, '{"a": 1, "b": [2, 3], "c": {"d": "e"}}'),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for merge, doc in JOBS:
        fh.write("resolve\t" + str(merge) + "\t" + doc + "\n")
