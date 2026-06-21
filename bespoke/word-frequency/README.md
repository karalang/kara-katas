# Word-frequency report (bespoke kata)

Count word occurrences in a text, then print an **ascending-by-word** report of
the counts. The canonical hash-histogram problem — every language has a one-liner
for it, and the shape (tokenize → tally → ordered report) exercises a language's
map, string, and sort surfaces all at once.

```
the quick brown fox the lazy dog the QUICK fox the the Brown
        │
        ▼  to_lowercase + split + trim
  the the quick quick brown brown fox fox lazy dog the the
        │
        ▼  *m.entry(w).or_insert(0) += 1     (write-through histogram)
  {the:5, quick:2, brown:2, fox:2, lazy:1, dog:1}
        │
        ▼  keys() + sort(),  counts via get_or
  -- frequency (ascending) --
  brown 2
  dog 1
  fox 2
  lazy 1
  quick 2
  the 5
  top the 5
  fox-after-bonus 12
```

## What it exercises

This kata is a **dogfooding probe** for a cluster of recently-landed Kāra
compiler features — it's the natural single program that uses them together:

| Idiom | Feature |
|---|---|
| `*m.entry(w).or_insert(0) += 1` | `Map.entry(k).or_insert(d)` write-through (the `mut ref V` contract) |
| `for w in words { …entry(w)… }` | moving a heap **for-loop element** into an owning sink (deep-copied) |
| `m.get_or(k, 0)` | `Map.get_or(k, default) -> V` |
| `m.keys()` + `keys.sort()` | `Map.keys() -> Vec[String]` (owned) + `Vec[String].sort()` |
| `m.entry(k).and_modify(\|v\| …)` | in-place modify of an existing entry |
| `raw.to_lowercase()`, `.split(" ")`, `.trim()` | the String surface |

Several of those were compiler gaps fixed while writing this kata (see the karac
bug-ledger entries `B-2026-06-20-8` entry/get_or write-through, `-9` map-key
no-adopt ownership, `-11` `keys().sort()` ordered-report codegen, `-13` heap
for-loop element moved into a retaining sink). A fourth, `-16`, is subtler and
specific to this shape: the statement-level **auto-parallelizer** raced the
histogram loop against the later `freq.keys()` read, because the write through
`*m.entry(w).or_insert(0)` wasn't recognized as a write to `m` — so the default
`karac build` could silently diverge from `karac run`. The point of the kata is
that the **same source runs identically** on both backends, including under the
default auto-par build.

## A/B parity (the actual test)

`karac run` (tree-walking interpreter) and `karac build` (LLVM codegen) must
print **byte-identical** output:

```bash
karac run word_frequency.kara                 > /tmp/a.txt
karac build word_frequency.kara && ./word_frequency > /tmp/b.txt
diff /tmp/a.txt /tmp/b.txt && echo "A/B identical"
```

## Notes

- The ascending report uses `keys() + sort()` rather than a `SortedMap` because
  `SortedMap` is **interpreter-only in codegen v1** (no B-tree runtime yet), so
  it would not be A/B-portable. `keys() + sort()` is the equally-canonical form.
- `keys` is annotated `let keys: Vec[String]` so codegen's `.sort()` sees the
  String element type — inferring it from `keys()` is a minor open type-inference
  follow-up.
- Kāra-first kata: the C/Rust/Go/Python mirrors and the `bench/` harness used by
  the rest of the corpus are a deliberate follow-up; this kata's job today is the
  A/B compiler check, not the cross-language benchmark.
