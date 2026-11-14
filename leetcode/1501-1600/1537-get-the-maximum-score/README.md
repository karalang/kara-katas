# 1537. Get the Maximum Score

You are given two sorted arrays of distinct integers `nums1` and `nums2`.
A valid path starts at index 0 of either array and traverses it from left
to right. When it reaches a value present in both arrays, it may change
to the other array (only one repeated value is counted in the path). The
score is the sum of the unique values in a valid path. Return the maximum
score over all valid paths, modulo `10^9 + 7`.

```
nums1 = [2,4,5,8,10], nums2 = [4,6,8,9]   ->  30   (2,4,6,8,10)
nums1 = [1,3,5,7,9], nums2 = [3,5,100]    ->  109  (1,3,5,100)
nums1 = [1,2,3,4,5], nums2 = [6,7,8,9,10] ->  40   (6,7,8,9,10)
```

**Constraints:** `1 <= nums1.length, nums2.length <= 10^5`;
`1 <= nums1[i], nums2[i] <= 10^7`; both arrays strictly increasing.

## Approaches

| file | mechanism |
|---|---|
| `score.kara` ★ | two pointers. The shared values split both arrays into segments, and a path takes each segment from whichever array sums more, plus every shared value once. Walking both arrays in step, `a` and `b` are the best sums of a path ending on each array; at a shared value both become the larger plus that value. The sums stay exact in `i64` and are reduced only at the end. O(n + m) |
| `score_segments.kara` | the cut made explicit: a `Set` of each array's values finds the shared ones, each array's values between two shared ones add up into a segment, and the answer is every shared value plus the larger of each pair of segments |
| `score_suffix.kara` | suffix DP: the best sum of a path from each place to an end, filled from the largest values down, a shared value taking the better of its two ways on |
| `score_solution.kara` | LeetCode's Rust template (`Vec<i32>`, the ★ arm with `i64` sums and a `const MOD`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples, `[7], [7]`
and `[1, 10], [5]`, 100000 shared values near 10^7 (a sum that passes
10^9 + 7), then checksums of the answers for 3000 random pairs built from
1 to 12 values, 300 from 1 to 1000 and 30 from 1 to 100000. Each value
from 1 up, in steps up to a limit, goes into the first array, the second
or both, with a share in both from 1% to 30%. `score.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every valid path walked by recursion, from the front of either
array, free at each shared value to go on in either, and scored by the
sum of its distinct values. It checks 3000 pairs built from 1 to 10
values, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the two arrays swapped have the same answer |
| P3 | the answer is at least either array's whole sum and at most the sum of every distinct value |
| P4 | one more value, above all others, in both arrays adds that value |
| P5 | every value doubled doubles the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 367812865, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a shared value taken as the first array's alone | P1 645, P6 645 |
| M2 | ★: a shared value joins the smaller sum | P1 1404, P3 1113, P4 2373, P6 1404 |
| M3 | ★: the answer read off the first array only | P1 1187, P2 2373, P3 1129, P4 1187, P6 1187 |
| M4 | segments: the smaller of each pair of segments | P1 2882, P3 2882, P6 2882 |
| M5 | segments: the shared values left out | P1 1703, P3 1637, P4 3000, P6 1703 |
| M6 | segments: the last pair of segments left out | P1 2416, P3 2368, P4 2416, P6 2416 |
| M7 | suffix: a shared value never switches | P1 823, P2 1405, P3 647, P6 823 |
| M8 | suffix: only paths that start on the first array | P1 1225, P2 2389, P3 994, P6 1225 |
| M9 | template: the second array's values halved | P1 1789, P2 2857, P3 1370, P5 871, P6 1789 |
| M10 | template: the second array's sum not carried over a shared value | P1 823, P2 1404, P3 631, P6 823 |

## Benchmarks

The bench builds 100 random pairs of arrays from 100000 values each
(steps up to 50) once and answers each 20 times by the ★ arm, in all five
languages. Every implementation prints `20 passes over 100 pairs of
100000 values: checksum 243227345`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `3d1fc8e26` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 1.494 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.531 s |
| C (`clang -O3`) | 1.568 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.663 s |
| Kāra (`karac build`) | 1.678 s |
| Go | 1.790 s |
| Python | 32.8 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (1.69 s and 1.72 s on one run).

Kāra is 1.09x Rust under overflow checks by median. Not traced. The walk
is a three-way branch on two compares of values that a random fill makes
unpredictable, so every language pays the same mispredictions; the rows
are within 20% of one another.

## Verification

All four arms print the same output as `score.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `3d1fc8e26`.

## Writing it

The ★, segments and suffix arms were written in Kāra and checked as
written. The differential took one edit from `karac fix`, Rust's array
type `[Vec[i64]; 2]` to `Array[Vec[i64], 2]`; its literal reading was then
rewritten to pass the two arrays as two parameters, since a list literal
of two borrowed parameters is a `Vec[ref Vec[i64]]`, not that array.

The Rust template took 8, 1 and 5 changed lines over three rounds:
`Vec<i32>` to `Vec[i32]` (and the wrapper's `Vec<i64>` and `Vec<i32>`),
`let (mut i, mut j)` and `let (mut a, mut b)` to `let mut (..)`, `||` and
`&&` to `or` and `and`, the wrapper's `|&x|` to `|x|` and `Solution::` to
`Solution.`; then the `struct Solution {}` the template leaves out added;
then every `as i64` dropped as a widening that needs no cast, which also
took the `0i64` suffixes off `a` and `b` (they keep `i64` as `+=` beside an
`i32` leaves them). It checks and agrees with no hand edit.
