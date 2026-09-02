# 304. Range Sum Query 2D — Immutable

Build a structure over a fixed integer matrix, then answer many
`sum_region(row1, col1, row2, col2)` queries — the sum of the rectangle whose
upper-left corner is `(row1, col1)` and lower-right corner is `(row2, col2)`,
inclusive on all four sides. The matrix never changes.

```
[3, 0, 1, 4, 2]
[5, 6, 3, 2, 1]
[1, 2, 0, 1, 5]     sum_region(2, 1, 4, 3) ->  8
[4, 1, 0, 1, 7]     sum_region(1, 1, 2, 2) -> 11
[1, 0, 3, 0, 5]     sum_region(1, 2, 2, 4) -> 12
```

## Approaches

| file | mechanism | build | query |
|---|---|---|---|
| `range_sum_query_2d.kara` ★ | 2D prefix table, nested `Vec[Vec[i64]]` — inclusion–exclusion | O(hw) | O(1) |
| `range_sum_query_2d_flat.kara` | same arithmetic, one flat `Vec[i64]` + stride | O(hw) | O(1) |
| `range_sum_query_2d_rows.kara` | per-row 1D prefixes — add disjoint row-slices | O(hw) | O(h) |
| `range_sum_query_2d_brute.kara` | walk the rectangle, the definition verbatim | O(1) | O(area) |
| `differential.kara` | 1,920 matrices, **every** rectangle, four arms, seven properties | — | — |
| `bench/rangesum2d.kara` | 257×257 table × 100,000 rectangles × 1,800 passes | — | — |

This is #303 one dimension up, and the extra dimension is not decoration: it
turns a two-term subtraction into a four-term signed combination, and it lets
the same algorithm be written over two genuinely different memory layouts.
Both of those turned out to matter.

### Inclusion–exclusion, and the sign that is the whole problem

`pre[r][c]` holds the sum of every cell strictly above and strictly left of
`(r, c)` — the rectangle anchored at the origin. Four of those origin-rectangles
combine into any rectangle at all:

```
sum(r1..r2, c1..c2) = pre[r2+1][c2+1]   the big block, origin to corner
                    - pre[r1  ][c2+1]   minus the strip above it
                    - pre[r2+1][c1  ]   minus the strip left of it
                    + pre[r1  ][c1  ]   plus the corner, subtracted twice
```

That final `+` is the entire idea. The top-left corner block lies inside *both*
strips, so subtracting each strip removes it twice and it has to be paid back
once. The build has the same shape: each cell folds in its two neighbouring
origin-rectangles, removes their shared overlap, and adds its own value.

As in #303, the table is `(h+1) × (w+1)` with a zero row and column, so a query
touching row 0 or column 0 reads a real zero instead of branching.

### Four arms that cannot make each other's mistakes

Arms **A** and **B** share their mathematics exactly and differ only in memory
layout, so a disagreement between *them* is a fault in an access path, not in
the algorithm. Arm **C** shares nothing with either: it adds disjoint row-slices
where they subtract overlapping origin-rectangles, so the four-term sign juggling
that A and B could get wrong **in agreement** has no counterpart in C at all.
Arm **D** answers the question the statement actually asks.

Nested indexing (`pre[r + 1][c + 1] = …`) is a compound assignment through two
levels of `Vec`, which is a different code path from a single-level store into a
flat buffer. Carrying both makes the differential a layout test as well as an
algorithm test.

## Properties, not just agreement

| # | property | what it pins down |
|---|---|---|
| P1 | four arms, one answer | the algorithm, from three independent directions |
| P2 | a 1×1 rectangle is the cell itself | ties the table to the actual data |
| P3 | the whole matrix is the grand total | the outermost query |
| P4 | a one-row rectangle is that row's slice | collapses the 2D structure to 1D |
| P5 | adding `k` to every cell lifts every answer by `k × area` | **no arm computes this** |
| P6 | inside + outside = the whole matrix | the rectangle against its complement |
| P7 | zeros → 0, ones → area, column-index → closed form | shapes the statement fixes outright |

The query space is **exhausted, not sampled**. An `h × w` matrix admits exactly
`(h(h+1)/2) × (w(w+1)/2)` rectangles and every one is asked of every arm — 1,296
apiece for the 8×8 matrices. Boundary rectangles, where the zero border does the
work, and 1×1 rectangles, where every term collapses, are precisely where a
random generator under-samples and where the off-by-ones live.

```
matrices 1920
queries 432000
P1..P7 all 0
DIFFERENTIAL OK
```

Values straddle zero on purpose. Sign errors are invisible on all-positive data.

## The property that cannot fail

The obvious eighth property is **split additivity**: cut a rectangle along a row
or column, sum the halves, get the whole back. It is deliberately *absent*,
because for every prefix-based arm it is unfalsifiable. Splitting arm A at row
`mid`:

