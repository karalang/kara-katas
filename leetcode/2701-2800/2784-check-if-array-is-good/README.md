# 2784. Check if Array is Good

You are given an integer array `nums`. We consider an array **good** if
it is a permutation of an array `base[n]`.

`base[n] = [1, 2, ..., n - 1, n, n]` (in other words, it is an array of
length `n + 1` which contains `1` to `n - 1` exactly once, plus two
occurrences of `n`). For example, `base[1] = [1, 1]` and `base[3] = [1,
2, 3, 3]`.

Return `true` *if the given array is good, otherwise return* `false`.

**Note:** A permutation of integers represents an arrangement of these
numbers.

```
nums = [2, 1, 3]             ->  false
nums = [1, 3, 3, 2]          ->  true
nums = [1, 1]                ->  true
nums = [3, 4, 4, 1, 2, 1]    ->  false
```

**Constraints:** `1 <= nums.length <= 100`, `1 <= num[i] <= 200`.

## Approaches

The only base an array can be a permutation of is base[n] for n one
less than its length, which is also its greatest number.

| file | mechanism |
|---|---|
| `good.kara` ★ | every number from 1 to n, counted in a `Vec[i64]`, each of 1 to n - 1 once and n twice. O(n) |
| `good_sorted.kara` | base[n] built outright for n the greatest number, a range with n pushed again, and compared by `==` with a sorted copy. O(n log n) |
| `good_distinct.kara` | the distinct numbers in a `Set`: m + 1 numbers, m the greatest, whose distinct ones are exactly 1 to m, with m there twice. O(n) |
| `good_places.kara` | no table: a cycle sort of a copy, each number swapped into place v - 1 until it is there or its place holds its like; places 0 to n - 1 must then hold 1 to n and the last place n again. O(n) |
| `good_solution.kara` | a Rust solution as LeetCode's Rust users write it, `mut nums` sorted by `sort_unstable`, each place i but the last checked to hold `(i + 1) as i32` and the last `(n - 1) as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's four examples; one
number; base[99] shuffled, LeetCode's longest, and the same with its
last number raised to 200; and 3000 random cases of base[n] for n from 1
to 12 shuffled, two in three with one number changed to one from 1 to
13, with the count of good ones and a checksum. `good.py` mirrors the ★
arm and its output is byte-identical.

```
false
true
true
false
false
true
false
3000 small cases: 1209 good, checksum 886251449
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: n the greatest number, base[n] written out, and the array
good when it is a permutation of it, each number of either counted in
both by `filter`; no sorting and no table. It draws 2000 random cases
of base[n] for n from 1 to 12 shuffled, two in three with one number
changed to one from 1 to 13, then 50 of base[99] so changed to one up to
200, all before any arm answers; the literal reading is asked only of
the first 2000.

| | property |
|---|---|
| P1 | up to 13 numbers, the answer is the literal reading's |
| P2 | the numbers reversed: the same answer |
| P3 | a 0 put first: not good |
| P4 | with n one less than the length and n there, one n made n + 1 and another n + 1 put after: the same answer |
| P5 | good only with two or more numbers, the greatest one less than the length, and the sum n(n + 1) / 2 + n |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 570325481, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same counts gives the same checksum.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each number counted at most once | P1 807, P6 826 |
| M2 | ★: n wanted once, not twice | P1 807, P6 826 |
| M3 | sorted: n not pushed again | P1 846, P4 39, P5 39, P6 865 |
| M4 | sorted: the copy left unsorted | P1 715, P2 66, P4 92, P6 734 |
| M5 | distinct: the greatest never counted twice | P1 138, P4 138, P5 138, P6 138 |
| M6 | distinct: one number more wanted | P1 807, P6 826 |
| M7 | places: the last place let hold any number | P1 138, P4 138, P5 138, P6 138 |
| M8 | places: one swap at each place | P1 442, P2 198, P4 117, P6 461 |
| M9 | solution: a place let hold a number below its own | P1 315, P3 95, P5 320, P6 320 |
| M10 | solution: the second last place never checked | P1 36, P4 36, P5 36, P6 36 |

## Benchmarks

The bench draws 50000 arrays of 100 numbers, LeetCode's longest,
base[99] shuffled and two in three with one number changed to one up to
200, all of them first, then answers each 40 times by the ★ arm in all
five languages. Every implementation prints `50000 arrays of 100, 40
rounds: 675120 good, checksum 64118845`.

BENCHTAB

## Verification

All five arms print the same output as `good.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The differential
matched an `Option` of the raised array inside the loop over the arms
by `Some(r)`, moving it on the first arm; `karac check` refused the
move in a loop, and `karac fix` made the binding `Some(ref r)`.

LeetCode's Rust template took 10 `karac fix` edits, the wrapper
included: `struct Solution {}` added; Rust's `mut nums: Vec<i32>`
parameter became `nums: own Vec[i32]` with `let mut nums = nums;` at the
body's start; the `Vec<..>`s became `Vec[..]`; `sort_unstable` became
`sort`; the wrapper's `|&v|` dropped its `&`; and `Solution::` became
`Solution.`. The `as i32` casts stayed.
