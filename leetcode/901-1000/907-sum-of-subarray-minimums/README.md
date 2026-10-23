# 907. Sum of Subarray Minimums

Given an array of integers `arr`, find the sum of `min(b)`, where `b`
ranges over every (contiguous) subarray of `arr`. Since the answer may
be large, return the answer **modulo** `10^9 + 7`.

```
arr = [3,1,2,4]         ->  17    (minimums 3, 1, 2, 4, 1, 1, 2, 1, 1, 1)
arr = [11,81,94,43,3]   ->  444
```

**Constraints:** `1 <= arr.length <= 3 * 10^4` and
`1 <= arr[i] <= 3 * 10^4`.

## Approaches

Each subarray's minimum is credited to one element holding it, and four
arms count, for each element, the subarrays it is credited with.

| file | mechanism |
|---|---|
| `sum_subarray_mins.kara` ★ | how far each element reaches: two passes with a stack of indices whose values rise find, for each element, the last smaller element to its left and the first smaller-or-equal one to its right; it adds its value times the starts times the ends between them. O(n) |
| `sum_subarray_mins_pop.kara` | one pass, adding on the pop: an element is popped by the first element to its right that is not larger, and the element under it on the stack is its left end, so its share is added then; a final value below everything empties the stack. O(n) |
| `sum_subarray_mins_dp.kara` | the sums of the subarrays ending at each place: with `p` the last smaller element to the left, `ending[i] = ending[p] + arr[i] * (i - p)`, and the answer is the sum of `ending`. O(n) |
| `sum_subarray_mins_split.kara` | split at the minimum: the leftmost smallest element of a range is the minimum of every subarray of the range containing it, and the rest lie wholly to one side; a sparse table finds it, and a stack of ranges replaces recursion that can be n deep. O(n log n) |
| `sum_subarray_mins_merge.kara` | the largest elements first: switched on from the largest down, ties from the right, each element joins the runs beside it and is the leftmost smallest of exactly the subarrays made from parts of them and itself. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and six
more (`[1]`, `[2,2,2]`, `[1,2,3,4,5]`, `[5,4,3,2,1]`, `[3,1,3,1,3]` and
`[30000,1,30000]`); for 300 random cases of up to 1,000 numbers up to
3, 100 or 30,000, a checksum of the sums; and three of LeetCode's
largest, 30,000 random numbers, 1 to 30,000 rising, and 30,000 copies
of 30,000. `sum_subarray_mins.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subarray taken, its minimum found afresh, and the
minimums summed. It checks 3,200 random cases: 3,000 of up to 12
numbers against the statement and 200 of up to 200 numbers against the
other properties, with numbers up to 3, 100 or 30,000; 39,790 numbers in
all. Every sum in it, before and after the changes P4 and P5 make, is
below 10^9 + 7, so P2 can compare exact sums.

| | property |
|---|---|
| P1 | the statement's sum, on the small cases |
| P2 | at least the number of subarrays times the least element and at most that times the largest, and at least the sum of the elements |
| P3 | the same sum for the array reversed |
| P4 | three times the sum, modulo 10^9 + 7, for every element tripled |
| P5 | the sum plus the number of subarrays times `c`, modulo 10^9 + 7, for every element raised by a random `c` from 1 to 100 |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 39790
numbers, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: equal elements to the left stopping the reach | P1 924, P2 621, P5 1048, P6 1048 |
| M2 | ★: the last element never an end | P1 3000, P2 1112, P3 2741, P5 3200, P6 3200 |
| M3 | ★: the first element never a start | P1 3000, P2 1084, P3 2741, P5 3200, P6 3200 |
| M4 | pop: the stack never emptied at the end | P1 3000, P2 1753, P3 2765, P5 3200, P6 3200 |
| M5 | pop: an empty stack reaching only to index 1 | P1 3000, P2 1084, P3 2741, P5 3200, P6 3200 |
| M6 | pop: one end too many | P1 3000, P2 763, P3 2771, P5 3200, P6 3200 |
| M7 | dp: the subarrays reaching past `p` dropped | P1 2530, P2 848, P3 2771, P5 2728, P6 2728 |
| M8 | dp: with nothing smaller to the left, one start too few | P1 3000, P2 1084, P3 2741, P5 3200, P6 3200 |
| M9 | dp: the single-element subarrays left out | P1 3000, P2 1900, P5 3200, P6 3200 |
| M10 | split: the table never comparing | P1 2307, P3 2760, P6 2504 |
| M11 | split: one end too few | P1 3000, P2 2609, P3 2709, P5 3200, P6 3200 |
| M12 | split: the element after the minimum lost | P1 2615, P2 1178, P3 2824, P5 2813, P6 2813 |
| M13 | merge: the smallest elements first | P1 2723, P6 2921 |
| M14 | merge: a run's left end never told its length | P1 2202, P2 828, P3 2460, P5 2399, P6 2399 |
| M15 | merge: the run to the right never joined | P1 2615, P2 1291, P3 2642, P5 2813, P6 2813 |

P1 and P6 kill all fifteen; P2 and P5 kill thirteen, P3 twelve and P4
none. Every arm, mutated or not, credits subarrays to elements by
comparing values only and adds each element's value times a count, so
tripling every value triples every answer and P4 cannot fail. M13
switches the smallest elements on first, which makes each element the
maximum of the subarrays it is credited with: it sums the subarray
maximums, which keeps P2's bounds, P3's symmetry and P5's shift, and
only the statement and the agreement see it. M10's table always names
a range's first element, so it sums every subarray's first element,
which also keeps P2 and P5; reversing the array changes that sum, so P3
sees it. M9 drops the single-element subarrays, which reversing does
not change, and P2's lower bound sees it.

No mutant was replaced.

## Verification

Every arm prints the same output as `sum_subarray_mins.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.7 to 2.7 s
each (the split arm, which builds a sparse table, the longest) and the
differential 4.2 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy lanes split. The pop, dp and split arms print the
same output under the legacy interpreter, the legacy JIT and both legacy
builds, with and without auto-par. The ★ arm prints it under the legacy
interpreter, the legacy JIT and the plain legacy build, but the legacy
build with auto-par (`KARAC_AUTO_PAR=1`) prints `300 cases: checksum
307263308` instead of `984924780`, the same wrong value on each of four
runs, with every other line right. Every legacy lane refuses the merge
arm and the differential: `*i` on an element of `.iter()` is rejected,
because legacy's iterator gives the value itself. Legacy is frozen, and
legacy auto-par with it, so none of this is filed.

