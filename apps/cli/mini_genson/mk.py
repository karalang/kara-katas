#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one schema-inference job per line. Each line is a
tab-separated list of JSON sample documents; the job feeds them all to one
genson SchemaBuilder (via add_object) and prints the inferred JSON Schema.

Only literal JSON here (no genson import); oracle.py replays each line through
the library to produce expected.out."""

# Each entry is the list of JSON sample documents for one build.
JOBS = [
    # scalars
    ["42"],
    ['"hi"'],
    ["true"],
    ["null"],
    ["3.14"],
    # arrays
    ["[]"],
    ["[1, 2, 3]"],
    ['[1, "a", true]'],
    ["[1, 2.5]"],
    ["[[1, 2], [3]]"],
    # objects
    ["{}"],
    ['{"a": 1, "b": "x"}'],
    # required intersection across two samples
    ['{"a": 1, "b": 2}', '{"a": 3}'],
    # union of keys across samples, required shrinks
    ['{"a": 1, "b": 2, "c": 3}', '{"a": 9, "c": 8}', '{"a": 7}'],
    # nested object + array
    ['{"user": {"id": 1, "name": "x"}, "tags": ["a", "b"]}'],
    # array of objects, required intersection inside items
    ['[{"a": 1}, {"a": 2, "b": 3}]'],
    # a field that changes scalar type -> sorted type list
    ['{"v": 1}', '{"v": "x"}'],
    # null + int on a field -> type list with null
    ['{"v": 1}', '{"v": null}'],
    # a field int here, object there -> anyOf
    ['{"v": 1}', '{"v": {"k": 2}}'],
    # array items mixing scalar and object -> anyOf in items
    ['[1, {"k": "v"}]'],
    # int then float on same field -> number
    ['{"x": 1}', '{"x": 2.0}'],
    # deeper nesting and mixed
    ['{"a": {"b": {"c": [1, 2]}}}', '{"a": {"b": {"c": [3], "d": true}}}'],
    # top-level type varies across samples -> sorted type list
    ["1", '"s"', "true"],
    # object then array at top level -> anyOf
    ['{"a": 1}', "[1, 2]"],
    # escapes in a key and in a value (value content is irrelevant to schema)
    ['{"a\\"b": "line1\\nline2\\ttab"}'],
    # empty nested structures
    ['{"items": [], "meta": {}}'],
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for samples in JOBS:
            fh.write("\t".join(samples) + "\n")


main()