```
top = P[mid+1][c2+1] - P[r1  ][c2+1] - P[mid+1][c1] + P[r1  ][c1]
bot = P[r2 +1][c2+1] - P[mid+1][c2+1] - P[r2 +1][c1] + P[mid+1][c1]
```

Every `P[mid+1][*]` term cancels against its twin, leaving exactly the unsplit
query **regardless of what `P` contains**. The same cancellation holds for B
(identical algebra) and for C (splitting a loop range).

This was measured, not assumed. Adding split additivity as a temporary P8 and
running it against deliberately corrupted builds:

| mutation | P1 | P2 | P3 | P4 | P5 | P6 | P7 | **P8 split** |
|---|---|---|---|---|---|---|---|---|
| build drops the overlap term | 1,121,556 | 23,058 | 1,464 | 93,007 | 376,320 | 373,852 | 23,520 | **0** |
| build *adds* the overlap term | 1,122,171 | 23,102 | 1,463 | 93,108 | 376,320 | 374,057 | 23,520 | **0** |
| build never reads the matrix at all | 1,256,043 | 37,029 | 1,892 | 124,267 | **432,000** | 418,681 | 27,840 | **0** |

The last row is the one that settles it: a prefix table built **without ever
looking at the input** violates P5 on *every single one of the 432,000 queries*, and split additivity
still reports zero. A property that holds for an arbitrarily corrupt table is not
a test of that table; it is a test that subtraction is associative.

This is the same trap #303 found one dimension down, and the extra dimension
makes it *worse*, not better — in 2D the property looks like it is testing the
inclusion–exclusion structure, which is exactly what it is blind to.

## Mutation-tested, because a differential that cannot fail is decoration

Ten line-anchored mutations, each verified to have actually applied and to have
compiled:

| # | mutation | caught by |
|---|---|---|
| M1 | build drops the overlap term | P1 P2 P3 P4 P5 P6 P7 |
| M2 | query corner sign flipped to minus | P1 P2 **·** P4 P5 P6 P7 |
| M3 | query big-block row off by one | P1 P2 P3 P4 P5 P6 P7 |
| M4 | query left-strip sign flipped | P1 P2 **·** P4 P5 P6 P7 |
| M5 | build adds instead of subtracting the overlap | P1 P2 P3 P4 P5 P6 P7 |
| M6 | flat build drops the overlap term | P1 P7 |
| M7 | flat query corner sign flipped | P1 P7 |
| M8 | row arm drops the left subtraction | P1 P7 |
| M9 | brute arm skips the last column | P1 |
| M10 | flat build overlap sign flipped | P1 P7 |

### P3 is blind to exactly the corner term

M2 and M4 are the interesting rows: both survive P3 (**·** above) while every
other property fires. The whole-matrix query has `r1 = 0, c1 = 0`, so
`pre[r1][c1]` and `pre[r2+1][c1]` are reads of the zero border — flipping the
sign of zero changes nothing. P3 cannot see any fault confined to terms that
vanish at the origin. It is a real property with a precisely describable blind
spot, which is a better thing to know about a test than a green tick.

### The properties interrogate arm A, so B, C and D ride on P1 alone

P2–P7 are all phrased against arm A's answer, so mutations to the other three
arms (M6–M10) can only be caught by cross-arm disagreement. That is by design —
P1 is a strong net when it has three independent arms behind it — but it does
mean the property battery is a test of the ★ arm specifically, not of all four.

## Benchmarks

Container x86-64, 30 runs, `hyperfine`. Build-once + punch: the matrix, its
prefix table and 100,000 random rectangles are all built before the timed loop,
which is 1,800 sweeps over them (180M queries).

Build a 256×256 matrix, its 257×257 flat prefix table, and 100,000 random
rectangles once; then punch 1,800 passes over the query list — 180,000,000
queries, `build-once + punch` ([BENCHMARKS.md](../../../BENCHMARKS.md)). All
five languages print `checksum 950743584`.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each.

| | mean | vs kara |
|---|---:|---:|
| c (`-O3 -march=x86-64-v3`, matched ISA) | 375.9 ms | 0.57× |
| c (`-O3`) | 379.8 ms | 0.58× |
| go | 548.8 ms | 0.83× |
| rust (`-O`) | 562.4 ms | 0.85× |
| **kara** (codegen, seq) | **659.1 ms** | **1.00×** |
| rust (equal safety + matched ISA) | 690.0 ms | 1.05× |
| rust (`-O -C overflow-checks=on`, equal safety) | 709.4 ms | 1.08× |
| python | 42.081 s | 63.8× |

