# 1304. Find N Unique Integers Sum up to Zero

Given an integer `n`, return **any** array containing `n` unique integers
such that they add up to `0`.

```
n = 5  ->  [-7,-1,1,3,4]    [-5,-1,1,2,3] and [-3,-1,2,-2,4] are accepted too
n = 3  ->  [-1,0,1]
n = 1  ->  [0]
```

**Constraints:** `1 <= n <= 1000`.

The arms are `fn sum_zero(n: i64) -> Vec[i64]`.

## Approaches

Any such array is an answer, so the arms give different arrays, and
every harness checks each array against the statement rather than
printing it.

| file | mechanism |
|---|---|
| `sum_zero.kara` ★ | the pairs 1 and -1, 2 and -2, up to `n / 2`, and 0 when n is odd. O(n) |
| `sum_zero_symmetric.kara` | n numbers two apart, centred on 0, `2i - n + 1` for i from 0 to n - 1: odd numbers when n is even, even ones when n is odd, by `map` and `collect`. O(n) |
| `sum_zero_running.kara` | 1 to n - 1, then the negative of their sum, which is below all of them (0 alone when n is 1). O(n) |
| `sum_zero_iter.kara` | `flat_map` turning each of 1 to `n / 2` into the pair `[i, -i]`, chained with a 0 taken only when n is odd. O(n) |
| `sum_zero_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `vec![0; n as usize]` with each pair written at `2 * i` and `2 * i + 1`, the last place left 0 when n is odd), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, four more properties |

Every arm prints the same 2 lines: LeetCode's three sizes, each answer
checked for n numbers, no two equal, summing to 0 (`5:ok 3:ok 1:ok`);
then every n from 1 to 1000 (`1000 sizes: 1000 valid, numbers total
500500`). `sum_zero.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, symmetric and running-sum arms checked clean as
first written. The iterator arm wrote Rust's `flat_map(|i| [i, -i])`,
which takes anything iterable; Kāra's `flat_map` takes a closure that
returns an `Iterator`, and `E0200` says so and gives the fix, which
`karac fix` writes: `[i, -i].into_iter()` (1 fix). The Rust arm takes one
round of 9 fixes by `karac fix`'s count, from 5 errors: `struct
Solution;` to `struct Solution {}`, `Vec<..>` to `Vec[..]`, `vec![0; n
as usize]` to `Vec.filled(n, 0)`, `::` to `.`, and the wrapper's `|&x|`
to `|x|`. Its output matches on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: n numbers, each compared with every other for an equal, all
added up to 0. Every n from 1 to 200, and 600 to 1000 in steps of 50;
the literal check compares every pair, so the large sizes are few. The
checksum folds every arm's answer, sorted, so that it pins what each arm
gives and not only that it passes.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | n numbers |
| P3 | no two equal, found by sorting |
| P4 | every number fits an `i32`, LeetCode's return type |
| P5 | the same n asked again: the same array |

All 5,225 checks pass on every arm: `209 sizes: checksum 576776578, 5225
checks over 5 arms: 0 failures`, under `karac __mir-run` and `karac
__mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under both
`karac __mir-llvm-run` and `karac __mir-run`. Every one is killed, fails
the same way under both backends and not by a crash, and no two fail the
same checks, so all ten are kept.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no 0 when n is odd | P1 100, P2 100 |
| M2 | ★: each i paired with -(i + 1) | P1 208 |
| M3 | symmetric: the numbers centred one below 0 | P1 209 |
| M4 | symmetric: the numbers halved | P1 109, P3 109 |
| M5 | running: counting from 0 | P1 1, P3 1 |
| M6 | running: the numbers `10^4` apart | P4 7 |
| M7 | iterator: the pairs from 0 | P1 208, P3 208 |
| M8 | iterator: one pair too many | P1 209, P2 209 |
| M9 | solution: each negative one short | P1 208, P3 99 |
| M10 | solution: the array filled with 1 | P1 100, P3 99 |

P1 kills nine, P3 five, P2 two and P4 one; P5 kills none. The statement
bounds the numbers nowhere, so numbers `10^4` apart (M6) pass it, and
only LeetCode's `i32` (P4) sees their negative sum grow past it, from n
= 700 among the sizes tried. The length (P2) sees the two edits that
change it, the 0 left out (M1) and the pair added (M8). Sorting (P3) sees
the edits that repeat a number: halving rounds both -1 and 1 to 0 when n
is even (M4), and the others repeat 0 or 1. Each arm
is a plain function of n, so asking again (P5) cannot tell an edit from
the arm.

## Benchmarks

The bench calls the ★ arm `10^6` times, each n from 1 to 1000, the
constraints' range, chosen from the checksum so far, so no answer
carries over, and folds one number of each answer, at a place also
chosen from the checksum, plus the call's number into the checksum. Each
answer is a fresh array: a `Vec` grown by `push` in Kāra and Rust, a
slice grown by `append` in Go, a list in Python, and a `malloc` of n
numbers in C. Every implementation prints `1000000 calls: checksum
120775963`.

BENCHTAB
