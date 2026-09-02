# 303. Range Sum Query — Immutable

Build a structure over a fixed integer array, then answer many
`sum_range(left, right)` queries — inclusive on both ends. The array never
changes.

```
nums = [-2, 0, 3, -5, 2, -1]

sum_range(0, 2) ->  1
sum_range(2, 5) -> -1
sum_range(0, 5) -> -3
```

## Approaches

| file | mechanism | build | query |
|---|---|---|---|
| `range_sum_query.kara` ★ | prefix sums — subtract two overlapping totals | O(n) | O(1) |
| `range_sum_query_naive.kara` | add the elements up, the definition verbatim | O(1) | O(n) |
| `range_sum_query_blocks.kara` | √n decomposition — add disjoint pieces | O(n) | O(√n) |
| `differential.kara` | 1,200 arrays, **every** (l, r) pair, three arms, seven properties | — | — |
| `bench/rangesum.kara` | 65,536-element table × 200,000 queries × 1,800 passes | — | — |

The algorithm is four lines. What makes it worth a kata is the **shape**: a
structure built once and read many times through `ref self`. That is a different
compiler surface from a free function taking its data as an argument — every
query here borrows the same `Vec[i64]` field immutably and returns a scalar,
which is precisely the read-only non-escaping borrow karāc's RC-elision hint
exists to make free. A kata that never builds a struct never exercises it.

### Why the prefix array is one longer than the input

`prefix[i]` is the total of the first `i` elements, so `prefix[0] = 0` and
`sum_range(l, r) = prefix[r + 1] - prefix[l]`. A prefix array of length `n`
would force a special case at `l == 0`, where there is no "sum of everything
before index 0" to subtract. Carrying an explicit leading zero makes the empty
prefix a representable value instead of a branch. That is the whole trick, and
`r + 1` versus `l` — one past, one at — is the thing to get right.

### Three arms that cannot make each other's mistakes

Arm B is the definition transcribed, which anchors the other two to the
statement. Between A and C the useful property is that their characteristic
bugs have no counterpart in each other:

- **A's** bug is an off-by-one at the prefix boundary — possible *only* because
  A indexes an array one longer than the input.
- **C's** bug is a partial edge that swallows one element too many — possible
  *only* because C decides per step whether a whole block still fits.
- **B** can commit neither, having no boundary and no blocks.

Arm C is also where this problem goes next. Prefix sums are optimal *because*
the array is immutable; make one element mutable and every prefix downstream is
invalidated, an O(n) repair. The block structure repairs in O(1) and still
answers in O(√n). That is LeetCode 307, visible from here instead of a surprise
later.

### A keyword collision worth knowing about

The natural name for arm C's per-block totals is `blocks`, and it does not
compile — `blocks` is one of Kāra's eight effect verbs and therefore a keyword,
rejected as an identifier everywhere. All eight are `reads`, `writes`, `sends`,
`receives`, `allocates`, `panics`, `blocks`, `suspends`, and several are names
ordinary code reaches for without thinking (`struct IoStats { reads: i64 }` is
rejected for the same reason).

The language has a designed answer — the raw-identifier escape from
design.md § Raw Identifiers — and it works on all three backends:

```kara
struct Decomp { r#blocks: Vec[i64] }     // legal; d.r#blocks reads it
```

Verified `run` == `build` == auto-par. This kata uses `block_sums` instead, not
to dodge anything but because the field holds the per-block *totals* rather than
the blocks.

## Properties, not just agreement

| | property |
|---|---|
| P1 | the three arms agree |
| P2 | a width-one range is the element itself |
| P3 | splitting a range anywhere inside it adds back up |
| P4 | the full range equals the array total, summed independently |
| P5 | adding `c` to every element raises every answer by exactly `c · width` |
| P6 | reversing the array mirrors every range onto its twin |
| P7 | fixed shapes: all-zeros → 0, all-ones → `r - l + 1` |

**The query space is exhausted, not sampled.** For an array of length `n` there
are exactly `n(n+1)/2` valid `(left, right)` pairs and every one is asked of
every arm — 356,400 queries over 1,200 arrays. That is a stronger claim than a
random differential can make, and it matters here because the boundary queries a
generator under-samples (`l = 0`, `r = n-1`, `l = r`) are exactly where
off-by-ones live.

## Mutation-tested, because a differential that cannot fail is decoration

Counts are cases flagged, out of 356,400 queries / 1,200 arrays.

| mutation | caught by | P1 count |
|---|---|---:|
| A reads `prefix[right]` not `prefix[right+1]` | P1–P7 | 237,165 |
| A shifts both ends | P1–P7 | 237,324 |
| **A's build drops the running carry** | **P1, P2, P4, P5, P6, P7 — not P3** | 252,873 |
| B stops one element short | **P1 only** | 237,165 |
| C takes a block ignoring the fit check | P1, P7 | 178,967 |
| C takes a block ignoring alignment | **P1 only** | 156,956 |
| C's block build overruns by one | P1, P7 | 158,960 |

Two rows carry the argument.

### P3 is satisfied by *any* prefix array, correct or not

