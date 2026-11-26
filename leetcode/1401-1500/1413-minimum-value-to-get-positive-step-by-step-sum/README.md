# 1413. Minimum Value to Get Positive Step by Step Sum

Given an array of integers `nums`, you start with an initial positive
value `startValue`. In each iteration, you calculate the step by step
sum of `startValue` plus the elements in `nums` (from left to right).
Return the minimum positive value of `startValue` such that the step by
step sum is never less than 1.

```
nums = [-3,2,-3,4,2]    ->  5    the sums from 5 are 2, 4, 1, 5, 7
nums = [1,2]            ->  1    the minimum start must be positive
nums = [1,-2,-3]        ->  5
```

**Constraints:** `1 <= nums.length <= 100`, `-100 <= nums[i] <= 100`.

Each arm is `fn min_start_value(nums: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_start_value.kara` ★ | the lowest the running sum goes, 0 among them for the start itself, and the start that lifts it to 1. O(n) |
| `min_start_value_backward.kara` | from the last step back: what the sum must be before each step for it to stay at least 1 from there on, never below 1. O(n) |
| `min_start_value_search.kara` | a start is enough when every running sum from it stays at least 1, and any larger start is then enough too: the least one found by halving between 1 and `100 n + 1`, the most a start ever needs, with a closure as the test. O(n log n) |
| `min_start_value_fold.kara` | the running sums as an iterator, a `map` whose closure adds to a captured sum, and their least taken by `fold` from 0. O(n) |
| `min_start_value_solution.kara` | a Rust solution as LeetCode's Rust users write it (`for &num in nums.iter()`, `min_sum.min(sum)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and four
more (`5 1 5 1 2 1 4`); the constraints' most, 100 numbers of -100, of
100, and drawn (`100 numbers: 10001 1 543`); and 2000 random arrays of 1
to 100 numbers up to 1 to 100 in size (`2000 random arrays: 288595 in
all, checksum 563037983`). `min_start_value.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: every arm first declared its sums bare, `let mut sum =
0`. Such a literal keeps the default `i64` beside `sum += x` with `x` an
`i32`, and the `i32` return then refuses it; `karac fix` declares each
`: i32`, 2 fixes in the ★ arm and 1 in the backward and search arms. The
harness first printed its seven examples with Rust's `[..].map(|x|
f"{x}").join(" ")`; `karac fix` writes `.into_iter()` before the `map`,
and the `join` on the iterator that leaves is refused, "no method 'join'
on type 'IterMap'", with no advice and no fix. Kāra joins a
`Vec[String]`, so the pieces were collected into one by hand in every
arm. The Rust solution takes one round of 18 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]`, `for &num` to `for num`, the sums declared `: i32`, the
harness's `.into_iter()`, and `Solution::` to `Solution.`.

The fold arm does not come through the loop. Its `fold(0, |low, s|
low.min(s))` is refused at the return as an `i64`, and `karac fix`
writes the seed `0i32`; `low.min(s)` is then refused, `min` expecting an
`i32` and getting an `i64`, with no explanation and no fix, since `s` is
the closure's `sum`, which kept the default. The refusal does not trace
`s` back to `sum`, where the same refusal on `sum` itself would declare
it `: i32`
([B-2026-11-26-8](https://github.com/karalang/kara/blob/main/docs/bugs-v2.jsonl)).
The arm declares `let mut sum: i32 = 0` by hand.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each positive start tried in turn, 1, 2 and on, the first
that keeps every step by step sum at least 1. LeetCode's examples, five
edge cases (one number at either end, zeros, sums that come back to 0
twice over), the constraints' most, 100 numbers of -100, of 100 and
drawn, and 1992 random arrays of 1 to 100 numbers up to 1 to 100 in
size, a third of them leaning down. Each case carries a number from -10
to 10 to append for P4.

The two cases of 100 equal numbers were first pushed as
`cases.push(((0..100).map(|_| -100).collect(), 100))` into `cases:
Vec[(Vec[i32], i32)]`, which is refused, "expected '(Vec[i32], i32)',
found '(C, i64)'", with no fix: the element type does not reach a
`collect` inside a tuple argument, though it reaches a bare
`v.push(it.collect())` and a typed `let` of the same tuple
([B-2026-11-26-9](https://github.com/karalang/kara/blob/main/docs/bugs-v2.jsonl)).
The differential binds each to a `let low: Vec[i32]` first.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | a positive start, never more than one past 100 for each number |
| P3 | the start keeps every sum at least 1, and one less than it, while positive, does not |
| P4 | a number added at the end that is not negative changes nothing |
| P5 | the numbers twice over need as much again as a negative total takes away |
| P6 | the ★ arm's answer |

All 55,575 checks pass on every arm: `2003 cases: checksum 287600114,
55575 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by the least of
`itertools.accumulate`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the highest running sum taken where the lowest is | P1 2002, P2 1576, P3 1992, P4 114, P5 1993, P6 8008 |
| M2 | ★: the start that lifts the lowest sum to 0, not 1 | P1 2003, P2 148, P3 1992, P6 8012 |
| M3 | backward: the need never below 0, where it is never below 1 | P1 1574, P2 145, P3 1563, P4 220, P6 1574 |
| M4 | backward: the numbers walked from the first, not the last | P1 1766, P3 1766, P4 896, P6 1766 |
| M5 | search: a sum of 0 taken as enough | P1 1855, P3 1855, P6 1855 |
| M6 | search: the low end moved two past a start that fails | P1 1238, P2 1, P3 1238, P4 415, P5 579, P6 1238 |
| M7 | fold: the least taken from 100, not 0, so the start itself is left out | P1 139, P2 139, P6 139 |
| M8 | fold: each number given on in place of the running sum | P1 1948, P3 1948, P5 1319, P6 1948 |
| M9 | solution: the least sum started at -1 | P1 148, P3 148, P6 148 |
| M10 | solution: the sum set to each number, not added to | P1 1948, P3 1948, P5 1319, P6 1948 |

## Benchmarks

The bench draws a pool of 10^5 numbers from -100 to 100 and runs the ★
arm, taking its window as a `Slice[i32]`, on 3 * 10^6 windows of 100 of
them, each window's start drawn. Every implementation prints `3 * 10^6
windows of 100 numbers: checksum 729562943`.

BENCHTAB

Kāra is level with Rust and C here, measured by hand at 0.18 s against
Rust's 0.17 s (0.18 s with overflow checks on), C's 0.17 s and Go's 0.20
s; Python takes 21 s.
