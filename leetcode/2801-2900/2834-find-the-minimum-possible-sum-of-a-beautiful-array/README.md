# 2834. Find the Minimum Possible Sum of a Beautiful Array

You are given positive integers `n` and `target`.

An array `nums` is **beautiful** if it meets the following conditions:

- `nums.length == n`.
- `nums` consists of pairwise **distinct** **positive** integers.
- There doesn't exist two **distinct** indices, `i` and `j`, in the
  range `[0, n - 1]`, such that `nums[i] + nums[j] == target`.

Return *the **minimum** possible sum that a beautiful array could have
modulo* `10^9 + 7`.

```
n = 2, target = 3  ->  4
n = 3, target = 3  ->  8
n = 1, target = 1  ->  1
```

**Constraints:** `1 <= n <= 10^9`; `1 <= target <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `sum.kara` ★ | the closed form: of each pair x and target - x only the smaller can be taken, so 1 to min(n, target / 2) first and the rest from target up, two arithmetic series reduced modulo 10^9 + 7 at the end |
| `sum_skip.kara` | the skipped run: the array is 1, 2, .. with target / 2 + 1 to target - 1 left out, so the sum of 1 to n plus the skipped count, less the skipped run's own sum |
| `sum_modular.kara` | in the field: the same two series with every product taken modulo 10^9 + 7 as it is made, and the halving done by the inverse of 2, found by Fermat's little theorem with a square-and-multiply power |
| `sum_search.kara` | binary search on the largest number taken: below x, the numbers that may be taken are x less the barred ones, counted by a struct's methods, and the least x with n of them ends the array |
| `sum_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `const MOD` inside the method, the `i32` parameters widened `as i64` in one tuple `let`, the two series, and the sum reduced `as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's three examples; a target
too small to bar anything and one too large to; n and target at
LeetCode's most, 10^9, with a target of 1, and n = 1 or 10^9 - 1; then
every n and target from 1 to 60, and 20000 random pairs up to 10^9, as
checksums. `sum.py` mirrors the ★ arm and its output is
byte-identical.

```
4 8 1
15 10
750000042 21
1 250000050
3600 small pairs: checksum 626598641
20000 random pairs: checksum 219842489
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every set of n distinct numbers from 1 to n + target,
by a bit mask, kept when no two of them sum to target, and the least
sum. Its cases are every n and target from 1 to 40, then 450 random
pairs up to 10^9; the literal reading is asked only of n and target up
to 8. The sums are compared modulo 10^9 + 7, as the arms return them.

| | property |
|---|---|
| P1 | n and target up to 8, the answer is the literal reading's |
| P2 | one number more: the sum grows by the next number taken, n + 1 below target / 2, else target + n - target / 2 |
| P3 | target 1 or 2, or at least 2n: 1 + 2 + .. + n, nothing to avoid |
| P4 | an even target made odd, one larger: each number taken from the target up moves up one |
| P5 | the answer is from 0 to 10^9 + 6 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 494910054, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: half the target rounded up | P1 25, P2 788, P3 39, P4 764, P6 768 |
| M2 | ★: the rest started one past the target | P1 48, P2 1572, P3 79, P6 1533 |
| M3 | skip: the target itself skipped too | P1 48, P2 1572, P3 79, P6 1533 |
| M4 | skip: the skipped run's sum never taken off | P1 33, P2 38, P4 764, P6 1454 |
| M5 | modular: the halving left out | P1 64, P2 2050, P3 596, P4 764, P6 2050 |
| M6 | modular: the power's odd step skipped | P1 64, P2 2050, P3 596, P4 764, P6 2050 |
| M7 | search: the barred run counted one short | P1 33, P2 1492, P4 764, P6 1454 |
| M8 | search: the search stopping one early | P1 33, P2 1492, P4 764, P6 1454 |
| M9 | solution: the pair split at the target, not its half | P1 46, P2 1571, P3 77, P4 764, P6 1531 |
| M10 | solution: the reduction left out | P2 246, P3 117, P4 120, P5 335, P6 450 |

## Benchmarks

The bench draws 10^6 random pairs of n and target up to 10^9, all of
them first, then answers each 20 times by the ★ arm in all five
languages. The answer is O(1), so the loop over the pairs and the
checksum's modulo are most of the work. Every implementation prints
`1000000 pairs, 20 rounds: checksum 776969392`.

BENCHTAB

## Verification

All five arms print the same output as `sum.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written; Kāra's checked
arithmetic held every product, the largest about 4 * 10^18 in the
search arm.

LeetCode's Rust template took 3 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`;
`Solution::` took `.`, and the wrapper's `as i64` went. The `const
MOD: i64 = 1_000_000_007` inside the method, the digit separators and
the tuple `let (n, t) = (n as i64, target as i64)` were accepted as
written.
