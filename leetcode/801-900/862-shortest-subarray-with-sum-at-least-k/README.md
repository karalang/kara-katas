# 862. Shortest Subarray with Sum at Least K

Given an integer array `nums` and an integer `k`, return the length of
the shortest non-empty subarray of `nums` whose sum is at least `k`. If
there is no such subarray, return `-1`. A subarray is a contiguous part
of an array.

```
nums = [1], k = 1          ->  1
nums = [1, 2], k = 4       ->  -1
nums = [2, -1, 2], k = 3   ->  3
```

**Constraints:** `1 <= nums.length <= 10^5`; `-10^5 <= nums[i] <= 10^5`;
`1 <= k <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `shortest_subarray.kara` ★ | prefix sums `p`, so a subarray from `i` to `j - 1` sums to `p[j] - p[i]`, and a `VecDeque` of the starts still worth trying, their sums increasing from front to back. At each end `j`, a front start with a sum at most `p[j] - k` gives an answer and leaves, since a later end would only be longer; a back start with a sum at least `p[j]` leaves too, since `j` is a later start with a smaller sum. Each index enters and leaves once. O(n) time and space |
| `shortest_subarray_heap.kara` | every start waits in a min-first `PriorityQueue` keyed by its prefix sum; at each end the starts whose sum is at most `p[j] - k` come off with their lengths. O(n log n) |
| `shortest_subarray_search.kara` | a stack of the starts whose sums are below every later start's, so increasing up the stack; at each end a binary search finds the latest start with a sum at most `p[j] - k`. O(n log n) |
| `shortest_subarray_brute.kara` | from each start, values added one at a time until the running sum reaches `k`. O(n^2) |
| `shortest_subarray_lengths.kara` | a binary search over the answer: "some subarray of length at most L reaches k" only becomes truer as L grows. One L is checked with a sliding-window minimum of the prefix sums, a list of indices with a moving head. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's three examples; eleven
more (a single value that reaches k and one that cannot, a run that
needs every value, a large negative value cutting the array in two, and
seven with negative values between the positive ones); the
15,620 queries over every array of one to five values from -2 to 2 with
k from 1 to 4, of which 6,669 have no subarray and the rest sum to
12,951; and 500 random arrays of up to 100 values from -100 to 100 with
k up to 1,000, with the number that have a subarray and a checksum.
`shortest_subarray.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subarray summed from scratch, shortest lengths first,
and the first length with a sum of at least k returned. Its 17,000
queries are the 15,620 small ones above and 1,380 random arrays of up to
30 values from -20 to 20 with k up to 60; 9,818 of them have a subarray.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | a smaller k never needs a longer subarray |
| P3 | the array reversed gives the same answer |
| P4 | a value added at either end never needs a longer subarray |
| P5 | the answer is 1 exactly when some value reaches k alone |
| P6 | every value and k doubled give the same answer |

It prints `17000 queries, 9818 with a subarray, 469455 checks over 5
arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the back of the deque never pruned | P1 3369, P2 1368, P3 3369, P4 11658, P5 2051, P6 3369 |
| M2 | ★: a length counted one too long | P1 9818, P2 3888, P3 9818, P4 19636, P5 6482, P6 9818 |
| M3 | ★: a sum of exactly k not enough | P1 5861, P3 5861, P4 11722, P5 3570, P6 5861 |
| M4 | heap: the empty prefix never a start | P1 1461, P2 391, P3 1457, P4 1461, P5 603, P6 1461 |
| M5 | heap: the largest sum first | P1 5387, P2 2479, P3 5391, P4 13985, P5 2051, P6 5387 |
| M6 | heap: an end's own value added late | P1 9818, P2 4045, P3 9818, P4 19636, P5 6482, P6 9818 |
| M7 | search: a start with a sum of exactly `p[j] - k` missed | P1 5861, P3 5861, P4 11722, P5 3570, P6 5861 |
| M8 | search: the stack never pruned | P1 1271, P2 397, P3 1270, P4 3275, P5 915, P6 1271 |
| M9 | search: the earliest start taken | P1 1163, P2 333, P3 1198, P4 2326, P5 617, P6 1163 |
| M10 | brute: the last start skipped | P1 596, P2 130, P3 603, P4 596, P5 596, P6 596 |
| M11 | brute: a start's own value left out | P1 9818, P2 4044, P3 9818, P4 19636, P5 6482, P6 9818 |
| M12 | brute: a sum must equal k | P1 2058, P2 2004, P3 2058, P4 4116, P5 1248, P6 2058 |
| M13 | lengths: the window one start too long | P1 3336, P3 3336, P5 2229, P6 3336 |
| M14 | lengths: the bisection steps past mid | P1 1029, P3 1029, P5 401, P6 1029 |
| M15 | lengths: no subarray answered with n | P1 7182, P3 7182, P5 60, P6 7182 |

P1, P3 and P6 kill all fifteen. M3 and M7 are one fault, a sum of
exactly k not counted, and fail the same cases. The mutations that make
the deque or the stack lose its order (M1, M8) fail far fewer queries
than an off-by-one: on small arrays the prefix sums are often already
increasing.

## Verification

Every arm prints the same output as `shortest_subarray.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `43a401a57b`. Under `karac
__mir-run` the arms take under a second and the differential 14 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends run the brute-force arm through `karac run
--legacy --interp`, `karac run --legacy`, `karac build` and a
`KARAC_AUTO_PAR=1` build with the same output. They refuse the other
four arms, the differential and the bench program at a `*` on a `for`
element over `nums.iter()`, or on an entry read from the deque or the
heap, saying the value is not a reference, where v2 yields a reference.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 100,000 values
from -100,000 to 100,000, LeetCode's largest input, built once, with
k = 5,000,000, and 300 rounds that each change one value, find the
shortest subarray, and change the value back. Each round builds the
prefix sums and runs the deque over all 100,001 of them. The C and Go
mirrors keep the deque in an array with a head and a tail, since every
index enters it once; Rust uses `VecDeque`, as Kāra does. Every
implementation prints `300 rounds on 100000 values, k = 5000000: lengths
sum to 280144, checksum 20133142`, the Kāra program under `karac
__mir-run` included, in 144 s.

Spot timings on a shared 4-core container, eight interleaved runs of
each compiled program and one of Python (`bench.sh` timings need a quiet
machine):

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.31 to 0.34 s | 0.31 s |
| Rust (`rustc -O`) | 0.45 to 0.50 s | 0.48 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.50 to 0.57 s | 0.52 s |
| Go | 0.51 to 0.59 s | 0.53 s |
| Python | 5.0 s | |
| Kāra (`karac build --mir`) | 1.06 to 1.19 s | 1.09 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 861's does. The frozen legacy `karac build`
refuses the bench program at the `*` on `nums.iter()`, so there is no
legacy time.

v2 takes 2.1 times Rust's median time under overflow checks, and 3.5
times C's. Under valgrind's cachegrind C runs 0.89 billion instructions,
Rust with overflow checks 2.22 billion and v2 7.50 billion, with 216
million, 420 million and 1,476 million branches; the mispredictions are
alike, 29 to 32 million. Of v2's branches 60 million are indirect, two
for every index the deque sees in the 300 rounds, where C and Rust have
almost none, so the deque's `front`, `back` or the `Option` they return
most likely goes through an indirect jump on each step (not traced). The
comparison with C and Rust waits until after M4.
