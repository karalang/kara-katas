# 2358. Maximum Number of Groups Entering a Competition

You are given a positive integer array `grades` which represents the
grades of students in a university. You would like to enter **all**
these students into a competition in **ordered** non-empty groups, such
that the ordering meets the following conditions:

- The sum of the grades of students in the `i`th group is **less than**
  the sum of the grades of students in the `(i + 1)`th group, for all
  groups (except the last).
- The total number of students in the `i`th group is **less than** the
  total number of students in the `(i + 1)`th group, for all groups
  (except the last).

Return *the **maximum** number of groups that can be formed*.

```
grades = [10,6,12,7,3,5]  ->  3
grades = [8,8]            ->  1
```

**Constraints:** `1 <= grades.length <= 10^5`;
`1 <= grades[i] <= 10^5`.

`k` groups of strictly rising sizes hold at least `1 + 2 + ... + k`
students. With the grades sorted, groups of 1, 2, 3, ... students taken
in order, the leftovers joining the last, have rising sizes and, each
holding more students and higher grades than the one before, rising
sums. So the answer is the largest `k` with `k (k + 1) / 2 <= n`, and
the grades themselves never matter.

## Approaches

| file | mechanism |
|---|---|
| `groups.kara` ★ | group sizes 1, 2, 3, ... added while the next still fits. O(sqrt n) |
| `groups_greedy.kara` | the groups built: the grades sorted, group `j` given the next `j + 1` students while that many are left, the rest added to the last group, and both conditions checked before the groups are counted. O(n log n) |
| `groups_search.kara` | binary search for the largest `k` with `k (k + 1) / 2 <= n`. O(log n) |
| `groups_root.kara` | `k = (sqrt(8 n + 1) - 1) / 2`, the root taken in `f64` and the result nudged by whole steps until it is exact. O(1) |
| `groups_iter.kara` | iterators: the sizes as a range, their running totals by `scan`, the totals that fit counted by `take_while` and `count` |
| `groups_solution.kara` | LeetCode's Rust template: the ★ arm's loop over `i32`, with `let (mut k, mut used) = (0, 0)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; one
student; three; `10^5` students; then 3000 random classes of 1 to 300
students graded 1 to `10^5`, with a checksum and the groups summed.
`groups.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked against every way to deal up to 6 students into
groups on 150 random classes.

`karac fix` carries the template in one call, reporting 7 edits.
`check` first reports 5 errors, each with its edit: `struct Solution;`
given braces, `Vec<i32>` made square, the two `mut` inside the tuple
pattern `(mut k, mut used)` moved before it as `let mut (k, used)`,
and the `::` call written with `.`. The rest follow from the first
two. `grades.len() as i32` stands, and the tuple's two 0s take `i32`
from the `n` they are compared with.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to cut the class into groups of strictly rising
sizes is searched, size by size, for the most groups; the sorted grades
dealt out in that order give the groups rising sums too, which is
checked. No triangle numbers. It checks 300 random classes of 1 to 40
students graded 1 to 1 up to 1 to `10^5`; then 30 of up to 3000; then
30 whose sizes sit next to a triangle number. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | up to 40 students, the answer is the literal reading's |
| P2 | `k (k + 1) / 2 <= n < (k + 1) (k + 2) / 2` |
| P3 | every grade made 1: the same answer |
| P4 | `k + 1` more students: one more group |
| P5 | one student fewer, when there are two or more: the same answer or one fewer |
| P6 | each arm agrees with at least three of the other five |

P3 holds even with every grade equal, since a larger group of equal
grades still has the larger sum.

The differential prints `360 cases: checksum 818223504, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and steps `k` up while the next triangle number fits. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a group that fits exactly refused | P1 61, P2 70, P6 70 |
| M2 | ★: each group counted one student too large | P1 185, P2 228, P4 49, P6 228 |
| M3 | ★: the size added before it grows | P1 241, P2 290, P6 290 |
| M8 | greedy: the leftover students given to the first group | P1 230, P2 279, P4 290, P5 107, P6 279 |
| M9 | greedy: the grades left unsorted | P1 194, P2 252, P3 252, P4 339, P5 171, P6 252 |
| M11 | greedy: the grades sorted from the highest | P1 234, P2 292, P3 292, P4 360, P5 17, P6 292 |
| M12 | search: a k that fits exactly refused | P1 53, P2 62, P4 8, P6 62 |
| M13 | search: the search capped at half the class | P1 5, P2 5, P4 8, P6 5 |
| M14 | search: the upper end moved past a miss | P1 115, P2 135, P4 161, P5 37, P6 135 |
| M17 | root: the upward nudge testing k (k + 1) / 2 | P1 302, P2 360, P6 360 |
| M18 | root: the upward nudge allowing one student over | P1 69, P2 83, P6 83 |
| M21 | root: the upward nudge against twice the class | P1 294, P2 352, P4 315, P6 352 |
| M24 | iter: the sizes stopped below n | P1 8, P2 8, P6 8 |
| M25 | iter: each total a group behind | P1 294, P2 352, P4 8, P6 352 |
| M26 | iter: the first group skipped | P1 302, P2 360, P4 70, P6 360 |
| M28 | solution: each group counted as one student | P1 270, P2 328, P4 336, P6 328 |
| M29 | solution: half the class | P1 291, P2 349, P4 170, P6 349 |

P1, P2 and P6 kill all seventeen, P4 twelve, P5 four and P3 two. P2, the
triangle bounds, holds the answer to exactly one value for each class
size, so every edit that changes any answer fails it, and it fails more
cases than P1, which stops at 40 students. P3, every grade made 1, fails
only the greedy arm's unsorted and reversed grades, the only arm that
reads a grade. P4, `k + 1` more students, misses the five (M1, M3, M17,
M18, M24) whose error is the same at `n` and at `n + k + 1`: adding one
whole group's worth of students keeps a class the same distance past its
triangle number, so an edit that errs only at, or only just off, a
triangle number errs alike on both.

Of the thirty-one, fourteen were not kept. Two crash: the greedy arm's
groups one student larger (M7) slice past the end of the class, and its
group that fits exactly refused (M10) leaves a class of one student no
group to index; both end in `index out of bounds`. A group that fits
exactly refused, a student taken as used at the start, and a student
left out in the ★ arm (M1, M4, M6) and the iter arm's total that fits
exactly refused and total started at 1 (M22, M23) all fail alike: each
answers one fewer just at the triangle numbers. The root arm's upward
nudge allowing one student over and student too many counted (M18,
M20) fail as the template's student too few needed and count started at
1 (M27, M30), each answering one more just below them; and the search
started at 2 (M15) as the root arm's at least 2 groups (M19). The ★
arm's at most 30 groups (M5), the search arm's `k` squared over 2
(M16) and the template's two groups at a time (M31) fail apart from
every kept one; they were left out to keep three to an arm and two to
the template.

## Verification

Every arm prints the same output as `groups.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.5 to 0.8 s but the greedy arm
and the template, 1.4 and 1.3 s: the greedy arm sorts the class and
builds the groups, and the template narrows every class to `i32` first.
The differential takes 1.9 s there and 0.52 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds 10 classes once, class `a` holding `10^4 (a + 1) - a`
students graded 1 to `10^5`, then makes 20000 passes, pass `p` folding
each answer plus `p` into the checksum, with the ★ arm in all five
languages. Every implementation prints `20000 passes over 10 classes:
checksum 735097803`. The work is the loop of about 300 steps per call,
which no implementation can skip, since the class size differs from
call to call only by class; the compiled runs are short, under a tenth
of a second.

BENCHTAB
