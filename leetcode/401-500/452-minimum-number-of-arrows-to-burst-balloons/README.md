# 452. Minimum Number of Arrows to Burst Balloons

Spherical balloons are taped to a flat wall, and balloon `i` spans the
horizontal diameter `points[i] = [x_start, x_end]`. An arrow shot
straight up from `x` bursts every balloon with `x_start <= x <= x_end`,
and keeps going. Return the minimum number of arrows needed to burst
all the balloons.

```
points = [[10,16],[2,8],[1,6],[7,12]]  ->  2   (x = 6 and x = 11)
points = [[1,2],[3,4],[5,6],[7,8]]     ->  4
points = [[1,2],[2,3],[3,4],[4,5]]     ->  2   (x = 2 and x = 4)
```

**Constraints:** `1 <= points.length <= 10^5`;
`-2^31 <= x_start < x_end <= 2^31 - 1`.

## Approaches

Every arm is `fn find_min_arrow_shots(points: Vec[(i64, i64)]) -> i64`.
Coordinates are `i64`, so the full 32-bit range needs no care, and
balloons of zero width (`x_start == x_end`) are allowed too.

| file | mechanism |
|---|---|
| `min_arrows.kara` ★ | greedy by end: sort by right end; the balloon that ends first is shot at its end, which bursts everything started by then, and the first balloon starting later needs a new arrow. O(n log n) |
| `min_arrows_start.kara` | greedy by start: sort by left end and grow a group while each new balloon starts no later than the smallest right end in the group. O(n log n) |
| `min_arrows_events.kara` | a sweep over opening and closing events, openings first at a tie; when a balloon closes unburst, shoot there and burst every balloon then open. O(n log n) |
| `min_arrows_select.kara` | the plain reference, no sort: repeatedly pick the unburst balloon with the smallest right end, shoot at that end, and mark every balloon covering it. O(n · arrows) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 9 lines: the three LeetCode examples, one
balloon of zero width, nested balloons, the whole 32-bit range, the two
32-bit extremes, a chain of overlaps, and for 300 random sets of 1 to
200 balloons (starts spread over 10, 100, 10,000 or all 2^32 values,
widths up to 0, 5, 50 or 2^31 - 1, clipped at 2^31 - 1) the total
arrows and a checksum. `min_arrows.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on 1 to 8 balloons within 0 to 19, the count is brute force's over every subset of the right ends (some best set of arrows can always be moved right onto right ends) |
| P2 | on 1 to 40 balloons over a mixed range, moving every balloon by up to 1,000 keeps the count |
| P3 | mirroring the balloons about 0 keeps it |
| P4 | listing them in another order keeps it |
| P5 | `k` clusters 1,000 apart, each of 1 to 5 balloons around a shared point, take exactly `k` arrows |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | end: a balloon starting at the arrow needs a new one | P1 477, P3 74, P4 55, P5 1 |
| M2 | end: the balloons are sorted by start | P1 109, P3 228, P4 58 |
| M3 | start: the group's reach grows instead of shrinking | P1 345 |
| M4 | start: a new group reaches only to its first start | P1 651, P3 519, P5 1468 |
| M5 | events: an opening is taken for a closing | P1 1500, P5 1500 |
| M6 | events: a balloon closes one past its end | P1 520 |
| M7 | select: the next arrow follows the earliest start | P1 295, P3 509, P4 190, P5 1390 |
| M8 | select: the arrow goes at the chosen balloon's start | P1 456, P3 268, P4 142, P5 1371 |

P2 sees none of them: every arm, mutated or not, compares positions only
with each other, so moving all the balloons together changes nothing.
P1, the only property with an independent answer, sees all eight; the
others compare an arm with itself. M3 and M6 go wrong only where
balloons touch or nest closely, which P1's small grid has and the wider
sets of P2 to P4 seldom do. M5 marks the label of an opening as `2`,
which the sweep then reads as a closing, so every balloon is counted at
its start.

## Verification

All four arms print the same output as `min_arrows.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm matches under
`karac run --interp`, and the differential prints `0 failures` there.
LLJIT and `karac build` stop in the legacy code generator on the
harness's index into an array literal ("Index operator applied to
non-array type"), in every arm and the differential. The bench program
builds and matches under legacy `karac build`. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 10 random sets of 100,000
balloons once, with starts over the whole 32-bit range and widths up to
99,999, then counts the arrows for each set 10 times; each count copies
and sorts its set. Every implementation prints `10 rounds on 10 sets of
100000: 4539600 arrows, checksum 675396807`, the Kāra program under
`karac __mir-run` included (in 17 s).

The mirrors keep the ★ arm's structure: copy, sort by right end, one
pass. Rust's `sort_by_key` and Go's `slices.SortStableFunc` are stable sorts
like Kāra's; C uses `qsort`, which is not, and the count does not
depend on the order of equal ends. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.0 to 2.1 s |
| Rust (`rustc -O`) | 0.52 to 0.64 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.52 to 0.59 s |
| Go | 3.0 to 3.3 s |
| Python | 5.3 to 5.5 s |
| Kāra (legacy `karac build`) | 1.28 to 1.33 s |

The sort is nearly all the work, so the table compares sorts. C's
`qsort` calls its comparison through a function pointer for every
step. Go's stable sort (`slices.SortStableFunc`) is an insertion sort
on blocks merged in place, O(n log² n); with the older
`sort.SliceStable` the Go program took 11.8 to 12.0 s. The Kāra
program prints the same line under `karac __mir-llvm-run` in 8.2 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

No new findings.
