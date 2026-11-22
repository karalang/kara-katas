# 2750. Ways to Split Array Into Good Subarrays

You are given a binary array `nums`.

A subarray of an array is **good** if it contains **exactly one**
element with the value `1`.

Return *an integer denoting the number of ways to split the array*
`nums` *into **good** subarrays*. As the number may be too large, return
it **modulo** `10^9 + 7`.

A subarray is a contiguous **non-empty** sequence of elements within an
array.

```
nums = [0, 1, 0, 0, 1]  ->  3
nums = [0, 1, 0]        ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`, `0 <= nums[i] <= 1`.

## Approaches

Each piece holds exactly one 1, so exactly one cut falls between each
two neighbouring 1s, at any of the places between them, and none
elsewhere: the answer is the product of the distances between
neighbouring 1s, and 0 with no 1 at all.

| file | mechanism |
|---|---|
| `splits.kara` ★ | one pass, the last 1's index kept as an `Option[i64]` and each new 1 multiplying in its distance from it, mod `10^9 + 7`. O(n) |
| `splits_dp.kara` | `ends[i]`, the ways to split the first i numbers; the last piece's cut lies after the 1 before the last and at or before the last 1, a range summed from a prefix sum of `ends`. O(n) |
| `splits_positions.kara` | the indices of the 1s by `enumerate`, `filter` and `map`, and the gaps between neighbours by `windows(2)` multiplied by `fold`. O(n) |
| `splits_text.kara` | the numbers written as a string of digits and `split` at each `"1"`: the pieces between the first and the last are the runs of 0s between neighbouring 1s, and a run of r 0s offers r + 1 cuts. O(n) |
| `splits_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `const MOD` inside the method written `1_000_000_007` and the last 1's index kept as an `i32` with -1 for none, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; no 1 at
all; `10^5` ones, LeetCode's most; `10^5` of 1 and 0 by turns; 3000
random arrays of 1 to 20 numbers, each with its own share of ones; and
20 of `10^5`, the last two with the sum of the answers and a checksum.
`splits.py` mirrors the ★ arm and its output is byte-identical.

```
3
1
0
1
509082729
3000 small arrays: ways sum to 32577, checksum 477746199
20 arrays of 100000: ways sum to 8980082952, checksum 343218074
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every choice of cuts among the n - 1 places between numbers,
as the bits of a number, counted when every piece it makes holds exactly
one 1; no product of gaps. It draws 2000 random arrays of 1 to 14
numbers, each with its own share of ones, then 100 of up to 5000, all
before any arm answers; the literal reading is asked only of the first
2000.

| | property |
|---|---|
| P1 | up to 14 numbers, the answer is the literal reading's |
| P2 | the numbers reversed: the same answer |
| P3 | 0s put at both ends: the same answer |
| P4 | 0, 0, 1 put at the end: the answer times the new 1's distance from the last 1, mod `10^9 + 7`, or 1 with no 1 before |
| P5 | from 0 to `10^9 + 6`; and every number made 1: 1 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2100 cases: checksum 186669484, 63000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same count of cuts gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1 and M4 fail the same checks, by the same
counts; so do M2 and M8, both taking an array with no 1 as one way.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each gap counted one place wider | P1 1339, P4 1765, P5 1973, P6 1438 |
| M2 | ★: no 1 at all taken as one way | P1 334, P6 335 |
| M3 | dp: the cut just after the earlier 1 left out | P1 1666, P4 335, P5 2100, P6 1765 |
| M4 | dp: the 1 before the last never moved on | P1 1339, P4 1765, P5 1973, P6 1438 |
| M5 | positions: each gap counted one place narrower | P1 1339, P4 536, P5 1973, P6 1438 |
| M6 | positions: a single 1 taken as no way | P1 327, P4 662, P5 127, P6 327 |
| M7 | text: the run before the first 1 counted too | P1 696, P2 975, P3 1765, P4 335, P6 748 |
| M8 | text: no 1 at all taken as one way | P1 334, P6 335 |
| M9 | solution: a 1 at index 0 forgotten | P1 256, P2 418, P3 273, P4 112, P6 273 |
| M10 | solution: a last 1 at index 0 taken as none | P1 446, P2 131, P3 112, P4 112, P5 127, P6 447 |

## Benchmarks

The bench draws 50 arrays of `10^5` numbers, LeetCode's most, each with
its own share of ones from 1 to 30 in 100, all of them first, then
answers each 20 times by the ★ arm in all five languages. Every
implementation prints `50 arrays of 100000, 20 rounds: ways sum to
555075261840, checksum 602101825`.

BENCHTAB

## Verification

All five arms print the same output as `splits.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took 11 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `Vec<i32>` and `Vec<i64>` became
`Vec[i32]` and `Vec[i64]`; the `&x` patterns dropped their `&`; `i as
i64 - prev as i64` lost both casts, an `i64` index and an `i32` widening
into `i64` arithmetic by themselves; and `Solution::` became
`Solution.`, with the wrapper's `as i64` dropped. The `const MOD`
inside the method and `1_000_000_007` stayed as written.
