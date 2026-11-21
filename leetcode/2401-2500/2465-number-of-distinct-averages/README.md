# 2465. Number of Distinct Averages

You are given a **0-indexed** integer array `nums` of **even** length.

As long as `nums` is **not** empty, you must repetitively:

- Find the minimum number in `nums` and remove it.
- Find the maximum number in `nums` and remove it.
- Calculate the average of the two removed numbers.

The **average** of two numbers `a` and `b` is `(a + b) / 2`.

- For example, the average of `2` and `3` is `(2 + 3) / 2 = 2.5`.

Return *the number of **distinct** averages calculated using the above
process*.

**Note** that when there is a tie for a minimum or maximum number, any
can be removed.

```
nums = [4,1,4,0,3,5]  ->  2
nums = [1,100]        ->  1
```

**Constraints:** `2 <= nums.length <= 100`; `nums.length` is even;
`0 <= nums[i] <= 100`.

The removals pair the `i`th smallest with the `i`th largest, so sorting
once gives every pair. Two averages are equal exactly when the two sums
are, so the answer is the number of distinct sums, and no division or
fraction is needed.

## Approaches

| file | mechanism |
|---|---|
| `averages.kara` ★ | sorted, the `i`th smallest paired with the `i`th largest, and the pairs' sums put in a `Set`. O(n log n) |
| `averages_naive.kara` | the statement read directly: while numbers are left, the least and the greatest found by a scan and removed, the average taken as an `f64` and kept when no earlier average equals it. O(n^2) |
| `averages_count.kara` | counts: the values lie from 0 to 100, so a count of each replaces the sort, two pointers walk in from both ends of the counts, and each pair's sum is marked in a table of the 201 sums possible. O(n + 101) |
| `averages_heaps.kara` | two heaps over the same numbers, `PriorityQueue.new()` popping the least first and `PriorityQueue.max_first()` the greatest: the first `n / 2` pops of each are the removals, since the smaller and larger halves never meet. O(n log n) |
| `averages_iter.kara` | iterators: the sorted numbers `zip`ped with themselves reversed, the first half's pairs summed by `map` and collected into a `Set`. O(n log n) |
| `averages_solution.kara` | LeetCode's Rust template: `mut nums: Vec<i32>` sorted in place, the pairs' sums put in a `HashSet<i32>`, and its size returned `as i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples; then four
more, every number the same, the two ends of the range, every pair
summing alike, and two averages that differ by a half; 0 to 99, the
constraints' longest list; 100 random numbers from 0 to 100 and 100
from 0 to 3; and 3000 random lists of 2 to 20 numbers from 0 to 100, as
a checksum. `averages.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on every list of 2, 4, 6 and
8 numbers from 0 to 4 against the removals done one by one with the
averages kept as fractions.

`check` first reports 6 errors on the template, and `karac fix` carries
it in one call, reporting 12 edits: the `use` line deleted; `mut nums:
Vec<i32>` written `nums: own Vec[i32]` with `let mut nums = nums;` at
the body's start; the brackets of `Vec<..>` and `HashSet<..>`, and
`HashSet` written `Set`; `HashSet::new` written `Set.new`; and `struct
Solution;` given its braces. `nums.sort()`, `n / 2` over the length and
`set.len() as i32` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: while numbers are left, the least and the greatest removed,
found by `min`, `max` and `position`, and their average kept as a
fraction in lowest terms, numerator and denominator, a new average
counted only when no earlier fraction is the same. No sort and no sum
stands in for the average. It checks 300 random lists of 2 to 12
numbers, an even count, from 0 to 10; then 30 of up to 100 from 0 to
100; then 30 of up to 100 from 0 to 3. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the list turned by one place: the same answer |
| P3 | every number `v` written `100 - v`: the same answer |
| P4 | the list followed by itself: the same answer |
| P5 | the answer between 1 and half the count |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the removals depend only on the values. P3 holds
because `100 - v` reverses the order, so the same pairs are removed,
and their sums become `200 - s`, as many distinct ones. P4 holds
because in the list doubled the `2i`th and `2i + 1`th smallest are both
the `i`th smallest of the original, and each is paired with a copy of
the original's `i`th largest. P5 holds because there are `n / 2` pairs.

