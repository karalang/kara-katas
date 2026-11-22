# 2765. Longest Alternating Subarray

You are given a **0-indexed** integer array `nums`. A subarray `s` of
length `m` is called **alternating** if:

- `m` is greater than `1`.
- `s1 = s0 + 1`.
- The **0-indexed** subarray `s` looks like `[s0, s1, s0, s1, ...,
  s(m-1) % 2]`. In other words, `s1 - s0 = 1`, `s2 - s1 = -1`, `s3 - s2
  = 1`, `s4 - s3 = -1`, and so on up to `s[m - 1] - s[m - 2] = (-1)^m`.

Return *the maximum length of all **alternating** subarrays present in*
`nums` *or* `-1` *if no such subarray exists*.

A subarray is a contiguous **non-empty** sequence of elements within an
array.

```
nums = [2, 3, 4, 3, 4]  ->  4
nums = [4, 5, 6]        ->  2
```

**Constraints:** `2 <= nums.length <= 100`, `1 <= nums[i] <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `alternating.kara` ★ | one pass with the length of the alternating run ending at each number: a run of at least 2 grows when the number equals the one two back, and otherwise a step up of 1 starts a run of 2. O(n) |
| `alternating_brute.kara` | every subarray `l..=r` of at least two numbers checked in full by `all`: each number must be `nums[l]` or `nums[l] + 1` by the parity of its distance from l. O(n^3) |
| `alternating_steps.kara` | the steps between neighbours by `windows(2)`, then the longest run of steps reading +1, -1, +1, ... from a +1; a run of k steps is a subarray of k + 1 numbers. O(n) |
| `alternating_starts.kara` | from each start with a step up of 1 the run is extended while each number repeats the one two back, and the next start is taken where the run ended; a `struct Run` holds the best. O(n) |
| `alternating_solution.kara` | a Rust solution as LeetCode's Rust users write it, from each start i a `while` loop running j on while `nums[j] - nums[i]` matches `(j - i) % 2`, with `ans.max((j - i) as i32)`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; no step up
of 1 at all; a run that must start on its second number; 100 numbers
alternating, LeetCode's most; a run of 4 ended by a step up that starts
a longer one; and 20000 random arrays of 2 to 100 numbers, each from 1
to its own top of 2 to 5, with the sum of the answers and a checksum.
`alternating.py` mirrors the ★ arm and its output is byte-identical.

```
4
2
-1
3
100
6
20000 arrays: lengths sum to 75425, checksum 263481480
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subarray of length m > 1, kept when its first step is
+1 and each later step `s[k] - s[k - 1]` is `(-1)^(k + 1)`, each step
asked by `all`; the longest kept, or -1. It draws 3000 random arrays of
2 to 15 numbers from 1 to a top of 2 to 5, then 500 of up to 100, all
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every number 100 more: the same answer |
| P3 | a number 50 above the greatest put at both ends: the same answer |
| P4 | the numbers written twice over: no shorter |
| P5 | -1 or from 2 to n, and -1 just when no neighbour steps up by 1 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `3500 cases: checksum 869029619, 105000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same `all`s gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M6 and M10 fail the same checks: both count
each run one short, one in the steps arm and one in the solution.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a step down of 1 starting a run | P1 1275, P5 424, P6 1275 |
| M2 | ★: the last run answered, not the longest | P1 671, P6 671 |
| M3 | brute: the last number never asked | P1 3045, P3 455, P5 771, P6 3045 |
| M4 | brute: runs of 2 never tried | P1 1287, P5 1287, P6 1287 |
| M5 | steps: every step wanted as +1 | P1 1466, P6 1466 |
| M6 | steps: a run of steps counted as its numbers | P1 2729, P5 1287, P6 2729 |
| M7 | starts: a run grown by repeats of its last number | P1 1801, P6 1801 |
| M8 | starts: the next start taken past the run's end | P1 126, P6 126 |
| M9 | solution: a number below the start let into the run | P1 1375, P6 1375 |
| M10 | solution: each run counted one short | P1 2729, P5 1287, P6 2729 |

## Benchmarks

The bench draws 100000 arrays of 100 numbers, LeetCode's most, each
from 1 to its own top of 2 to 5, all of them first, then answers each 10
times by the ★ arm in all five languages. Every implementation prints
`100000 arrays of 100, 10 rounds: lengths sum to 4707530, checksum
570581152`.

BENCHTAB

## Verification

All five arms print the same output as `alternating.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The steps arm first
walked the steps by `enumerate` and never used the index; nothing
warned, Kāra having no lint for a binding never read (kara
`B-2026-11-20-146`, open), and the `enumerate` went by hand. Looking for
that lint, `karac explain E_LINT_LEVEL_NO_ARGS` showed
`#[allow(unused_variables)]`, a lint Kāra does not have, which the
attribute as shown reports as unknown; that was kara `B-2026-11-20-144`,
fixed at `0d28296389`.

LeetCode's Rust template took 10 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `Vec<i32>` and `Vec<i64>` became
`Vec[i32]` and `Vec[i64]`; `let mut ans = -1` gained its type, `let mut
ans: i32 = -1`, the answer being an `i32`; `&&` became `and`; the `&x`
pattern dropped its `&`; and `Solution::` became `Solution.`, with the
wrapper's `as i64` dropped. The `as i32` casts on `j - i` stayed.
