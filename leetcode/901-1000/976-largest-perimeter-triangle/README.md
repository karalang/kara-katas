# 976. Largest Perimeter Triangle

Given an integer array `nums`, return the largest perimeter of a
triangle with a non-zero area, formed from three of these lengths. If
it is impossible to form any triangle of a non-zero area, return `0`.

```
nums = [2,1,2]     ->  5
nums = [1,2,1,10]  ->  0
```

**Constraints:** `3 <= nums.length <= 10^4`; `1 <= nums[i] <= 10^6`.

## Approaches

| file | mechanism |
|---|---|
| `largest_perimeter.kara` ★ | sort and scan from the top: three lengths a <= b <= c make a triangle of non-zero area exactly when a + b > c, and the best triangle whose longest side is c uses the two next longest, so the sorted lengths are walked from the top and the first consecutive three that work are the answer. O(n log n) |
| `largest_perimeter_heap.kara` | a heap of lengths: the same walk, taking the lengths one at a time from a largest-first `PriorityQueue` instead of sorting them all. A failing run grows at least like the Fibonacci numbers, so about 30 lengths are ever taken. O(n + 30 log n) |
| `largest_perimeter_scan.kara` | the longest three by scanning: one pass finds the positions of the three longest lengths still in play, and if they fail the longest is struck out and the pass repeated; with no length above 10^6, at most 28 passes fail. O(30 n) |
| `largest_perimeter_multiset.kara` | a sorted multiset: a `SortedMap` counts each length, the counts are read back longest first into a list, one entry per copy, and each length as it arrives is tested as the shortest side under the two before it. O(n log n) |
| `largest_perimeter_top32.kara` | every triple of the 32 longest: a run of 29 failures would need a length past Fibonacci's 832040 and 1346269, above 10^6, so the answer lies among the 31 longest. A short list keeps the 32 longest as the lengths stream past, and every triple of it is tried, without assuming which triple wins. O(32 n + 32^3) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines. The first ten are LeetCode's two
examples and eight more: [3, 2, 3, 4] (10); [3, 6, 2, 3] (8); three
equal sides; [1, 2, 3], whose only triple is flat (0); three sides of
10^6; [10^6, 1, 1, 999999, 2], whose best triangle has a short side
of 2 (2,000,001); the 30 Fibonacci numbers up to 832040, no three of
which make a triangle (0); and the same with 2, 2 and 3 added, where
the best is 3, 3 and 5 (11). The last three are totals and checksums
over random lists: 300 of up to 12 lengths up to 10 (perimeters
6,806), 3,000 of up to 60 lengths up to 1,000 (8,034,630), and 4 of
10^4 lengths up to 10^6 (11,997,771). `largest_perimeter.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every three lengths, kept when each is shorter than the
other two together, the largest sum kept. It checks 3,200 lists: 3,000
of 3 to 30 lengths against the statement, and 200 of 300 lengths up to
10^6 against the other properties. Of the 3,000, four in five are
random lengths up to 5, 30, 1,000 or 10^6, and every fifth is a chain
in which each length is at least the sum of the two before it, so that
no three of it make a triangle, stopping below 10^6, followed by up to
three short lengths that may make one. Random lengths almost always
hold a triangle among the longest few; the chains make every arm walk
down to the bottom.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 lists |
| P2 | the order of the lengths does not matter: the list rotated by a random amount gives the same perimeter |
| P3 | every length doubled doubles the perimeter, when the doubled lengths stay within 10^6 |
| P4 | three more copies of the longest length make the best triangle, 3 times the longest; one more random length never shortens the best perimeter |
| P5 | a length equal to the two longest together is never in a triangle, so adding it changes nothing, when it is within 10^6 |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 109405 lengths: perimeters total 2088058446,
checksum 533807600, 95000 checks over 5 arms: 0 failures` under
`karac __mir-run` (20.1 s) and `karac __mir-llvm-run`, and the same
under `karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty-one edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a flat triangle allowed | P1 553, P5 2346, P6 553 |
| M2 | ★: the three shortest never tried | P1 87, P6 87 |
| M3 | ★: the scan from the shortest | P1 2910, P4 3199, P6 3110 |
| M4 | heap: the longest never dropped | P1 461, P5 1788, P6 461 |
| M5 | heap: the middle side counted for the longest | P1 2156, P6 2356 |
| M6 | heap: the wrong side tested | P1 642, P5 2346, P6 642 |
| M7 | scan: the third place never shifted down | P1 1215, P2 1356, P6 1345 |
| M8 | scan: the shortest side counted twice | P1 2106, P6 2306 |
| M9 | scan: a new length never placed below the second | P1 1836, P2 2267, P4 1602, P6 2036 |
| M10 | multiset: each length once | P1 977, P4 3200, P6 977 |
| M11 | multiset: one copy too many of each length | P1 2621, P5 2346, P6 2821 |
| M12 | multiset: the three longest never tested | P1 2115, P5 1545, P6 2315 |
| M13 | top32: the list kept shortest first | P1 642, P2 191, P4 217, P5 2346, P6 842 |
| M14 | top32: only the 20 longest kept | P1 147, P5 15, P6 147 |
| M15 | top32: only the first 32 lengths kept | P2 191, P4 217, P6 200 |

P6 kills all fifteen, P1 fourteen (all but M15), P5 seven (M1, M4, M6,
M11, M12, M13, M14), P4 five (M3, M9, M10, M13, M15), P2 four (M7, M9,
M13, M15) and P3 none. Every answer is a sum of three input lengths
chosen by comparing lengths and sums of two, and doubling every length
keeps every comparison, so no edit here can tell the doubled list from
the original; P3 guards against an arm that adds or compares against a
constant. M15 escapes the statement because P1's lists hold at most 33
lengths, and only P2's rotation moves a long length past the first 32;
P4's three extra copies of the longest do the same. M14 survived an
earlier differential whose chains could stop short of failing to the
end: on random lengths the answer sits among the longest few, and only
a list that fails far down reaches the 21st longest.

Sixteen other edits were tried and set aside. Thirteen failed exactly
the same checks as a kept one: a flat triangle allowed in the heap,
scan, multiset and top32 arms, as M1; the heap taking the shortest
first, scan finding the three shortest and the multiset reading the
lengths shortest first, as M3; scan striking out the shortest or the
middle of the three, and top32 keeping only the three longest, as M4;
top32 never testing the last kept length as the shortest side, as M2;
the multiset counting the middle side for the longest, as M5; and the
multiset taking each length in at the front of its list, as M6. Three
were sound but beyond three for ★: the longest never the longest side,
and the middle side counted twice in the test; and one beyond three for
top32, keeping the last triangle found rather than the largest.

## Verification

Every arm prints the same output as `largest_perimeter.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 0.36 s (★) to 6.7 s (top32, which tries
every triple of 32), and the differential 20.1 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

