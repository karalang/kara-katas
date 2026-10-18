# 719. Find K-th Smallest Pair Distance

The distance of a pair of integers a and b is the absolute difference
between a and b. Given an integer array `nums` and an integer `k`,
return the k-th smallest distance among all the pairs `nums[i]` and
`nums[j]` with 0 <= i < j < `nums.length`.

```
nums = [1, 3, 1], k = 1  ->  0   (the pair (1, 1))
nums = [1, 1, 1], k = 2  ->  0
nums = [1, 6, 1], k = 3  ->  5
```

**Constraints:** 2 <= `nums.length` <= 10^4; 0 <= `nums[i]` <=
10^6; 1 <= k <= n * (n - 1) / 2.

## Approaches

A pair's distance depends only on its two values, so three of the arms
sort first. In a sorted list the pairs within d of each other are easy
to count, and the pairs of one number come in order of distance.

| file | mechanism |
|---|---|
| `find_k_th_smallest_pair_distance.kara` ★ | a binary search on the distance, between 0 and the largest number less the smallest; a distance is tested by counting the pairs at most that far apart with two pointers in one pass, and the answer is the least distance with at least k; O(n log n + n log W), W the largest distance |
| `find_k_th_smallest_pair_distance_bisect.kara` | the same search, but each count finds, for every number, how many later numbers lie within the distance by its own binary search in the sorted list; O(n log n log W) |
| `find_k_th_smallest_pair_distance_pairs.kara` | the distance of every pair listed and sorted, and the k-th read off; O(n^2 log n) time, O(n^2) space |
| `find_k_th_smallest_pair_distance_heap.kara` | a smallest-first heap that starts with every adjacent pair and is popped k times, pushing (i, j + 1) after each (i, j), so it always holds the next pair of every i; O((n + k) log n) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the three LeetCode examples; two
numbers far apart and two equal ones; five numbers asked for their
first, fifth and last distance; 400 random numbers up to 10^6 and 400 up
to 10, each asked for the first, middle and last distance; and
300 random arrays of 2 to 41 numbers with a checksum. The heap arm's
last query pops all 79,800 pairs of 400 numbers, which is why the arrays
stop there. `find_k_th_smallest_pair_distance.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which sorts nothing: it takes every pair's distance in turn, counts pair
by pair how many pairs are no further apart, and keeps the least
distance with at least k. 3,000 random arrays are checked, each of 2 to
12 numbers from 0 to at most 20, so equal numbers and equal distances
are common, with a random k.

| | property |
|---|---|
| P1 | the distance is the definition's |
| P2 | the numbers reversed give the same distance |
| P3 | the numbers doubled give twice the distance |
| P4 | the distance is no smaller than the (k - 1)-th, and the last is the largest number less the smallest |

It prints `3000 arrays (536 with a distance of 0), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a distance with enough pairs ruled out itself | P1 906, P3 1270 |
| M2 | ★: each number counted as a pair with itself | P1 2380, P4 2657 |
| M3 | ★: exactly k pairs not taken as enough | P1 860 |
| M4 | bisect: a number exactly d above left out | P1 2175, P3 2175 |
| M5 | bisect: the search capped below the largest distance | P1 496, P4 1879 |
| M6 | bisect: a failed distance ruling out the next one too | P1 1838, P3 2425, P4 1796 |
| M7 | pairs: each number paired with itself | P1 2380, P4 2657 |
| M8 | pairs: signed differences kept | P1 2210, P2 2347, P4 1124 |
| M9 | pairs: the list reversed instead of sorted | P1 1997, P2 1833, P4 2273 |
| M10 | heap: the next pair given the adjacent gap | P1 1553, P4 2523 |
| M11 | heap: one pop too few | P1 1169, P4 1371 |
| M12 | heap: the pair after (i, j) taken as (i + 1, j + 1) | P1 1550, P4 2523 |
| E1 | bisect: the search for later numbers started at the number itself | 0 |
| E2 | ★: the midpoint as lo + (hi - lo) / 2 | 0 |
| E3 | ★: the search started one above the largest distance | 0 |

P1 kills all twelve, and is the only property that sees M3, which wants
more than k pairs: that answers the same for the reversed and the
doubled numbers, never falls below the (k - 1)-th, and still finds the
last distance, since no distance has more pairs than all of them.
P2 sees only M8 and M9, signed differences and a list reversed instead
of sorted, the two whose answer depends on the order of the numbers.
P3 sees only M1, M4 and M6, which go wrong by one in the distance
itself: doubling the numbers doubles every distance but not a step of
one, while an error in the count or in which pairs are listed doubles
with the numbers. P4 misses M1, M3 and M4. M2 and M7 fail the same
checks, since both count each number as a pair with itself. E1 starts
each number's search at the number itself, which is never above itself
plus the distance, so the search ends where it did; E2 takes the
midpoint as lo + (hi - lo) / 2, the same for distances that cannot be
negative; E3 starts the search one above the largest distance, which
never has fewer than k pairs.

## Verification

Every arm prints the same output as
`find_k_th_smallest_pair_distance.py` under `karac __mir-run` (the
v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer) with no error; the differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. The debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the release
build that runs `check` and `__mir-run` are both at kara `a73d3c10ad`,
whose last compiler change is `3c8e763161`. The runtime archives were
built after that change.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms and the differential at
type checking. The arms stop at `next_random(mut seed)` in the harness's
`random_nums`, whose argument is already a `mut ref`, where legacy wants
the marker dropped and design.md § Call-site `mut` markers now requires
it (kara B-2026-10-14-25); the differential stops at `*x` over `iter()`,
since legacy gives those by value where v2 gives references. Legacy
refuses the bench program at `smallest_distance_pair(arrays[a], k)`,
which it reads as moving a vector out of the vector of arrays
(E_INDEX_MOVE_NON_COPY); v2 borrows bare parameters. Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
40 random arrays of 5,000 numbers from 0 to 10^6 once, and in each of
25 rounds asks every array for its k-th smallest distance, with a
different k for each query, summing the answers; each query sorts its
own copy. Every implementation prints `25 rounds of 40 arrays of
5000 numbers: sum 91243591`, the Kāra program under `karac __mir-run`
included (in 37 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.19 to 1.29 s |
| Rust (`rustc -O`) | 0.97 to 1.05 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.89 to 1.12 s |
| Go | 1.17 to 1.25 s |
| Python | 9.7 to 9.9 s |
| Kāra (`karac build --mir`) | 0.91 to 1.06 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 4.5 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is level with Rust, 1.00 s against 1.01 at the medians
of the interleaved runs, and ahead of C (1.23) and Go (1.22). Under
valgrind's cachegrind it runs 3.2 billion instructions against Rust's
3.1 and C's 4.1, and mispredicts 90 million branches against Rust's
93 million and C's 122 million. C's extra instructions include
62 million indirect calls, `qsort` calling its comparison function
through a pointer; each language sorts with its own library sort, so the
sort is not the same algorithm in all five.

## Compiler findings

None new.
