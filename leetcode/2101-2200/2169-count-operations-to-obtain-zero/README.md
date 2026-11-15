# 2169. Count Operations to Obtain Zero

You are given two **non-negative** integers `num1` and `num2`.

In one **operation**, if `num1 >= num2`, you must subtract `num2` from
`num1`, otherwise subtract `num1` from `num2`.

- For example, if `num1 = 5` and `num2 = 4`, subtract `num2` from `num1`,
  thus obtaining `num1 = 1` and `num2 = 4`. However, if `num1 = 4` and
  `num2 = 5`, after one operation, `num1 = 4` and `num2 = 1`.

Return *the **number of operations** required to make either `num1 = 0`
or `num2 = 0`*.

```
num1 = 2,  num2 = 3   ->  3
num1 = 10, num2 = 10  ->  1
```

**Constraints:** `0 <= num1, num2 <= 10^5`.

The larger number loses the smaller one as many times as it holds it
before it is the smaller, so a round of Euclid's algorithm counts
`a / b` operations at once and leaves `a % b`. O(log max).

## Approaches

| file | mechanism |
|---|---|
| `operations.kara` ★ | the larger and the smaller, `a / b` operations a round and `a % b` left, until the smaller is 0 |
| `operations_subtract.kara` | the statement as written: one subtraction a step, whichever number is larger losing the other, counted until either is 0 |
| `operations_recursive.kara` | a `match` on the pair: a zero ends it, otherwise the larger's quotient and the count of what its remainder leaves, by recursion |
| `operations_struct.kara` | a `struct Pair` of the larger and the smaller, made `of` two numbers, `done` when the smaller is 0, and a `round` (`mut ref self`) that takes the quotient's worth off and returns how many |
| `operations_iter.kara` | `successors` over the pairs of Euclid's algorithm from the larger and the smaller, each `map`ped to its quotient, and their `sum` |
| `operations_solution.kara` | LeetCode's Rust template: `mut num1: i32` parameters, `&&`, `%=` on whichever is larger, `struct Solution;`, `Solution::`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and six more
(both zero, one zero, equal, 1 and the most, the most and 1, and two
neighbouring Fibonacci numbers, which take the most rounds), each with
its count; then the total and a checksum over 2000 random pairs, each
number up to 10, 1000 or 10^5 in turn and about one in ten of them 0;
then a checksum over every pair up to 300. `operations.py` mirrors the ★
arm and its output is byte-identical.

`karac fix` carries the template in two rounds of 6 and 2 edits: Rust's
spellings (each `mut num1: i32` parameter to `num1: i32` and a `let mut
num1 = num1;` at the top of the body, `&&` to `and`, `struct Solution;`
to `struct Solution {}`, `Solution::` to `.`); then `let mut ops = 0` to
`let mut ops: i32 = 0`, which Rust types from the `i32` it is added to
and Kāra keeps at the default `i64` (design.md §8 Literals), and the
adapter's widening `as i64` dropped. A Rust `mut` parameter is a copy
the body changes; a scalar's was first carried to `own i32`, which takes
nothing a plain `i32` does not, and is now carried to the copy (ledger
row B-2026-11-14-65, fixed in karac 17c3e234b6).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: one subtraction an operation, counted. It checks 300 random
pairs, each number up to 10, 100 or 1000 in turn and about one in ten of
them 0; then 30 multiples of two neighbouring Fibonacci numbers, in
either order; then 30 pairs of a number and a multiple of it. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the numbers swapped: the same count |
| P3 | both numbers times 3: the same count |
| P4 | the smaller added to the larger, when neither is 0: one operation more |
| P5 | the count at least the larger's quotient by the smaller and at most the larger, and 0 when either is 0 |
| P6 | each arm agrees with at least three of the other five |

P3 holds since every operation of the pair times 3 is the operation of
the pair, times 3. P4 holds since the first operation of the larger pair
takes the smaller off the larger and leaves the pair it was made from.

