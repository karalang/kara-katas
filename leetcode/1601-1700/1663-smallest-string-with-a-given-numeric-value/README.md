# 1663. Smallest String With A Given Numeric Value

The **numeric value** of a **lowercase character** is defined as its
position `(1-indexed)` in the alphabet, so the numeric value of `a` is
`1`, the numeric value of `b` is `2`, the numeric value of `c` is `3`,
and so on.

The **numeric value** of a **string** consisting of lowercase characters
is defined as the sum of its characters' numeric values. For example,
the numeric value of the string `"abe"` is equal to `1 + 2 + 5 = 8`.

You are given two integers `n` and `k`. Return *the
**lexicographically smallest string** with **length** equal to `n` and
**numeric value** equal to `k`.*

```
n = 3, k = 27  ->  "aay"
n = 5, k = 73  ->  "aaszz"
```

**Constraints:** `1 <= n <= 10^5`; `n <= k <= 26 * n`.

## Approaches

| file | mechanism |
|---|---|
| `smallest.kara` ★ | every letter starts as an `a`, and what k has left over is spent from the last letter backwards, each taking up to 25 more. The front letters, the ones that matter most for the order, stay `a`. O(n) |
| `smallest_count.kara` | the answer is a run of a's, at most one letter, and a run of z's: (k - n) / 25 z's, the remainder as the letter between, built with `repeat`. O(n) |
| `smallest_front.kara` | from the front: each letter the smallest that leaves the rest able to make up k, at most 26 a letter, mapped over `0..n` and collected into a `String`. O(n) |
| `smallest_solution.kara` | a Rust solution as LeetCode's Rust users write it (from the front, pushed onto a `String::with_capacity`), carried by `karac fix`, which made 5 changes in one pass |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one letter at each end, a string of z's, and the one letter between
coming last), then the z's and a checksum of every letter for 3000
random problems with n up to 10, 300 up to 1000 and 10 up to `10^5`, k
drawn from n to 26n. `smallest.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the strings of length n in alphabetical order from `aa..a`,
and the first whose letters sum to k. It checks 3000 random problems
with n up to 3, all 26^n strings being few enough to walk.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is n lowercase letters |
| P3 | its letters' values sum to k |
| P4 | its letters never go down: the smallest such string is sorted |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 392806282, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a letter allowed 26 more than an `a` | P1 1148, P2 1148, P5 1148 |
| M2 | ★: the leftover spent from the front | P1 1957, P4 1957, P5 1957 |
| M3 | ★: one less left over to spend | P1 2931, P3 2931, P5 2931 |
| M4 | count: a z counted as 26 more than an `a` | P1 140, P3 140, P5 140 |
| M5 | count: the z's put first | P1 1139, P4 1139, P5 1139 |
| M6 | count: a remainder of 1 never written | P1 106, P2 106, P3 106, P5 106 |
| M7 | front: the letters after this one worth at most 25 each | P1 1183, P2 57, P4 89, P5 1183 |
| M8 | front: each letter's value counted as 1 | P1 1148, P2 1148, P3 1148, P4 972, P5 1148 |
| M9 | template: the letters after this one counted one too many | P1 2931, P3 2931, P5 2931 |
| M10 | template: no letter below `b` | P1 1252, P3 114, P5 1252 |

## Benchmarks

The bench draws 400 problems with n = `10^5`, LeetCode's largest, and k
from n to 26n, all of them first, then builds each string by the ★ arm
in all five languages and folds every letter into a checksum. Every
implementation prints `400 problems with n = 100000: 19247347 z's,
checksum 212518643`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.163 s |
| Kāra (`karac build`) | 0.166 s |
| C (`clang -O3`) | 0.170 s |
| Rust (`rustc -O`) | 0.171 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.179 s |
| Go | 0.203 s |
| Python | 4.0 s |

The sequential Kāra build is level with Rust and 9% faster than Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.156 s and 0.162 s on one
run).

## Verification

All four arms print the same output as `smallest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ arm first wrote `let mut left = k as i64 - n;`, and `karac fix`
dropped the cast, an `i32` widening to `i64` by itself; the harness's
`b as i64` went the same way. The count and front arms checked clean as
first written.

LeetCode's Rust template takes one `karac fix` of 5 edits: `struct
Solution {}` added, `String::with_capacity(n as usize)` to
`String.with_capacity(n)`, and `std::cmp::max` to `max`.

The differential's first draft tested the order with
`bytes.windows(2).any(..)`, as Rust reads; Kāra's `windows` gives a
`Vec` of slices, not an iterator, and `karac fix` wrote
`bytes.windows(2).into_iter().any(..)`.
