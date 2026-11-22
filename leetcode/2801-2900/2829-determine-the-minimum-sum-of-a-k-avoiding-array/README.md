# 2829. Determine the Minimum Sum of a k-avoiding Array

You are given two integers, `n` and `k`.

An array of **distinct** positive integers is called a **k-avoiding**
array if there does not exist any pair of distinct elements that sum to
`k`.

Return *the **minimum** possible sum of a k-avoiding array of length*
`n`.

```
n = 5, k = 4  ->  18     [1,2,4,5,6]
n = 2, k = 6  ->  3      [1,2]
```

**Constraints:** `1 <= n, k <= 50`.

## Approaches

The numbers below k pair off, v with k - v; the smaller of each pair
comes first, so taking every number from 1 up unless its partner is
already in gives the least sum: 1 to k / 2, then k and on.

| file | mechanism |
|---|---|
| `avoid.kara` ★ | the numbers walked up from 1, each taken unless its partner `k - v` was, marked in a `Vec[bool]` |
| `avoid_formula.kara` | the closed form: m = min(n, k / 2) numbers from 1, then n - m from k, as two arithmetic series |
| `avoid_set.kara` | a `Set` of the numbers taken, each new number tested by `contains(k - v)`, and the set summed by `iter().sum()` |
| `avoid_chain.kara` | the two runs, `1..=k / 2` and `k..`, joined by `chain`, the first n taken and summed |
| `avoid_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `HashSet` of the numbers taken, `i` counting up in a `while`, `contains(&(k - i))`, and `iter().sum()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; n = 1;
k = 1, which avoids nothing; n and k both 50; and every n and k from 1
to 50, as a total and a checksum. `avoid.py` mirrors the ★ arm and its
output is byte-identical.

```
18
3
1
1275
1875
2500 pairs: sums total 1455000, checksum 590522021
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every set of n distinct numbers from 1 to n + k, by a
bit mask, kept when no two distinct ones sum to k, and the least sum.
It asks every n and k from 1 to 50; the literal reading is asked only
of n and k up to 8.

| | property |
|---|---|
| P1 | n and k up to 8, the answer is the literal reading's |
| P2 | one number more: a larger sum |
| P3 | k at least 2n, or k of 1 or 2: 1 + 2 + .. + n, nothing to avoid |
| P4 | at least 1 + 2 + .. + n, and at most k + (k + 1) + .. + (k + n - 1) |
| P5 | k + 1 in place of an even k: no smaller sum |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2500 cases: checksum 143996016, 75000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases, by `itertools.combinations`, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: k itself never taken | P1 48, P3 99, P4 50, P6 1875 |
| M2 | ★: the partner never marked | P1 33, P6 1776 |
| M3 | formula: the second run started past k | P1 48, P3 99, P4 50, P6 1875 |
| M4 | formula: half of k rounded up | P1 25, P3 49, P4 49, P5 876, P6 949 |
| M5 | set: the partner tested as k + v | P1 33, P6 1776 |
| M6 | set: the count stopping one short | P1 64, P3 724, P4 917, P6 2500 |
| M7 | chain: the high run started at k + 1 | P1 48, P3 99, P4 50, P6 1875 |
| M8 | chain: the low run one short | P1 47, P3 98, P6 1874 |
| M9 | solution: the set never asked | P1 33, P6 1776 |
| M10 | solution: i counted from 2 | P1 64, P3 724, P4 50, P6 2500 |

## Benchmarks

The bench answers every n and k from 1 to 50, LeetCode's whole range,
2000 times by the ★ arm in all five languages, a fresh table of marks
for every answer. Every implementation prints `2500 pairs, 2000 rounds:
sums total 2910000000, checksum 151221934`.

BENCHTAB

## Verification

All five arms print the same output as `avoid.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms, the harness and the differential checked clean as
first written.

LeetCode's Rust template took 10 `karac fix` edits in a first run:
`use std::collections::HashSet` became `struct Solution {}`;
`HashSet::new()` became `Set.new()`; `n as usize` became `n as i64`;
`!set.contains(&(k - i))` became `not set.contains(k - i)`; and
`Solution::` took `.`. One error stayed with no edit: E0200 at the
tail, `set.iter().sum()`, an `i64` narrowed to the `i32` result, with
only the generic advice to write `as i32`. By design `k - i` leaves
`let mut i = 1`'s literal at its default `i64` beside the `i32` k
(design.md §8), so the set is a `Set[i64]`; the edit wanted is `let mut
i: i32 = 1`, written by hand, which `karac fix` offers for a literal
pushed into a `Vec` and read back but not for one inserted into a `Set`
and summed. It is not in the kara ledger yet: the kata rows are at their cap, so
the row waits for a free slot. A second `karac fix` run then
took 2 more edits: the `as i64` it had written, which W0310 now called
an unnecessary widening, and the wrapper's `as i64`.
