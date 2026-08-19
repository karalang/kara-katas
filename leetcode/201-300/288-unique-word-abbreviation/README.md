# 288. Unique Word Abbreviation

Abbreviate a word as **first letter + middle length + last letter**, so `deer`
becomes `d2r` and `internationalization` becomes `i18n`. A word of two
characters or fewer has no middle to shrink and abbreviates to *itself* — the
encoding would otherwise be longer than the word.

Build a dictionary once, then answer `is_unique(word)` many times. The word is
unique when **no** dictionary word shares its abbreviation, **or** when every
dictionary word that shares it *is that same word*.

```
dictionary = ["deer", "door", "cake", "card"]

is_unique("dear")  ->  false    "d2r" is also "deer", and "deer" != "dear"
is_unique("cart")  ->  true     "c2t" belongs to nobody
is_unique("cane")  ->  false    "c2e" is "cake"
is_unique("cake")  ->  true     "c2e" is "cake" — which IS the word asked about
```

## Approaches

| file | index | build | query |
|---|---|---|---|
| `unique_word_abbr.kara` ★ | `Map[String, Bucket]` — `Sole(word)` \| `Conflicted` | O(n·w) | O(w) |
| `unique_word_abbr_buckets.kara` | `Map[String, Vec[String]]` — every distinct colliding word | O(n·w·c) | O(w) |
| `unique_word_abbr_counts.kara` | `Map[String, i64]` + `Set[String]` | O(n·w) | O(w) |
| `unique_word_abbr_brute.kara` | none — the predicate, transcribed | — | O(n·w) |
| `differential.kara` | 3600 queries, four solvers, three density axes | — | — |

`n` is the dictionary size, `w` the word length, `c` a bucket's width.

## The index is a three-way choice

Per abbreviation the dictionary is in exactly one of three states: nothing has
it, exactly one distinct word has it, or two or more do. Only the middle state
needs to remember anything, so the ★ file writes:

```kara
enum Bucket {
    Sole(String),
    Conflicted,
}
```

with "nothing has it" left to the map's own absence. Once two distinct words
collide, *which* words they were stops mattering — no later query can be
answered differently by knowing them — so `Conflicted` carries no payload and
the strings are dropped. `unique_word_abbr_buckets.kara` keeps every colliding
word alive to support an answer that was already decided; that is the honest
cost of the obvious first index.

The bucket-list file earns its place elsewhere: it is the only one that can
still answer **which** words collide, so `collisions_of` there is a real
function rather than one needing a re-scan.

## The trap is duplicates

The dictionary is a **multiset on input** and a **set in meaning**. Given
`["deer", "deer"]`, `is_unique("deer")` is **true** — the only word abbreviating
to `d2r` is `deer` itself. An index that counts *occurrences* rather than
*distinct words* reads 2 and answers false.

Each file pays for this differently, and each payment is a place to get it
wrong:

- ★ compares `prev != w` before promoting `Sole` to `Conflicted`.
- buckets guards its push with `contains` — the bucket is a *set* that happens
  to be stored as a list.
- counts bumps only on a word its `Set` had not yet seen, so the guard **is**
  the set insert and there is no separate check to forget.
- brute force cannot get it wrong at all: it excludes `d == word` on every
  occurrence, so a repeat behaves like a single entry without anything having
  to deduplicate it.

That last property is why the brute-force file is the differential's reference.
It has no representation to be wrong about — the other three pre-compute an
index and then *argue* the index preserves the predicate.

## Verifying it

`differential.kara` runs all four against 3600 queries over three axes —
alphabet size, dictionary size, and word length — and reports its own coverage
rather than just a pass:

```
cases 3600
mismatches 0
dictionaries 360, of which with a repeated word 140
answers true 3202, false 398
```

The coverage lines are the point. A differential that reports zero mismatches
while never building a dictionary with a repeat, or while every answer comes
back the same, has proved nothing. Word **length** is the axis that controls how
hard the abbreviation squeezes: a 1–2 character word abbreviates to itself and
can only collide by being equal, while a 5-character word over a 2-letter
alphabet has just four possible abbreviations. Both regimes are generated,
because the short one is the only thing that exercises the `n <= 2` branch.

It is also mutation-tested. Breaking the duplicate guard in any one of the three
indexes — `contains` in buckets, `prev != w` in ★, the `Set` insert in counts —
produces **582 mismatches**, with the differential naming the broken solver
while the other three agree.

## What this kata found

`Set.contains(w)` with `w: ref String` was rejected by the typechecker:
*expected 'String', found 'ref String'* — against a spec (design.md § Set) that
reads `fn contains(ref self, val: ref T) -> bool`.

The rule had already been established: `B-2026-08-15-22` fixed exactly this for
`Vec`/`VecDeque`, on the grounds that *a probe scans for its needle and never
keeps it, so a borrowed needle is exactly as usable as an owned one*. That fix
was inlined at the two arms it was reported against and never swept sideways, so
four more probes — `Set.contains`, `SortedSet.contains`, both `remove`s, and
both `binary_search`es — kept comparing raw types and rejecting a `ref`, each
against its own written signature.

The cause was structural: the set arms grouped `"contains" | "insert" | "remove"`
into one match arm, so the probes inherited `insert`'s ownership requirement —
and `insert` genuinely does store its argument (`val: T`), so the grouping had
to be split rather than patched. Filed and fixed as `B-2026-08-19-19`.

The benchmark surfaced a second gap, `B-2026-08-19-20`: **`String` has no O(1)
indexed character access.** Every mirror language spells first-and-last in
constant time (`w[0]` / `w[-1]`); Kara's String offers only a `chars()`
iterator, so the natural phrasing allocates a whole `Vec[char]` to read two
characters. Deleting that allocation — walking `chars()` once and tracking
first/last in flight — is worth **1.30× ± 0.18** (274.6 ms → 212.0 ms) on the
bench below.

That does *not* account for the whole gap: Kara is 2.76× slower than Go here,
and the allocation closes only part of it. The rest is undiagnosed — plausibly
String hashing and the per-query abbreviation construction, but that has not
been measured and is not claimed.

## Benchmarks

Container x86_64, 3000-word dictionary built once, then 1M `is_unique` punches
over a 20k-word pool. All five implementations agree on the sink (`unique
573650`). Numbers are from `bench/results.container-x86.json` — the canonical
`results.json` holds Apple-silicon figures and is deliberately not overwritten
from this host.

| | relative |
|---|---|
| go | 1.00 (fastest) |
| c | 1.04 ± 0.06 |
| c (`-march=x86-64-v3`) | 1.03 ± 0.07 |
| rust (`-C overflow-checks=on`, equal-safety) | 1.26 ± 0.11 |
| rust (`-O`) | 1.29 ± 0.11 |
| **kara** | **2.76 ± 0.21** |

The equal-safety row is the honest comparison: Kāra checks integer overflow by
default and `rustc -O` silently wraps, so the `overflow-checks=on` twin is the
like-for-like one. See `BENCHMARKS.md` for the full methodology.

Run-to-run variance in a shared container is real — an earlier run of this same
bench ranked C ahead of Go — so treat the sub-10% separations as noise and only
the Kāra gap as signal.
