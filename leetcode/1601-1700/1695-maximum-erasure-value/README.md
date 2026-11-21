# 1695. Maximum Erasure Value

You are given an array of positive integers `nums` and want to erase a
subarray containing **unique elements**. The **score** you get by erasing
the subarray is equal to the **sum** of its elements.

Return *the **maximum score** you can get by erasing **exactly one**
subarray.*

An array `b` is called to be a subarray of `a` if it forms a contiguous
subsequence of `a`, that is, if it is equal to `a[l],a[l+1],...,a[r]` for
some `(l,r)`.

```
nums = [4,2,4,5,6]             ->  17
nums = [5,2,1,2,5,2,1,2,5]     ->  8
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `erasure.kara` ★ | the window ending at i starts just after the last place any value in it was seen before, so it only moves right; its sum is a difference of prefix sums, and each value's last place is kept in a vector over the values. O(n) |
| `erasure_set.kara` | the window's values in a `Set` and its sum alongside; a value already in it drops values from the left, and their sum, until it is not. O(n) |
| `erasure_starts.kara` | every start tried: the window grows right until a value repeats, a `Vec` of flags over the values marking what it holds, cleared for the next start. O(n * w) for windows of w values |
| `erasure_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashSet` window with `contains(&nums[r])` and `remove(&nums[l])` and the sum and best in a tuple `let`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, one value,
one value three times, and five that differ; then the answers summed and
a checksum for 3000 random arrays of up to 12 values up to 5, 300 of up
to 1000 values up to 100, and 10 of up to `10^5` values up to `10^4`.
`erasure.py` mirrors the ★ arm and its output is byte-identical.

```
17
8
1
3
15
3000 arrays of up to 12 values up to 5: answers sum to 28547, checksum 584323140
300 arrays of up to 1000 values up to 100: answers sum to 459307, checksum 985941344
10 arrays of up to 100000 values up to 10000: answers sum to 18234015, checksum 392967580
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every subarray, from every start to every end, is kept when
no two of its values are equal and scored by its sum, and the best score
wins. It checks 3000 random arrays of 1 to 12 values from 1 to between 1
and 8. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | every value doubled doubles the answer |
| P4 | the last value written again at the end gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 767513168, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, every slice whose `set` is as long as it is,
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M8 answers 0 for every array, which
the reversed, doubled and lengthened arrays agree with, so only P1 and
P5 see it. Deleting the set arm's `remove` was not used: its window then
never empties and the loop runs off the array.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the start allowed to move back left | P1 1700, P2 1335, P5 1700 |
| M2 | ★: a value's last place recorded as the window's start | P1 1634, P2 1475, P4 877, P5 1634 |
| M3 | ★: the window's sum without its last value | P1 3000, P2 1710, P5 3000 |
| M4 | set: a dropped value left in the sum | P1 2415, P4 3000, P5 2415 |
| M5 | set: the last window's sum, not the best | P1 1219, P2 1696, P4 1867, P5 1219 |
| M6 | starts: no window reaches the last value | P1 960, P2 1070, P4 960, P5 960 |
| M7 | starts: the start's flag never cleared | P1 1259, P2 1589, P5 1259 |
| M8 | solution: `min` for `max` | P1 3000, P5 3000 |
| M9 | solution: one value dropped for a repeat, not as many as needed | P1 1504, P2 1420, P4 877, P5 1504 |
| M10 | solution: the left value inserted, not the new one | P1 1714, P2 1557, P4 2265, P5 1714 |

## Benchmarks

The bench draws 50 random arrays of `10^5` values up to `10^4`,
LeetCode's largest, all of them first, then answers each 60 times by the
★ arm in all five languages. Every implementation prints `50 arrays of
100000 values, 60 rounds: answers sum to 5929664280, checksum
761557604`. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.280 s |
| Rust (`rustc -O`) | 0.316 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.449 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.635 s |
| Kāra (`karac build`) | 0.650 s |
| Go | 0.930 s |
| Python | 48 s |

The sequential Kāra build takes 2.01x Rust's time and 1.41x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.280 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.617 s and 0.626 s on one
run).

## Verification

All four arms print the same output as `erasure.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ arm checked clean as first written. The set and starts arms kept
their sums and best in `let mut sum = 0`, which the `i32` values added
to them do not fix (an operator does not type a literal), and returned
one as the `i32` answer; `karac check` refused the narrowing (E0200) and
`karac fix` declared each `: i32`, two edits in each.

LeetCode's Rust template took one `karac fix` of 14 edits: the
`use std::collections::HashSet;` line replaced by `struct Solution {}`
(`Set` is in Kāra's prelude), `Vec<i32>` written `Vec[i32]`,
`HashSet::new` written `Set.new`, `let (mut l, mut sum, mut best) = (0,
0, 0)` written `let mut (l, sum, best) = (0, 0i32, 0i32)`, the two sums
typed as the narrowing needs, and the `&` dropped from `contains` and
`remove`.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
