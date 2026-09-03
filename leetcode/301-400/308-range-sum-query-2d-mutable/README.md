# 308. Range Sum Query 2D — Mutable

Build a structure over a matrix, then interleave `update(r, c, val)` with
`sum_region(r1, c1, r2, c2)` — the sum of a rectangle, inclusive on all four
sides.

```
[3, 0, 1, 4, 2]
[5, 6, 3, 2, 1]
[1, 2, 0, 1, 5]     sum_region(2, 1, 4, 3) ->  8
[4, 1, 0, 1, 7]     update(3, 2, 2)
[1, 0, 3, 0, 5]     sum_region(2, 1, 4, 3) -> 10
```

This is the fourth corner of a square the corpus has been filling in:

|  | immutable | mutable |
|---|---|---|
| **1D** | [#303](../303-range-sum-query-immutable/) prefix array | [#307](../307-range-sum-query-mutable/) Fenwick tree |
| **2D** | [#304](../304-range-sum-query-2d-immutable/) 2D prefix table | **#308** — this kata |

And it is the corner where the two hard parts **meet**. #304 contributed the
four-term inclusion–exclusion whose final `+` is the whole idea; #307
contributed the opposite `lowbit` walks whose transposition is the mistake
everybody makes. The ★ arm is both at once — a Fenwick tree of Fenwick trees.

## Approaches

| file | mechanism | update | query |
|---|---|---|---|
| `range_sum_query_2d_mutable.kara` ★ | 2D Fenwick — nested lowbit walks + inclusion–exclusion | O(log h · log w) | O(log h · log w) |
| `range_sum_query_2d_mutable_rowfen.kara` | one 1D Fenwick per row — adds disjoint row-slices | O(log w) | O(h · log w) |
| `range_sum_query_2d_mutable_rowprefix.kara` | eager per-row prefix arrays — **no bit trick at all** | O(w) | O(h) |
| `range_sum_query_2d_mutable_naive.kara` | the matrix itself, the definition verbatim | O(1) | O(area) |
| `range_sum_query_2d_mutable_nested.kara` | arm ★'s mathematics over a nested `Vec[Vec[i64]]` | O(log h · log w) | O(log h · log w) |
| `differential.kara` | 1,000 matrices, 245,000 queries, five arms, seven properties | — | — |
| `bench/fenwick2d.kara` | 256×256 tree × 100,000 ops × 54 passes (5.4M operations) | — | — |

## The mechanism

`tree[x][y]` covers a rectangle `lowbit(x)` rows tall and `lowbit(y)` columns
wide, ending at `(x, y)`. A write must reach every slot covering its cell in
**both** dimensions, which is a nested climb; a prefix read gathers the disjoint
slots tiling the origin-rectangle, descending in both:

```kara
fn add(mut ref self, r: i64, c: i64, delta: i64) {
    let mut x = r + 1;
    while x <= self.h {                       // every row-band covering r
        let mut y = c + 1;                    // reset per outer step
        while y <= self.w {                   // every column-band covering c
            self.tree[x * stride + y] += delta;
            y += y & -y;
        }
        x += x & -x;
    }
}
```

The query is then #304's inclusion–exclusion over four such 2D prefixes.

## Non-square shapes are load-bearing, and here is the proof

The inner loop is bounded by `w` and the outer by `h`, and the inner index is
reset on **every** outer step. Transposing the bounds is a one-token slip — and
its consequences are shape-dependent in a way that makes a careless differential
useless. Measured directly, with the inner bound changed to `h`:

| shape | what the transposition does | result |
|---|---|---|
| square (3×3, 2×2) | nothing — the bounds are equal | **correct** |
| wide, `w > h` (2×5) | inner loop stops early, missing column bands | **silently wrong** — printed `0`, wanted `55` |
| tall, `w < h` | index runs past the row | **panics** on the bounds check |

**A differential over square matrices alone would pass a broken arm.** Twenty of
the twenty-five shapes in `differential.kara` are non-square for exactly this
reason. The silent half is the dangerous one: it produces plausible numbers with
no crash, and on the corpus's usual square test grids it would never appear at
all.

## Properties, not just agreement

| # | property | what it pins down |
|---|---|---|
| P1 | five arms, one answer, at every state | the algorithm, from five directions |
| P2 | a 1×1 rectangle is the cell itself | ties the summary to the data |
| P3 | the whole matrix is the independent total | the outermost query |
| P4 | a write is invertible — put the old value back and every answer returns | that a write leaves no residue |
| P5 | every answer matches an independent recount of the reference grid | the summary against a from-scratch count |
| P6 | writing the value already there changes nothing | idempotence |
| P7 | answers depend only on the matrix's **contents**, never on the write history | **no arm computes this** |

The rectangle space is **exhausted at every state**: after each write, all
`(h(h+1)/2)·(w(w+1)/2)` rectangles are asked of all five arms.

```
matrices 1000
queries 245000
P1..P7 all 0
DIFFERENTIAL OK
```

**P7 lifts #307's history-independence into 2D**, and gains a route that only
exists here: the same final matrix is reached by writing **row-major**, by
writing **column-major**, by junk intermediates, and by direct construction. A
2D structure that got its two dimensions confused could plausibly be
order-sensitive in one axis and not the other, and column-major is what would
catch it.

### A property deliberately absent, for the fourth kata running

Split additivity — cut a rectangle, sum the halves — is unfalsifiable for every
prefix-shaped arm: the shared boundary terms cancel regardless of what the table
contains. #303 found it in 1D; **#304 measured it** — a 2D prefix table built
*without ever reading its input* still satisfied it on all 432,000 queries; #307
inherited it. Arm A is prefix differences in two dimensions, the same shape
again. Not re-derived here, only not used.

## Mutation-tested, because a differential that cannot fail is decoration

| # | mutation | caught by |
|---|---|---|
| M1 | inner climb bounded by `h` instead of `w` | **bounds-check panic** (and silently wrong on wide shapes — see above) |
| M2 | inner index reset hoisted out of the climb | P1 P2 · P5 · P7 |
| M3 | inclusion–exclusion corner term sign flipped | P1 P2 · P5 · P7 |
| M4 | inclusion–exclusion left-strip sign flipped | P1 P2 · P5 · P7 |
| M5 | per-row arm's climb bounded by `h` instead of `w` | **bounds-check panic** |
| M6 | per-row prefix rebuild drops the running carry | P1 |

M1 and M5 continue the pattern [#307](../307-range-sum-query-mutable/) found:
the `lowbit` family's most-feared mistakes tend to **announce themselves** —
there by non-termination and a bounds panic, here by a bounds panic — rather
than producing quietly wrong answers. What the properties actually earn their
keep on is the unglamorous middle ground: a hoisted loop reset (M2) and the
inclusion–exclusion signs (M3, M4), none of which crash anything.

The same transposition in the C mirror is an out-of-bounds read: silent, and
unbounded.

## Benchmarks

Build a 256×256 2D Fenwick tree and a 100,000-operation script (half writes,
half rectangle reads) once; then punch 54 passes — 5.4M operations,
`build-once + punch` ([BENCHMARKS.md](../../../BENCHMARKS.md)). All five
languages print `checksum 108334916`.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each.

| | mean | vs kara |
|---|---:|---:|
| c (`-O3 -march=x86-64-v3`, matched ISA) | 199.6 ms | 0.33× |
| c (`-O3`) | 204.9 ms | 0.34× |
| rust (`-O`) | 277.6 ms | 0.46× |
| rust (equal safety + matched ISA) | 496.0 ms | 0.82× |
| rust (`-O -C overflow-checks=on`, equal safety) | 512.3 ms | 0.85× |
| go | 583.2 ms | 0.97× |
| **kara** (codegen, seq) | **603.3 ms** | **1.00×** |
| python | 33.600 s | 55.7× |

**2.94× behind `clang -O3` — the widest gap in the corpus, and it breaks the
trend the previous three katas established.** #307 reported a monotone
progression in how much the loop body waits on memory (#304 1.74×, #303 1.52×,
#305 1.18×, #307 1.10×) and predicted that a `lowbit` walk amortises the
checking overhead well. This kata is also a `lowbit` walk and lands nearly three
times worse, so that account was incomplete.

What it missed is **where the index arithmetic sits**. #307's Fenwick indexes a
1D array — `tree[x]`, one bounds check, no arithmetic. This one indexes a 2D
tree as `tree[x * stride + y]`: a *checked multiply* and two *checked adds* on
every access, inside a **doubly** nested walk. It is #304's exposed-arithmetic
shape (1.74×) placed in #307's hot loop, and the two compound rather than
cancel. The tell is in the Rust column: plain `rustc -O` is 2.17× faster than
kāra, but the equal-safety twin is only 1.18× faster — so **checked arithmetic
costs Rust 1.85× on this same code**, which is most of the gap and is not a Kāra
property.

### The published lane understates kāra by 1.59×

The flat layout above is what the C, Rust, Go and Python mirrors use, so it is
what the cross-language lane must measure. It is *not* the faster spelling in
kāra. Timing the two layouts against each other, same workload, same machine:

| kāra layout | mean | |
|---|---:|---|
| flat `Vec[i64]` + `x * stride + y` | 596.9 ms ± 10.3 | |
| nested `Vec[Vec[i64]]`, `tree[x][y]` | **374.4 ms ± 14.9** | **1.59× faster** |

Both are in the corpus as arms ★ and E, and both produce `checksum 108334916`.
At 374.4 ms the gap to `clang -O3` would be **1.83×**, not 2.94×.

This is [#304](../304-range-sum-query-2d-immutable/)'s finding again, larger.
There the inversion was 1.18× and the cause was established by a controlled
cross-language experiment: `rustc -O` prefers flat (556.0 vs 594.9 ms) and
`rustc -O -C overflow-checks=on` prefers nested (715.2 vs 617.9 ms) — the
inversion appears the moment overflow checking is switched on, at nearly the
identical ratio, and disappears when it is switched off. The effect is larger
here because the arithmetic sits in a doubly nested walk and so runs far more
often per operation.

The rule worth carrying: **"flatten your 2D arrays" is advice derived from
unchecked languages, and it inverts in a checked-by-default one** — the more
deeply nested the loop, the more it inverts.

## Compiler findings

The arms are clean — zero `karac check` diagnostics across all six sources, all
byte-identical under `karac run`, `karac build` and the default
auto-parallelising build, matching the Python oracle.

**No compiler defect surfaced.** Probed deliberately before shipping this time,
rather than after being asked — the discipline the previous four katas in this
range each had to learn the hard way:

- **A nested `Vec[Vec[i64]]` 2D Fenwick** — clean, and 1.59× faster than the
  flat form (above). It is now arm E rather than a discarded probe.
- **A generic `Fenwick2D[T: Copy + Add + Sub]`** — the shape that failed in
  #307 as `B-2026-09-02-42` and again earlier as `-18`/`-19`. Clean on this
  build in two dimensions, including the `let mut tree: Vec[Vec[T]] = Vec.new();`
  body annotation that was the trigger.
- Nested compound index-assign `tree[x][y] += delta` through `mut ref self`;
  `x & -x` with unary minus inside a doubly nested walk; range-`for` over an
  expression bound (`0..(h + 1)`); associated-function constructors taking
  `ref Vec[Vec[i64]]`.

The one thing this kata leans on that earlier ones did not is **two levels of
mutable indexing under a `mut ref self` receiver** (`self.tree[x][y] += delta`
inside a nested `while`), which is the compound-index-assign path on a
heap-of-heaps that kata #200 exercises for reads. It is clean here on all three
backends.

## Running it

```bash
karac run range_sum_query_2d_mutable.kara            # ★ 2D Fenwick tree
karac run range_sum_query_2d_mutable_rowfen.kara     # one 1D Fenwick per row
karac run range_sum_query_2d_mutable_rowprefix.kara  # eager row prefixes
karac run range_sum_query_2d_mutable_naive.kara      # the definition
karac run range_sum_query_2d_mutable_nested.kara     # arm ★, nested layout
karac run differential.kara                          # 1,000 matrices, 245,000 queries

bash bench/bench.sh                                  # cross-language lane
```
