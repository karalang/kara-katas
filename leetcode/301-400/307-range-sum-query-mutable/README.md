# 307. Range Sum Query — Mutable

Build a structure over an integer array, then interleave two operations freely:
`update(i, val)` writes one element, `sum_range(l, r)` reads an inclusive range.

```
nums = [1, 3, 5]

sum_range(0, 2) -> 9
update(1, 2)
sum_range(0, 2) -> 8
```

This is [#303](../303-range-sum-query-immutable/) with writes, and the writes
change everything. A prefix array answers #303 in O(1) but needs O(n) to absorb
a single write, so the structure that wins there is useless here. Every arm
below maintains a **second representation** of the array and answers from it;
keeping that second representation in step with the first is the whole
difficulty of the problem, and the whole source of its bugs.

## Approaches

| file | mechanism | update | query |
|---|---|---|---|
| `range_sum_query_mutable.kara` ★ | Fenwick tree — opposite `lowbit` walks | O(log n) | O(log n) |
| `range_sum_query_mutable_segment.kara` | segment tree — child arithmetic, repairs upward | O(log n) | O(log n) |
| `range_sum_query_mutable_blocks.kara` | √n decomposition — block totals, partial edges | O(1) | O(√n) |
| `range_sum_query_mutable_naive.kara` | the array itself, the definition verbatim | O(1) | O(n) |
| `differential.kara` | 640 arrays, 76,800 queries, four arms, seven properties | — | — |
| `bench/fenwick.kara` | 65,536-element tree × 200,000 ops × 110 passes (22M operations) | — | — |

## The mechanism, and the two lines that are the whole trick

Each Fenwick slot `tree[x]` holds the sum of the `lowbit(x)` elements ending at
`x`, where `lowbit(x) = x & -x` is the value of x's lowest set bit. Both
operations are logarithmic because both are walks over that one bit — in
**opposite directions**:

```kara
fn add(mut ref self, i: i64, delta: i64) {
    let mut x = i + 1;
    while x <= self.n { self.tree[x] += delta; x += x & -x; }   // climb: every slot COVERING i
}

fn prefix(ref self, i: i64) -> i64 {
    let mut total = 0;
    let mut x = i;
    while x > 0 { total += self.tree[x]; x -= x & -x; }         // descend: the slots TILING [0, i)
}
```

The tree is **1-indexed** internally, because `lowbit(0) == 0` and a 0-indexed
Fenwick would loop forever on the first slot. The `i + 1` in `add` and the
`prefix(r + 1) - prefix(l)` in `sum_range` are the whole of the conversion.

`data` carries a shadow copy of the array, because a Fenwick absorbs a **delta**
rather than a value: `update` must know what was there before to compute
`val - old`. The segment tree needs no such shadow — it writes the leaf and
repairs upward from children — and that asymmetry is load-bearing in the
differential: a corrupted shadow is invisible to the Fenwick arm's own internal
consistency and shows up only as a disagreement with the segment tree.

## Properties, not just agreement

| # | property | what it pins down |
|---|---|---|
| P1 | four arms, one answer, at every state | the algorithm, from four directions |
| P2 | a width-one range is the element itself | ties the summary to the data |
| P3 | the whole array is the independent total | the outermost query |
| P4 | a write is invertible — put the old value back and every answer returns | that a write leaves no residue |
| P5 | every answer matches an independent recount of the reference array | the summary against a from-scratch count |
| P6 | writing the value already there changes nothing | idempotence |
| P7 | answers depend only on the array's **contents**, never on the write history | **no arm computes this** |

The query space is **exhausted at every state**: after each write, all
`n(n+1)/2` valid `(l, r)` pairs are asked of all four arms.

```
arrays 640
queries 76800
P1..P7 all 0
DIFFERENTIAL OK
```

**P7 is what this problem is really about.** A mutable structure's answers must
depend only on the array's current contents — never on the sequence of writes
that produced them. Every arm is inherently history-dependent: each carries
mutated state forward and none ever recomputes from scratch. So a history
dependence is exactly the fault four-way agreement is blind to, because all four
would carry it. The differential reaches each final array by four routes —
built directly, written left-to-right from zeros, written right-to-left, and
written with junk intermediates (`999`, then `-999`, then the real value twice)
— and demands one answer from all of them.

### A property deliberately absent, for the third kata running

Split additivity — cut a range, sum the halves — is unfalsifiable for every
prefix-shaped arm, because the shared boundary term cancels regardless of what
the table contains. [#303](../303-range-sum-query-immutable/) found it in one
dimension; [#304](../304-range-sum-query-2d-immutable/) measured it in two,
where a prefix table built **without ever reading its input** still satisfied it
on all 432,000 queries. Arm A here is `prefix(r+1) - prefix(l)`, the same shape.
It is not re-derived — only not used.

## Mutation-tested, because a differential that cannot fail is decoration

| # | mutation | caught by |
|---|---|---|
| M1 | `lowbit` direction swapped in `add` (climb → descend) | **non-termination** |
| M2 | `lowbit` direction swapped in `prefix` (descend → climb) | **bounds-check panic** |
| M3 | `update` absorbs the value, not the delta | P1 P2 P3 P4 P5 P6 P7 |
| M4 | `add` folds into only the first covering slot | P1 P2 P3 · P5 · P7 |
| M5 | segment query frontier closed instead of half-open | P1 |
| M6 | segment low-pointer parity test inverted | P1 |
| M7 | segment internal repair uses one child twice | P1 |
| M8 | blocks partial-edge guard drops its fits-entirely test | P1 |
| M9 | blocks total not adjusted on a write | P1 |
| M10 | **control** — blocks always walk element-wise | *(correctly survives)* |

### The bug everyone fears cannot produce a wrong answer

M1 and M2 are the interesting rows, and they say something the properties
cannot. The two `lowbit` lines are one token apart and are exactly what a
writer transposes — and **neither transposition yields wrong output**. Swapping
the direction in `add` makes `x -= x & -x` reach 0, where `0 & -0 == 0`, so the
loop subtracts zero forever: it **hangs**. Swapping it in `prefix` climbs past
the end of the array and **panics on the bounds check**. The differential's
seven properties never get a chance to fire.

That is worth knowing in both directions. The Fenwick arm's most-feared mistake
is self-announcing, so no test is needed for it — while the mistakes that *do*
silently corrupt are the unglamorous ones about the shadow array (M3 fires all
seven properties) and about how far a write propagates (M4). Those are what the
differential is actually for here.

M2 is also a safety note: the same transposition in the C mirror is an
out-of-bounds read, silent and unbounded.

## Benchmarks

Build a 65,536-element Fenwick tree and a 200,000-operation script (half
writes, half range reads) once; then punch 110 passes over that script — 22M
operations, `build-once + punch`
([BENCHMARKS.md](../../../BENCHMARKS.md)). All five languages print
`checksum 701187399`.

Nothing is rebuilt per pass: a Fenwick tree is mutable and stays valid across
passes, so each pass starts from the state the previous one left. That is
deterministic and identical in every mirror, and it keeps per-pass allocation
out of the measurement entirely — unlike [#305](../305-number-of-islands-ii/),
where a destructive union-find forced a rebuild.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each.

| | mean | vs kara |
|---|---:|---:|
| c (`-O3 -march=x86-64-v3`, matched ISA) | 484.3 ms | 0.80× |
| c (`-O3`) | 548.6 ms | 0.91× |
| rust (`-O`) | 555.0 ms | 0.92× |
| **kara** (codegen, seq) | **602.3 ms** | **1.00×** |
| rust (equal safety + matched ISA) | 617.9 ms | 1.03× |
| rust (`-O -C overflow-checks=on`, equal safety) | 644.6 ms | 1.07× |
| go | 660.8 ms | 1.10× |
| python | 39.299 s | 65.3× |

Kāra is **1.10× behind `clang -O3`** — the narrowest compiled gap of the four
range/grid katas in this run — and ahead of Go and of equal-safety Rust in both
its forms.

The trend across those four is the interesting part, because it is monotone in
one variable: how much the loop body waits on memory.

| kata | hot loop | vs `clang -O3` |
|---|---|---:|
| [#304](../304-range-sum-query-2d-immutable/) | 4 indexed loads, 3 subtractions | 1.74× |
| [#303](../303-range-sum-query-immutable/) | 2 indexed loads, 1 subtraction | 1.52× |
| [#305](../305-number-of-islands-ii/) | union-find pointer chasing | 1.18× |
| **#307** | `lowbit` walks over a 512 KB tree | **1.10×** |

#304's body is four bounds checks against seven real instructions, which is as
exposed as the overhead ever gets. A Fenwick walk is a short dependent chain of
data-dependent loads with an unpredictable trip count — the machine is already
waiting, and the check rides inside that wait. The same bounds check costs
proportionally less the less the surrounding code is compute-bound, and this
kata is the far end of that scale.

## Compiler findings

The four arms are clean — zero `karac check` diagnostics across all five
sources, all byte-identical under `karac run`, `karac build` and the default
auto-parallelising build, matching the Python oracle.

**A fifth arm is missing, and its absence is the finding.** A Fenwick tree is a
monoid structure, so `Fenwick[T: Copy + Add + Sub]` is what a reader who knows
the structure reaches for — and it was to be this kata's twin arm precisely to
dogfood [`fe82c7b`](https://github.com/karalang/kara), this session's fix for
the generic-arithmetic and `T: Copy` gaps found in #304. It does not compile:

- **`B-2026-09-02-42`** (typecheck, medium) — a body type annotation that names
  the impl's own type parameter poisons every later bounded method call on that
  value:

  ```kara
  struct Box[T] { v: T }
  impl[T: Copy] Box[T] {
      fn set(mut ref self, v: T) { self.v = v; }
      fn make(v: T) -> Box[T] {
          let w: T = v;          // delete this annotation and it compiles
          let mut b = Box { v: w };
          b.set(v);              // error[E0236]: trait bound `T: Copy` is not
          return b;              //   satisfied; `T` does not implement `Copy`
      }
  }
  ```

  The bound it reports unsatisfied is declared three lines above. The control is
  one token — `let w = v;` compiles and prints 5 — and the trigger is precisely
  *writing `T` in a body annotation*: `let mut xs: Vec[T] = Vec.new()` fails,
  `let mut xs = Vec.new()` and `let mut xs: Vec[i64] = Vec.new()` both pass.
  This is very likely the same Named-vs-`TypeParam` spelling trap `fe82c7b`
  diagnosed, reaching a third consumer — the method-resolution bound gate — but
  that mechanism is inferred from that commit rather than read out of the source,
  so the row files it as the leading hypothesis rather than a finding.

The arm is **absent rather than rewritten**. Dropping the annotation would make
it compile, but the annotated form is the idiomatic spelling used throughout this
corpus, and rewriting to dodge a gap is exactly what the kata rules forbid.

Idioms probed and found clean: `x & -x` with unary minus on a variable,
bitwise-and in both walk directions, range-`for` over an `i64` bound, `+=` and
`-=` on `Vec` elements through `mut ref self`, associated-function constructors
taking `ref Vec[i64]`, and a generic `Fenwick[T]` *free-standing* (the generic
structure itself is fine — it is only the annotated-local constructor that
fails).

## Running it

```bash
karac run range_sum_query_mutable.kara            # ★ Fenwick tree
karac run range_sum_query_mutable_segment.kara    # segment tree
karac run range_sum_query_mutable_blocks.kara     # sqrt decomposition
karac run range_sum_query_mutable_naive.kara      # the definition
karac run differential.kara                       # 640 arrays, 76,800 queries

bash bench/bench.sh                               # cross-language lane
```
