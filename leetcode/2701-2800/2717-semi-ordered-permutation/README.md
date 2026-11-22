# 2717. Semi-Ordered Permutation

You are given a **0-indexed** permutation of `n` integers `nums`.

A permutation is called **semi-ordered** if the first number equals `1`
and the last number equals `n`. You can perform the below operation as
many times as you want until you make `nums` a **semi-ordered**
permutation:

- Pick two adjacent elements in `nums`, then swap them.

Return *the minimum number of operations to make* `nums` *a
**semi-ordered permutation***.

```
nums = [2,1,4,3]    ->  2
nums = [2,4,1,3]    ->  3
nums = [1,3,4,2,5]  ->  0
```

**Constraints:** `2 <= nums.length == n <= 50`, `1 <= nums[i] <= 50`;
`nums` is a permutation.

## Approaches

| file | mechanism |
|---|---|
| `semi.kara` ★ | 1 must travel to the front, one swap a place, and n to the back; each swap moves one of them a place unless it moves both, which happens once when 1 starts right of n, for they cross. So the answer is 1's index plus n's distance from the end, less one when 1 starts right of n; the indices come from `position`. O(n) |
| `semi_bubble.kara` | the swaps done on a copy: 1 bubbled to the front a place at a time, then n bubbled to the back, each swap counted. O(n) |
| `semi_pass.kara` | one walk over the numbers by `enumerate` notes where 1 and n stand, and the answer comes from the two places by a `match` on which stands first. O(n) |
| `semi_count.kara` | 1 needs a swap for each number before it and n one for each number after it, but the swap that takes 1 past n serves both; the numbers are counted by `take` and `skip` after `filter` over `enumerate` finds the two. O(n) |
| `semi_solution.kara` | a Rust solution as LeetCode's Rust users write it, `position(\|&x\| x == 1)`, `usize` arithmetic and a final `as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples; two
numbers both ways; 50, LeetCode's most, backwards, and with only 1 and
50 traded; 1 and 50 side by side in the middle, both ways round; then
the swaps summed and a checksum for 10000 random permutations of 2 to
50. `semi.py` mirrors the ★ arm and its output is byte-identical.

```
2
3
0
0
1
97
97
48
49
10000 permutations: swaps sum to 243165, checksum 760840583
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: from the permutation given, every swap of two adjacent
numbers tried, breadth first, until a permutation is reached that begins
with 1 and ends with n, with no positions. It checks 1000 random
permutations of 2 to 6, then 500 of 2 to 50. Every case is drawn before
any arm answers.

| | property |
|---|---|
| P1 | up to 6 numbers, the answer is the literal reading's |
| P2 | the permutation reversed and every v made n + 1 - v: the same answer |
| P3 | the numbers other than 1 and n rotated among their places: the same answer |
| P4 | the answer is between 0 and 2 n - 3 |
| P5 | 1 swapped a place toward the front, where it is not there: one less |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1500 cases: checksum 658083914, 45000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
breadth-first search over the same 1000 small cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. P3 kills only M9, the one edit that looks at a
number other than 1 and n. One first choice was equivalent and was
replaced: the bubble arm looking for n from where 1 stopped, which is
always the front by then.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no swap shared when 1 starts right of n | P1 478, P4 174, P5 320, P6 721 |
| M2 | ★: n's distance taken from n, not the end | P1 1000, P4 174, P6 1500 |
| M3 | bubble: 1 bubbled to the second place only | P1 422, P2 581, P5 149, P6 850 |
| M4 | bubble: n bubbled to the second last place only | P1 541, P2 439, P6 996 |
| M5 | pass: the shared swap taken off when 1 stands first | P1 1000, P4 356, P5 320, P6 1500 |
| M6 | pass: n's place kept as the one before it | P1 694, P4 174, P5 477, P6 1165 |
| M7 | count: the numbers before 1 counted with 1 | P1 1000, P4 174, P6 1500 |
| M8 | count: the swap shared when n stands after 1 | P1 1000, P4 356, P5 320, P6 1500 |
| M9 | solution: 1 found as 2 | P1 898, P2 1054, P3 762, P5 954, P6 1397 |
| M10 | solution: the shared swap taken off when n starts right of 1 | P1 1000, P4 356, P5 320, P6 1500 |

## Benchmarks

The bench draws `2 * 10^5` permutations of 50, LeetCode's most, by
Fisher and Yates, all of them first, then answers each 20 times by the
★ arm in all five languages; C and Go find each index by a scan of their
own, Rust and Kāra by `position`, Python by `list.index`. Every
implementation prints `200000 permutations of 50, 20 rounds: swaps sum
to 194393420, checksum 382626763`.

BENCHTAB

## Verification

All five arms print the same output as `semi.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four arms of our own checked clean as first written.

LeetCode's Rust template took one `karac fix` of 10 edits, the wrapper
included: `struct Solution {}` added, `Vec<i32>` respelled `Vec[i32]`,
the `&x` and `&v` closure patterns dropped their `&`, since a Kāra
pattern matches through a reference, `Solution::` became `Solution.`,
and the wrapper's `as i64` on the `i32` answer was dropped. The `usize`
arithmetic needed nothing, since `len` and `position` answer `i64`.
