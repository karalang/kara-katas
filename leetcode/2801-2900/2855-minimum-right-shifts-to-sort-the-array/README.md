# 2855. Minimum Right Shifts to Sort the Array

You are given a **0-indexed** array `nums` of length `n` containing
**distinct** positive integers. Return *the **minimum** number of
**right shifts** required to sort* `nums` *and* `-1` *if this is not
possible.*

A **right shift** is defined as shifting the element at index `i` to
index `(i + 1) % n`, for all indices.

```
nums = [3,4,5,1,2]  ->  2
nums = [1,3,5]      ->  0
nums = [2,1,4]      ->  -1
```

**Constraints:** `1 <= nums.length <= 100`; `1 <= nums[i] <= 100`;
`nums` contains distinct integers.

## Approaches

| file | mechanism |
|---|---|
| `shifts.kara` ★ | a sorted array shifted has at most one place where a value is followed by a smaller one: with none it is sorted, with two no shift sorts it, and with one at i the last value must be below the first, and n - 1 - i shifts bring the tail round to the front |
| `shifts_each.kara` | every shift from 0 to n - 1 tried in turn, the array turned one more place with `rotate_right` and checked with `windows(2)`; O(n^2), for LeetCode's 100 |
| `shifts_min.kara` | the smallest value must end up first, so the only candidate is the shift that brings its place m, by `min_by_key`, to the front, (n - m) % n, and the array read round from m must rise throughout |
| `shifts_cycle.kara` | the array as a cycle: the places followed by a smaller value, the last followed by the first, gathered with `filter`; a sortable array has exactly one, which the shifts bring to the end, or none for one element, settled by a `match` on the count |
| `shifts_solution.kara` | a Rust solution as LeetCode's Rust users write it: the first drop found with `(1..n).find(\|&i\| ..)`, matched as `None` or `Some(i)`, the rest after it checked with `nums[i..].windows(2)`, and the answer `(n - i) as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's three examples and one
element; 100 values, LeetCode's most, sorted, shifted by 1 and by 99,
and with the last two swapped; then every permutation of 1 to 7
elements, 5913 of them, and 3000 random arrays of 1 to 100 distinct
values up to 100, two times in three sorted and shifted, as a count
sortable and a checksum. `shifts.py` mirrors the ★ arm and its output
is byte-identical.

```
2 0 -1 0
0 99 1 -1
5913 permutations: 28 sortable, checksum 625930465
3000 random arrays: 2038 sortable, checksum 633864929
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the array shifted right one place at a time, every
element to the next index and the last to the front, up to n - 1
times, and the first count at which it is sorted, else -1. It draws
2000 random arrays of 1 to 8 distinct values up to 20, then 50 of up to
100 up to 100, each half the time sorted and shifted, all before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every value made 3x + 1: the same answer |
| P3 | the array shifted right once more: a sortable one one shift less, mod n |
| P4 | the values negated and the array reversed: n - a shifts, mod n |
| P5 | -1, or from 0 to n - 1 and that many right shifts sort it |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 1380 sortable: checksum 667780431,
61500 checks over 5 arms: 0 failures` under every lane in Verification,
and a Python reading of the same cases gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, three to the ★ arm, one to the cycle arm
and two to each of the others, each run under `karac __mir-run` and
`karac __mir-llvm-run`. All ten are killed, each the same way under both
backends. M2 and M8 fail the same checks, both leaving out the wrap from
the last value to the first; so do M1 and M9, both letting a second drop
through.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a second drop allowed | P1 313, P3 431, P4 313, P5 313, P6 313 |
| M2 | ★: the wrap from last to first not checked | P1 125, P3 204, P5 125, P6 125 |
| M3 | ★: one shift too many | P1 835, P3 611, P4 835, P5 835, P6 835 |
| M4 | each: the shift counted before it is checked | P1 1380, P3 545, P4 1258, P5 1380, P6 1380 |
| M5 | each: the array shifted left, not right | P1 647, P3 890, P5 647, P6 647 |
| M6 | min: the largest value taken to the front | P1 1126, P6 1126 |
| M7 | min: the last pair of the cycle not checked | P1 127, P4 127, P5 127, P6 127 |
| M8 | cycle: the wrap from last to first left out | P1 125, P3 204, P5 125, P6 125 |
| M9 | solution: the rest after the drop not checked | P1 313, P3 431, P4 313, P5 313, P6 313 |
| M10 | solution: one shift too few | P1 835, P3 611, P4 721, P5 835, P6 835 |

## Benchmarks

The bench draws 10^5 arrays of 100 distinct values up to 100,
LeetCode's most, two times in three sorted and shifted, else with two
values swapped after it, all of them first, then answers each 50 times
by the ★ arm in all five languages. C lays the arrays end to end in one
allocation. Every implementation prints `100000 arrays, 50 rounds:
3331150 sortable, checksum 114648316`.

BENCHTAB

## Verification

All five arms print the same output as `shifts.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The harness, as first written, built a shifted array with
`[100].iter().chain((1..100).collect().iter())`, which Rust rejects
too; `karac check` reported E0236, "no method 'iter' on type parameter
'C'; add a trait bound declaring it", where the gap is the `collect()`
with no type to collect into, as Rust's E0282 says. Since kara 0d28296389
the check says the `collect()` has no target type and to bind the
collection with its type first (B-2026-11-21-207). Here the range
became a `let rest: Vec[i64]` by hand. `(2..101).chain([1].iter())`
drew an associated-type error, `Item = ref i64` where `i64` is wanted,
and `karac fix` added `.cloned()`; `minimum_right_shifts(p.clone())`
drew `redundant_clone`, and `karac fix` passed `p`. The each arm's
`turned.windows(2).all(..)` drew E0236, a `Vec` of windows needing
`.into_iter()`, which `karac fix` added. The other arms checked clean.

LeetCode's Rust template took 11 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]`; `|&i|` and `|&x|` lost their `&`; `&&` became `and`;
`nums[i..].windows(2)` took `.into_iter()`; `Solution::` took `.`, and
the wrapper's `as i64` went, an `i32` widening. `(n - i) as i32` was
accepted as written.