## Benchmarks

The bench program uses the ★ arm on 1,000,000 numbers from 1 to 30,000,
built once. Each round sums the subarray minimums, folds the sum into a
checksum and changes one number; 40 rounds. Every implementation
allocates its two reach arrays and its stack each round, as the arm
does. Every implementation prints `40 rounds over 1000000 numbers:
checksum 300897406`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.46 to 1.51 s | 1.49 s |
| Rust (`rustc -O`) | 1.24 to 1.38 s | 1.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.26 to 1.35 s | 1.29 s |
| Go | 1.18 to 1.28 s | 1.26 s |
| Python | 21.0 s | |
| Kāra (`karac build --mir`) | 1.18 to 1.27 s | 1.24 s |
| Kāra (legacy `karac build`) | 1.15 to 1.40 s | 1.27 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does.

v2 takes 0.96 times Rust's median time under overflow checks, 0.83
times C's and 0.98 times legacy's. Under valgrind's cachegrind C runs
4.03 billion instructions and 1.06 billion branches, Rust with overflow
checks 4.63 billion and 1.54 billion, v2 4.22 billion and 1.48 billion,
and legacy 4.33 billion and 1.52 billion; each mispredicts 74 to 91
million times, on the stack pops of random values. C is the slowest
even though it runs the fewest instructions; why was not profiled. The
comparison with C and Rust waits until after M4.
