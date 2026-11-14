# 1562. Find Latest Group of Size M

Given an array `arr` that represents a permutation of the numbers from
`1` to `n`, and a binary string of size `n` that starts with all its bits
set to zero: at each step `i` (1-indexed), the bit at position `arr[i]` is
set to `1`. Given an integer `m`, find the latest step at which there
exists a group of ones of length exactly `m`: a run of ones that cannot
be extended in either direction. Return `-1` if there is no such group.

```
arr = [3,5,1,2,4], m = 1   ->  4
arr = [3,1,5,4,2], m = 2   ->  -1
```

**Constraints:** `1 <= m <= n <= 10^5`; `arr` is a permutation of
`1..n`.

## Approaches

| file | mechanism |
|---|---|
| `latest.kara` ★ | each group's length kept at both of its ends in a `Vec`: a new 1 reads the groups beside it from the cells next to it, writes the merged length at the new ends, and a count of groups of length `m` says after every step whether one exists. O(n) |
| `latest_back.kara` | the steps undone: all ones at the end (so `m == n` answers `n`), the positions cleared from the last step down, and a `SortedSet` of cleared positions, with `0` and `n + 1` as walls, giving the zeros either side of each through `range(..).next_back()` and `range(..).next()`; the first clear that leaves a group of `m` beside it undoes the step after the answer. O(n log n) |
| `latest_union.kara` | union-find: each new 1 joined to a 1 on either side, through a `mut ref Vec[i64]` helper with path halving, the set's size kept at its root and a count of sets of size `m` kept as sets join. O(n α) |
| `latest_solution.kara` | LeetCode's Rust template (`find_latest_step(arr: Vec<i32>, m: i32) -> i32`, the ★ arm over `i32` with `usize` indices), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples, then
`[1]`, `[2, 1]` with `m` of 2 and of 1, `[1, 2, 3, 4]` with 2,
`[4, 3, 2, 1]` with 1, `[1, 3, 5, 2, 4]` with 1 and
`[2, 4, 6, 1, 3, 5]` with 3; then the count of answers that are not -1
and a checksum for 3000 random orders of up to 8 positions, 300 of up to
1000 and 30 of up to 100000, each with an `m` from 1 to 8 half the time
and from 1 to `n` the other half. `latest.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the bits set one step at a time, and after every step the
string scanned for a group of ones exactly `m` long that cannot be grown
either way; the answer is the last such step. It checks 3000 orders of 1
to 8 positions, each with an `m` from 1 to `n`, every random choice drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is -1 or from `m` to `n`, and is `n` exactly when `m` is `n` |
| P3 | every position mirrored (`v` to `n + 1 - v`) leaves the answer |
| P4 | a position `n + 1` set as one more last step leaves the answer |
| P5 | an `m` of 1 always has an answer, and an `m` of `n` answers `n` |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 41648330, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the merged length not written at the left end | P1 1114, P2 852, P3 1206, P4 597, P5 1700, P6 1114 |
| M2 | ★: a group of `m` on the right never uncounted | P1 853, P2 853, P3 1126, P4 853, P6 853 |
| M3 | ★: the step recorded one early | P1 2436, P2 1654, P5 3000, P6 2436 |
| M4 | back: no answer of `n` when `m` is `n` | P1 1022, P2 1022, P4 1022, P5 3000, P6 1022 |
| M5 | back: only the group on the left looked at | P1 668, P3 1306, P5 670, P6 668 |
| M6 | back: the answer one step late | P1 1414, P2 816, P4 1022, P6 1414 |
| M7 | union: a lone 1 never counted as a group of 1 | P1 1014, P2 381, P5 3000, P6 1014 |
| M8 | union: a joining set of `m` on the new 1's side never uncounted | P1 1066, P2 1066, P3 500, P4 1447, P6 1066 |
| M9 | template: the new 1 not counted in the merged length | P1 2436, P2 1022, P5 3000, P6 2436 |
| M10 | template: the first step with a group kept, not the latest | P1 537, P6 537 |

## Benchmarks

The bench builds 20 random orders of 100000 positions once, and asks
each for `m` from 1 to 10 by the ★ arm, in all five languages. Every call
allocates its lengths. Every implementation prints `m from 1 to 10 over
20 orders of 100000 positions: steps sum 19943880, checksum 557478530`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.072 s |
| Rust (`rustc -O`) | 0.083 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.117 s |
| Kāra (`karac build`) | 0.121 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.136 s |
| Go | 0.136 s |
| Python | 4.7 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.11 s and 0.12 s on one run).

Kāra is 0.86x Rust under overflow checks by median. Not traced. Each
step is two loads beside a random position, three compares and two
stores, so the scattered accesses are most of every row; overflow checks
cost Rust 64% here, on `left + right + 1` and the index arithmetic.

The ★ arm is not where the backward arm is. It was timed by hand, the
arm's own program against the same program in Rust with `BTreeSet` and
`range(..).next_back()` / `next()` under overflow checks: 0.855 s against
0.281 s, with 70% of Kāra's instructions in `karac_mir_map_at`. The
library finds each bound of a `SortedSet` range by a binary search over
positions, and each probe is an O(log n) walk of the tree, so a bound
costs O(log² n) where Rust's costs O(log n). Filed as B-2026-11-14-16
(perf). The backward arm also takes about a minute under `karac
__mir-run`, whose sorted table is one array with an O(n) insert, as
collections.md says.

## Verification

All four arms print the same output as `latest.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, backward and union-find arms were written in Kāra and checked as
written; the backward arm's `range(..).next_back()` checked as Rust
spells it.

The Rust template took 5 changed lines, then 1 added, then 2 changed,
over three rounds of `karac fix`: the `Vec<..>` types to `Vec[..]`,
`for (i, &x)` to `for (i, x)`, the wrapper's `|&a|` to `|a|` and
`Solution::` to `Solution.`; then `struct Solution {}` added; then
`vec![0i32; n + 2]` to `Vec.filled(n + 2, 0i32)` and the wrapper's
closing `as i64` dropped. Its `x as usize` and `l as usize` indices
check, since nothing mixes them with an `i64`. It checks and agrees with
no hand edit.
