# 2342. Max Sum of a Pair With Equal Sum of Digits

You are given a **0-indexed** array `nums` consisting of **positive**
integers. You can choose two indices `i` and `j`, such that `i != j`,
and the sum of digits of the number `nums[i]` is equal to that of
`nums[j]`.

Return *the **maximum** value of* `nums[i] + nums[j]` *that you can
obtain over all possible indices* `i` *and* `j` *that satisfy the
conditions*, or `-1` if there are none.

```
nums = [18,43,36,13,7]   ->  54
nums = [10,12,19,14]     ->  -1
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`.

A value up to `10^9` has a digit sum from 1 to 81. The best pair of a
digit sum is its two largest values, so it is enough to keep, for each
digit sum, the largest value seen so far, and to pair each value with
the largest before it of its own sum. The sum reaches `2 * 10^9`, which
still fits LeetCode's `i32` answer.

## Approaches

| file | mechanism |
|---|---|
| `digits.kara` ★ | a table of 82 keeping the largest value seen for each digit sum; each value paired with the largest before it of its own sum. O(n) |
| `digits_naive.kara` | every pair: each value's digit sum once, then every pair of places with equal sums. O(n^2) |
| `digits_sorted.kara` | the values as (digit sum, value) pairs sorted, so each sum's two largest are its last two, side by side. O(n log n) |
| `digits_map.kara` | a `SortedMap` from each digit sum to its two largest values as a pair, -1 for one not yet seen; the best sum of the full pairs. O(n log 82) |
| `digits_iter.kara` | iterators: for each digit sum from 1 to 81 its values by `filter`, the largest two by a `fold`, the full pairs summed by `filter_map`, and the best by `max`. O(81 n) |
| `digits_solution.kara` | LeetCode's Rust template: a `HashMap` from each digit sum to the largest value, read through `if let Some(&b) = best.get(&s)` and raised through `entry().or_insert`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one value;
the largest digit sum twice; `10^9` beside its own digit sum's 1, 10 and
100; 2000 values spread to `10^9`; then 2000 random cases of 1 to 30
values up to 10, 100, `10^4` or `10^9`, with a checksum, the answers'
sum and how many have a pair. `digits.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked against every pair
on 3000 random arrays.

`karac fix` carries the template in one call, reporting 19 edits.
`check` first reports 11 errors and offers 15 edits for them: the
`use std::collections::HashMap;` line deleted, since `Map` is in the
prelude; the six brackets of `Vec<i32>`, `HashMap<i32, i32>` and the
wrapper's `Vec<i32>`; `HashMap::new` and `Solution::` to `.`; the `&`
of the patterns `&x` and `|&x|` dropped; `Some(&b)` from `best.get(&s)`
to `Some(b)` from `best.get(s).cloned()`, three edits; and
`struct Solution;` to `struct Solution {}`. The other four follow from
those: `HashMap` to `Map` in the type and the call; `ans` annotated
`i32`, as its `-1` would otherwise be an `i64` beside the `i32` sums;
and the wrapper's `as i64` on the `i32` answer dropped, since it widens
on its own. `entry(s).or_insert(0)` and `*e = (*e).max(x)` stand as
Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of places `i < j`, each value's digit sum read
from its decimal text one character at a time, and the largest sum of
a pair whose digit sums are equal, or -1. No table and no sorting. It
checks 300 random cases of 1 to 12 values up to 10, 100, `10^4` or
`10^9`; then 30 of up to 300 values up to `10^9`; then 30 of up to 300
values up to 100. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 12 values, the answer is the literal reading's |
| P2 | -1 exactly when no two values share a digit sum, and otherwise between twice the smallest value and twice the largest |
| P3 | the values reversed: the same answer |
| P4 | every value ten times itself, where that stays within `i32`: ten times the answer, or -1 |
| P5 | the largest value once more: twice the largest value |
| P6 | each arm agrees with at least three of the other five |

P4 holds because a 0 put after a value keeps its digit sum. P5 holds
because the largest value then pairs with its copy, and no pair sums to
more. The differential was first written with P2's lower bound as more
than the largest value, which a pair of two smaller values breaks; the
first run failed it on every arm alike, and it was corrected to twice
the smallest. `karac fix` dropped five `.clone()`s of vectors passed to
parameters that only borrow them.

The differential prints `360 cases: checksum 733454856, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and sums each value's digits from `str`. On a failure it
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
| M2 | ★: the latest value kept, not the largest | P1 9, P5 60, P6 30 |
| M3 | ★: a value recorded before it is paired | P1 281, P2 141, P6 327 |
| M5 | ★: every other digit skipped | P1 155, P2 67, P4 152, P6 193 |
| M8 | naive: pairs of different digit sums taken | P1 279, P2 121, P5 360, P6 339 |
| M9 | naive: the first value never paired | P1 31, P2 15, P3 66, P5 77, P6 32 |
| M11 | naive: a digit 9 summed as 0 | P1 89, P2 41, P6 115 |
| M12 | sorted: the sort left out | P1 119, P2 87, P3 4, P5 283, P6 178 |
| M13 | sorted: only the last digit sum tried | P1 129, P2 162, P5 191, P6 179 |
| M14 | sorted: the first two places never paired | P1 16, P2 11, P5 46, P6 16 |
| M17 | map: a new largest dropping the old one | P1 56, P2 37, P3 144, P6 71 |
| M18 | map: a new second taking the largest place | P1 107, P2 77, P3 171, P5 360, P6 154 |
| M21 | map: the pair kept under its sum modulo 9 | P1 121, P2 118, P3 68, P5 290, P6 180 |
| M22 | iter: digit sums from 50 never tried | P1 2, P5 37, P6 13 |
| M23 | iter: the second largest never raised | P1 104, P2 84, P3 176, P5 360, P6 147 |
| M25 | iter: every smaller digit sum gathered too | P1 253, P2 120, P6 299 |
| M30 | solution: a new digit sum starting at `10^9` | P1 160, P2 184, P3 134, P4 151, P5 360, P6 219 |
| M31 | solution: each digit summed one more | P1 28, P2 18, P6 28 |

