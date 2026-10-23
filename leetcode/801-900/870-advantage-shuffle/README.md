# 870. Advantage Shuffle

You are given two integer arrays `nums1` and `nums2` of the same length.
The advantage of `nums1` with respect to `nums2` is the number of
indices `i` for which `nums1[i] > nums2[i]`. Return any permutation of
`nums1` that maximizes its advantage with respect to `nums2`.

```
nums1 = [2, 7, 11, 15], nums2 = [1, 10, 4, 11]   ->  [2, 11, 7, 15]
nums1 = [12, 24, 8, 32], nums2 = [13, 25, 32, 11] ->  [24, 32, 8, 12]
```

**Constraints:** `1 <= nums1.length <= 10^5`, `nums2.length ==
nums1.length`, `0 <= nums1[i], nums2[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `advantage_shuffle.kara` ★ | greedy from the largest: nums2's values are taken from largest to smallest (its indices sorted by value). The largest value left in nums1 either beats the current one, and then nothing smaller in nums2 needs it more, or it beats nothing left in nums2, and then the current value is beaten by nothing and takes the smallest value left. Two pointers into nums1 sorted. O(n log n) |
| `advantage_shuffle_ascending.kara` | greedy from the smallest: nums1 from smallest to largest against nums2's values from smallest to largest. A value of nums1 that beats the smallest value of nums2 not yet beaten takes it; one that does not beats nothing left and is kept spare, and the values of nums2 never beaten get the spares |
| `advantage_shuffle_sortedmap.kara` | the smallest value that beats it: nums1's values in a `SortedMap` from value to count; each value b of nums2, in its own order, takes the smallest value left above b (`ceiling(b + 1)`), or the smallest value left when none is above it |
| `advantage_shuffle_heap.kara` | a heap of nums2: the ★ greedy with nums2 in a max-first `PriorityQueue` of (value, index) pairs instead of a sorted index list |
| `advantage_shuffle_count.kara` | binary search on the advantage: k wins are possible exactly when nums1's k largest values, in order, beat nums2's k smallest, in order. That holds for k - 1 whenever it holds for k, so the largest such k is found by binary search; nums2's k smallest values then take nums1's k largest in order, and the rest take what is left |
| `differential.kara` | the five arms against the statement read literally, six properties |

LeetCode accepts any permutation that reaches the most wins, and the
arms return different ones, so every arm prints the advantage its answer
reaches, after checking that the answer is a permutation of nums1; none
prints the permutation itself. Every arm prints the same 16 lines:
LeetCode's two examples and ten more (one value each way, every value
equal, nums1 beating nums2 everywhere, the same values in either order,
and LeetCode's extremes, 0 and 10^9); the advantages of 3,000 random
arrays of 1 to 8 values below 10, 8,610 in all; those of 60 random
arrays of up to 1,000 values, either up to 10^9 or below their length,
with a checksum; and two arrays of LeetCode's largest size, 10^5 values,
up to 10^9 (advantage 99,912) and below 100 (98,831). No answer fails to
be a permutation. `advantage_shuffle.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every permutation of nums1, built one position at a time,
the most wins any of them reaches. It checks 1,700 pairs of arrays:
1,500 of 1 to 6 values, below 3 or below 10 so that values repeat,
against the statement, and 200 of up to 60 values, up to 10^9 or below
their length, against the other properties. The ★ arm's advantages sum
to 8,540.

| | property |
|---|---|
| P1 | the answer is a permutation of nums1 |
| P2 | the statement's answer: its advantage is the most any permutation reaches (up to six values) |
| P3 | nums2 in a random order gives the same advantage |
| P4 | nums1 with every value raised by 1 never gives a smaller advantage |
| P5 | a value above every other added to nums1, and one just below it added to nums2, adds exactly one win |
| P6 | nums1 in a random order gives the same advantage |

P5 adds exactly one: pairing the two new values is a win, and in any
pairing the new value in nums2 can only be beaten by the new value in
nums1, so at most one more win is possible than before. (Adding a value
below everything to nums2 instead could add two.)