Kāra is **1.74× behind `clang -O3`** — wider than #303's 1.52×, and the widest
compiled gap in the corpus so far. It is also **faster than equal-safety Rust**
(1.08×, and 1.05× against the matched-ISA equal-safety twin), which is the
comparison that holds the safety story fixed.

Both facts have the same cause. The query body is four indexed loads, three
add/subs and a masked accumulate; the four index expressions are checked
arithmetic and the four loads are bounds-checked. Against unchecked C that is
eight extra operations on a body of roughly seven real ones, so the gap widens
relative to #303's two-load version exactly as you would expect. Against Rust
compiled to the same safety level, Kāra comes out ahead.

The prefix table is 257 × 257 × 8 = **528 KB**, L2-resident by design. A table
big enough to miss to DRAM would measure memory latency, and four scattered DRAM
loads cost the same in every language — which would hide the one thing this kata
is positioned to measure: four bounds-checked indexed loads against four raw
ones. The query body is four loads, three add/subs and a masked accumulate, so
the checking overhead is about as exposed as it ever gets.

### The layout that should have been slower

The ★ arm uses a nested `Vec[Vec[i64]]`; the benchmark uses the flat
`Vec[i64]` + stride, because that is what the C/Rust/Go mirrors would naturally
write and honest benchmarking requires the same algorithm on both sides. Timing
the two Kāra layouts against each other gave the opposite of the expected
answer:

| kāra layout | mean | |
|---|---:|---|
| flat `Vec[i64]` + stride multiply | 638.5 ms ± 16.0 | |
| nested `Vec[Vec[i64]]` | **543.3 ms ± 9.3** | **1.18× faster** |

Nested wins despite doing *more* bounds checks (two per access rather than one).
The obvious explanation is the stride multiply, so that was tested directly: a
third variant keeping the flat layout but replacing `r * stride` with a
precomputed row-base lookup. It came out at 660.0 ms — **slower still**, which
refutes the multiply as the cause rather than confirming it.

What does explain it is **checked arithmetic**, and the control is Rust:

| | flat | nested | |
|---|---:|---:|---|
| `rustc -O` | **556.0 ms** | 594.9 ms | flat wins — the usual intuition |
| `rustc -O -C overflow-checks=on` | 715.2 ms | **617.9 ms** | nested wins, 1.16× |
| `karac build` (checked by default) | 638.5 ms | **543.3 ms** | nested wins, 1.18× |

The inversion is not a Kāra property. It appears in Rust the moment overflow
checking is switched on, at nearly the identical ratio, and it disappears when
it is switched off. Explicit index arithmetic (`(r+1)*stride + (c+1)`) is a chain
of *checked* operations; nested indexing performs the same address computation
inside the pointer load, where no overflow check applies. Under checked
arithmetic, hiding index math inside the data structure beats writing it out.

Worth stating plainly because the folk rule — "flatten your 2D arrays" — is
sound advice derived from unchecked languages, and it inverts in a
checked-by-default one.

(The three tables above are one hyperfine session each, run back-to-back on an
otherwise idle container so the layouts are compared under identical
conditions. They are a controlled side experiment, not the published lane —
the cross-language numbers of record are the results.json table above, which
was measured separately and puts kāra at 659.1 ms.)

### The sink, and a lesson carried over from #303

#303's first benchmark used `% 1000000007` as its sink and measured **itself**:
two 64-bit divisions per query are a fixed hardware cost no backend can optimise,
they came to roughly 75% of runtime, and every compiled language tied to within
3%. This lane used `& 0x3FFFFFFF` from the start.

The same swap also sidesteps a cross-language trap met on #303: `%` truncates
toward zero in Kāra, C, Rust and Go but **floors** in Python, so a modulo sink
over a signed running total prints a number differing by exactly one modulus.
Masking is two's-complement in all five languages.

### Verifying the timed loop is real

Before fixing the pass count, the lane was run at 130 / 260 / 520 passes
(0.05 / 0.09 / 0.18 s). Clean linear scaling — the loop is not being elided, and
generation is not dominating.

## Compiler findings

None. All five sources produced zero `karac check` diagnostics on the first
pass — including the nested compound index-assign `pre[r + 1][c + 1] = …`,
`Vec[Vec[i64]]` parameters passed by `ref`, and four `impl` blocks reading
through `ref self` — and all five are byte-identical under `karac run`,
`karac build` and the default auto-parallelising build.

## Running it

```bash
karac run range_sum_query_2d.kara          # ★ nested 2D prefix
karac run range_sum_query_2d_flat.kara     # flat layout, same arithmetic
karac run range_sum_query_2d_rows.kara     # per-row prefixes
karac run range_sum_query_2d_brute.kara    # the definition
karac run differential.kara                # 1,920 matrices, 432,000 queries

bash bench/bench.sh                        # cross-language lane
```
