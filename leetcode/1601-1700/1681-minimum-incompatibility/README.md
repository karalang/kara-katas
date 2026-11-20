# 1681. Minimum Incompatibility

You are given an integer array `nums` and an integer `k`. You are asked to
distribute this array into `k` subsets of **equal size** such that there
are no two equal elements in the same subset.

A subset's **incompatibility** is the difference between the maximum and
minimum elements in that array.

Return *the **minimum possible sum of incompatibilities** of the* `k`
*subsets after distributing the array optimally, or return* `-1` *if it
is not possible.*

A subset is a group of integers that appear in the array with no
particular order.

```
nums = [1,2,1,4], k = 2              ->  4
nums = [6,3,8,1,3,1,2,2], k = 4      ->  6
nums = [5,3,3,6,3,3], k = 3          ->  -1
```

**Constraints:** `1 <= k <= nums.length <= 16`; `nums.length` is
divisible by `k`; `1 <= nums[i] <= nums.length`.

## Approaches

| file | mechanism |
|---|---|
| `incompatibility.kara` ★ | every set of n / k indexes with distinct values is a possible subset, costed largest less smallest; `best[m]` is the least cost of splitting the indexes in m, and the next subset always takes the lowest index not in m, so each split is built once. O(3^n) at worst |
| `incompatibility_sequential.kara` | the values sorted, each subset filled in rising order, so its cost is the sum of its steps and a strict step keeps its values distinct; `best[m][i]` with i the last index placed, and a full subset lets the next start anywhere. O(2^n * n^2) |
| `incompatibility_memo.kara` | the lowest index left goes with every choice of n / k - 1 later companions of distinct values, and the rest is solved the same way, each set left solved once through a `Map` |
| `incompatibility_solution.kara` | a Rust solution as LeetCode's Rust users write it, the ★ arm's two tables as `vec![-1i32; 1 << n]` and `vec![i32::MAX; 1 << n]` over `usize` masks with `count_ones() as usize`, a `u32` of values used, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, one value
per subset (0), one subset of all (2), and 16 values, every value twice
(12); then the answers summed, the impossible ones counted, and a
checksum for 3000 random arrays of up to 8 values, 300 of up to 12 and 20
of up to 16, n values from 1 to n each, with a random k that divides n.
`incompatibility.py` mirrors the ★ arm and its output is byte-identical.

```
4
6
-1
0
2
12
3000 arrays of up to 8 values: answers sum to 2526, 1032 impossible, checksum 146940310
300 arrays of up to 12 values: answers sum to 546, 115 impossible, checksum 207060474
20 arrays of up to 16 values: answers sum to 56, 7 impossible, checksum 584209196
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way to split the indexes into groups, each index in
turn joining a group so far or starting a new one while there are fewer
than k; a split counts when its k groups are of equal size and none
repeats a value, and costs the sum of their largest less smallest. It
checks 3000 random arrays of n values from 1 to n, n from 1 to 8, each
with a random k that divides n. Every case is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | every value v written n + 1 - v gives the same answer |
| P4 | the answer is -1 exactly when some value appears more than k times |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 158984676, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, over the same set partitions, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M1 also priced the subsets of
fewer values than a subset holds; a table entry that does not hold a
whole number of subsets is never extended, so no such price is used, and
it passed every check. A first M6 read the answer only where the largest
value was placed last; the subsets can always be placed with the one
holding the largest value last, so it was never different. Both were
replaced. P3 fails for no mutant: each edit is as wrong on the values
mirrored as on the values themselves.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the repeat check remembers only the last value | P1 411, P4 359, P5 411 |
| M2 | ★: a subset's values told apart by index, not value | P1 1355, P4 1032, P5 1355 |
| M3 | ★: a later subset overwrites a table entry, not its minimum | P1 149, P2 14, P5 149 |
| M4 | sequential: equal values allowed in one subset | P1 1355, P4 1032, P5 1355 |
| M5 | sequential: a new subset opened one value late | P1 2054, P4 1370, P5 2054 |
| M6 | sequential: a new subset opened only above the last value | P1 1236, P4 1236, P5 1236 |
| M7 | memo: a companion told apart by index, not value | P1 1355, P4 1032, P5 1355 |
| M8 | memo: the companions skip a value | P1 258, P2 42, P4 201, P5 258 |
| M9 | solution: a subset of one value, priced 0, never used | P1 1427, P4 1427, P5 1427 |
| M10 | solution: each subset's largest value one less | P1 1968, P4 1427, P5 1968 |

## Benchmarks

The bench draws 300 arrays of 16 values from 1 to 16, LeetCode's
largest, each with a random k that divides 16, all of them first, then
answers each 4 times by the ★ arm in all five languages, each allocating
its two tables of `2^16` entries per answer. Every implementation prints
`300 arrays of 16 values, 4 rounds: answers sum to 10096, checksum
36196921`. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.860 s |
| Kāra (`karac build`) | 0.875 s |
| Go | 0.908 s |
| C (`clang -O3`) | 0.979 s |
| Rust (`rustc -O`) | 0.986 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.992 s |
| Python | 54 s |

The sequential Kāra build is 13% faster than Rust and 13% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.861 s and 0.875 s on one
run).

## Verification

All four arms print the same output as `incompatibility.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports no error or
warning on any of them, and `karac fix` has nothing left to change. The
memo arm, and the differential that copies it, get one note, L0002: its
`solve` and `companions` call each other, and their effects are found
together by a fixed point. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ and sequential arms checked clean as first written. The memo arm's
first draft passed its `Map` on from `solve` to `companions` bare, where
the parameter is `mut ref`; `karac check` asked for the call-site marker
(E0218), and `karac fix` wrote `mut memo`.

LeetCode's Rust template took one `karac fix` of 20 edits:
`struct Solution {}` added, `Vec<i32>` written `Vec[i32]`, each
`vec![x; 1 << n]` written `Vec.filled(1 << n, x)`, the `as usize` casts
and the `1usize` suffix dropped (an index is an `i64`), `let (mut lo, mut
hi) = ..` written `let mut (lo, hi) = ..`, each `i32::MAX` and `i32::MIN`
written with a `.`, and `||` written `or`. The `0u32` of values used,
shifted by an `i32`, carried over as written.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does (B-2026-11-19-131).
