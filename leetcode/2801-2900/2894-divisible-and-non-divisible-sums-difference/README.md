# 2894. Divisible and Non-divisible Sums Difference

You are given positive integers `n` and `m`.

Define two integers as follows:

- `num1`: The sum of all integers in the range `[1, n]` (both
  **inclusive**) that are **not divisible** by `m`.
- `num2`: The sum of all integers in the range `[1, n]` (both
  **inclusive**) that are **divisible** by `m`.

Return *the integer* `num1 - num2`.

```
n = 10, m = 3  ->  19
n = 5,  m = 6  ->  15
n = 5,  m = 1  ->  -15
```

**Constraints:** `1 <= n, m <= 1000`.

## Approaches

| file | mechanism |
|---|---|
| `sums.kara` ★ | by formula: the integers 1 to n sum to n(n + 1) / 2, the multiples of m among them are m, 2m, .., km for k = n / m, summing to m k(k + 1) / 2, and num1 - num2 is the whole less twice the multiples |
| `sums_loop.kara` | the statement as written: 1 to n walked, each added to num1 or num2 |
| `sums_filter.kara` | two iterator chains: the non-multiples by `filter`, the multiples by `step_by(m)` from m |
| `sums_fold.kara` | one `fold`, each integer added with its sign: minus for a multiple of m |
| `sums_solution.kara` | a Rust solution as LeetCode's Rust users write it: `(1..=n)` mapped to a signed term and summed, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 2 lines: LeetCode's three examples and 1000
with 1000, LeetCode's most; then every n and m from 1 to 200, as a
total of the answers and a checksum. `sums.py` mirrors the ★ arm and its
output is byte-identical.

```
19 15 -15 498500
40000 pairs: differences total 255454664, checksum 133894700
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the integers 1 to n listed, split by `partition` into
those m does not divide and those it does, and the two lists summed. It
takes every n and m from 1 to 60, then 50 random pairs up to 1000.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | m made 1: minus the sum of 1 to n |
| P3 | m made n + 1: the sum of 1 to n |
| P4 | n raised by one: n + 1 more, or n + 1 less when m divides it |
| P5 | as odd as the sum of 1 to n, and no further from 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `3650 cases, differences total 9559587:
checksum 661717433, 109500 checks over 5 arms: 0 failures` under every
lane in Verification, and a Python reading of the same cases gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: n itself left out of the multiples | P1 261, P2 3650, P4 463, P6 261 |
| M2 | ★: the multiples taken once, not twice | P1 1859, P2 3650, P4 262, P5 739, P6 1859 |
| M3 | loop: n left out | P1 3650, P2 3650, P3 3650, P4 3650, P5 1824, P6 3650 |
| M4 | loop: each multiple counted as m | P1 912, P2 3590, P4 202, P5 330, P6 912 |
| M5 | filter: the values one past a multiple dropped too | P1 3590, P3 3650, P4 201, P5 2677, P6 3590 |
| M6 | filter: n left out of the multiples | P1 261, P2 3650, P4 463, P5 84, P6 261 |
| M7 | fold: a multiple left out, not taken away | P1 1859, P2 3650, P4 262, P5 739, P6 1859 |
| M8 | fold: the sum started at 1 | P1 3650, P2 3650, P3 3650, P5 3650, P6 3650 |
| M9 | solution: n left out | P1 3650, P2 3650, P3 3650, P4 3650, P5 1824, P6 3650 |
| M10 | solution: the signs the wrong way round | P1 3649, P2 3650, P3 3650, P4 3650, P6 3649 |

## Benchmarks

The bench answers every n and m from 1 to 1000, LeetCode's most, 100
times over by the ★ arm in all five languages, m shifted by the round
and each answer folded into the checksum, so that no round can be
skipped. Every implementation prints `1000 by 1000 pairs, 100 rounds:
differences total 16474980150400, checksum 51340223`.

BENCHTAB

## Verification

All five arms print the same output as `sums.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written, `(m..n + 1)
.step_by(m).sum()` among them. The differential's literal reading did
not: `let (divided, rest): (Vec[i64], Vec[i64]) = all.iter().partition(..)`
was refused, since `partition` keeps the iterator's `ref i64` items,
where `collect` and `sum` read a `Copy` item as a value
(docs/library/iterators.md, "Items read through a reference"). `karac
fix` wrote the `.cloned()` in.

LeetCode's Rust template took 3 `karac fix` edits in one run: `struct
Solution {}` came for the `impl`, the wrapper's `Solution::` took `.`
and its `as i64` on the `i32` result went. `(1..=n)` and the closure's
`-x` were accepted as written.
