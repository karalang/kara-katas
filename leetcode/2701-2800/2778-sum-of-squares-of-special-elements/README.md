# 2778. Sum of Squares of Special Elements

You are given a **1-indexed** integer array `nums` of length `n`.

An element `nums[i]` of `nums` is called **special** if `i` divides
`n`, i.e. `n % i == 0`.

Return *the **sum of the squares** of all **special** elements of*
`nums`.

```
nums = [1, 2, 3, 4]           ->  21
nums = [2, 7, 1, 19, 18, 3]  ->  63
```

**Constraints:** `1 <= nums.length == n <= 50`, `1 <= nums[i] <= 50`.

## Approaches

| file | mechanism |
|---|---|
| `squares.kara` ★ | every 1-indexed place i from 1 to n asked whether it divides n, and the squares at those places summed. O(n) |
| `squares_pairs.kara` | the divisors of n found in pairs, d and n / d for every d up to the square root, the root once, each square read by a closure. O(sqrt n) |
| `squares_iter.kara` | one chain: `enumerate` gives each number its place, `filter` keeps the places whose 1-indexed number divides n, `map` squares and `sum` adds. O(n) |
| `squares_multiples.kara` | each place walks its multiples up to n, and a `Vec[bool]` marks the places whose walk lands on n. O(n log n) |
| `squares_solution.kara` | a Rust solution as LeetCode's Rust users write it, `iter().enumerate()` with a `filter` on `n % (i + 1) == 0` and a `map` to `x * x`, summed in `i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; one number;
50 numbers of 50, LeetCode's most; 47 numbers rising, a prime count;
and 5000 random arrays of 1 to 50 numbers from 1 to 50, with the sum of
the answers and a checksum. `squares.py` mirrors the ★ arm and its
output is byte-identical.

```
21
63
81
15000
2210
5000 arrays: sums total 17722149, checksum 808494635
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a place i is special when some k from 1 to n makes `i * k`
equal n, asked by `any`, and the squares at the special places summed;
no remainder. It draws 3000 random arrays of 1 to 50 numbers from 1 to
50, all before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every number negated: the same answer |
| P3 | the numbers at places that do not divide n raised by 1: the same answer |
| P4 | every number doubled: four times the answer |
| P5 | at least the first square, and the last too when n > 1; at most the sum of every square |
| P6 | each arm agrees with at least three of the other four |

The differential prints `3000 cases: checksum 734886199, 90000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same products gives the same checksum.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: n itself left out | P1 3000, P5 1372, P6 3000 |
| M2 | ★: each number taken, not its square | P1 2998, P2 3000, P4 3000, P5 2944, P6 2998 |
| M3 | pairs: the root counted twice | P1 410, P5 98, P6 410 |
| M4 | pairs: the search stopped short of the root | P1 410, P5 69, P6 410 |
| M5 | iter: the places taken 0-indexed | P1 2997, P3 2858, P5 1283, P6 2997 |
| M6 | iter: every place's square summed | P1 2858, P3 2858, P6 2858 |
| M7 | multiples: the walk of multiples stopped before n | P1 3000, P5 3000, P6 3000 |
| M8 | multiples: every place a multiple marks taken | P1 2858, P3 2858, P6 2858 |
| M9 | solution: the places taken 0-indexed | P1 2838, P3 2858, P5 623, P6 2838 |
| M10 | solution: the last place left out | P1 3000, P5 1372, P6 3000 |

## Benchmarks

The bench draws 100000 random arrays of 1 to 50 numbers from 1 to 50,
LeetCode's most, all of them first, then answers each 20 times by the ★
arm in all five languages. Every implementation prints `100000 arrays,
20 rounds: sums total 7096324580, checksum 432955429`.

BENCHTAB

## Verification

All five arms print the same output as `squares.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took 10 `karac fix` edits, the wrapper
included: `struct Solution {}` added; the `Vec<..>`s became `Vec[..]`;
the `&x` patterns, in the method's `map` and the wrapper's, dropped
their `&`; the wrapper's `&Vec<i64>` became `ref Vec[i64]`; and
`Solution::` became `Solution.`, with the wrapper's `as i64` dropped.
