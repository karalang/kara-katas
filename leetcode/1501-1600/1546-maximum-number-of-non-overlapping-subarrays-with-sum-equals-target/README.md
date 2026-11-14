# 1546. Maximum Number of Non-Overlapping Subarrays With Sum Equals Target

Given an array `nums` and an integer `target`, return the maximum number
of non-empty, non-overlapping subarrays such that the sum of values in
each subarray equals `target`.

```
nums = [1,1,1,1,1], target = 2            ->  2
nums = [-1,3,5,1,4,2,-9], target = 6      ->  2   ([5,1] and [4,2])
```

**Constraints:** `1 <= nums.length <= 10^5`; `-10^4 <= nums[i] <= 10^4`;
`0 <= target <= 10^6` (the arms take any `target`, and the differential
uses negative ones too).

## Approaches

| file | mechanism |
|---|---|
| `subarrays.kara` ★ | greedy, the earliest-ending subarray first: prefix sums since the last cut go in a `Set`; the first place whose sum minus the target is in it closes a subarray, and the count starts over from there with the set cleared. Ending as early as possible never costs a later one. O(n) |
| `subarrays_dp.kara` | a DP over prefixes: `best[i]` is `best[i - 1]` or one more than `best[j]` for the latest `j` whose prefix sum is this one's minus the target, from a `Map` of each sum's latest place (an `if let` on `get`). `best` never falls, so the latest `j` is the best. O(n) |
| `subarrays_cut.kara` | the greedy without clearing: every prefix sum stays in a `Map` with its latest place, and a match counts only when that place is at or after the last cut (a `match` with a guard). O(n) |
| `subarrays_solution.kara` | LeetCode's Rust template (`max_non_overlapping(nums: Vec<i32>, target: i32) -> i32`, the ★ arm with `std::collections::HashSet`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples, then
`[0, 0, 0]` with 0, `[5]` with 5 and 4, `[1, -1, 1, -1]` with 0 and
`[3, -3, 3]` with 3; then the total and a checksum of the answers for 3000
random arrays of up to 12 values in -3..3, 300 of up to 1000 in -5..5 and
30 of up to 100000 in -10..10, each with a target from twice the spread
below to twice above. `subarrays.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: `most[i]`, the most such subarrays within the first `i`
values, over every subarray `j..i` whose sum, added up from the slice,
is the target. It checks 3000 arrays of 1 to 14 values from `-s` to `s`,
`s` from 1 to 4, each with a target from `-2s` to `2s`, every random
choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is from 0 to the length |
| P3 | the array reversed has the same answer |
| P4 | every value and the target negated leave the answer |
| P5 | the target put after the array adds one |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 373819135, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. One first choice for the template,
`seen.insert(sum)` after a cut as well, was equivalent (the sum is 0 then,
already in the set) and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a cut that keeps the set and the sum | P1 1216, P3 978, P6 1216 |
| M2 | ★: a cut that clears the set but keeps the sum | P1 742, P3 750, P5 502, P6 742 |
| M3 | ★: `target - sum` looked up | P1 1347, P3 1394, P5 2198, P6 1347 |
| M4 | dp: one more on every place, matched or not | P1 1216, P3 978, P6 1216 |
| M5 | dp: each sum's first place kept, not its latest | P1 584, P3 361, P5 793, P6 584 |
| M6 | cut: a match that starts exactly at the cut refused | P1 932, P3 681, P5 417, P6 932 |
| M7 | cut: the cut one place early | P1 659, P3 405, P6 659 |
| M8 | template: a cut that leaves 0 out of the cleared set | P1 582, P5 457, P6 582 |
| M9 | template: only a subarray starting at the cut matched | P1 1323, P3 1108, P5 2455, P6 1323 |
| M10 | template: the count starting at 1 | P1 3000, P2 34, P6 3000 |

## Benchmarks

The bench builds 100 arrays of 1 to 100000 values in -10..10 once, each
with a target in -20..20, and asks each 5 times by the ★ arm, in all
five languages. Kāra's `Set`, Rust's `HashSet` and Go's map are each
language's own hash set; C's is an open-addressing table that doubles
when half full and is cleared over its whole capacity. Every
implementation prints `5 passes over 100 arrays of up to 100000 values:
2656865 subarrays, checksum 949474091`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.293 s |
| Rust (`rustc -O`) | 0.652 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.653 s |
| Go | 0.687 s |
| Kāra (`karac build`) | 0.872 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.876 s |
| Python | 3.4 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.83 s and 0.84 s on one run).

Kāra is 1.34x Rust under overflow checks by median, with both on
SipHash-1-3, and executes 1.37x its instructions (callgrind: 9.68 G
against 7.05 G). Which of hashing, probing and the 2.6 million `clear`s
carries the difference is not traced; it is filed as B-2026-11-14-11.
C's lead is its cheaper hash.

## Verification

All four arms print the same output as `subarrays.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, dp and cut arms were written in Kāra and checked as written.

The Rust template took 8 changed lines, 2 and 1 over three rounds: the
`use std::collections::HashSet` line dropped, the three `Vec<..>` types
to `Vec[..]`, `HashSet::new()` to `HashSet.new()`,
`let (mut sum, mut count)` to `let mut (sum, count)`,
`seen.contains(&(sum - target))` to `seen.contains(sum - target)`,
`|&x| x as i32` to `|x| x as i32` and `Solution::` to `Solution.`; then
`struct Solution {}` added and `HashSet.new()` to `Set.new()`; then the
closing `as i64` dropped (an `i32` widens). It checks and agrees with no
hand edit.
