# 1713. Minimum Operations to Make a Subsequence

You are given an array `target` that consists of **distinct** integers
and another integer array `arr` that **can** have duplicates.

In one operation, you can insert **any** integer at any position in
`arr`. For example, if `arr = [1,4,1,2]`, you can add `3` in the middle
and make it `[1,4,3,1,2]`. Note that you can insert the integer at the
very beginning or end of the array.

Return *the **minimum** number of operations needed to make* `target`
*a **subsequence** of* `arr`*.*

A **subsequence** of an array is a new array generated from the original
array by deleting some elements (possibly none) without changing the
remaining elements' relative order.

```
target = [5,1,3], arr = [9,4,2,3,4]                        ->  2
target = [6,4,8,1,3,2], arr = [4,7,6,2,3,8,6,1]            ->  3
```

**Constraints:** `1 <= target.length, arr.length <= 10^5`;
`1 <= target[i], arr[i] <= 10^9`; `target` contains no duplicates.

## Approaches

| file | mechanism |
|---|---|
| `operations.kara` ★ | the target's values are distinct, so the part of it the array already holds is a run of the array's values whose places in the target rise: the longest such run stays and every other value is inserted. A `Map` gives each value's place, and `tails[k]`, the smallest place that ends a rising run of k + 1, is searched with `partition_point`. O(n log n) |
| `operations_fenwick.kara` | the longest rising run ending at place p is one more than the longest ending at any place below p: a Fenwick tree of maxima over the target's places answers that prefix and takes the new length. O(n log m) |
| `operations_sorted.kara` | no map: the target's (value, place) pairs sorted, each value of the array found by `partition_point` on them, and the tails searched by a binary search written out. O(n log m) |
| `operations_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashMap<i32, usize>` collected from `target.iter().enumerate()`, `if let Some(&p) = pos.get(&a)`, and `tails.binary_search(&p)` matched on `Ok` and `Err`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, a target
already there, one with nothing in common, and an array that holds the
target backwards; then the answers summed and a checksum for 3000 random
problems of up to 10 values from 1 to 12, 300 of up to 1000 from 1 to
1500, and 10 of up to `10^5` from 1 to 120000, each target the first
values of a shuffle. `operations.py` mirrors the ★ arm and its output is
byte-identical.

```
2
3
0
2
3
3000 problems of up to 10 values from 1 to 12: answers sum to 12252, checksum 895530425
300 problems of up to 1000 values from 1 to 1500: answers sum to 140906, checksum 928169830
10 problems of up to 100000 values from 1 to 120000: answers sum to 579660, checksum 464546402
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the target's values that no insertion has to supply are a
part of the target, in order, that the array already holds as a
subsequence; every part of the target, from all `2^m`, is tried against
the array, taking each match as early as it comes, and the rest
inserted. It checks 3000 random problems: a target of distinct values
from a shuffle of 1 to between 1 and 8, and an array of 1 to 10 values
from 1 to two past the target's largest. Every case is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the target and the array both reversed give the same answer |
| P3 | the array with the target put after it needs nothing inserted |
| P4 | a value outside the target put at both ends of the array changes nothing |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 563715884, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the largest of `itertools.combinations` of the
target that is a subsequence of the array, gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M5, the Fenwick tree's update
stepping one place at a time instead of by its low bit, was equivalent:
it writes every slot above the place, which costs O(m) but keeps every
prefix maximum right. It was replaced. M1 and M4 both let a run take a
place equal to its last, as M2 and M9 both keep a tail that should
shrink, and each pair fails the very same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tail equal to the place passed over | P1 1144, P3 1908, P5 1144 |
| M2 | ★: a tail never lowered | P1 307, P2 452, P3 1361, P5 307 |
| M3 | ★: the places counted from the target's end | P1 719, P3 1491, P5 719 |
| M4 | fenwick: the prefix maximum takes in the place itself | P1 1144, P3 1908, P5 1144 |
| M5 | fenwick: an update overwrites a longer run | P1 21, P2 36, P5 21 |
| M6 | fenwick: the answer is the last run's length, not the longest | P1 278, P2 423, P5 278 |
| M7 | sorted: the tails' search turned around | P1 719, P3 1491, P5 719 |
| M8 | sorted: a value outside the target given its neighbour's place | P1 524, P5 524 |
| M9 | solution: a tail never lowered | P1 307, P2 452, P3 1361, P5 307 |
| M10 | solution: two places share each slot | P1 450, P2 158, P3 2022, P5 450 |

## Benchmarks

The bench draws 20 random problems, each a target of `10^5` distinct
values below `10^9` and an array of `10^5` values, half of them from the
target, LeetCode's largest, all of them first, then answers each 5
times by the ★ arm in all five languages; each answer builds its map
anew. Every implementation prints `20 problems of 100000 values, 5
rounds: answers sum to 9956530, checksum 458521031`. C has no map: its
mirror probes a table of `2^18` slots linearly, the key hashed by one
multiply, which is less work than Kāra's SipHash `Map`, Rust's SipHash
`HashMap` or Go's `map` do. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Kāra (`karac build`) | 0.605 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.612 s |
| C (`clang -O3`) | 0.614 s |
| Rust (`rustc -O`) | 0.617 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.619 s |
| Go | 1.136 s |
| Python | 6.4 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.606 s and 0.615 s on one
run).

## Verification

All four arms print the same output as `operations.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★, Fenwick and sorted arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 20 edits:
`struct Solution {}` added, `use std::collections::HashMap;` deleted,
`Vec<i32>` and `HashMap<i32, usize>` written `Vec[i32]` and `Map[i32,
i64]`, `usize` written `i64`, `Vec::new()` written `Vec.new()`, `|(i,
&v)|` written `|(i, v)|`, and `if let Some(&p) = pos.get(&a)` written
`if let Some(p) = pos.get(a).cloned()`. Kāra's `binary_search` gives
`Option[i64]`, the place of an equal value or `None`, not Rust's
`Result` with the insertion point, so the fix rewrote the `match` on
`Ok(_)` and `Err(i)` as a block that finds `i` with
`tails.partition_point(|y| y < p)` and runs the `Err` arm's body when
`tails[i]` is not `p`. It first read `if i < tails.len() and tails[i] ==
p {} else { ... }`, the empty `Ok` arm kept as an empty branch; since
kara `93fd9b2078` (B-2026-11-20-43) it reads `if not (i < tails.len() and tails[i] ==
p) { ... }`. The `collect()` into the `Map` carried over as written.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
