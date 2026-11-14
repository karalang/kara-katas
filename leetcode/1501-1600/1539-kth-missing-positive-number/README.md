# 1539. Kth Missing Positive Number

Given an array `arr` of positive integers sorted in strictly increasing
order, and an integer `k`, return the `k`-th positive integer that is
missing from `arr`.

```
arr = [2,3,4,7,11], k = 5  ->  9   (missing: 1, 5, 6, 8, 9, ...)
arr = [1,2,3,4], k = 2     ->  6   (missing: 5, 6, 7, ...)
```

**Constraints:** `1 <= arr.length <= 1000`; `1 <= arr[i] <= 1000`;
`1 <= k <= 1000`; `arr[i] < arr[j]` for `i < j`.

## Approaches

| file | mechanism |
|---|---|
| `kth.kara` ★ | binary search on the count of missing numbers: below `arr[i]` there are `i` values of `arr`, so `arr[i] - i - 1` numbers are missing there, and that count never falls. With `lo` the first place where it reaches `k`, the answer is `lo + k`. O(log n) |
| `kth_scan.kara` | the values walked in order: each one at or below the `k`-th missing number so far pushes it up by one, and the first above it ends the walk. O(n) |
| `kth_walk.kara` | the statement walked: the positive numbers counted up from 1, a pointer into `arr` stepping past the ones it holds, the rest counted as missing until the `k`-th. O(n + k) |
| `kth_set.kara` | `arr` collected into a `Set`, the open range `1..` filtered to the numbers it lacks, the `k`-th taken with `nth(k - 1)`. O(n + k) |
| `kth_solution.kara` | LeetCode's Rust template (`find_kth_positive(arr: Vec<i32>, k: i32) -> i32`, the ★ arm with `usize` places), carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples, then `[1]`
and `[2]` with `k = 1`, `[1000]` with 1000, `[5, 6, 7]` with 4 and 5,
1 to 1000 with 1000 and the odd numbers to 999 with 500; then checksums of
the answers for 3000 random arrays of up to 12 values, steps up to 4 and
`k` up to 30, and 300 of up to 1000 values, steps up to 2 and `k` up to
1000. `kth.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the positive numbers from 1, each one `arr` does not contain
counted, until the `k`-th. It checks 3000 arrays of 1 to 10 values, steps
of 1 to 4, with `k` from 1 to 20, every random choice drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is not in `arr`, and lies from `k` to `k + n` |
| P3 | `k + 1` gives a larger answer |
| P4 | one more value, above the answer and every value, leaves the answer |
| P5 | 1 put in front and every value raised by one moves the answer up by one |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3000 problems: checksum 822846470, 90000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. All eleven are
killed, each the same way under both backends; M6 by a hang (with
`k = 1` the count never meets `k - 1`), stopped after 40 s under both,
and M10 by a crash, an index out of bounds, under both. Two first
choices were equivalent and were replaced: the scan's `break` as
`continue` (once a value is above the `k`-th missing number, every later
one is too) and the walk's `arr[i] == x` as `arr[i] <= x` (the pointer
never falls behind `x`).

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the missing count taken as `arr[mid] - mid` | P1 472, P2 472, P5 139, P6 472 |
| M2 | ★: the answer `hi + k - 1` | P1 3000, P2 578, P4 2385, P6 3000 |
| M3 | ★: `hi = mid - 1` | P1 248, P2 152, P4 1211, P5 289, P6 248 |
| M4 | scan: a value pushes the answer only when below it | P1 472, P2 472, P5 139, P6 472 |
| M5 | scan: the first value skipped | P1 2894, P2 142, P5 248, P6 2894 |
| M6 | walk: stops at the `(k - 1)`-th missing number | hangs |
| M7 | walk: the count starts at 1, so 1 is never asked | P1 2803, P2 1390, P5 3000, P6 2803 |
| M8 | set: `nth(k)` | P1 3000, P2 2486, P6 3000 |
| M9 | set: the range from 2 | P1 1446, P2 1052, P5 1446, P6 1446 |
| M10 | template: `mid` rounded up | index out of bounds |
| M11 | template: the answer `lo + k - 1` | P1 3000, P2 578, P4 2385, P6 3000 |

## Benchmarks

The bench builds 1000 arrays of 1 to 1000 values, steps of 1 to 4, and
1000 values of `k` from 1 to 2000 once, then asks every array for every
`k` 5 times by the ★ arm, in all five languages. Every implementation
prints `5 passes over 1000 arrays of up to 1000 values and 1000 values of
k: checksum 302171194`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `3d1fc8e26` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.090 s |
| C (`clang -O3`) | 0.097 s |
| Kāra (`karac build`) | 0.099 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.100 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.104 s |
| Go | 0.104 s |
| Python | 4.2 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time equals its real time (0.10 s and 0.10 s on one run).

Kāra is 0.96x Rust under overflow checks by median. Not traced. Each
search is about ten steps, each a load, a compare and a branch the
predictor cannot learn, plus a `%` in the checksum per search, so the
rows sit close together.

## Verification

All five arms print the same output as `kth.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `3d1fc8e26`.

## Writing it

The ★, scan, walk and set arms were written in Kāra and checked as
written; the scan compares the borrowed `x` with `kth` directly, and the
set arm's open range `1..` with `filter` and `nth` needed nothing. The
shared harness took one edit from `karac fix`: `*k` to `k` where a tuple
pattern over `examples.iter()` had already copied `k` out.

The Rust template took 5, 1 and 2 changed lines over three rounds: the
three `Vec<..>` types to `Vec[..]`, `let (mut lo, mut hi)` to
`let mut (lo, hi)`, `|&x| x as i32` to `|x| x as i32` and `Solution::`
to `Solution.` (11 fixes over those lines); then `struct Solution {}`
added; then `0usize` to `0` and the closing `as i64` dropped (an `i32`
widens). It checks and agrees with no hand edit.
