# 757. Set Intersection Size At Least Two

Each interval `[a, b]` holds the integers from a to b. Return the size
of the smallest set of integers that has at least two members in every
interval.

```
[[1, 3], [3, 7], [8, 9]]          ->  5   for example {2, 3, 4, 8, 9}
[[1, 3], [1, 4], [2, 5], [3, 5]]  ->  3   for example {2, 3, 4}
[[1, 2], [2, 3], [2, 4], [4, 5]]  ->  5   for example {1, 2, 3, 4, 5}
```

**Constraints:** 1 to 3,000 intervals; 0 <= a < b <= 10^8.

## Approaches

Points as far right as an interval allows serve the most intervals that
end later, so taking the intervals by their right ends and choosing
greedily is optimal; one arm works the mirror image of that from the
left ends.

| file | mechanism |
|---|---|
| `intersection_size_two.kara` ★ | sort by right end, the narrowest first among equal ends; keep the two largest points chosen, adding the right end, or the two rightmost points, when an interval holds fewer than two; O(n log n) |
| `intersection_size_two_points.kara` | sort by right end only; keep every chosen point in a sorted list, count the ones an interval holds by binary search, and add its rightmost points not yet chosen |
| `intersection_size_two_reverse.kara` | sort by left end, the widest first among equal starts, and work from the last: each interval owes points, taken at its start and just after, and each is credited to every earlier interval that still owes one and reaches it; O(n^2) |
| `intersection_size_two_fold.kara` | the ★ greedy as a `fold` carrying a tuple, sorted by comparing the pairs (end, -start) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 10 lines: the three LeetCode examples; one
interval, short and as long as allowed; one interval three times; five
nested intervals; a chain of intervals that share their ends, and one
that shares none; and 200 random sets of up to 400 intervals up to
10^8, with the total of their answers and a checksum.
`intersection_size_two.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tries every subset of the points 0 to 9 and returns the size of
the smallest that holds two points of every interval. 1,500 random sets
of one to six intervals within 0 to 9 are checked against it, and
300 sets of up to 400 intervals up to 10^8 against the other properties.

| | property |
|---|---|
| P1 | the answer is the definition's (the 1,500 small sets) |
| P2 | moving every interval right by the same random amount, up to 10^8 at the far end, changes nothing |
| P3 | nor does a mirror, each interval [a, b] made [m - b, m - a] |
| P4 | one more random interval needs no fewer points and at most two more |

It prints `1800 interval sets (122109 points), 4 arms, 27600 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the widest first among equal ends | P1 5, P3 9, P4 1 |
| M2 | ★: an interval starting at the largest point taken as holding neither | P1 371 |
| M3 | ★: after one new point, the second largest taken as its left neighbour | P1 50, P3 78, P4 9 |
| M4 | points: a point at the start not counted | P1 658, P3 93 |
| M5 | points: the intervals taken by left end | P1 186, P3 228, P4 84 |
| M6 | points: every other point tried | P1 303, P3 139, P4 1 |
| M7 | left ends: the narrowest first among equal starts | P1 4, P3 9, P4 2 |
| M8 | left ends: a point at an earlier interval's right end not counted | P1 607, P3 196 |
| M9 | left ends: the interval just before never credited | P1 1119, P3 239, P4 44 |
| M10 | fold: two new points put at the ends | P1 167, P3 11, P4 6 |
| M11 | fold: an interval starting at the second point taken as holding one | P1 337, P3 264 |
| M12 | fold: the old second point kept after one new point | P1 94, P3 180, P4 3 |
| E1 | ★: an interval past the largest point also tested against the second | 0 |
| E2 | left ends: the interval itself also credited | 0 |
| E3 | fold: the second point started at -5 | 0 |

P1 kills all twelve. P2 kills none: no edit here treats one coordinate
unlike another, so moving every interval by the same amount leaves each
arm's count as it was, edit or not; P2 is there for arithmetic far from
0, which every arm does right. P3 sees every edit but M2, and P4 sees
M1, M3, M5, M6, M7, M9, M10 and M12. M1 and M7, the orders among equal
ends and among equal starts, are seen least often, since they matter
only when two intervals share an end or a start. E1 also requires an
interval past the largest point to be past the second, which it always
is, the second being smaller; E2 credits the last interval with its own
points, but the points it owes are counted out once, before the
crediting starts, and its count is never read again; E3 starts the
fold's second point at -5 rather than -1, and every start is at least
0, so neither is ever held.

## Verification

Every arm prints the same output as `intersection_size_two.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a62eacd307`, whose last compiler change is `7d736aae75`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept every program here: each arm prints
the same output under the legacy interpreter, `karac run`, `karac build`
and an auto-par build, and the differential prints its line under the
legacy interpreter and `karac build`.

## Benchmarks

The bench program uses the ★ arm in all five languages, on 2,000 random
sets of 3,000 intervals, the most LeetCode allows, each up to
100,000 wide within 0 to 10^8, adding up the answers and a checksum. The
sort is presumably most of the time (inferred, not profiled). Every
implementation prints `2000 sets of 3000 intervals: 8243783 points in
all, checksum 498514710`, the Kāra program under `karac __mir-run`
included (in 45 s). Kāra, Rust, Go and Python hold the intervals as a
vector of two-element vectors; C holds them as pairs in one array and
sorts with `qsort`, and Go sorts with `sort.Slice`.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.52 to 0.70 s |
| Rust (`rustc -O`) | 0.57 to 0.63 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.55 to 0.63 s |
| Go | 1.19 to 1.29 s |
| Python | 4.5 to 4.9 s |
| Kāra (`karac build --mir`) | 0.68 to 0.96 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
3.0 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.84 s,
against C's 0.67, Rust's 0.59 (0.60 under overflow checks) and Go's
1.26. Under valgrind's cachegrind v2 runs 7.9 billion instructions,
about Rust's 7.8 billion, against C's 3.7 billion, whose `qsort` calls
its comparison through a pointer and mispredicts more branches. The
legacy build of the same program ran 0.92 to 1.22 s, a median of 1.19 s
in the interleaved runs, so v2 takes about 0.7 times legacy's time,
inside M2's limit of twice legacy; new katas' benches are outside M2's
frozen set in any case. The comparison with C and Rust waits until after
M4.

## Compiler findings

None new. `Ordering` has no `then`, so the fold arm compares the pairs
(end, -start) instead; design.md's `Ordering` defines only the `is_*`
helpers, so that is not a bug.
