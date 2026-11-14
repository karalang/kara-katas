# 1534. Count Good Triplets

Given an array of integers `arr` and three integers `a`, `b` and `c`,
count the good triplets. A triplet `(arr[i], arr[j], arr[k])` is good when
`0 <= i < j < k < arr.length` and

- `|arr[i] - arr[j]| <= a`,
- `|arr[j] - arr[k]| <= b`,
- `|arr[i] - arr[k]| <= c`.

```
arr = [3,0,1,1,9,7], a = 7, b = 2, c = 3  ->  4   ((3,0,1), (3,0,1), (3,1,1), (0,1,1))
arr = [1,1,2,2,3], a = 0, b = 0, c = 1    ->  0
```

**Constraints:** `3 <= arr.length <= 100`; `0 <= arr[i] <= 1000`;
`0 <= a, b, c <= 1000`.

## Approaches

| file | mechanism |
|---|---|
| `triplets.kara` ★ | every `i < j < k` tried, the pair `(i, j)` checked against `a` before `k` is walked, so a failing pair costs no inner loop. O(n³) |
| `triplets_counts.kara` | the middle `j` walked left to right with a count of the values seen before it. For each `k > j` that meets `b`, the `i` that fit both `a` around `arr[j]` and `c` around `arr[k]` are the earlier values in the overlap of the two windows, read off prefix sums of that count. O(n² + n · max) |
| `triplets_iter.kara` | the ★ arm with iterators: the pairs that meet `a` from a `flat_map`, and for each the `k` that meet `b` and `c` counted by `filter` and summed |
| `triplets_solution.kara` | LeetCode's Rust template (`arr: Vec<i32>`, the ★ arm with `&&`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples, `[0, 1000, 0]`
with `c = 0`, `[5, 5, 5]` with all bounds 0, 100 equal values (161700
triplets), 0 to 990 by 10 with `a = b = 10, c = 20`, then checksums of the
answers for 3000 random arrays of 3 to 12 values up to 10 and 300 of 3 to
100 values up to 1000, each with its own `a`, `b` and `c`.
`triplets.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every `(i, j, k)` of places tried, the ones with `i < j < k`
that meet all three bounds counted. It checks 3000 arrays of 3 to 12
values from 0 to 10 with `a`, `b` and `c` from 0 to 10, every random
choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed, with `a` and `b` swapped, has the same answer |
| P3 | every value raised by the same amount leaves the answer |
| P4 | one of `a`, `b`, `c` raised by one never lowers the answer, and all three at the largest value allow every one of the n(n-1)(n-2)/6 triplets |
| P5 | every value `v` replaced by `10 - v` leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 74337739, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a pair exactly `a` apart skipped | P1 1270, P2 1784, P4 596, P6 1270 |
| M2 | ★: `k` starting at `j` | P1 2875, P2 1549, P4 3000, P6 2875 |
| M3 | ★: `c` taken as a strict bound | P1 1332, P4 610, P6 1332 |
| M4 | counts: the window's top value left out | P1 1959, P2 1995, P4 2185, P5 1908, P6 1959 |
| M5 | counts: the window floored at 1 rather than 0 | P1 615, P2 800, P3 615, P4 1136, P5 1050, P6 615 |
| M6 | counts: the prefix sums stop before the largest value | P1 2345, P2 2296, P4 3000, P5 2295, P6 2345 |
| M7 | iter: `j` starting at `i` | P1 2866, P2 1549, P4 3000, P6 2866 |
| M8 | iter: `b` or `c` rather than both | P1 2286, P2 2192, P6 2286 |
| M9 | template: `j` starting at `i + 2` | P1 2249, P2 1647, P4 3000, P6 2249 |
| M10 | template: `b`'s pair held to `c` | P1 1791, P2 2000, P6 1791 |

## Benchmarks

The bench builds 100 random arrays of 100 values up to 1000 once, each
with its own `a`, `b` and `c` up to 1000, and answers each 10 times by
the ★ arm, in all five languages. Every implementation prints `10 passes
over 100 arrays of 100 values: checksum 755157009`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `fcd87e1f1` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.140 s |
| Rust (`rustc -O`) | 0.144 s |
| Go | 0.250 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.284 s |
| Kāra (`karac build`) | 0.293 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.501 s |
| Python | 10.8 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time equals its real time (0.31 s and 0.31 s on one run).

Kāra is 0.57x Rust under overflow checks by median. Not traced. The inner
loop is two subtractions, two `abs` and two compares; with overflow
checks on, Rust checks each subtraction and each `abs` (whose `i64::MIN`
case overflows), and the gap between the two Rust rows is that work.

## Verification

All four arms print the same output as `triplets.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `fcd87e1f1`.

## Writing it

The ★ and counts arms were written in Kāra and checked as written. The
iterator arm took one edit: Rust's `move` before the inner closure
`|j| (i, j)` is refused (captures are inferred) with a fix that deletes
it, applied.

The Rust template took 5, 1 and 1 changed lines over three rounds: `Vec<i32>` to
`Vec[i32]` (and `Vec<i64>`, `Vec<i32>` in the wrapper), `&&` to `and`, the wrapper's
`|&x|` to `|x|` and `Solution::` to `Solution.`; then the
`struct Solution {}` the template leaves out added; then the closing
`as i64` dropped (an `i32` widens). It checks and agrees with no hand
edit.