`multiset` was first written with `counts.insert(x, *c + 1)`, where
`c` came from `counts.get(x) ?? 0`. `karac` refused the `*` with a
diagnostic saying the value is a copied `i64`, so drop the `*`, and
the arm uses `c + 1`.

## Benchmarks

The bench runs the ★ arm in all five languages. The program makes 20
lists of 10,000 random lengths up to 10^6 once. In each of 50 rounds it
runs the arm on every list, each round starting from a different one,
and folds every perimeter into a checksum. Every implementation prints
`50 rounds over 20 lists of 10000 lengths: perimeters total 2999416300,
checksum 720811084`. Each call copies the list and sorts it: Kāra and
Rust with `sort`, C with `qsort` and a comparator, Go with
`slices.Sort` and Python with `sorted`. Random lengths hold a triangle
among the top three almost always, so the time is the copy and the
sort.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.971 to 1.13 s | 1.04 s |
| Rust (`rustc -O`) | 0.200 to 0.260 s | 0.207 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.201 to 0.258 s | 0.219 s |
| Go | 0.719 to 0.782 s | 0.733 s |
| Python | 1.41 s | |
| Kāra (`karac build --mir`) | 0.136 to 0.186 s | 0.141 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 10 times
Kāra's.

v2 took 0.64 times Rust's median time under overflow checks and 0.14
times C's. Under valgrind's cachegrind v2 ran 1,393 million
instructions and 160 million branches with 5.3 million mispredicted,
Rust with overflow checks 1,808 million, 300 million and 11.1 million,
and C 3,844 million, 880 million and 74.0 million, 135 million of its
branches indirect: `qsort` calls its comparator through a pointer. All
of the work is the library sort, so the gap between v2 and Rust is
between their sorts of 10,000 `i64`s; which part of v2's sort saves the
instructions was not measured.
