# 1672. Richest Customer Wealth

You are given an `m x n` integer grid `accounts` where `accounts[i][j]`
is the amount of money the `i`th customer has in the `j`th bank.
Return *the **wealth** that the richest customer has*.

A customer's **wealth** is the amount of money they have in all their
bank accounts. The richest customer is the customer that has the maximum
**wealth**.

```
accounts = [[1,2,3],[3,2,1]]              ->  6
accounts = [[1,5],[7,3],[3,5]]            ->  10
accounts = [[2,8,7],[7,1,3],[1,9,5]]      ->  17
```

**Constraints:** `m == accounts.length`; `n == accounts[i].length`;
`1 <= m, n <= 50`; `1 <= accounts[i][j] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `wealth.kara` ★ | a customer's wealth is the sum of their row: `map` gives each, by `iter().sum()`, and `max().unwrap()` the largest. O(m * n) |
| `wealth_loops.kara` | each row's sum built by an inner loop, the largest kept by the outer one, from 0, since every account holds at least 1. O(m * n) |
| `wealth_fold.kara` | one `fold` over the rows carries the largest wealth so far, each row's own wealth a `fold` of its accounts. O(m * n) |
| `wealth_solution.kara` | a Rust solution as LeetCode's Rust users write it, `sum::<i32>()` named by turbofish inside a `map`, then `max().unwrap()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, one
customer, one bank each, and the richest last; then the answers summed
and a checksum for 3000 random grids of up to 5 by 5 with up to 10 in
each account, and 1000 of up to 50 by 50, LeetCode's largest, with up to
100. `wealth.py` mirrors the ★ arm and its output is byte-identical.

```
6
10
17
16
9
200
3000 grids of up to 5 by 5, up to 10 in each account: answers sum to 59991, checksum 595990788
1000 grids of up to 50 by 50, up to 100 in each account: answers sum to 1532334, checksum 937990906
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each customer's wealth added up account by account, and the
richest found as the first customer no other is richer than. It checks
3000 random grids of 1 to 6 customers by 1 to 6 banks with 1 to 10 in
each account, each drawn with a shuffle of its customers and a customer
to copy. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the customers in another order give the same answer |
| P3 | one more in an account of a richest customer gives one more |
| P4 | a customer added as a copy of another gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 637211022, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Three pairs make the same mistake in
two arms and fail the same checks: M3 and M9 keep the last customer's
wealth, not the largest; M4, M6 and M10 take each customer's largest
account for their wealth.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the poorest customer's wealth | P1 2491, P3 2527, P5 2491 |
| M2 | ★: each customer's first account left out | P1 3000, P3 3000, P5 3000 |
| M3 | loops: the last customer's wealth kept, not the largest | P1 1722, P2 1693, P3 1857, P4 1700, P5 1722 |
| M4 | loops: a customer's largest account for their wealth | P1 2512, P3 1772, P5 2512 |
| M5 | loops: each wealth counted from 1 | P1 3000, P5 3000 |
| M6 | fold: a customer's largest account for their wealth | P1 2512, P3 1772, P5 2512 |
| M7 | fold: the wealths added up, not the largest kept | P1 2527, P4 3000, P5 2527 |
| M8 | fold: the first customer left out | P1 1138, P2 903, P3 1288, P4 720, P5 1138 |
| M9 | solution: `last()` for `max()` | P1 1722, P2 1693, P3 1857, P4 1700, P5 1722 |
| M10 | solution: a customer's largest account for their wealth | P1 2512, P3 1772, P5 2512 |

## Benchmarks

The bench draws 4000 random grids of 50 customers by 50 banks,
LeetCode's largest, up to 100 in each account, all of them first, then
answers each 100 times by the ★ arm in all five languages. Every
implementation prints `4000 grids of 50 by 50, 100 rounds: answers sum
to 1192802100, checksum 652823640`. The C build also runs clean under
gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.214 s |
| Rust (`rustc -O`) | 0.386 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.586 s |
| Kāra (`karac build`) | 0.593 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.801 s |
| Go | 1.328 s |
| Python | 8.2 s |

The sequential Kāra build takes 1.52x Rust's time and 0.73x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.214 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.590 s and 0.619 s on one
run).

## Verification

All four arms print the same output as `wealth.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ arm checked clean as first written. The loops arm's first draft
started both sums at a bare `0`; the narrowing check saw an `i64` returned
as the `i32` the signature names, and `karac fix` annotated both
`let`s `: i32`.

The fold arm's inner `fold(0, |sum, money| sum + money)` is an `i64`
fold by its seed's default, since the outer `max` against an `i64` seed
fixes nothing, and its result, compared with `i32` wealths, narrowed.
`karac check` refused it (E0200, a narrowing coercion) with no fix until
kara `93fd9b2078` (B-2026-11-20-33); since then it names the inner seed and `karac
fix` writes `0i32`, which keeps the fold as written.

LeetCode's Rust template took one `karac fix` of 3 edits:
`struct Solution {}` added, `Vec<Vec<i32>>` written `Vec[Vec[i32]]`, and
`sum::<i32>()`'s turbofish dropped, since the closure's return already
names the sum's type.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
