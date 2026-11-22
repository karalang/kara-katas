# 2841. Maximum Sum of Almost Unique Subarray

You are given an integer array `nums` and two positive integers `m`
and `k`.

Return *the **maximum sum** out of all **almost unique** subarrays of
length* `k` *of* `nums`. If no such subarray exists, return `0`.

A subarray of `nums` is **almost unique** if it contains at least `m`
distinct elements.

A subarray is a contiguous **non-empty** sequence of elements within an
array.

```
nums = [2,6,7,3,1,7], m = 3, k = 4      ->  18
nums = [5,9,9,2,4,5,4], m = 1, k = 3    ->  23
nums = [1,2,1,2,1,2,1], m = 3, k = 3    ->  0
```

**Constraints:** `1 <= nums.length <= 2 * 10^4`; `1 <= m <= k <=
nums.length`; `1 <= nums[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `almost.kara` ★ | a window of k slid along the array, its sum kept as it goes and a `Map` from each value in it to its count through `entry().or_insert()`, an entry removed when its count falls to zero, so the map's length is the window's distinct values |
| `almost_windows.kara` | every window by `windows(k)`, its distinct values counted by collecting it into a `Set`, the sums of those with m or more by `filter_map`, and `max().unwrap_or(0)`; O(nk), for the harness's sizes |
| `almost_ranks.kara` | the values ranked first, sorted, `dedup`ed and each found by `binary_search`, so the window's counts are a plain `Vec` by rank and a count of ranks above zero; the sum from prefix sums |
| `almost_sorted.kara` | each window from scratch by recursion over its start: the slice `nums[i..i + k]` collected into a `SortedSet` and summed, the best of this window and the rest; O(nk log k), for the harness's sizes |
| `almost_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `HashMap<i32, i32>` of the window's counts, the leaving value counted down through `get_mut(&x).unwrap()` and removed at zero, an `i64` sum, and `m as usize` against the map's `len()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's three examples; one
number; 2 x 10^4 numbers, LeetCode's most, all distinct and near 10^9,
as one window and then with m one more than k; then 3000 random arrays
of 1 to 8 numbers from 1 to 4, and 50 of up to 2000 from 1 to 10^9 or
from 1 to 50 with k up to 100, as a count with no such window and a
checksum. `almost.py` mirrors the ★ arm and its output is
byte-identical.

```
18 23 0
7
19999800010000 0
3000 short arrays: 401 with none, checksum 459720521
50 long arrays: 7 with none, checksum 989937255
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every subarray of length k, its distinct values
counted by comparing each with those before it, the sums of those with
m or more, and the most. It draws 2000 random arrays of 1 to 8 numbers
from 1 to 4, then 50 of up to 500 with k up to 50, from 1 to 30 or from
1 to 5 x 10^8, so that P3's doubling stays in `i32` for the Rust
solution; all are drawn before any arm answers, and the literal
reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 8 numbers, the answer is the literal reading's |
| P2 | the array reversed: the same answer |
| P3 | every number doubled: the answer doubled |
| P4 | m lowered to 1: no smaller |
| P5 | k the whole length and m 1: the whole array's sum |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 799637013, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Nine are killed, each the same
way under both backends. M3 survives and is equivalent: every value is
at least 1, so a window shorter than k that holds m distinct values is
part of the first full window, which holds as many and sums to more.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a value's count never let go | P1 88, P2 94, P6 95 |
| M2 | ★: the leaving value's sum kept | P1 1192, P2 165, P6 1234 |
| M3 | ★: a short window counted | survives: equivalent (above) |
| M4 | windows: more than m distinct wanted | P1 1210, P5 304, P6 1219 |
| M5 | ranks: the leaving rank uncounted from distinct | P1 166, P2 194, P6 173 |
| M6 | ranks: the window's sum one place short | P1 1726, P2 569, P5 2050, P6 1770 |
| M7 | sorted: the last window never tried | P1 813, P2 580, P5 2050, P6 817 |
| M8 | sorted: the window one longer | P1 1231, P6 1273 |
| M9 | solution: the leaving value left counted | P1 88, P2 94, P6 95 |
| M10 | solution: the window started one late | P1 1231, P6 1273 |

## Benchmarks

The bench draws 100 arrays of 2 x 10^4 numbers, LeetCode's most, from
1 to 10^4, k up to 5000 and m up to k, all of them first, then answers
each 20 times by the ★ arm in all five languages. Kāra, Rust, Go and
Python count in their own hash maps (Kāra's and Rust's SipHash); C,
with none of its own, counts in an open-addressed table with
backward-shift deletion. Every implementation prints `100 arrays of
20000, 20 rounds: sums total 18986353260, checksum 651027879`.

BENCHTAB

## Verification

All five arms print the same output as `almost.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The windows arm, as first written, called `filter_map` straight on
`nums.windows(k)`, as Rust's `windows` allows, and `karac check`
reported E0236, "no method 'filter_map' on type 'Vec': iterator
adaptors/terminals require an explicit `.into_iter()`", Kāra's
`windows` giving a `Vec` of the windows; `karac fix` added the
`.into_iter()`. The other own arms checked clean.

LeetCode's Rust template took 22 `karac fix` edits in one run, the
wrapper included: `use std::collections::HashMap;` gave way to `struct
Solution {}` for the `impl`; `Vec<..>` became `Vec[..]` and
`HashMap<..>` `Map[..]`, `HashMap::new()` `Map.new()`; `k as usize`
became `as i64`; `nums[i] as i64` and `x as i64` lost their casts, `i32`
widenings, and `m as usize` its cast against the map's `len()`;
`get_mut(&x)` and `remove(&x)` lost their `&`; `&&` became `and`; in
the wrapper `&Vec<i64>` became `ref Vec[i64]`, `|&v|` lost its `&`, and
`Solution::` took `.`. The `let c = cnt.get_mut(x).unwrap()` held while
`cnt.remove(x)` runs, as Rust's borrow checker allows once `c` is
done, was accepted as written.
