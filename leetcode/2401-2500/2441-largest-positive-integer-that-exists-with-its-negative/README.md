# 2441. Largest Positive Integer That Exists With Its Negative

Given an integer array `nums` that **does not contain** any zeros, find
**the largest positive** integer `k` such that `-k` also exists in the
array.

Return *the positive integer* `k`. If there is no such integer, return
`-1`.

```
nums = [-1,2,-3,3]         ->  3
nums = [-1,10,6,7,-7,1]    ->  7
nums = [-10,8,6,7,-2,-3]   ->  -1
```

**Constraints:** `1 <= nums.length <= 1000`; `-1000 <= nums[i] <= 1000`;
`nums[i] != 0`.

A pair `k` and `-k` is found when the second of the two arrives, so one
pass that remembers which values it has seen finds every pair, and the
largest magnitude among them is the answer. The values lie in a range of
2001, so a table of flags remembers them in O(1) each.

## Approaches

| file | mechanism |
|---|---|
| `largest.kara` ★ | a table of 2001 flags offset by 1000: each value whose negative was already seen offers its magnitude, the largest kept by `max`. O(n) |
| `largest_naive.kara` | the statement read directly: every pair of positions tried, and a pair adding to 0 offers its magnitude. O(n^2) |
| `largest_sorted.kara` | sorted, two pointers from both ends: the first pair adding to 0 is the answer, a negative sum moving the left pointer and a positive one the right. O(n log n) |
| `largest_set.kara` | a `Set[i64]` of every value, each positive value tested for its negative; the set is only asked, never walked, so its order never shows. O(n) expected |
| `largest_iter.kara` | iterators: the positive values by `filter`, each kept when `any` finds its negative, the largest by `max`, -1 by `unwrap_or`. O(n^2) |
| `largest_solution.kara` | LeetCode's Rust template: a `HashSet<i32>` collected from `nums.iter().cloned()`, and `filter(\|&&x\| x > 0 && s.contains(&-x))` then `max().cloned().unwrap_or(-1)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; `1000`
and `-1000`; `-1000` alone; three 4s and a -3; then 1000 values, the
constraints' most, every value from 1 to 500 with its negative but 500,
whose partner is a second 499; 1000 random values from -1000 to 1000;
and 3000 random arrays of 1 to 10 values from -6 to 6, as a checksum and
the total. `largest.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 50000 random arrays of 1
to 12 values against every `k` from 1 to 1000 tested.

`check` first reports 7 errors on the template, and `karac fix` carries
it in one call, reporting 11 edits: the line `use
std::collections::HashSet` deleted, since `Set` is in Kāra's prelude;
the brackets of `Vec<i32>` and `HashSet<i32>`, and `HashSet` written
`Set`; the `&&` dropped from the closure's pattern `&&x`, since a Kāra
pattern already matches through a reference; the operator `&&` written
`and`; the `&` dropped from the argument `&-x`; `struct Solution;`
given its braces; and, once the template parses, the harness's `as i64`
on the `i64` the template returns. `cloned()` before `collect` and after
`max`, and `unwrap_or(-1)`, stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every `k` from 1000 down to 1 tried in turn, the array scanned
once for `k` and once for `-k`, and the first `k` found both ways is the
answer, -1 when none is. No table, sort or set is used. It checks 300
random arrays of 1 to 10 values from `-m` to `m`, `m` from 1 to 6; then
30 of 50 to 300 values from -1000 to 1000; then 30 of 2 to 40 values
from 1 to 50 with one of them negated. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the array reversed: the same answer |
| P3 | every value negated: the same answer |
| P4 | the answer is -1, or positive with both it and its negative in the array |
| P5 | a pair `a` and `-a` added, `a` from 1 to 1000, `a` at a random place and `-a` at the end: the larger of `a` and the answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because whether `k` and `-k` are both present does not depend
on their order, and P3 because negating takes each pair to itself. P5
holds because the new pair is one more candidate, and every old one
stays.

The differential prints `360 cases: checksum 635867275, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tests every `k`. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the second of the pair kept as it is | P1 74, P2 158, P3 158, P5 337, P6 74 |
| M4 | ★: the last pair kept | P1 65, P2 71, P5 17, P6 65 |
| M6 | ★: each answer one short | P1 242, P4 192, P5 333, P6 242 |
| M7 | naive: neighbours never paired | P1 29, P5 55, P6 29 |
| M10 | naive: the first value never paired | P1 43, P2 59, P5 55, P6 43 |
| M11 | naive: the first of the pair kept as it is | P1 84, P2 158, P3 158, P4 49, P5 5, P6 84 |
| M13 | sorted: the pointers moved the wrong way | P1 109, P5 28, P6 109 |
| M14 | sorted: never sorted | P1 214, P2 140, P3 140, P4 74, P5 360, P6 214 |
| M15 | sorted: the last two never compared | P1 13, P6 13 |
| M17 | set: the value itself looked up | P1 178, P3 227, P4 178, P6 178 |
| M19 | set: the magnitudes stored | P1 242, P5 360, P6 242 |
| M21 | set: the first value never tested | P1 25, P2 46, P3 43, P5 55, P6 25 |
| M23 | iter: the least | P1 110, P5 242, P6 110 |
| M25 | iter: the first value never a negative | P1 18, P2 31, P3 43, P6 18 |
| M26 | iter: 1 never taken | P1 68, P6 68 |
| M30 | solution: one less looked up | P1 204, P3 194, P4 103, P5 330, P6 204 |
| M31 | solution: the set of the first half only | P1 85, P2 160, P3 137, P5 333, P6 85 |


P1 and P6 kill all seventeen, P5 thirteen, P2 and P3 eight each and P4
five.

Fourteen are not kept. Three fail exactly as a kept one: the ★ arm's
only a positive second (M5) as its second of the pair kept as it is
(M2), each losing the pairs whose negative comes second; the iter arm's
value itself looked for (M22) as the set arm's value itself looked up
(M17); and the template's least (M27) as the iter arm's (M23). Ten more
fall into groups that fail alike and apart from every kept one, and none
is kept: the ★ arm's value itself looked up and the naive arm's equal
values paired (M1, M8), both pairing a value with a repeat of itself;
the ★ and sorted arms' none answered 0, the set arm's and the
template's none answered 1, and the iter arm's none answered 0 (M3,
M16, M20, M29, M24), each wrong only where there is no pair, since an
answer of 1 is still 1; and, alone, the naive arm's only a positive
first (M9), the sorted arm's negative answered (M12) and the template's
negatives taken (M28), left out because those arms keep their share
already.

One survives, and is equivalent: the set arm's negative value kept
(M18) lets a negative `x` with `|x|` above the best so far become the
best. Its positive partner is in the array, and has not been tested
yet, or the best would already be at least `|x|`; so it comes later,
is larger than the negative best, and takes its place.

## Verification

Every arm prints the same output as `largest.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 to 0.8 s, and the
differential 4.3 s; under `karac __mir-llvm-asan` the differential
takes 1.2 s and under `karac run` 0.8 s.

## Benchmarks

The bench builds 100 arrays of 1000 values from -1000 to 1000, the
constraints' largest, once from its own generator. It then makes 1000
passes; each sets one value of every array, so no answer can be carried
from one pass to the next, then answers every array, folding the answer
plus the pass into the checksum. The bench uses the ★ arm, the table of
2001 flags, in all five languages, each answer allocating its table
afresh. Every implementation prints `1000 passes over 100 arrays of
1000 values: checksum 873064691`.

BENCHTAB
