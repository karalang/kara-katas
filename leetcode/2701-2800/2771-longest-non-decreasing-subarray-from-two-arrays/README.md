# 2771. Longest Non-decreasing Subarray From Two Arrays

You are given two **0-indexed** integer arrays `nums1` and `nums2` of
length `n`.

Let's define another **0-indexed** integer array, `nums3`, of length
`n`. For each index `i` in the range `[0, n - 1]`, you can assign either
`nums1[i]` or `nums2[i]` to `nums3[i]`.

Your task is to maximize the length of the **longest non-decreasing
subarray** in `nums3` by choosing its values optimally.

Return *an integer representing the length of the **longest
non-decreasing** subarray in* `nums3`.

**Note:** A **subarray** is a contiguous **non-empty** sequence of
elements within an array.

```
nums1 = [2, 3, 1],    nums2 = [1, 2, 1]     ->  2
nums1 = [1, 3, 2, 1], nums2 = [2, 2, 3, 4]  ->  4
nums1 = [1, 1],       nums2 = [2, 2]        ->  2
```

**Constraints:** `1 <= nums1.length == nums2.length == n <= 10^5`, `1 <=
nums1[i], nums2[i] <= 10^9`.

## Approaches

A run ending at index i ends with nums1[i] or with nums2[i], and only
its length and that last number matter to what can follow, so two
lengths per index carry everything.

| file | mechanism |
|---|---|
| `nondecreasing.kara` ★ | two running lengths, the longest non-decreasing run ending at i that takes nums1[i] and the one that takes nums2[i], each extending whichever run before it ends no higher. O(n) |
| `nondecreasing_memo.kara` | the longest run ending at each index with each array's number, by a recursive call remembered in a `Vec[i64]`, the two arrays passed as one `Slice[Vec[i64]]`; asked first of the last index, so the calls reach back to the first before any returns. O(n), recursing as deep as n |
| `nondecreasing_windows.kara` | each array's neighbours by `windows(2)`, the two walked together by `zip`; the numbers before and now and the two lengths are fixed arrays of two, and each length now takes the best before whose number is no higher. O(n) |
| `nondecreasing_fold.kara` | one `fold` over the two arrays `zip`ped together, carrying the two numbers before, the two lengths ending at them and the best so far in a tuple, with a closure for a run that can be extended. O(n) |
| `nondecreasing_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `vec![[1i32; 2]; n]` table of the two lengths at every index filled by four `if`s, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; `10^5`
numbers, LeetCode's most, one array rising and one falling, both
falling, and a run that must change arrays at every step; 3000 random
pairs of 1 to 12 numbers from 1 to 5; and 10 pairs of `10^5`, one array
rising with noise and the other random up to `10^9`, the last two with
the sum of the answers and a checksum. `nondecreasing.py` mirrors the ★
arm and its output is byte-identical.

```
2
4
2
100000
1
100000
3000 small pairs: lengths sum to 12529, checksum 966947673
10 pairs of 10^5: lengths sum to 100227, checksum 425238874
```

The memo arm recurses `10^5` deep on the large pairs, under the MIR
interpreter as well as compiled.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to build nums3, each index's choice of array a bit
of a number, and every subarray of each nums3 checked by `all` for no
step down; the longest over every choice. It draws 2000 random pairs of
1 to 11 numbers from 1 to a top of 2 to 6, then 50 of up to 2000 from 1
to `10^9` with one array rising with noise, all before any arm answers;
the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 11 numbers, the answer is the literal reading's |
| P2 | the two arrays swapped: the same answer |
| P3 | every number doubled: the same answer |
| P4 | both arrays reversed and every number negated: the same answer |
| P5 | from 1 to n, and no shorter than the longest run in either array alone |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 166222649, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by every choice of nums3 gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a change from nums2 to nums1 never taken | P1 571, P2 674, P4 674, P6 571 |
| M2 | ★: a step down of 1 in nums1 let through | P1 641, P2 560, P3 650, P6 650 |
| M3 | memo: an equal step taken as a step down | P1 1395, P5 1103, P6 1407 |
| M4 | memo: only the same array asked before | P1 811, P6 859 |
| M5 | windows: the best taken over the nums1 run only | P1 384, P2 820, P4 645, P5 151, P6 432 |
| M6 | windows: the lengths never carried on | P1 1796, P5 1842, P6 1846 |
| M7 | fold: a step down of 1 let through | P1 1003, P3 1012, P6 1012 |
| M8 | fold: runs before the first pair counted | P1 1317, P4 1320, P5 780, P6 1320 |
| M9 | solution: the change from nums1 to nums2 compared the wrong way | P1 1051, P2 787, P4 787, P6 1099 |
| M10 | solution: every run started at 0 | P1 1796, P5 987, P6 1846 |

## Benchmarks

The bench draws 20 pairs of `10^5` numbers, LeetCode's most, one array
rising with noise and the other random up to `10^9`, all of them first,
then answers each 10 times by the ★ arm in all five languages. Every
implementation prints `20 pairs of 10^5, 10 rounds: lengths sum to
5150, checksum 923720801`.

BENCHTAB

## Verification

All five arms print the same output as `nondecreasing.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara
`684b860a5`. At `e514b7b29` the check refuses `nondecreasing_fold.kara`
and the differential, "expected 'i64', found 'ref i64'" at the
closure's `(x, y, ..)`: holding the `fold` seed's literals open
(449dd49566) lost the copy of a `ref i64` into the seed's slot. That
is kara B-2026-11-22-3; the kata keeps its natural fold.

## Writing it

The memo, windows and fold arms checked clean as first written. The ★
arm wrote Rust's `let (mut one, mut two) = (1, 1)`; `karac check`
refused it and `karac fix` wrote `let mut (one, two) = (1, 1)`.

LeetCode's Rust template took 19 `karac fix` edits, the wrapper
included: `struct Solution {}` added; the `Vec<..>`s became `Vec[..]`;
`vec![[1i32; 2]; n]` became `Vec.filled(n, [1i32; 2])`; `let mut ans =
1` gained its type, `let mut ans: i32 = 1`; the wrapper's `&Vec<i64>`s,
in its parameters and its closure's, became `ref Vec[i64]`; the `&x`
pattern dropped its `&`; and `Solution::` became `Solution.`, with the
wrapper's `as i64` dropped.
