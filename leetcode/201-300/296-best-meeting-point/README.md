# 296. Best Meeting Point

A binary grid; each `1` is someone's home. Everyone walks to one meeting cell,
distance measured in Manhattan steps. Return the minimum possible **total**
travel distance.

```
1 0 0 0 1        meet at (0, 2):
0 0 0 0 0        2 + 2 + 2  =  6
0 0 1 0 0
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `best_meeting_point.kara` ★ | separate the axes, take the median of each | O(m·n) |
| `best_meeting_point_pairs.kara` | separate, then sum the nested pair spans | O(m·n) |
| `best_meeting_point_brute.kara` | try every cell, keep the smallest total | O(m·n·k) |
| `differential.kara` | 3,240 generated grids, three arms, seven properties | — |
| `bench/meetpoint.kara` | 400 grids × 128×128 × 30 passes | benchmark lane |

### The problem is two problems

The cost of meeting at `(r, c)` is `sum |r - ri| + |c - ci|`, and that regroups
into `(sum |r - ri|) + (sum |c - ci|)` — two brackets sharing no variable. So
the best row and the best column can be chosen **independently**. This is not an
approximation; it is the sum being rewritten. A search over m·n cells collapses
into two one-dimensional problems, and nothing about the grid survives into
either half except a list of coordinates.

The one-dimensional problem is then "minimise `sum |x - p|`", whose answer is
the median — because moving `p` one step right changes the total by
`(#left of p) − (#right of p)`, so the total falls while more points lie right
and rises once more lie left.

### The sort is free, and that is the part people miss

Both coordinate lists must be sorted for a median to mean anything. But
sortedness is a property of the **scan order**, not something to compute
afterwards:

| scan | yields |
|---|---|
| row-major (`for r { for c }`) | row coordinates, already ascending |
| column-major (`for c { for r }`) | column coordinates, already ascending |

Walking the grid twice, once in each direction, costs O(m·n) and hands back two
sorted lists. Collecting both in one row-major pass and sorting the columns
afterwards is the same answer for an extra O(k log k), and it is the version
almost everyone writes first. No arm here calls `sort`, in any of the five
languages.

### Why a second arm that never picks a meeting point

`..._pairs.kara` computes the same number without choosing anywhere to meet.
Take the leftmost and rightmost homes on one axis. Wherever `p` ends up, if it
lies between them the pair walks `(p - a[lo]) + (a[hi] - p) = a[hi] - a[lo]` —
the `p` cancels, so their joint cost depends only on the span. Outside the
interval they walk strictly more, so an optimum lies between them. Peel the pair
off and recurse inward. The total is the sum of the nested spans, read straight
off the sorted list by a two-pointer walk, with no median, no `abs`, and no
minimiser.

It is a *counting* argument where the ★ arm has an *optimisation* argument, and
it shares no line of code with it — which is what makes agreement between them
evidence rather than repetition.

## Properties, not just agreement

| | property |
|---|---|
| P1 | the three arms agree |
| P2 | the meeting cell arm A names really does cost what arm A says |
| P3 | translating every home by a constant leaves the total unchanged |
| P4 | transposing the grid leaves the total unchanged |
| P5 | mirroring the grid left-right or top-bottom leaves the total unchanged |
| P6 | adding one more home never *lowers* the total |
| P7 | statement-fixed shapes: one home → 0, two homes → their Manhattan distance, no homes → 0 |

P3–P5 are the ones no arm computes. They are isometries of the Manhattan metric,
so the answer cannot move under them, and they catch the family of bugs that a
three-way agreement is structurally blind to — an off-by-one symmetric in the
input, a row/column mix-up invisible on square grids, an index correct only when
the first home sits at zero. All three arms share the coordinate-collection
code, so agreement alone cannot see a fault inside it.

## Mutation-tested, because a differential that cannot fail is decoration

Each row is one line changed in `differential.kara`, rebuilt and rerun. Counts
are cases flagged, out of 3,240.

| mutation | caught by | counts |
|---|---|---|
| row coords push the column index | P1, P2, P4, P5, P6 | 1781 / 1886 / 1648 / 1116 / 71 |
| col coords push the row index | P1, P2, P4, P5, P6 | 1781 / 1888 / 1648 / 1141 / 81 |
| A's median index moves outside the middle pair | P1, P2, P5, P6 | 938 / 938 / 1158 / 76 |
| B's span drops the outermost pair | P1, P7 | 1812 / 11 |
| C drops the column term | P1, P2, P7 | 1580 / 1580 / 11 |
| C searches only cells that contain a home | P1 | 131 |
| transpose reads `(r, c)` instead of `(c, r)` | *bounds panic* | — |
| **A's median convention `n/2` → `(n-1)/2`** | **nothing — and correctly so** | **0** |

Three rows are worth reading.

**The last row is not a gap in the suite.** It is the mutation everyone expects
to fire, and it does not, because it is not a bug: for a sum of absolute
deviations *every* point between the two middle elements is a minimiser, both
conventions included, so they return the identical total. Verified separately
over 20,000 random sorted lists — `(n-1)/2` and `n/2` agree with each other and
with an exhaustive minimum on every one. This kata's prose originally claimed
the convention was load-bearing and that arm B would catch a slip in it. That
claim was false, the mutation table is what caught it, and the comment in
`differential.kara` now says so. What *is* load-bearing is landing inside the
middle pair at all — row 3, an index one step outside it, fires on 938 cases.

**Row 6** is why the brute-force arm searches cells nobody lives in. Restricting
it to occupied cells still returns the right answer on 96% of grids, because the
optimum usually *is* at a home. It is caught 131 times, and those 131 are the
whole point: "the meeting point must be a home" is a plausible false belief that
the other two arms avoid silently and neither of them tests.

**Row 7** is caught by Kāra's bounds check rather than by any property —
transposing with swapped indices reads out of range on a non-square grid and the
program dies at `at()`. Recorded as caught, but honestly labelled: the
differential did not earn that one.

## Benchmarks

Build 400 grids of 128×128 at 10% density once, then punch 30 median-solve
passes — `build-once + punch` ([BENCHMARKS.md](../../../BENCHMARKS.md)). The
coordinate buffers are allocated once at worst-case capacity and reused by
resetting a logical length, so nothing allocates in the timed loop. All five
languages print `checksum 258938743`.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each. See [BENCHMARKS.md](../../../BENCHMARKS.md) for methodology and caveats.

| | mean | vs kara |
|---|---:|---:|
| c (`-O3 -march=x86-64-v3`, matched ISA) | 582.9 ms | 0.86× |
| c (`-O3`) | 620.8 ms | 0.91× |
| rust (`-O`) | 655.2 ms | 0.96× |
| rust (`-O -C target-cpu=x86-64-v3`, matched ISA) | 668.4 ms | 0.98× |
| **kara** (codegen, seq) | **679.3 ms** | **1.00×** |
| rust (`-O -C overflow-checks=on`, equal safety) | 706.5 ms | 1.04× |
| go | 768.2 ms | 1.13× |
| python | 30.775 s | 45.3× |

This is the closest the corpus has come on a compute lane. Kāra is **ahead of Go
by 1.13× and ahead of equal-safety Rust by 1.04×**, and behind unchecked
`rustc -O` by only 1.04× and `clang -O3` by 1.09×, while carrying bounds checks
on every one of the 393 million grid reads that C's raw indexing does not.

### Two things ruled out, each measured

- **Not the strided scan.** The column-major pass touches a new cache line on
  every read, so it looks like the obvious cost. Rewriting it row-major — same
  cells, same comparison, nothing else changed — moves clang by **1.2%**
  (620.8 → 613.3 ms) and karac not at all (679.3 → 696.3 ms, the wrong way, and
  inside noise). A 128×128 grid of bytes is 16 KiB and stays L1-resident in
  either order; a 128-byte stride inside a resident block is what a prefetcher
  is for. The cost is the per-cell compare and the deviation loop.
- **Not auto-parallelism.** The default build measures 667 ms against
  `KARAC_AUTO_PAR=0`'s 677, and user time tracks wall in both, so the timed
  build is single-threaded.

### The winner depends on the grid size, and the sign flips

Shrinking to 32×32 grids while holding the total cell count fixed (6,400 grids
instead of 400) **reverses the order**: kāra 643.4 ms, `clang -O3` 691.3 ms —
Kāra ahead by 1.07×, where at 128×128 clang leads by 1.09×.

Stated carefully, because the probe changes two things at once: the grid count
rises with the shrink, so this varies *work per grid* (k ≈ 102 versus k ≈ 1638
homes) as well as footprint, and it does **not** isolate cache residency. What it
does establish is that the ranking on this workload is not a fixed property of
the two compilers — it moves with the shape of the input, the same lesson
[#300](../300-longest-increasing-subsequence/) reached from the opposite
direction when its branchless-versus-branchy winner flipped on the data
distribution alone.

### Elsewhere

| | kara | c | rust | go |
|---|---:|---:|---:|---:|
| binary size | 341.5 KiB | 15.7 KiB | 3863.5 KiB | 2179.0 KiB |
| compile (cold) | 413.6 ms | 106.6 ms | 167.9 ms | — |
| peak RSS | 8.8 MiB | 7.9 MiB | 8.4 MiB | 8.1 MiB |

Python's peak RSS is 14.2 MiB.

## Running it

```bash
karac run   best_meeting_point.kara
karac build best_meeting_point.kara && ./best_meeting_point
karac run   best_meeting_point_pairs.kara
karac run   best_meeting_point_brute.kara
karac run   --interp differential.kara
python3     best_meeting_point.py
KARA_BENCH_INCLUDE_PY=1 BENCH_OUT=results.container-x86.json bash bench/bench.sh
```
