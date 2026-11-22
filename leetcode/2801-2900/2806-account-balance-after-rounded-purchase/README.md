# 2806. Account Balance After Rounded Purchase

Initially, you have a bank account balance of **100** dollars.

You are given an integer `purchaseAmount` representing the amount you
will spend on a purchase in dollars, in other words, its price.

When making the purchase, first the `purchaseAmount` **is rounded to
the nearest multiple of 10**. Let us call this value `roundedAmount`.
Then, `roundedAmount` dollars are removed from your bank account.

Return an integer denoting your final bank account balance after this
purchase.

**Notes:**

- 0 is considered to be a multiple of 10 in this problem.
- When rounding, 5 is rounded upward (5 is rounded to 10, 15 is rounded
  to 20, 25 to 30, and so on).

```
purchaseAmount = 9    ->  90
purchaseAmount = 15   ->  80
```

**Constraints:** `0 <= purchaseAmount <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `balance.kara` ★ | integer arithmetic: 5 added before the division by 10 so that a 5 rounds up, times 10, taken from 100 |
| `balance_remainder.kara` | by the last digit: the remainder by 10 taken off, and 10 more when it is 5 or over |
| `balance_nearer.kara` | the nearer of the multiples just below and just above by `min_by_key` on the distance and then the multiple turned negative, so a tie goes up |
| `balance_float.kara` | in floating point: the amount over 10 rounded by `f64.round`, which takes a half away from zero, then times 10 |
| `balance_solution.kara` | a Rust solution as LeetCode's Rust users write it, the remainder matched against the range pattern `0..=4`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; nothing
spent; everything; 5 and 95, which round up; every amount from 0 to
100, LeetCode's whole range, in turn; and 3000 drawn at random, the last
two with the sum of the balances and a checksum. `balance.py` mirrors
the ★ arm and its output is byte-identical.

```
90
80
100
0
90
0
0 to 100: balances sum to 5000, checksum 924832998
3000 random amounts: balances sum to 148590, checksum 614838876
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every multiple of 10 from 0 up past the amount, the nearest
kept and the largest of the nearest on a tie, and the balance 100 less
it; no division. It draws 2050 amounts from 0 to 100 before any arm
answers, and asks the literal reading of all of them.

| | property |
|---|---|
| P1 | the balance is the literal reading's |
| P2 | a multiple of 10 from 0 to 100 |
| P3 | the rounded amount within 5 of the amount |
| P4 | 10 more spent, when it is still within 100: 10 less left |
| P5 | 1 more spent: no more left |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 675091048, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 4 added, not 5 | P1 222, P6 222 |
| M2 | ★: the rounding left out | P1 1850, P2 1850, P6 1850 |
| M3 | remainder: a 5 rounded down | P1 222, P6 222 |
| M4 | remainder: rounding up by the remainder, not to the next 10 | P1 830, P2 830, P3 830, P5 202, P6 830 |
| M5 | nearer: a tie taken by the multiple below | P1 222, P6 222 |
| M6 | nearer: the farther kept | P1 2050, P2 20, P3 1828, P5 212, P6 2050 |
| M7 | float: the tens truncated | P1 1052, P3 830, P6 1052 |
| M8 | float: the tens rounded up always | P1 798, P3 798, P6 798 |
| M9 | solution: a remainder of 4 rounded up | P1 212, P3 212, P6 212 |
| M10 | solution: up to the same 10 rather than the next | P1 1052, P3 830, P6 1052 |

## Benchmarks

The bench draws 10^6 amounts from 0 to 100, all of them first, then
answers each 100 times by the ★ arm in all five languages, every answer
folded into a running checksum so that no two answers are independent
and the loop cannot be vectorized away. Every implementation prints
`1000000 amounts, 100 rounds: balances sum to 4957704000, checksum
489030520`.

BENCHTAB

## Verification

All five arms print the same output as `balance.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The nearer arm first read `let rounded = [below, below +
10].iter().min_by_key(...).unwrap();`, and `karac check` refused it: the
`ref i64` that `min_by_key` returns borrows the list literal, a
temporary dropped at the `;` (core-semantics.md §5.5, no temporary
lifetime extension). That is the rule as written, and Rust refuses the
same line. `karac fix` bound the list to `rounded_src` first. A `let
rounded: i64` would also have been accepted, since a `Copy` value is
read through the reference where an `i64` is expected (§5.10). The other
three own arms checked clean as first written.

LeetCode's Rust template took 3 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `Solution::` became `Solution.`;
and the wrapper's `as i64`, an `i32` widening by itself, was dropped.
The range pattern `0..=4` is Kāra as written.