The differential prints `360 pairs: checksum 901091849, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
pairs. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-three edits to the differential, four to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one operation a round | P1 274, P4 281, P5 100, P6 274 |
| M3 | ★: the last round never counted | P1 281, P4 73, P5 73, P6 281 |
| M25 | ★: a round's quotient one more | P1 281, P5 42, P6 281 |
| M6 | subtract: the loop ending when either is 1 | P1 158, P3 158, P4 20, P5 20, P6 158 |
| M8 | subtract: an operation counted twice when equal | P1 274, P4 7, P5 34, P6 274 |
| M26 | subtract: the larger's subtraction counted twice | P1 281, P2 248, P4 149, P5 49, P6 281 |
| M9 | recursive: zero handled only in the first place | P1 166, P2 348, P5 46, P6 166 |
| M12 | recursive: the smaller first left whole | P1 203, P2 264, P4 132, P5 48, P6 203 |
| M27 | recursive: the smaller-first round one more | P1 245, P2 160, P5 25, P6 245 |
| M29 | struct: the last round one more | P1 281, P5 35, P6 281 |
| M30 | struct: done when the two are equal | P1 7, P4 7, P5 7, P6 7 |
| M33 | struct: a round counted at most ten times | P1 79, P4 27, P5 24, P6 79 |
| M17 | iter: the last pair's quotient counted | P1 355, P5 109, P6 355 |
| M20 | iter: a remainder's operations its count | P1 208, P3 208, P5 41, P6 208 |
| M31 | iter: the last pair counted one | P1 360, P5 114, P6 360 |
| M24 | solution: the larger's quotient counted once | P1 203, P2 263, P4 132, P5 46, P6 203 |
| M32 | solution: the smaller-first quotient one short | P1 245, P2 160, P5 37, P6 245 |

P1, P5 and P6 kill all seventeen, P4 nine, P2 six and P3 two. P5 bounds
the count by the larger's quotient and the larger itself, and a 0 when
either is 0; every kept edit leaves those bounds somewhere. P4 adds the
smaller to the larger, and sees an edit whose first round is counted
wrong, but not one wrong by the same amount on both pairs, as a last
round counted one more is (M25, M29, M31). P2 swaps the numbers, and
sees the edits that count the two orders differently: the subtract
arm's larger counted twice (M26), the recursive arm's zero and its
smaller-first branch (M9, M12, M27), and the template's (M24, M32). P3
multiplies both numbers by 3, and sees only the edits that read a
number's size and not its ratio: the loop ending at 1 (M6) and a
remainder's operations its count (M20).

Of the thirty-three, sixteen were not kept. Ten are equivalent. Taking
the numbers as given rather than larger first, in the ★, struct and
iter arms (M2, M16, M19), costs a round of quotient 0 that swaps them.
The recursive arm's rest handed down swapped (M10) is the same count,
as P2 says, and so is the template's adapter swapping the numbers
(M23). One subtraction a call (M11) is the statement itself. Equal
numbers taken from the other one, in the subtract and template arms
(M5, M21), still end in one operation. The subtract arm's clamp of the
smaller's loss at 0 (M7) never binds, since it loses only while larger.
And the iter arm ending a pair early when its remainder is 0 (M18) drops
a pair whose quotient it counts as 0. Two never end: the ★ arm's
remainder its quotient (M4) and the struct arm's rest one more (M13).
Two crash: the struct arm done when the larger is 0 divides by zero
(M14), and its rest one subtraction runs to an integer overflow (M28).
Two fail as a kept one does: the struct arm's one operation a round, as
M1, and the template's loop ending at the first 1, as M6.

## Verification

Every arm prints the same output as `operations.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 s to 0.4 s, but for the iter
arm, 1.5 s, which builds a chain of `successors` for each of the 92609
pairs; the differential takes 0.2 s.

## Benchmarks

The bench solves every pair of numbers up to 3000, 9006001 solves, with
the ★ arm in all five languages, and sums the counts. Every
implementation prints `9006001 solves: 372783248 in all, checksum
662091847`.

BENCHTAB
