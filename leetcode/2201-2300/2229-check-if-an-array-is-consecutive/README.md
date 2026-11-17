# 2229. Check if an Array Is Consecutive

Given an integer array `nums`, return `true` *if* `nums` *is
**consecutive**, otherwise return* `false`*.*

An array is **consecutive** if it contains every number in the range
`[x, x + n - 1]` (**inclusive**), where `x` is the minimum number in the
array and `n` is the length of the array.

```
nums = [1,3,4,2]  ->  true
nums = [1,3]      ->  false
nums = [3,5,4]    ->  true
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^5`.

The numbers are consecutive when the largest less the smallest is one
less than how many there are and no number repeats: n distinct numbers
in a span of n can only be all of it. A `Set` finds a repeat. O(n).

## Approaches

| file | mechanism |
|---|---|
| `consecutive.kara` ★ | one walk keeping the smallest, the largest and a `Set` of those seen, `false` at the first repeat; then the span against the count |
| `consecutive_sort.kara` | a sorted copy, each number one more than the one before it |
| `consecutive_marks.kara` | n slots from the smallest number, each number filling its own, `false` when it falls past the last slot or on one already filled |
| `consecutive_struct.kara` | a `struct Run` taking the numbers with `add` (`mut ref self`), keeping the smallest, the largest, a `Set` and whether one repeated; `consecutive` (`ref self`) compares the span with the count |
| `consecutive_iter.kara` | the smallest and largest by `min` and `max`, the distinct numbers by `collect`ing into a `Set`, and the span, the distinct count and the length compared |
| `consecutive_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, the bounds through `*nums.iter().min().unwrap()`, the span compared as `(mx - mn + 1) as usize`, the distinct numbers a `HashSet<i32>` `collect`ed from `nums.iter().cloned()`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and four
more (one number, a repeat, the two ends of the range, and a run missing
its middle), each with its answer; then the count and a checksum of 3000
random cases, each a shuffled run of 1 to 20 numbers anywhere from 0 to
10^5, two in three of them with one number then drawn again near the
run; then the constraints' largest, all of 0 to 99999 shuffled, then
with one moved to 100000, then with one written twice. `consecutive.py`
mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 9 edits: `use
std::collections::HashSet` dropped, `Vec<i32>` and `HashSet<i32>` to
`Vec[i32]` and `Set[i32]`, `struct Solution;` to `struct Solution {}`,
and the cast `(mx - mn + 1) as usize` dropped, since the `i32` widens
into the `i64` that `len()` returns where it is compared.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: x the smallest number, and every number from x to x + n - 1
looked for by a walk over the array; no set, no sort. It checks 300
random cases of a shuffled run of 1 to 12 numbers, two in three of them
with one number then drawn again near the run; then 30 runs with one
number written twice; then 30 of 1 to 6 numbers each from 0 to 5. All
360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | when it is true, the numbers add up to n * x + n * (n - 1) / 2 |
| P3 | the numbers rotated by a random amount: the same answer |
| P4 | every number 5 higher: the same answer |
| P5 | one more number, one past the largest: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 530302006, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
compares the sorted numbers with `range(min, min + n)`. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-eight edits to the differential: thirty-one first, six to the ★
arm and five to each of the others, and then seven more, since the
first thirty-one gave too few distinct failures for the struct, iter
and template arms. Each was run under `karac __mir-llvm-run`, and the
kept ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the span one short | P1 215, P2 44, P6 215 |
| M3 | ★: the smallest starting at 0 | P1 166, P4 5, P6 166 |
| M8 | sort: never sorted | P1 127, P3 15, P6 127 |
| M9 | sort: the first pair skipped | P1 34, P2 34, P6 34 |
| M11 | sort: sorted downwards | P1 138, P5 33, P6 138 |
| M12 | marks: a slot filled twice allowed | P1 141, P2 141, P6 141 |
| M15 | marks: a repeat answering `true` | P1 142, P2 142, P3 1, P5 1, P6 142 |
| M16 | marks: the smallest slot never marked filled | P1 33, P2 33, P6 33 |
| M17 | struct: a repeat forgotten | P1 63, P2 63, P6 63 |
| M22 | iter: repeats ignored | P1 76, P2 76, P6 76 |
| M23 | iter: the smallest the first number | P1 117, P2 4, P3 51, P6 117 |
| M30 | solution: the first number left out of the set | P1 171, P6 171 |
| M32 | ★: a repeat ending the walk, not the answer | P1 42, P2 42, P3 31, P5 42, P6 42 |
| M33 | struct: the largest the last number | P1 113, P2 7, P3 60, P5 113, P6 113 |
| M34 | struct: one number never consecutive | P1 33, P5 33, P6 33 |
| M35 | iter: the last number left out of the largest | P1 38, P2 6, P3 58, P5 177, P6 38 |
| M37 | solution: the span never checked | P1 46, P2 46, P6 46 |

P1 and P6 kill all seventeen, P2 twelve, P3 and P5 six each, and P4
one. P2 catches the edits that let a repeat or a gap through: a true
answer for numbers that are not a run has the wrong sum. P3 catches the
edits that read the numbers in their order: the first or last taken for
the smallest or largest, a walk cut short, and the unsorted copy. P4
raises every number by 5, and only the edit that starts the smallest at
0 (M3) cares where the numbers lie.

Of the thirty-eight, twenty-one were not kept. Three survive and are
equivalent: the ★ arm's span at most the count (M4), since n distinct
numbers span at least n; the sort arm's each number checked against
the first (M10), `sorted[i] - sorted[0] == i` for every i being the same
condition; and the iter arm's span compared with the distinct count
(M24), which the other half of the test has already made the length.
None crashes, and none differs between the backends. Sixteen fail as a
kept one does, the struct, iter and template arms sharing most of the ★
arm's edits: the ★ arm's repeats never checked or never recorded and the
template's repeats allowed (M1, M6, M28) as the iter arm's repeats
ignored (M22); the struct arm's and the template's span one short (M18,
M27) as the ★ arm's (M2); their smallest from 0 (M19, M29) as the ★
arm's (M3); the ★ arm's smallest the first (M5) as the iter arm's (M23);
the sort arm's repeats allowed and the struct arm's repeats ignored (M7,
M21) as the struct arm's repeat forgotten (M17); the marks arm's slot
never filled (M13) as its repeats allowed (M12); the marks arm's slot
short, the struct arm's nothing seen, the iter arm's first left out of
its set and the template's largest one higher (M14, M20, M25, M31) as
the template's first left out of the set (M30); and the template's one
number never consecutive (M38) as the struct arm's (M34). Two fail
their own way and are left out for the count of three: the iter arm's
either test enough (M26) and its first left out of the smallest (M36).

## Verification

Every arm prints the same output as `consecutive.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.5 s to 1.3 s, and the
differential 0.4 s.

## Benchmarks

The bench draws 4 shuffled runs of 0 to 99999 once, the last two with
one number then written over by another, and answers each 25 times, two
numbers trading places before each answer, with the ★ arm in all five
languages; C's set is an open-addressing table, since C has none of its
own. The ★ arm stops at the first repeat, so the two lists that are not
consecutive cost a random part of a walk. Every implementation prints
`100 answers: 50 consecutive, checksum 6693126`.

BENCHTAB
