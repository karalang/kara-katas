# 2860. Happy Students

You are given a **0-indexed** integer array `nums` of length `n` where
`n` is the total number of students in the class. The class teacher
tries to select a group of students so that all the students remain
happy.

The `ith` student will become happy if one of these two conditions is
met:

- The student is selected and the total number of selected students
  is **strictly greater than** `nums[i]`.
- The student is not selected and the total number of selected
  students is **strictly less than** `nums[i]`.

Return *the number of ways to select a group of students so that
everyone remains happy.*

```
nums = [1,1]                ->  2
nums = [6,0,3,3,6,7,2,7]    ->  3
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <
nums.length`.

## Approaches

| file | mechanism |
|---|---|
| `happy.kara` ★ | a group of k makes everyone happy only if it is the k smallest values, every one below k, and every value left out above k; sorted, that is nums[k - 1] < k and nums[k] > k, checked for every k from 0 to n |
| `happy_counts.kara` | no sort: the values counted by size, all below n; a group of k works when exactly k values are below k and none equals k, read off a running count as k walks up from 0 |
| `happy_search.kara` | the same rule by search: in the sorted values, `partition_point` finds how many are below k and how many are at most k, and a group of k works when both are k |
| `happy_sizes.kara` | the distinct values in a `SortedMap` with their counts, walked in order: between a value v and the next value w, with c values at most v, the only size that can work is c, and it does when v < c < w; the empty group works when the smallest value is above 0 |
| `happy_solution.kara` | a Rust solution as LeetCode's Rust users write it: `nums.sort()` on a `mut nums` parameter, the empty group by `(nums[0] > 0) as i32`, then a loop over `1..=n` with `as i32` on every comparison, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; 10^5
zeros, LeetCode's most, 10^5 values of 10^5 - 1, and 0 to 10^5 - 1
once each; then 3000 random classes of 1 to 8 and 30 of 10^4 to 10^5,
half of them random values and half built around a group size g, g
values below it and the rest above, one in four with one value set to
g itself, as a total of ways and a checksum. `happy.py` mirrors the ★
arm and its output is byte-identical.

```
2 3
1 2 1
3000 small classes: 5053 ways, checksum 824187534
30 large classes: 3642 ways, checksum 852451204
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: for a class of up to 10, every group tried as a bit
mask, each student checked happy, chosen with more chosen than their
value or left out with fewer, and the groups where everyone is counted.
It draws 2000 random classes of 1 to 10, then 50 of up to 300, all
before any arm answers; the literal reading is asked only of the first
2000.

| | property |
|---|---|
| P1 | up to 10 students, the answer is the literal reading's |
| P2 | the students in reverse order: the same answer |
| P3 | each student v made two, 2v and 2v + 1: the same answer |
| P4 | the whole class chosen always works: from 1 to n + 1 |
| P5 | the values sorted: the same answer |
| P6 | each arm agrees with at least three of the other four |

P3 holds because, for the doubled class, a group of 2k has 2a values
below it exactly when the class has a below k, and has a value equal to
2k exactly when the class has one equal to k, while an odd size can
never be matched. The differential prints `2050 cases, 3912 ways:
checksum 750857414, 61500 checks over 5 arms: 0 failures` under every
lane in Verification, and a Python reading of the same cases, every
group tried for the first 2000, gives the same checksum. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. A first draft of M4 left every answer as it
was, equivalent to the arm, and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the chosen allowed to equal k | P1 617, P3 877, P6 661 |
| M2 | ★: the full group never tried | P1 2000, P4 764, P6 2050 |
| M3 | counts: a value equal to k let pass | P1 1684, P3 1570, P6 1734 |
| M4 | counts: a group size some student asks for allowed | P1 1684, P3 1570, P6 1734 |
| M5 | search: the values at most k only | P1 617, P3 877, P6 661 |
| M6 | search: the values below k only | P1 1684, P3 1570, P6 1734 |
| M7 | sizes: the empty group always counted | P1 1388, P6 1423 |
| M8 | sizes: a group size equal to the next value allowed | P1 1179, P3 1570, P6 1228 |
| M9 | solution: the empty group never counted | P1 612, P6 627 |
| M10 | solution: the left-out students not checked | P1 1389, P3 1775, P6 1439 |

## Benchmarks

The bench draws 50 classes of 10^5 students, LeetCode's most, half of
them random and half built around a group size, all of them first, then
answers each 20 times by the ★ arm in all five languages, the copy and
the sort included. C sorts with the C library's `qsort`, which calls
its comparison through a pointer, where the others use their own
languages' sorts; on a loaded machine it took several times as long as
the rest. Every implementation prints `50 classes of 100000, 20 rounds:
163940 ways, checksum 600779042`.

BENCHTAB

## Verification

All five arms print the same output as `happy.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The search arm, as first written, sorted with `sort_unstable()`, and
`karac check` reported E0236, the library having only the stable
`sort`, which is also an unstable one; `karac fix` wrote `sort()`. The
differential's `flat_map(|v| [2 * v, 2 * v + 1])` drew E0200, the
closure returning a `Vec`, a collection, where `flat_map` takes an
`Iterator` (Rust's takes anything `IntoIterator`); `karac fix` added
`.into_iter()`. The other arms checked clean.

LeetCode's Rust template took 12 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; the `mut
nums: Vec<i32>` parameter became `nums: own Vec[i32]` with `let mut
nums = nums;` at the body's start; `Vec<..>` became `Vec[..]`; `&&`
and `||` became `and` and `or`; `|&x|` lost its `&`; `Solution::` took
`.`, and the wrapper's `as i64` went, an `i32` widening. `(nums[0] >
0) as i32` and `k as i32` were accepted as written.
