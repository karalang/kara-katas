# 973. K Closest Points to Origin

Given an array of `points` where `points[i] = [xi, yi]` represents a
point on the X-Y plane and an integer `k`, return the `k` closest points
to the origin `(0, 0)`.

The distance between two points on the X-Y plane is the Euclidean
distance, `sqrt((x1 - x2)^2 + (y1 - y2)^2)`.

You may return the answer in any order. The answer is guaranteed to be
unique (except for the order that it is in).

```
points = [[1,3],[-2,2]],        k = 1  ->  [[-2,2]]
points = [[3,3],[5,-1],[-2,4]], k = 2  ->  [[3,3],[-2,4]]
```

**Constraints:** `1 <= k <= points.length <= 10^4`;
`-10^4 <= xi, yi <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `k_closest.kara` ★ | sort by distance: a point's distance orders points the same way as its square, x^2 + y^2, which stays an integer; a copy of the points is sorted by that square and the first k kept, and since the k closest are unique no tie straddles the cut. O(n log n) |
| `k_closest_heap.kara` | a heap of the k best: a largest-first `PriorityQueue` holds the k closest points seen so far, keyed by squared distance, and each further point closer than the farthest of them takes its place. O(n log k) |
| `k_closest_select.kara` | quickselect: a copy is partitioned in place, Hoare's way, around the middle point's squared distance, and only the side that holds place k is partitioned again until the first k places hold the k closest. O(n) on average |
| `k_closest_threshold.kara` | binary search on the distance, with no reordering: the k-th smallest squared distance is the least value with at least k points at or within it, found between 0 and the largest squared distance in at most 28 counting passes; exactly k points lie within it, kept in input order. O(n log(max distance)) |
| `k_closest_tree.kara` | a sorted map of rings: a `SortedMap` from squared distance to the points at that distance, read back nearest first until k points are taken. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines. The first ten are LeetCode's two
examples and eight more, each answer sorted since any order is
accepted: a lone point at the origin; four points at distance 1 and a
farther one, with k = 4 and k = 5; a corner of the range against
another corner; the two far corners and the origin with k = n; a ring
of three points at distance 5 between a nearer and a farther one, with
k = 1 and k = 4; and a point given twice. The last three are counts
and checksums over random cases: 300 of up to 12 points with
coordinates from -5 to 5 (1,278 points kept), 3,000 of up to 40
points from -100 to 100 (32,748 kept), and 4 of 10^4 points over
LeetCode's whole range (34,553 kept). Each case takes a random k from
those whose k closest points are unique. `k_closest.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a point is among the k closest when fewer than k points are
strictly closer than it. It checks 3,200 cases: 3,000 of 1 to 30
points with coordinates within 1, 2, 3, 10 or 100 of zero, so that many
points share a distance, against the statement, and 200 of 100 points
over LeetCode's whole range against the other properties. Each case
takes a random k from those whose k closest points are unique, and
every answer is sorted before it is compared.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 cases |
| P2 | the input rotated by a random amount gives the same answer |
| P3 | turning the plane a quarter, or mirroring it in the diagonal, turns or mirrors the answer |
| P4 | k = n gives every point, and the answer for the next smaller k whose closest points are unique lies within this one |
| P5 | dropping the last point keeps the answer when it is not in it, and otherwise gives the answer for k - 1 without it |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 65992 points: 36354 kept, checksum 352970256,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (15.8 s)
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one point too few kept | P1 3000, P2 567, P4 3200, P5 120, P6 3200 |
| M2 | ★: y counted unsquared | P1 1941, P2 289, P3 2377, P5 42, P6 2139 |
| M3 | ★: distance taken as \|x\| + \|y\| | P1 617, P2 228, P5 13, P6 783 |
| M4 | heap: a farther point taking the top's place | P1 2303, P2 2004, P3 93, P5 378, P6 2501 |
| M5 | heap: the closest on top | P1 1934, P2 1955, P3 144, P5 387, P6 2131 |
| M6 | heap: the top never dropped | P1 2188, P2 1605, P5 446, P6 2386 |
| M7 | select: y counted unsquared | P1 1944, P2 338, P3 2385, P5 197, P6 2142 |
| M8 | select: the left side cut one short | P1 965, P2 1432, P5 1117, P6 1126 |
| M9 | select: the last point never partitioned | P1 1104, P2 1513, P5 1219, P6 1217 |
| M10 | threshold: more than k points needed within | P1 2303, P5 258, P6 2501 |
| M11 | threshold: the k-th point left out | P1 3000, P4 3200, P5 307, P6 3200 |
| M12 | threshold: the upper bound moved one past | P1 1047, P5 320, P6 1124 |
| M13 | tree: one point too many taken | P1 2303, P2 489, P6 2501 |
| M14 | tree: a ring replaced, not added to | P1 1743, P2 1235, P4 2086, P5 1180, P6 1743 |
| M15 | tree: rings keyed by x^2 - y^2 | P1 2217, P2 477, P3 2494, P5 66, P6 2415 |