Breaking arm A's build so that `prefix[i+1] = nums[i]` — dropping the running
carry entirely, which is as wrong as this arm gets — leaves **P3 at exactly
zero**. Additivity survives because it telescopes:

```
sum(l,mid) + sum(mid+1,r)
  = (p[mid+1] − p[l]) + (p[r+1] − p[mid+1])
  = p[r+1] − p[l]
  = sum(l,r)                    ← the middle term cancels, whatever p contains
```

Confirmed separately over 20,000 random arrays under the broken build: zero
violations. So P3 tests the *shape* of arm A — that it is a difference of two
stored values — and says nothing whatever about whether those values are right.
It looks like the most statement-derived property in the list and is the least
discriminating one in it. Worth keeping, because it does pin the shape; worth
not trusting, because a green P3 is compatible with every prefix entry being
wrong.

### The properties interrogate arm A, so B and C ride on P1 alone

P2–P6 are all computed through arm A. That is why two of the three B/C mutations
above are caught by **P1 and nothing else** — a fault in the naive or block arm
is invisible to every property that never calls it. Same structural lesson as
[#296](../../201-300/296-best-meeting-point/)'s brute-force row and
[#301](../301-remove-invalid-parentheses/)'s BFS row, and it is the argument for
keeping a third arm rather than trusting a rich property set over two.

## Benchmarks

Build a 65,536-element array, its prefix table, and 200,000 query pairs once;
then punch 1,800 passes over the query list — 360,000,000 queries,
`build-once + punch` ([BENCHMARKS.md](../../../BENCHMARKS.md)). All five
languages print `checksum 1017312464`.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each.

| | mean | vs kara |
|---|---:|---:|
| c (`-O3 -march=x86-64-v3`, matched ISA) | 449.4 ms | 0.63× |
| c (`-O3`) | 464.8 ms | 0.66× |
| rust (`-O`) | 595.3 ms | 0.84× |
| rust (equal safety + matched ISA) | 648.6 ms | 0.92× |
| rust (`-O -C overflow-checks=on`, equal safety) | 700.9 ms | 0.99× |
| **kara** (codegen, seq) | **708.7 ms** | **1.00×** |
| go | 719.5 ms | 1.02× |
| python | 94.948 s | 134.0× |

Kāra ties equal-safety Rust and Go, and is **1.52× behind `clang -O3`** — the
widest compiled gap in the corpus so far, and the honest one for this workload.
The loop body is two indexed loads, a subtract and an accumulate, so there is
nothing for a bounds check to hide behind: two checks per query against four
real instructions is as exposed as that overhead ever gets. #296's grid scan and
#301's recursion both give it more to amortise against.

### The first version of this lane measured its own sink

This is the correction worth reading, because the original result looked
*better* and was meaningless.

The lane initially folded each answer into a running total mod 1e9+7, matching
the other katas here. Every compiled language tied:

| sink | c | kara | rust | verdict |
|---|---:|---:|---:|---|
| `% 1000000007` (original) | 728.6 ms | 728.9 ms | 748.2 ms | "everyone ties" |
| `& 0x3FFFFFFF` (shipped) | **177.0 ms** | **274.5 ms** | — | **1.55× apart** |

Two 64-bit integer divisions per query are a fixed hardware cost no backend can
optimise, and they were roughly **75% of the runtime**. The lane was mostly
timing `idiv` and reporting it as a range-sum benchmark; the tie was a property
of the sink, not of the query. Swapping the modulo for a mask — changing nothing
else — exposes the real spread.

This is BENCHMARKS.md's "the optimizer erases the work you meant to measure"
hazard wearing a different coat: nothing was erased, the sink simply cost more
than the subject. The mask keeps a genuine loop-carried dependency, so nothing
is hoisted or vectorised away, at about one cycle instead of forty.

### A cross-language `%` trap, met on the way

While the modulo sink was still in place, the five mirrors disagreed: C printed
`-853741824` and Python `146258183`. Range sums go negative here, and `%`
**truncates toward zero** in Kāra, C, Rust and Go but **floors** in Python — the
two answers differ by exactly one modulus. The fix is the standard
`((x % M) + M) % M`, which agrees everywhere. The shipped mask sink sidesteps it
entirely (`&` on a negative left operand agrees across all five, Python
included), but the trap is worth recording for any kata that does need a modular
sink.

### Elsewhere

| | kara | c | rust | go |
|---|---:|---:|---:|---:|
| binary size | 341.5 KiB | 15.7 KiB | 3862.6 KiB | 2178.1 KiB |
| compile (cold) | 417.3 ms | 110.0 ms | 146.3 ms | — |
| peak RSS | 6.9 MiB | 5.2 MiB | 5.5 MiB | 5.4 MiB |

Python's peak RSS is 25.4 MiB.

## Running it

```bash
karac run   range_sum_query.kara
karac build range_sum_query.kara && ./range_sum_query
karac run   range_sum_query_naive.kara
karac run   range_sum_query_blocks.kara
karac run   --interp differential.kara
python3     range_sum_query.py
KARA_BENCH_INCLUDE_PY=1 BENCH_OUT=results.container-x86.json bash bench/bench.sh
```