The differential prints `360 cases: checksum 464576361, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and keeps the averages as `Fraction`s. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: each smallest paired with its neighbour | P1 225, P4 327, P6 225 |
| M5 | ★: the pairs one place in | P1 149, P3 151, P4 277, P6 149 |
| M6 | ★: a difference for the sum | P1 210, P6 210 |
| M7 | naive: the first number for the least | P1 205, P2 110, P3 135, P4 297, P6 205 |
| M9 | naive: each average counted | P1 232, P4 360, P6 232 |
| M11 | naive: the least weighted twice | P1 186, P3 173, P6 186 |
| M12 | count: an odd least marked one sum low | P1 140, P3 110, P6 140 |
| M14 | count: the sums halved into the table | P1 172, P3 143, P6 172 |
| M16 | count: the sum 200 never counted | P3 1 |
| M17 | heaps: both heaps the least first | P1 186, P3 177, P6 186 |
| M18 | heaps: one number left out | P1 123, P2 136, P4 233, P6 123 |
| M19 | heaps: the greatest read modulo 50 | P1 24, P3 105, P6 24 |
| M22 | iter: reversed against itself unsorted | P1 204, P2 139, P6 204 |
| M24 | iter: the reverse one place along | P1 150, P3 158, P4 292, P6 150 |
| M26 | iter: the larger doubled | P1 188, P3 177, P6 188 |
| M28 | solution: one pair too few | P1 212, P4 212, P5 58, P6 212 |
| M29 | solution: the count one more | P1 360, P5 128, P6 360 |

P1 and P6 kill sixteen, P3 ten, P4 seven, P2 three and P5 two. The
count arm's sum 200 never counted (M16) is killed by P3 alone, once:
only a pair of two 100s sums to 200, which no case holds, and it
appears only when a case whose least and greatest left are both 0 at
some step is written `100 - v`.

Fourteen are not kept. Twelve fail exactly as a kept one: the ★ arm's
and the template's never sorted (M1, M27) as the iter arm's reversed
against itself unsorted (M22); the naive arm's greatest for the least
(M8) as the ★ arm's each smallest paired with its neighbour (M2); the
★ arm's larger alone counted, the count arm's least never used up and
the heaps arm's greatest counted twice (M4, M13, M20) as the iter arm's
larger doubled (M26), each counting the distinct larger halves; the
naive arm's average truncated (M10) as the count arm's sums halved into
the table (M14); the heaps arm's second greatest each time (M21) as
the iter arm's reverse one place along (M24); the iter arm's first pair
dropped (M23) as the template's one pair too few (M28); and the iter
arm's each number paired with itself and the template's smaller doubled
and largest paired with each (M25, M30, M31) as the heaps arm's both
heaps the least first (M17), each counting the distinct smaller halves.
Two fail apart from every kept one, and alike: the ★ arm's last pair
never counted (M3) and the count arm's one pair too few (M15).

Five edits of the first run were replaced: the count arm's top count
skipped ended in an index below 0, and four could not be killed by any
check. The naive arm's greatest taken no smaller than the least, the
count arm's greatest not used up when it meets the least, the heaps
arm's one pop too many, and the iter arm's every pair taken are each
equivalent: the greatest left is never below the least just removed;
when the two pointers meet every number left is the same, so every
pair left has one sum; the extra pop pairs the two middle numbers,
which the last pair already did; and the pairs past the middle repeat
the first half's sums in reverse.

## Verification

Every arm prints the same output as `averages.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 to 0.8 s, and the differential 1.6 s; under `karac __mir-llvm-asan` the differential takes 0.7 s, and under `karac run` 0.7 s.

## Benchmarks

The bench builds 1000 lists of 100 numbers from 0 to 100, the
constraints' longest, once from its own generator, then makes 900
passes; each sets one number of every list from the checksum so far, so
no answer carries over, then answers every list, folding the answer
plus the pass into the checksum. The bench uses the ★ arm, a sorted copy
and a set of sums, in all five languages. Every implementation prints
`900 passes over 1000 lists of 100: checksum 898892092`. The set is the
language's own, `Set` in Kāra, `HashSet` in Rust, `map` in Go and `set`
in Python; C has none, and marks the sums, at most 200, in a table of
201 flags cleared for every answer.

BENCHTAB
