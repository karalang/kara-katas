# 2475. Number of Unequal Triplets in Array

You are given a 0-indexed array of positive integers `nums`. Find the
number of triplets `(i, j, k)` that meet the following conditions:

- `0 <= i < j < k < nums.length`
- `nums[i]`, `nums[j]`, and `nums[k]` are pairwise **distinct**. In other
  words, `nums[i] != nums[j]`, `nums[i] != nums[k]`, and
  `nums[j] != nums[k]`.

Return *the number of triplets that meet the conditions.*

```
nums = [4,4,2,4,3]  ->  3
nums = [1,1,1,1,1]  ->  0
```

**Constraints:** `3 <= nums.length <= 100`; `1 <= nums[i] <= 1000`.

A triplet of distinct values is one place chosen from each of three
different values, so the count is the sum, over every three different
values, of the product of their counts. Taking the values in any order,
each is the middle one of `left * c * right` such triplets, `left` the
places of the values before it and `right` those after.

## Approaches

| file | mechanism |
|---|---|
| `triplets.kara` ★ | by counts: a `Map` counts the values, and the walk over it in its own order adds `left * c * (n - left - c)` for each. O(n) |
| `triplets_every.kara` | every triplet: three nested loops over `i < j < k`, a pair of equal values skipped before the third loop. O(n^3) |
| `triplets_sorted.kara` | sorted runs: a sorted copy puts equal values side by side, and a run of `c` from place `start` adds `start * c * (n - end)`. No map. O(n log n) |
| `triplets_complement.kara` | the complement: `n choose 3` less, for each count `c`, the `(c choose 2) * (n - c)` triplets holding a value twice and the `c choose 3` holding it three times, the counts in a list indexed by value. O(n + 1000) |
| `triplets_iter.kara` | iterators: the counts gathered by `fold` into a `Map`, then a `fold` over its values carrying the places before and the triplets so far as a pair. O(n) |
| `triplets_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out; a `std::collections::HashMap` filled by `*count.entry(x).or_insert(0) += 1`, then the ★ arm's walk; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples; then four
more, three distinct values, two values only, a value held by every
triplet but one, and one value three times among two others; then four
lists of 100 values, the constraints' longest, all distinct, random
from 1 to 1000, from 1 to 10 and from 1 to 3; and 3000 random lists of
3 to 100 values from 1 to between 1 and 20, as a checksum.
`triplets.py` mirrors the ★ arm and its output is byte-identical, and
the mirror was checked on 20000 random lists of 3 to 12 values against
every triplet of places.

`check` first reports 8 errors on the template, and `karac fix` carries
it in one call, reporting 15 edits: the brackets of `Vec<i32>`;
`std::collections::HashMap::new` becomes `Map.new`; the `&` before each
loop pattern goes and the one on `&nums` becomes `ref`; `let (mut ans,
mut left) = (0, 0)` becomes `let mut (ans, left) = (0i32, 0i32)`;
`struct Solution;` is given its braces; and the `0` of `or_insert(0)`
is written `0i32`. That last literal took the default when the map was
built, so the counts are `i64`, and `left * c` narrows into the `i32`
answer; the refusal offered only "an explicit 'as i32'", and `karac fix`
stopped with two errors until B-2026-11-24-9 traced a loop over
`count.values()` back to the literal.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of three places, each a mask over the list's
places with three bits set, counted when the three values there differ
pairwise. No count stands in for the triplets. It checks 300 random
lists of 3 to 10 values, then 60 of up to 12, their values from 1 to
between 1 and 6. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | the list reversed: the same count |
| P3 | a value not in the list appended: one more for every pair of places holding different values |
| P4 | the list twice over: eight times the count |
| P5 | every value replaced by its place: `n choose 3` |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a triplet's values do not depend on the order of its
places. P3 holds because the new value differs from both values of
every unequal pair, and every new triplet takes it as its last place.
P4 holds because every count doubles, and the count is a sum of
products of three counts. P5 holds because every triplet then holds
three different values.

The differential prints `360 cases: checksum 466476710, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and takes `itertools.combinations`. On a failure it
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
| M1 | ★: the places after left out | P1 277, P3 341, P4 291, P5 308, P6 277 |
| M2 | ★: left never grown | P1 191, P3 291, P5 360, P6 191 |
| M5 | ★: each count from 1 | P1 291, P3 360, P4 291, P5 360, P6 291 |
| M7 | every: equal first pairs not skipped | P1 232, P2 220, P3 345, P4 288, P6 232 |
| M8 | every: the third only unlike the first | P1 242, P2 220, P4 285, P6 242 |
| M10 | every: the last place never third | P1 191, P2 106, P3 291, P4 191, P5 360, P6 191 |
| M13 | sorted: runs never sorted | P1 222, P3 222, P4 291, P6 222 |
| M14 | sorted: each run counted as one place | P1 129, P3 247, P4 191, P6 129 |
| M15 | sorted: the places after counted from the run start | P1 291, P3 360, P5 360, P6 291 |
| M17 | complement: the threes not taken out | P1 256, P4 345, P6 256 |
| M18 | complement: the pairs not taken out | P1 276, P3 345, P4 291, P6 276 |
| M19 | complement: a pair with any third | P1 345, P4 360, P6 345 |
| M24 | iter: every count one | P1 272, P3 325, P4 291, P6 272 |
| M25 | iter: values counted in threes | P1 188, P3 268, P5 360, P6 188 |
| M26 | iter: the left given out as the answer | P1 351, P3 360, P4 360, P5 321, P6 351 |
| M30 | solution: the first value never counted | P1 217, P2 154, P3 286, P4 291, P6 217 |
| M31 | solution: values counted in pairs | P1 153, P3 159, P5 360, P6 153 |