P1 and P6 kill all seventeen, P2 fifteen, P5 eleven, P3 seven and P4
two. P2 misses the edits that still answer a pair of equal digit sums,
only not the best one: the latest value kept rather than the largest,
and digit sums from 50 never tried, which the values here rarely reach.
P5, the largest value once more, fails where an edit keeps the wrong
value for a digit sum or cannot pair the largest with its copy: the
latest value kept, pairs of different sums, the second largest never
raised or put in the largest's place, the sort left out. P3, the values
reversed, fails where an edit depends on their order: the first value
never paired, the sort left out, a new largest dropping the old one or a
new second taking its place, the second largest never raised, the pair
kept under its sum modulo 9, and a sum starting at `10^9`. P4, every
value ten times itself, fails only where an edit's digit sum changes
with a trailing 0, every other digit skipped, or where a sum can start
at `10^9`.

Of the thirty-one, fourteen were not kept. The table filled with 0 in
the ★ arm (M1), an unseen sum starting from 0 in the map arm (M20) and
the fold starting from two zeros in the iter arm (M26) fail alike; so do
the latest value kept in the ★ arm (M2) and the template (M27), and the
leading digit never summed in both (M4, M28); and no pair answered 0 in
the ★ (M6), iter (M24) and template (M29) arms. Of those groups only
M2 is kept. A value recorded before it is paired in the ★ arm (M3)
fails as a value paired with itself in the naive arm (M7), and only M3
is kept. The naive arm's pair kept only when it is smaller (M10), the
sorted arm's largest taken twice (M15) and digit sums keyed by their
last digit (M16), and the map arm's lone value counted with -1 (M19)
fail apart from every kept one, and were left out to keep three to an
arm.

## Verification

Every arm prints the same output as `digits.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.25 to 1 s but the iter arm,
which walks the values once for each of the 81 digit sums, 5.6 s. The
differential takes 8 to 9 s there and 0.6 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values from 1 to `10^9` once, from
a scramble that never repeats, then makes 20 passes, pass `p` folding
each answer plus `p` into the checksum, with the ★ arm in all five
languages. Every implementation prints `20 passes over 10 arrays of
10^5 values: checksum 444007347`. Each allocates its 82 entries afresh
for every call, as 64-bit integers.

BENCHTAB