It prints `1700 pairs of arrays, advantages sum to 8540, 50000 checks
over 5 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the smallest value not used up after a loss | P1 609, P2 447, P3 609, P5 609, P6 609 |
| M2 | ★: nums2 taken from smallest to largest | P2 584, P5 792 |
| M3 | ★: a loss given the largest value left | P2 703 |
| M4 | ascending: a tie taken for a win | P2 427, P4 73 |
| M5 | ascending: a win not counted | P1 1348, P2 1151, P3 1348, P5 857, P6 1348 |
| M6 | ascending: nums1 never sorted | P2 344, P6 384 |
| M7 | sortedmap: a tie taken for a win | P2 601, P3 398, P4 134, P5 107 |
| M8 | sortedmap: a repeated value never used up | P1 387, P2 293, P3 387, P5 387, P6 387 |
| M9 | sortedmap: each value counted twice | P1 1214, P2 1018, P3 1214, P5 1538, P6 1214 |
| M10 | heap: smallest first | P2 584, P5 792 |
| M11 | heap: every index taken as 0 | P1 1395, P2 1208, P3 1407, P4 1, P5 698, P6 1395 |
| M12 | heap: a tie taken for a win | P2 431, P4 77 |
| M13 | count: a tie taken for a win | P2 238, P4 39 |
| M14 | count: the search steps two below a failed k | P2 232, P5 208 |
| M15 | count: nums2 ordered from largest | P2 807, P4 16, P5 688 |

P2 kills all fifteen. The four tie mutations (M4, M7, M12, M13) each
count a tie as a win, so they give a value to a position it does not
beat; P4 catches all four as well, where the arm with nums1 raised by 1
reaches fewer wins than with nums1 as it was. M2 and
M10 are one fault in two arms, nums2 from the wrong end, and fail the
same pairs. The first M8 and M9 tried (a value removed from the map
whatever its count, and repeats counted once) made the arm index the map
at a key no longer there, which panics rather than failing a property;
they were replaced with the two above, which only miscount.

## Verification

Every arm prints the same output as `advantage_shuffle.py` under
`karac __mir-llvm-run` and under `karac __mir-llvm-asan`
(AddressSanitizer) with no error; the differential prints its line under
both and under `karac __mir-run`. `karac check` passes all five arms, the
differential and the bench program. `karac run` and a `karac build
--mir` binary print the same output for every arm and the differential.
The release build and the runtime archives are at kara `e903d5b111`.

Under `karac __mir-run` four arms print the same output in 3 to 17 s
and the differential in 5 s, but the SortedMap arm runs past 300 s: the
MIR interpreter copies and orders every key of the map on each
`ceiling` call, so the 2 x 10^5 queries of the two largest cases are
quadratic (kara `B-2026-10-23-1`, 16,000 queries take 37.5 s there and
0.4 s compiled). The arm is left as written; its corpus entry will read
`timeout` until that row is fixed.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak. As a control, a
two-node `shared struct` cycle run the same way reports a 48-byte leak.

The frozen legacy backends refuse the ★, ascending and SortedMap arms,
the differential and the bench program at a `*` on a `for` element,
saying the value is not a reference, where v2 yields a reference. The
count arm prints the same output on all four legacy lanes. The heap arm
prints it under the legacy interpreter but stops with "vec index out of
bounds" at `sorted[lo]` under the legacy JIT, `karac build` and
auto-par. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 20 pairs of
arrays of 10^5 values up to 10^9, LeetCode's largest, from the same
generator, counting the wins and a checksum of each answer weighted by
position. The answer depends on how ties in nums2 are ordered, so every
language sorts nums2's indices stably by value, largest first: Kāra's
`sort_by_key`, Rust's `sort_by_key`, Go's `sort.SliceStable`, Python's
`sorted`, and in C a `qsort` that breaks ties by index. Every
implementation prints `20 pairs of 100000 values: 1995018 wins, checksum
300345002`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.56 to 0.64 s | 0.61 s |
| Rust (`rustc -O`) | 0.22 to 0.28 s | 0.24 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.26 to 0.33 s | 0.27 s |
| Go | 1.39 to 1.51 s | 1.44 s |
| Python | 6.6 s | |
| Kāra (`karac build --mir`) | 0.38 to 0.48 s | 0.41 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 869's does. Legacy refuses the bench program
(above), so it has no lane here.

v2 takes 1.5 times Rust's median time under overflow checks, 0.67 times
C's and 0.28 times Go's. C pays for `qsort`'s comparison through a
function pointer, and Go most likely for `sort.SliceStable`'s calls of
its closure and reflection-based swaps (inferred, not profiled). Built for x86-64-v3, the ISA `karac build`
targets, C and Rust take the same time (0.61 s and 0.28 s), so the ISA
is not the difference here. Under valgrind's cachegrind C runs 2.39
billion instructions, Rust with overflow checks 1.57 billion and v2 2.18
billion; under callgrind three quarters of v2's are in two functions of
the closure-keyed `sort_by_key`, about 1.6 billion, where Rust's stable
sort of the indices by key takes about 0.7 billion. Sorting nums1 itself
costs v2 38 million, in `karac_mir_sort_int`. The comparison with C and
Rust waits until after M4.
