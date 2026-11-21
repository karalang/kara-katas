# 1679. Max Number of K-Sum Pairs

You are given an integer array `nums` and an integer `k`.

In one operation, you can pick two numbers from the array whose sum
equals `k` and remove them from the array.

Return *the maximum number of operations you can perform on the array*.

```
nums = [1,2,3,4], k = 5     ->  2
nums = [3,1,3,4,3], k = 6   ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`;
`1 <= k <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | one pass with a `Map` of the values still waiting for a partner: a value whose partner, k less it, is waiting takes one and makes an operation, else it waits itself. A value's only partners are equal to each other, so pairing as early as possible never costs one. O(n) |
| `pairs_sorted.kara` | two pointers over the sorted values: the smallest and largest left are paired when they sum to k; a smaller sum drops the smallest, a larger one the largest. O(n log n) |
| `pairs_counts.kara` | every value counted first; a value below its partner makes as many pairs as the fewer of the two counts, and one exactly half of k half its own count, summed in a `fold` over the `Map`, whose order does not matter. O(n) |
| `pairs_solution.kara` | a Rust solution as LeetCode's Rust users write it, the ★ arm's count in a `std::collections::HashMap` read with `get_mut(&target)` and written with `*map.entry(num).or_insert(0) += 1`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, no pair (0),
every value half of k (2), and one value (0); then the operations summed
and a checksum for 3000 random arrays of up to 12 values up to 6, 300 of
up to 1000 values up to 1000 and 10 of up to `10^5` values up to `10^5`,
each with a k from 2 to twice the largest value allowed. `pairs.py`
mirrors the ★ arm and its output is byte-identical.

```
2
1
0
2
0
3000 arrays of up to 12 values up to 6: 2763 operations, checksum 682540589
300 arrays of up to 1000 values up to 1000: 13391 operations, checksum 485247370
10 arrays of up to 100000 values up to 100000: 25107 operations, checksum 611491201
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the first value left is either never picked, or picked with
some later value that sums to k, both removed, and the most operations
over every such choice wins. It checks 3000 random arrays of 1 to 10
values from 1 to between 1 and 6, each with a k from 2 to twice that.
Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | every value 1000 more, and k 2000 more, gives the same answer |
| P4 | a pair that sums to k added, one at each end, gives one more |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 805399551, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. None moves P3: every edit counts pairs
by their difference from k, which raising every value and k together
keeps.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a partner with a count of 0 still taken | P1 670, P2 379, P4 871, P5 670 |
| M2 | ★: a taken partner never counted down | P1 964, P2 368, P4 1639, P5 964 |
| M3 | ★: the partner counted as waiting, not the value | P1 1531, P4 950, P5 1531 |
| M4 | sorted: a small sum drops the largest | P1 1163, P4 1542, P5 1163 |
| M5 | sorted: a pair drops only the smallest | P1 1102, P4 1722, P5 1102 |
| M6 | counts: a value half of k pairs its whole count | P1 1580, P4 1162, P5 1580 |
| M7 | counts: the more of the two counts | P1 1607, P4 192, P5 1607 |
| M8 | solution: a partner taken only when two wait | P1 1301, P2 426, P4 1024, P5 1301 |
| M9 | solution: a paired value also waits | P1 1201, P4 1253, P5 1201 |
| M10 | solution: the partner one too small | P1 1811, P4 2184, P5 1811 |

## Benchmarks

The bench draws 50 arrays of `10^5` values up to `10^5`, LeetCode's
longest, each with a random k up to `2 * 10^5`, all of them first, then
answers each 10 times by the ★ arm in all five languages: Kāra's `Map`,
Rust's `HashMap`, Go's `map` and Python's `dict`, and in C an
open-addressing table written for the bench and cleared for each answer.
Values up to `10^5`, not LeetCode's `10^9`, so that pairs are common.
Every implementation prints `50 arrays of 100000 values, 10 rounds:
6155570 operations, checksum 579057845`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.574 s |
| Rust (`rustc -O`) | 1.727 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.741 s |
| Kāra (`karac build`) | 1.759 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.767 s |
| Go | 2.532 s |
| Python | 8.8 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.574 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.672 s and 1.691 s on one
run).

## Verification

All four arms print the same output as `pairs.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★, sorted and counts arms checked clean as first written; the counts
arm's `fold(0, ..)` returns the function's `i32`, so its seed takes that
type.

LeetCode's Rust template took one `karac fix` of 10 edits: the
`use std::collections::HashMap;` line replaced by `struct Solution {}`,
`Vec<i32>` written `Vec[i32]`, `HashMap<i32, i32>` and `HashMap::new()`
written `Map[i32, i32]` and `Map.new()`, and `get_mut(&target)` written
`get_mut(target)`; `if let Some(cnt) = map.get_mut(..)` with `*cnt -= 1`
and the `entry(..).or_insert(0)` carried over as written.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does (B-2026-11-19-131).