P1 and P6 kill all fifteen, P5 fourteen (all but M13), P2 twelve (all
but the three threshold edits), P3 five (M2, M4, M5, M7, M15) and P4
three (M1, M11, M14). The threshold arm's answer is the set of points
within a distance worked out from counts, which no reordering of the
input can change, edited or not, so P2 cannot see its edits. P3 sees an
edit that stops treating x and y alike (M2, M7, M15), or the heap's
edits, whose answers depend on how the heap breaks ties between equal
distances by coordinates, which a turn of the plane changes. P4 sees an
edit that keeps the wrong number of points when k = n.

Ten other edits were tried and set aside. Seven were sound but beyond
three an arm: ★ keeping the k farthest and sorting by x alone; heap
counting y unsquared; threshold taking its upper bound from x alone and
counting points strictly within; tree swapping the coordinates on the
way out and taking the distance as |x| + |y|. One was equivalent:
select moving on when place k is the last of the left side, rather
than one before it, since everything up to that place is then at or
below the pivot and everything after it at or above, so the first k
places already hold the k closest. Two crashed and were not counted:
heap holding one point too few peeks into an empty heap when k = 1
(`called unwrap() on None`), and select making no swap runs its
right-hand index off the front (`index out of bounds`).

## Verification

Every arm prints the same output as `k_closest.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 0.63 s (★) to 2.8 s (heap), and the differential 15.8 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 100 sets of 1,000 random points over LeetCode's
whole range once, each with a k whose k closest points are unique. In
each of 100 rounds it runs the ★ arm on every set, each round starting
from a different one, and folds every point kept into a checksum by a
sum of squares, since the order of the answer is free and the
languages' sorts may order equal distances differently. Every
implementation prints `100 rounds over 100 sets of 1000 points:
4796700 points kept, checksum 34008162`. Each call copies its set and
sorts the copy by squared distance: Kāra and Rust with `sort_by_key`,
C with `qsort` and a comparator, Go with `sort.Slice` and Python with
`sorted` and a key.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.18 to 1.37 s | 1.28 s |
| Rust (`rustc -O`) | 0.353 to 0.513 s | 0.397 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.431 to 0.599 s | 0.463 s |
| Go | 1.69 to 1.82 s | 1.77 s |
| Python | 2.96 s | |
| Kāra (`karac build --mir`) | 0.591 to 0.653 s | 0.608 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 4.9 times
Kāra's: `sorted` with a key runs in C and works out each key once.

v2 took 1.31 times Rust's median time under overflow checks and 0.47
times C's. Under valgrind's cachegrind v2 ran 3,860 million
instructions and 906 million branches with 12.6 million mispredicted,
Rust with overflow checks 3,742 million, 936 million and 24.0 million,
and C 5,723 million, 980 million and 58.5 million, 190 million of its
branches indirect: `qsort` calls its comparator through a pointer for
every comparison, where v2 and Rust each ran under a million indirect
branches. Go's `sort.Slice` likewise calls a closure for every
comparison; Go was not run under cachegrind.