P1 and P6 kill all seventeen, P3 fourteen, P4 thirteen, P5 eight, and
P2 four.

Fourteen are not kept. Nine fail exactly as a kept one: the ★ arm's and
template's every count one (M3, M29) as the iter arm's (M24); the
sorted arm's places after one short and places before counted from 1,
and the complement arm's choose one term short (M12, M16, M20), as the
★ arm's each count from 1 (M5), each wrong on every list that holds a
triplet; the iter arm's and template's places after left out (M22,
M27) as the ★ arm's (M1); and their left never grown (M23, M28) as the
★ arm's (M2). The complement arm's choose divided before it multiplies
(M21) fails apart from every kept one, the arm having three kept
already. Two fail differently under the two backends, and for no
compiler's fault: the ★ arm's value itself counted after and its
middle value taken once (M4, M6) make each value's share depend on the
values walked before it, and the walk is the `Map`'s own order, which
differs from run to run. Two survive and are equivalent: the every
arm's third from `j` on and second from `i` on (M9, M11), since the
place added holds the value it is compared against, so the triplet is
skipped. Every other edit is killed.

Six edits were replaced before this table was drawn: the sorted arm's
run walk one short, which never ends once the last run is one value;
the iter arm's middle value taken once and the template's value itself
counted after, which depend on the `Map`'s order as M4 and M6 do; their
first replacements, the iter arm's length one short and the template's
length one more; and the template's first count from 1. The last three
failed exactly as M5.

## Verification

Every arm prints the same output as `triplets.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.4 to 1.0 s, the complement arm 4.7 s, the every arm 37.2 s, and the differential 3.6 s; under `karac __mir-llvm-asan` the arms take 0.4 to 1.8 s, the every arm 5.5 s, and the differential 1.7 s, and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench builds 2000 lists of 100 values from 1 to 50 once from its own
generator, then makes 600 passes; each sets one value of every list
from the checksum so far, so no answer carries over, then answers it,
folding the count plus the pass into the checksum. The bench uses the
★ arm in all five languages, the counts in a hash map in each: C, which
has none, keeps them in an open-addressing table of 256 slots, walked
in slot order and emptied after every list. Every implementation prints
`600 passes over 2000 lists of 100: checksum 867591357`.

BENCHTAB
