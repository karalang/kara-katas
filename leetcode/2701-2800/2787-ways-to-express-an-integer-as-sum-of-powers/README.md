# 2787. Ways to Express an Integer as Sum of Powers

Given two **positive** integers `n` and `x`.

Return *the number of ways* `n` *can be expressed as the sum of the*
`x`*th power of **unique** positive integers, in other words, the
number of sets of unique integers* `[n1, n2, ..., nk]` *where* `n =
n1^x + n2^x + ... + nk^x`.

Since the result can be very large, return it modulo `10^9 + 7`.

For example, if `n = 160` and `x = 3`, one way to express `n` is `n = 2^3
+ 3^3 + 5^3`.

```
n = 10, x = 2  ->  1
n = 4, x = 1   ->  2
```

**Constraints:** `1 <= n <= 300`, `1 <= x <= 5`.

## Approaches

Each power `i^x` up to n is used at most once, so the count is a 0/1
knapsack over the powers.

| file | mechanism |
|---|---|
| `powers.kara` ★ | `ways[s]` counts the sets of the powers so far summing to s, and each power i^x, smallest first, is added by walking s down from n by `rev()` so no power is used twice. O(n * n^(1/x)) |
| `powers_table.kara` | the whole table: the powers by `take_while` over a lazy `map`, and `ways[k][s]` the sets of the first k powers summing to s, each row the one above with or without the k-th power. O(n * n^(1/x)) time and space |
| `powers_memo.kara` | top down: the ways to make `rest` from powers of i and above are those that skip i^x and those that take it, remembered in a `Map[(i64, i64), i64]` keyed by (i, rest). O(n * n^(1/x)) |
| `powers_sums.kara` | only the sums that can be made: a `Map[i64, i64]` from each reachable sum to its count, each power adding a copy of every entry moved up by it while that stays within n. O(n * n^(1/x)) |
| `powers_solution.kara` | a Rust solution as LeetCode's Rust users write it, `vec![0i64; n + 1]` over `n as usize`, the powers by `(i as i64).pow(x as u32)` in a `loop` that breaks past n, and the sums walked down by `(p..=n).rev()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; 300,
LeetCode's most, as distinct numbers and as distinct squares, cubes,
4th and 5th powers; and every n from 1 to 300 with every x from 1 to 5,
with the count that have a way and a checksum. `powers.py` mirrors the
★ arm and its output is byte-identical.

```
1
2
872471266
25
0
0
0
1500 pairs: 626 with a way, checksum 647956238
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: with m the most numbers whose x-th powers can stay within n,
every subset of 1 to m taken by the bits of a mask, and those whose x-th
powers sum to n counted; no table. It takes every n from 1 to 300 with
every x from 1 to 5, LeetCode's whole range, and asks the literal
reading where m is at most 10, 1030 of the 1500.

| | property |
|---|---|
| P1 | m at most 10, the count is the literal reading's |
| P2 | n a power i^x, or the sum of two different ones: at least one way |
| P3 | x = 1: Euler's count of n as odd parts, any number of times each |
| P4 | 2^x past n: one way for n = 1, none for the rest |
| P5 | from 0 to `10^9 + 6` |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1500 cases, 1030 asked literally: checksum
950658172, 45000 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases by the same masks
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the sums walked up, so a power is used again | P1 1025, P3 299, P4 52, P6 1495 |
| M2 | ★: 1 never taken as a power | P1 101, P2 21, P3 299, P4 5, P6 563 |
| M3 | table: a row forgetting the sets without its power | P1 143, P2 429, P3 299, P6 612 |
| M4 | table: the power never making its own sum | P1 157, P2 438, P3 300, P4 5, P6 626 |
| M5 | memo: nothing left to make counted as no way | P1 157, P2 438, P3 300, P4 5, P6 626 |
| M6 | memo: a power taken may be taken again | P1 1025, P3 299, P4 52, P6 1495 |
| M7 | sums: a sum reaching n exactly never moved | P1 157, P2 438, P3 300, P4 5, P6 626 |
| M8 | sums: each moved count added twice | P1 157, P3 300, P4 5, P6 626 |
| M9 | solution: a power equal to n left out | P1 33, P2 20, P3 300, P4 5, P6 330 |
| M10 | solution: a power never added to the empty set | P1 157, P2 438, P3 300, P4 5, P6 626 |

## Benchmarks

The bench answers every n from 1 to 300 with every x from 1 to 5,
LeetCode's whole range, 20 times over by the ★ arm in all five
languages, each answer a new table. Every implementation prints `1500
pairs, 20 rounds: ways sum to 1194937895600, checksum 538600753`.

BENCHTAB

## Verification

All five arms print the same output as `powers.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ arm first raised i by `i.pow(x)`, x an `i64`; `pow` takes a `u32`
exponent, as Rust's does, and `karac fix` wrote `x as u32`. `karac
check` had also refused the next line, `for s in (p..=n).rev()`, "the
type argument for `T` could not be inferred", though nothing was wrong
there: the call with the wrong exponent had been typed as an error, so
`p` had no type. That was kara `B-2026-11-20-149`, fixed at `0d28296389`:
the power keeps the receiver's type, and only the exponent is reported.
The other three own arms, written after, checked clean.

LeetCode's Rust template took 8 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `n as usize` became `n as i64`;
`vec![0i64; n + 1]` became `Vec.filled(n + 1, 0)`; `(i as i64).pow(x as
u32) as usize` became `i.pow(x as u32)`; and `Solution::` became
`Solution.`, with the wrapper's `as i64` dropped. The `const MOD`, the
`x as u32` and the `dp[n] as i32` stayed.
