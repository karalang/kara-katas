# 1509. Minimum Difference Between Largest and Smallest Value in Three Moves

You are given an integer array `nums`. In one move, you can choose one
element of `nums` and change it to any value. Return the minimum
difference between the largest and smallest value of `nums` after
performing at most three moves.

```
nums = [5, 3, 2, 4]               ->  0   (change 5, 3, 4 to 2)
nums = [1, 5, 0, 10, 14]          ->  1   (change 10, 14 and 0 to 1, 5 left)
nums = [3, 100, 20]               ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`; `-10^9 <= nums[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `moves.kara` ★ | three moves are best spent on three of the ends, so sort a copy, and of the four ways to take three numbers off the two ends (three low, two low and one high, one and two, three high), keep the narrowest rest: `sorted[n - 4 + low] - sorted[low]`. O(n log n) |
| `moves_scan.kara` | no sort: one pass keeps the four smallest numbers, and the four largest negated, in order by insertion, then the same four ways. O(n) |
| `moves_heap.kara` | two heaps of four: a largest-first `PriorityQueue` keeps the four smallest and a smallest-first one the four largest, each dropping its top when a fifth arrives. O(n log 4) |
| `moves_iter.kara` | sorted, then the first four zipped with the last four (`zip` with `skip(n - 4)`), each pair's gap, and the least by `min` |
| `moves_solution.kara` | LeetCode's Rust template, `pub fn min_difference(mut nums: Vec<i32>) -> i32`, the ★ arm: blocked by B-2026-11-08-11 |
| `differential.kara` | the four arms that check against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more, then a checksum of the answers for 3000 arrays of 1 to 10 numbers
within 50, 300 of 1 to 1000 within 10^9, and 3 of 1 to 100000 within
10^9. `moves.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms that check and the
statement read literally: for every choice of three numbers to change,
each changed number can take a value of the rest, so the spread is that
of the rest; keep the least. It checks 3000 arrays of 1 to 9 numbers
from -20 to 20. Every random choice of a problem is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the numbers in another order leave the answer |
| P3 | every number shifted by the same amount leaves the answer |
| P4 | every number negated leaves the answer |
| P5 | every number tripled triples the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 687859055, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property. The Rust arm joins it
once it checks.

## Mutation testing

Twenty-four edits to the differential, five to seven to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Twelve are kept.
Fifteen are killed by a property and four by a crash, each the same way
under both backends; five survive, all equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only three of the four ways tried | P1 413, P4 850, P6 413 |
| M2 | ★: each way's gap biased by its index | P1 1122, P4 1565, P5 1099, P6 1122 |
| M3 | ★: sorted by size, not value | P1 1573, P2 242, P3 1496, P4 1635, P6 1573 |
| M4 | scan: the low four paired with the high four the wrong way round | P1 1657, P6 1657 |
| M5 | scan: the largest kept by absolute value | P1 1261, P3 1436, P4 1604, P6 1261 |
| M6 | scan: the smallest rounded down to even | P1 851, P3 993, P4 1084, P5 864, P6 851 |
| M7 | heap: the smallest capped at 15 | P1 42, P3 854, P4 92, P5 298, P6 42 |
| M8 | heap: the largest pushed one too high | P1 1662, P5 1662, P6 1662 |
| M9 | iter: the last five zipped, not the last four | P1 1570, P6 1570 |
| M10 | iter: the widest gap kept, not the narrowest | P1 1662, P6 1662 |
| M11 | iter: four numbers answered 0, not only up to four | P1 281, P6 281 |
| M12 | iter: the answer rounded down to even | P1 865, P5 865, P6 865 |

P1 and P6 kill all twelve, P4 six, P3 four, P5 five, and P2 one: M3, the
one edit whose answer depends on the order the numbers come in (equal
sizes keep their order). P3 and P4 see the edits that look at a number's
value rather than its place among the others.

The other three killed: the heap arm's low four taken in the wrong order
and paired the wrong way (both as M4), and the iterator arm sorting
largest first (as M10). Four crash: the ★ arm pairing with the last three
or deduplicating first, the scan arm keeping three, and the heap arm
keeping three of the smallest all index past the end. Five survive and
are equivalent: the ★ arm answering 0 only for three numbers (four sorted
give 0 the same way), the ★ arm's first bound taken from `sorted[1]` and
the heap arm's from `low[3]` (the loop overwrites it), the scan arm
keeping ties in another order, and the scan arm keeping five of the four.

## Rust template: B-2026-11-08-11

LeetCode's Rust template is `pub fn min_difference(mut nums: Vec<i32>)`,
the shape kata 1502 met. `karac fix` makes 6 edits and then stops at the
parameter with the error printed three times; with
`nums: own Vec[i32]` and `let mut nums = nums;` written by hand, 2 more
edits and the arm checks and prints the ★ arm's output.

## Benchmarks

The bench builds 20 arrays of 100000 numbers within 10^9 once and
answers each five times by the ★ arm in all five languages, each answer
sorting a copy. Every implementation prints `100 answers over 20 arrays
of 100000 numbers: checksum 923222781`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `acb9d4c5b` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.168 s |
| Kāra (`karac build`) | 0.173 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.263 s |
| Rust (`rustc -O`) | 0.265 s |
| Go | 0.818 s |
| C (`clang -O3`) | 1.16 s |
| Python | 2.78 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is its real time (0.158 s and 0.158 s on one run).

Kāra is 0.64x Rust under overflow checks by median. The time is the
sorts, and the languages do not sort alike: Kāra's `sort` on integers
runs `runtime/src/int_sort.rs`, Rust's unstable ipnsort (equal integers
cannot be told apart, so it is stable in effect), while Rust's `sort` is
its stable merge sort; Go's `slices.Sort` is pdqsort; C's `qsort` calls
its comparison through a pointer for every step. With `sort_unstable`
the Rust program would use the same algorithm as Kāra (not measured here).

## Verification

The ★, scan, heap and iterator arms print the same output as `moves.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
and `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.4 to 0.6 s, the heap arm 3.4 s,
and the differential 1.9 s.

## Writing it

The arms were written in Kāra and `karac fix` had nothing to change.
